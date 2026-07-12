#!/usr/bin/env python3
import sys
import json
import argparse
import subprocess
import os
import fnmatch
import tempfile
from pathlib import Path

PASS = "PASS"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"
BLOCKED = "BLOCKED"

def print_result(status, reason, errors=None, is_json=False, stats=None, extra=None):
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
        if extra:
            out.update(extra)
        print(json.dumps(out, indent=2))
    else:
        print(f"final_status: {status}")
        print(f"reason_code: {reason}")
        if errors:
            print("errors:")
            for e in errors:
                print(f"  - {e}")
    if status == HUMAN_REVIEW_REQUIRED:
        sys.exit(2)
    if status == UNKNOWN_BLOCKED:
        sys.exit(3)
    if status == BLOCKED:
        sys.exit(4)
    sys.exit(0)

def run_git(repo_root, args, env=None):
    git_env = os.environ.copy()
    if env:
        git_env.update(env)
    return subprocess.run(["git"] + args, cwd=repo_root, env=git_env, capture_output=True, text=True, check=True)

def get_repo_root():
    res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return Path(res.stdout.strip()).resolve()

def get_head_sha(repo_root):
    try:
        res = run_git(repo_root, ["rev-parse", "HEAD"])
        return res.stdout.strip()
    except:
        return ""

def get_current_branch(repo_root):
    try:
        res = run_git(repo_root, ["branch", "--show-current"])
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
    if "candidate_files" in contract and not isinstance(contract.get("candidate_files"), list): return False, "Invalid candidate_files"
    if "repository" in contract and not isinstance(contract.get("repository"), str): return False, "Invalid repository"
    if "branch" in contract and not isinstance(contract.get("branch"), str): return False, "Invalid branch"
    if "commit_message" in contract and not isinstance(contract.get("commit_message"), str): return False, "Invalid commit_message"
    
    scope = contract.get("conditional_scope")
    if not isinstance(scope, dict): return False, "Missing or invalid conditional_scope"
    if not isinstance(scope.get("approved", scope.get("enabled")), bool): return False, "Invalid approved/enabled"
    
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
    res = run_git(repo_root, ["status", "--porcelain", "-z", "-uall"])
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

def candidate_files(contract):
    return contract.get("candidate_files") or contract.get("primary_files") or []

def validate_candidate_paths(repo_root, paths):
    safe_paths = []
    for path in paths:
        if not isinstance(path, str) or not path:
            return None, "Invalid candidate file path"
        sp, serr = safe_path(repo_root, path)
        if sp is None:
            return None, f"{path}: {serr}"
        safe_paths.append(sp)
    return safe_paths, ""

def get_contract_candidate_paths(repo_root, contract):
    raw_paths = contract.get("candidate_files")
    if raw_paths is None:
        return None, None, ""
    safe_paths, err = validate_candidate_paths(repo_root, raw_paths)
    if safe_paths is None:
        return None, None, err
    duplicates = sorted({p for p in safe_paths if safe_paths.count(p) > 1})
    return raw_paths, safe_paths, duplicates

def get_actual_changed_paths(repo_root, contract):
    baseline = contract.get("baseline", {})
    preexisting = set(baseline.get("preexisting_untracked_paths", []))
    git_changes = parse_git_status(repo_root)
    changed_paths = {}
    for p, ctype in git_changes.items():
        if p.startswith(".aos-tmp/") or p.startswith(".venv/") or p.startswith(".git/"):
            continue

        sp, serr = safe_path(repo_root, p)
        if sp is None:
            return None, "PATH_SAFETY_UNKNOWN", [f"{p}: {serr}"]
        if sp in preexisting and ctype == "added":
            continue
        if ctype not in ("added", "modified", "deleted"):
            return None, "CANDIDATE_CHANGED_PATH_SET_UNKNOWN", [f"File {sp} has unsupported change type {ctype}"]
        changed_paths[sp] = ctype
    return sorted(changed_paths), "", []

def enforce_exact_candidate_set(repo_root, contract):
    _raw_paths, contract_paths, duplicates = get_contract_candidate_paths(repo_root, contract)
    if contract_paths is None:
        return True, None
    if duplicates:
        return False, {
            "status": BLOCKED,
            "reason": "CANDIDATE_FILE_SET_MISMATCH",
            "errors": [f"Duplicate contract candidate path: {p}" for p in duplicates],
            "extra": {
                "mismatch_type": "DUPLICATE_CONTRACT_PATH",
                "candidate_file_count": len(sorted(set(contract_paths))),
            },
        }

    actual_paths, reason, errors = get_actual_changed_paths(repo_root, contract)
    if actual_paths is None:
        return False, {
            "status": UNKNOWN_BLOCKED,
            "reason": reason,
            "errors": errors,
            "extra": {},
        }

    contract_set = set(contract_paths)
    actual_set = set(actual_paths)
    if contract_set == actual_set:
        return True, {
            "candidate_file_count": len(contract_set),
            "actual_changed_count": len(actual_set),
        }

    extra_contract = sorted(contract_set - actual_set)
    if extra_contract:
        return False, {
            "status": BLOCKED,
            "reason": "CANDIDATE_FILE_SET_MISMATCH",
            "errors": [f"Contract candidate path is unchanged relative to baseline: {p}" for p in extra_contract],
            "extra": {
                "mismatch_type": "EXTRA_UNCHANGED_CONTRACT_PATH",
                "candidate_file_count": len(contract_set),
                "actual_changed_count": len(actual_set),
            },
        }

    missing_contract = sorted(actual_set - contract_set)
    return False, {
        "status": BLOCKED,
        "reason": "CANDIDATE_FILE_SET_MISMATCH",
        "errors": [f"Changed path missing from contract candidate_files: {p}" for p in missing_contract],
        "extra": {
            "mismatch_type": "CHANGED_PATH_MISSING_FROM_CONTRACT",
            "candidate_file_count": len(contract_set),
            "actual_changed_count": len(actual_set),
        },
    }

def compute_candidate_content_oid(repo_root, contract):
    exact_match, details = enforce_exact_candidate_set(repo_root, contract)
    if not exact_match:
        raise ValueError(json.dumps(details))

    paths, err = validate_candidate_paths(repo_root, candidate_files(contract))
    if paths is None:
        raise ValueError(err)
    if not paths:
        raise ValueError("candidate_files must not be empty")

    with tempfile.TemporaryDirectory(prefix="aos-freeze-index-") as tmp:
        env = {"GIT_INDEX_FILE": str(Path(tmp) / "index")}
        run_git(repo_root, ["read-tree", "HEAD"], env=env)
        run_git(repo_root, ["add", "--"] + paths, env=env)
        res = run_git(repo_root, ["write-tree"], env=env)
        return res.stdout.strip(), paths

def get_commit_parent(repo_root, commit="HEAD"):
    res = run_git(repo_root, ["rev-list", "--parents", "-n", "1", commit])
    parts = res.stdout.strip().split()
    if len(parts) != 2:
        return ""
    return parts[1]

def get_commit_tree(repo_root, commit="HEAD"):
    res = run_git(repo_root, ["rev-parse", f"{commit}^{{tree}}"])
    return res.stdout.strip()

def get_commit_message(repo_root, commit="HEAD"):
    res = run_git(repo_root, ["log", "-1", "--format=%s", commit])
    return res.stdout.rstrip("\n")

def get_committed_paths(repo_root, commit="HEAD"):
    res = run_git(repo_root, ["diff-tree", "--no-commit-id", "--name-only", "-r", "--no-renames", commit])
    return sorted(p for p in res.stdout.splitlines() if p)

def require_expected_oid(value, name):
    if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        return f"Invalid {name}"
    return ""

def mode_freeze(repo_root, contract, args):
    try:
        tree_oid, paths = compute_candidate_content_oid(repo_root, contract)
    except subprocess.CalledProcessError as e:
        print_result(UNKNOWN_BLOCKED, "GIT_ERROR", [e.stderr or str(e)], args.json)
    except ValueError as e:
        try:
            details = json.loads(str(e))
        except Exception:
            print_result(UNKNOWN_BLOCKED, "CANDIDATE_FREEZE_UNKNOWN", [str(e)], args.json)
        print_result(details["status"], details["reason"], details["errors"], args.json, None, details.get("extra"))
    except Exception as e:
        print_result(UNKNOWN_BLOCKED, "CANDIDATE_FREEZE_UNKNOWN", [str(e)], args.json)

    print_result(
        PASS,
        "CANDIDATE_FREEZE_VERIFIED",
        [],
        args.json,
        {"candidate_file_count": len(paths)},
        {"candidate_content_oid": tree_oid},
    )

def mode_verify_freeze(repo_root, contract, args):
    err = require_expected_oid(args.expected_tree_oid, "expected-tree-oid")
    if err:
        print_result(UNKNOWN_BLOCKED, "INVALID_EXPECTED_TREE_OID", [err], args.json)
    try:
        tree_oid, paths = compute_candidate_content_oid(repo_root, contract)
    except subprocess.CalledProcessError as e:
        print_result(UNKNOWN_BLOCKED, "GIT_ERROR", [e.stderr or str(e)], args.json)
    except ValueError as e:
        try:
            details = json.loads(str(e))
        except Exception:
            print_result(UNKNOWN_BLOCKED, "CANDIDATE_FREEZE_UNKNOWN", [str(e)], args.json)
        print_result(details["status"], details["reason"], details["errors"], args.json, None, details.get("extra"))
    except Exception as e:
        print_result(UNKNOWN_BLOCKED, "CANDIDATE_FREEZE_UNKNOWN", [str(e)], args.json)

    if tree_oid != args.expected_tree_oid:
        print_result(
            BLOCKED,
            "CANDIDATE_FREEZE_MISMATCH",
            ["Candidate content differs from expected freeze tree"],
            args.json,
            {"candidate_file_count": len(paths)},
        )

    print_result(PASS, "CANDIDATE_FREEZE_MATCH", [], args.json, {"candidate_file_count": len(paths)})

def mode_verify_authorization(repo_root, contract, args):
    if not args.authorization_task_id:
        print_result(BLOCKED, "AUTHORIZATION_TASK_ID_MISSING", ["authorization task_id missing"], args.json)
    if not args.expected_task_id:
        print_result(BLOCKED, "AUTHORIZATION_TASK_ID_MISSING", ["expected task_id missing"], args.json)
    if args.authorization_task_id != args.expected_task_id:
        print_result(BLOCKED, "AUTHORIZATION_TASK_ID_MISMATCH", [f"authorization task_id {args.authorization_task_id} != expected task_id {args.expected_task_id}"], args.json)
    if contract.get("task_id") != args.expected_task_id:
        print_result(BLOCKED, "AUTHORIZATION_CANDIDATE_MISMATCH", [f"contract task_id {contract.get('task_id')} != expected task_id {args.expected_task_id}"], args.json)

    required = {
        "expected_repository": args.expected_repository,
        "expected_branch": args.expected_branch,
        "expected_baseline_oid": args.expected_baseline_oid,
        "expected_tree_oid": args.expected_tree_oid,
        "expected_commit_message": args.expected_commit_message,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print_result(UNKNOWN_BLOCKED, "AUTHORIZATION_BINDING_INCOMPLETE", missing, args.json)
    for value, name in ((args.expected_baseline_oid, "expected-baseline-oid"), (args.expected_tree_oid, "expected-tree-oid")):
        err = require_expected_oid(value, name)
        if err:
            print_result(UNKNOWN_BLOCKED, "INVALID_AUTHORIZATION_BINDING", [err], args.json)

    try:
        tree_oid, _paths = compute_candidate_content_oid(repo_root, contract)
    except subprocess.CalledProcessError as e:
        print_result(UNKNOWN_BLOCKED, "GIT_ERROR", [e.stderr or str(e)], args.json)
    except ValueError as e:
        try:
            details = json.loads(str(e))
        except Exception:
            print_result(UNKNOWN_BLOCKED, "AUTHORIZATION_VERIFICATION_UNKNOWN", [str(e)], args.json)
        print_result(details["status"], details["reason"], details["errors"], args.json, None, details.get("extra"))
    except Exception as e:
        print_result(UNKNOWN_BLOCKED, "AUTHORIZATION_VERIFICATION_UNKNOWN", [str(e)], args.json)

    errors = []
    if contract.get("repository") and contract.get("repository") != args.expected_repository:
        errors.append("Repository binding mismatch")
    if contract.get("branch") and contract.get("branch") != args.expected_branch:
        errors.append("Branch binding mismatch")
    if contract.get("baseline", {}).get("head") != args.expected_baseline_oid:
        errors.append("Baseline binding mismatch")
    if tree_oid != args.expected_tree_oid:
        errors.append("Tree binding mismatch")
    if contract.get("commit_message") and contract.get("commit_message") != args.expected_commit_message:
        errors.append("Commit message binding mismatch")

    if errors:
        print_result(BLOCKED, "AUTHORIZATION_BINDING_MISMATCH", errors, args.json)

    print_result(PASS, "AUTHORIZATION_BINDING_VERIFIED", [], args.json)

def mode_post_commit_verify(repo_root, contract, args):
    required = {
        "expected_parent_oid": args.expected_parent_oid,
        "expected_tree_oid": args.expected_tree_oid,
        "expected_commit_message": args.expected_commit_message,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print_result(UNKNOWN_BLOCKED, "POST_COMMIT_BINDING_INCOMPLETE", missing, args.json)
    for value, name in ((args.expected_parent_oid, "expected-parent-oid"), (args.expected_tree_oid, "expected-tree-oid")):
        err = require_expected_oid(value, name)
        if err:
            print_result(UNKNOWN_BLOCKED, "INVALID_POST_COMMIT_BINDING", [err], args.json)

    _raw_paths, paths, duplicates = get_contract_candidate_paths(repo_root, contract)
    if paths is None:
        print_result(UNKNOWN_BLOCKED, "INVALID_CANDIDATE_SCOPE", [duplicates], args.json)
    if duplicates:
        print_result(BLOCKED, "CANDIDATE_FILE_SET_MISMATCH", [f"Duplicate contract candidate path: {p}" for p in duplicates], args.json, {"mismatch_type": "DUPLICATE_CONTRACT_PATH", "candidate_file_count": len(sorted(set(paths)))})

    try:
        parent = get_commit_parent(repo_root)
        tree = get_commit_tree(repo_root)
        message = get_commit_message(repo_root)
        committed_paths = get_committed_paths(repo_root)
    except subprocess.CalledProcessError as e:
        print_result(UNKNOWN_BLOCKED, "GIT_ERROR", [e.stderr or str(e)], args.json)

    errors = []
    if parent != args.expected_parent_oid:
        errors.append("Parent mismatch")
    if tree != args.expected_tree_oid:
        errors.append("Tree mismatch")
    if message != args.expected_commit_message:
        errors.append("Commit message mismatch")
    if committed_paths != sorted(paths):
        errors.append("Committed path set mismatch")

    if errors:
        print_result(BLOCKED, "POST_COMMIT_BINDING_MISMATCH", errors, args.json, {"committed_path_count": len(committed_paths)})

    print_result(PASS, "POST_COMMIT_BINDING_VERIFIED", [], args.json, {"committed_path_count": len(committed_paths)})

def mode_scope(repo_root, contract, args):
    scope = contract.get("conditional_scope", {})
    scope_enabled = scope.get("approved", scope.get("enabled"))
    if not scope_enabled:
        print_result(HUMAN_REVIEW_REQUIRED, "CONDITIONAL_SCOPE_NOT_APPROVED", ["Contract not approved"], args.json)

    baseline = contract.get("baseline", {})
    head = get_head_sha(repo_root)
    if head != baseline.get("head"):
        print_result(HUMAN_REVIEW_REQUIRED, "BASELINE_HEAD_CHANGED", [f"Current HEAD {head} != Contract HEAD {baseline.get('head')}"], args.json)

    exact_match, exact_details = enforce_exact_candidate_set(repo_root, contract)
    if not exact_match:
        print_result(
            exact_details["status"],
            exact_details["reason"],
            exact_details["errors"],
            args.json,
            None,
            exact_details.get("extra"),
        )

    preexisting = set(baseline.get("preexisting_untracked_paths", []))
    primary_files = set(contract.get("primary_files", []))
    forbidden_paths = scope.get("forbidden_paths", [])
    allowed_paths = scope.get("allowed_paths", [])
    limits = scope.get("limits", {})

    git_changes = parse_git_status(repo_root)

    conditional_files = {}
    for p, ctype in git_changes.items():
        if p.startswith(".aos-tmp/") or p.startswith(".venv/") or p.startswith(".git/"):
            continue

        sp, serr = safe_path(repo_root, p)
        if sp is None:
            print_result(UNKNOWN_BLOCKED, "PATH_SAFETY_UNKNOWN", [f"{p}: {serr}"], args.json)
            
        if sp in preexisting and ctype == "added":
            continue
        if sp in primary_files:
            continue
            
        conditional_files[sp] = ctype

    if not conditional_files:
        stats = {"total_conditional": 0}
        if exact_details:
            stats["candidate_file_count"] = exact_details["candidate_file_count"]
        print_result(PASS, "CONDITIONAL_SCOPE_VALID", [], args.json, stats)

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

    stats = {
        "total_conditional": total_count,
        "prod_count": prod_count,
        "test_count": test_count,
    }
    if exact_details:
        stats["candidate_file_count"] = exact_details["candidate_file_count"]
    print_result(PASS, "CONDITIONAL_SCOPE_VALID", [], args.json, stats)

def main():
    parser = argparse.ArgumentParser(description="AOS Conditional Scope Checker")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--contract", type=str, default="aos/templates/execution-artifacts/aos-build-step-scope-contract-template.json")
    parser.add_argument("--mode", choices=["scope", "freeze", "verify-freeze", "verify-authorization", "post-commit-verify"], default="scope")
    parser.add_argument("--expected-tree-oid")
    parser.add_argument("--expected-parent-oid")
    parser.add_argument("--expected-baseline-oid")
    parser.add_argument("--expected-repository")
    parser.add_argument("--expected-branch")
    parser.add_argument("--expected-commit-message")
    parser.add_argument("--expected-task-id")
    parser.add_argument("--authorization-task-id")
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

    if args.mode == "freeze":
        mode_freeze(repo_root, contract, args)
    if args.mode == "verify-freeze":
        mode_verify_freeze(repo_root, contract, args)
    if args.mode == "verify-authorization":
        mode_verify_authorization(repo_root, contract, args)
    if args.mode == "post-commit-verify":
        mode_post_commit_verify(repo_root, contract, args)
    mode_scope(repo_root, contract, args)

if __name__ == "__main__":
    main()
