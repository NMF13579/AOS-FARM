#!/usr/bin/env python3
import sys
import json
import argparse
import subprocess
import os
import fnmatch
from pathlib import Path

PASS = "PASS"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"

def print_result(status, reason, errors=None, is_json=False, stats=None):
    if is_json:
        out = {
            "checker": "conditional_scope",
            "final_status": status,
            "reason_code": reason
        }
        if errors is not None:
            out["errors"] = errors
        if stats is not None:
            out["stats"] = stats
        print(json.dumps(out, indent=2))
    else:
        print(f"final_status: {status}")
        print(f"reason_code: {reason}")
        if errors:
            print("errors:")
            for e in errors:
                print(f"  - {e}")
    sys.exit(2 if status == HUMAN_REVIEW_REQUIRED else (3 if status == UNKNOWN_BLOCKED else 0))

def get_repo_root():
    res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return Path(res.stdout.strip()).resolve()

def get_head_sha(repo_root):
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except:
        return ""

def validate_structure(contract):
    if not isinstance(contract, dict): return False, "Not an object"
    if contract.get("schema_name") != "aos_build_step_scope_contract": return False, "Invalid schema_name"
    if not isinstance(contract.get("schema_version"), int): return False, "Invalid schema_version"
    if not contract.get("task_id"): return False, "Empty task_id"
    
    baseline = contract.get("baseline")
    if not isinstance(baseline, dict): return False, "Missing or invalid baseline"
    if not isinstance(baseline.get("head"), str) or len(baseline.get("head")) != 40: return False, "Invalid baseline.head"
    if not isinstance(baseline.get("preexisting_untracked_paths"), list): return False, "Invalid preexisting_untracked_paths"
    
    if not isinstance(contract.get("primary_files"), list): return False, "Invalid primary_files"
    
    scope = contract.get("conditional_scope")
    if not isinstance(scope, dict): return False, "Missing or invalid conditional_scope"
    if not isinstance(scope.get("approved"), bool): return False, "Invalid approved"
    
    limits = scope.get("limits")
    if not isinstance(limits, dict): return False, "Missing or invalid limits"
    mt = limits.get("max_total_files")
    mp = limits.get("max_production_files")
    mtest = limits.get("max_test_files")
    if not (isinstance(mt, int) and isinstance(mp, int) and isinstance(mtest, int)): return False, "Limits must be integers"
    if mt < 0 or mp < 0 or mtest < 0: return False, "Limits cannot be negative"
    if mt < mp or mt < mtest: return False, "Total limit must be >= prod and test limits"
    
    allowed = scope.get("allowed_paths")
    if not isinstance(allowed, list): return False, "Invalid allowed_paths"
    for a in allowed:
        if not isinstance(a, dict): return False, "allowed_path item must be object"
        if not isinstance(a.get("pattern"), str): return False, "allowed_path missing pattern"
        role = a.get("role")
        if role not in ("test", "production"): return False, "allowed_path role must be test or production"
        act = a.get("allowed_change_types")
        if not isinstance(act, list): return False, "allowed_path missing allowed_change_types"
        for t in act:
            if t not in ("added", "modified"): return False, "allowed_change_types must be added or modified"
            
    forbidden = scope.get("forbidden_paths")
    if not isinstance(forbidden, list): return False, "Invalid forbidden_paths"
    
    return True, ""

def safe_path(repo_root, path_str):
    if os.path.isabs(path_str):
        return None, "Absolute path"
    if ".." in path_str.split(os.sep):
        return None, "Traversal path"
    try:
        p = (repo_root / path_str).resolve()
        if not str(p).startswith(str(repo_root)):
            return None, "Outside repo root"
        # Check for symlink
        if (repo_root / path_str).is_symlink():
            return None, "Symlink"
        return str(p.relative_to(repo_root)), ""
    except Exception as e:
        return None, f"Resolution error: {e}"

def parse_git_status(repo_root):
    # Porcelein format v1
    res = subprocess.run(["git", "status", "--porcelain", "-z", "-uall"], cwd=repo_root, capture_output=True, text=True, check=True)
    items = res.stdout.split('\0')
    changes = {}
    i = 0
    while i < len(items) - 1:
        item = items[i]
        if not item:
            i += 1
            continue
        status = item[:2]
        path = item[3:]
        
        # If it's a rename, there's another path after it
        if "R" in status or "C" in status:
            i += 1
            path = items[i]
            changes[path] = "unknown"
            i += 1
            continue
            
        if status == "??":
            changes[path] = "added"
        elif "D" in status:
            changes[path] = "deleted"
        elif status in (" A", "A ", "AA", "AM"):
            changes[path] = "added"
        elif status in (" M", "M ", "MM"):
            changes[path] = "modified"
        else:
            changes[path] = "unknown"
        i += 1
    return changes

def check_pattern(path, patterns):
    for pat in patterns:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path, pat.replace("/**", "/*")):
            return True
        if "/**/" in pat:
            parts = pat.split("/**/")
            if path.startswith(parts[0]) and fnmatch.fnmatch(path[len(parts[0]):], "/*" + parts[1]):
                return True
        if pat.endswith("**") and path.startswith(pat[:-2]):
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="AOS Conditional Scope Checker")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--contract", type=str, default="aos/templates/execution-artifacts/aos-build-step-scope-contract-template.json")
    args = parser.parse_args()

    try:
        repo_root = get_repo_root()
    except Exception as e:
        print_result(UNKNOWN_BLOCKED, "GIT_ERROR", [str(e)], args.json)

    contract_path = repo_root / args.contract
    if not contract_path.exists():
        print_result(UNKNOWN_BLOCKED, "REQUIRED_CONTRACT_MISSING", ["Contract file not found"], args.json)

    try:
        with open(contract_path, "r") as f:
            contract = json.load(f)
    except Exception as e:
        print_result(UNKNOWN_BLOCKED, "INVALID_CONTRACT", [f"JSON parse error: {e}"], args.json)

    valid_struct, err = validate_structure(contract)
    if not valid_struct:
        print_result(UNKNOWN_BLOCKED, "INVALID_CONTRACT", [err], args.json)
        
    if contract.get("schema_version") != 1:
        print_result(UNKNOWN_BLOCKED, "UNSUPPORTED_SCHEMA_VERSION", ["Only version 1 is supported"], args.json)

    scope = contract.get("conditional_scope", {})
    if not scope.get("approved"):
        print_result(HUMAN_REVIEW_REQUIRED, "CONDITIONAL_SCOPE_NOT_APPROVED", ["Contract not approved"], args.json)

    baseline = contract.get("baseline", {})
    head = get_head_sha(repo_root)
    if head != baseline.get("head"):
        print_result(HUMAN_REVIEW_REQUIRED, "BASELINE_HEAD_CHANGED", [f"Current HEAD {head} != Contract HEAD {baseline.get('head')}"], args.json)

    preexisting = set(baseline.get("preexisting_untracked_paths", []))
    primary_files = set(contract.get("primary_files", []))
    forbidden_paths = scope.get("forbidden_paths", [])
    allowed_paths = scope.get("allowed_paths", [])
    limits = scope.get("limits", {})

    git_changes = parse_git_status(repo_root)

    conditional_files = {}
    for p, ctype in git_changes.items():
        sp, serr = safe_path(repo_root, p)
        if sp is None:
            print_result(UNKNOWN_BLOCKED, "PATH_SAFETY_UNKNOWN", [f"{p}: {serr}"], args.json)
            
        if sp.startswith(".aos-tmp/") or sp.startswith(".venv/") or sp.startswith(".git/"):
            continue
        if sp in preexisting and ctype == "added":
            continue
        if sp in primary_files:
            continue
            
        conditional_files[sp] = ctype

    if not conditional_files:
        print_result(PASS, "CONDITIONAL_SCOPE_VALID", [], args.json, {"total_conditional": 0})

    errors = []
    prod_count = 0
    test_count = 0
    
    for f, ctype in conditional_files.items():
        if ctype not in ("added", "modified"):
            print_result(UNKNOWN_BLOCKED, "UNSUPPORTED_OR_UNKNOWN_CHANGE_TYPE", [f"File {f} has unsupported change type {ctype}"], args.json)
            
        if any(f.startswith(fp) or f == fp for fp in forbidden_paths):
            errors.append(f"Forbidden path activated: {f}")
            continue
            
        role = None
        allowed_types = []
        for a in allowed_paths:
            if check_pattern(f, [a["pattern"]]):
                role = a["role"]
                allowed_types = a["allowed_change_types"]
                break
                
        if not role:
            errors.append(f"File not matching any allowed patterns: {f}")
            continue
            
        if ctype not in allowed_types:
            errors.append(f"File {f} change type {ctype} not allowed for role {role}")
            continue

        if role == "test":
            test_count += 1
        else:
            prod_count += 1

    total_count = prod_count + test_count
    
    if total_count > limits.get("max_total_files", 0):
        errors.append(f"Max total files exceeded")
    if prod_count > limits.get("max_production_files", 0):
        errors.append(f"Max production files exceeded")
    if test_count > limits.get("max_test_files", 0):
        errors.append(f"Max test files exceeded")

    if errors:
        is_forbidden = any("Forbidden path" in e for e in errors)
        if is_forbidden:
            print_result(HUMAN_REVIEW_REQUIRED, "FORBIDDEN_PATH_ACTIVATED", errors, args.json)
        else:
            print_result(HUMAN_REVIEW_REQUIRED, "CONDITIONAL_SCOPE_LIMIT_EXCEEDED", errors, args.json)

    print_result(PASS, "CONDITIONAL_SCOPE_VALID", [], args.json, {
        "total_conditional": total_count,
        "prod_count": prod_count,
        "test_count": test_count
    })

if __name__ == "__main__":
    main()
