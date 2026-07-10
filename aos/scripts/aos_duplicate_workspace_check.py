#!/usr/bin/env python3
import sys
import json
import argparse
import subprocess
import hashlib
import os
from pathlib import Path

PASS = "PASS"
FAILED_OR_BLOCKED = "FAILED_OR_BLOCKED"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"

EXACT_DUPLICATE = "EXACT_DUPLICATE"
CONTENT_DIVERGED = "CONTENT_DIVERGED"
ORPHAN_NO_CANONICAL_PAIR = "ORPHAN_NO_CANONICAL_PAIR"
AMBIGUOUS = "AMBIGUOUS"

DUPLICATE_SUFFIXES = (
    " conflicted copy",
    " copy",
    " (1)",
    " (2)",
    " 2",
)

def get_repo_root():
    try:
        res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
        return Path(res.stdout.strip()).resolve()
    except Exception:
        return None

def get_git_state(repo_root):
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=repo_root, capture_output=True, text=True, check=True).stdout.splitlines()
        untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=repo_root, capture_output=True, text=True, check=True).stdout.splitlines()
        staged = subprocess.run(["git", "diff", "--name-only", "--cached"], cwd=repo_root, capture_output=True, text=True, check=True).stdout.splitlines()
        return set(tracked), set(untracked), set(staged)
    except Exception:
        return None, None, None

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def file_byte_compare(path1, path2):
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        while True:
            c1 = f1.read(8192)
            c2 = f2.read(8192)
            if c1 != c2:
                return False
            if not c1:
                return True

def determine_counterpart(duplicate_path_obj):
    stem = duplicate_path_obj.stem
    for pat in DUPLICATE_SUFFIXES:
        if stem.endswith(pat):
            new_stem = stem[:-len(pat)]
            return duplicate_path_obj.with_name(new_stem + duplicate_path_obj.suffix)
    return None

def aggregate_status(summary: dict) -> tuple[str, int]:
    if summary["orphan_count"] > 0 or summary["ambiguous_count"] > 0:
        return UNKNOWN_BLOCKED, 3
    if summary["content_diverged_count"] > 0:
        return HUMAN_REVIEW_REQUIRED, 2
    if summary["exact_duplicate_count"] > 0:
        return FAILED_OR_BLOCKED, 1
    return PASS, 0

def is_path_safe(path: Path, repo_root: Path):
    try:
        resolved = path.resolve()
        resolved.relative_to(repo_root)
        return True
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="AOS Duplicate Workspace Checker")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    errors = []

    repo_root = get_repo_root()
    if repo_root is None:
        errors.append("Git command failure: repo root")
        if args.json:
            print(json.dumps({"checker": "duplicate_workspace", "final_status": UNKNOWN_BLOCKED, "repository_root": ".", "scan_complete": False, "errors": errors}))
        else:
            print("Final Status:", UNKNOWN_BLOCKED)
            print("Errors:", errors)
        sys.exit(3)

    tracked, untracked, staged = get_git_state(repo_root)
    if tracked is None:
        errors.append("Git command failure: git state")
        if args.json:
            print(json.dumps({"checker": "duplicate_workspace", "final_status": UNKNOWN_BLOCKED, "repository_root": ".", "scan_complete": False, "errors": errors}))
        else:
            print("Final Status:", UNKNOWN_BLOCKED)
            print("Errors:", errors)
        sys.exit(3)

    items = []
    summary = {
        "suspicious_count": 0,
        "exact_duplicate_count": 0,
        "content_diverged_count": 0,
        "orphan_count": 0,
        "ambiguous_count": 0,
        "tracked_duplicate_count": 0,
        "untracked_duplicate_count": 0,
        "staged_duplicate_count": 0
    }

    try:
        for root, dirs, files in os.walk(repo_root, followlinks=False):
            if Path(root).resolve() == repo_root:
                dirs[:] = [name for name in dirs if name not in {".git", ".aos-tmp", ".venv"}]

            for f in files:
                p = Path(root) / f
                if not p.is_file():
                    continue
                
                try:
                    rel_path = p.relative_to(repo_root)
                    rel_str = str(rel_path)
                except ValueError:
                    continue

                counterpart = determine_counterpart(p)
                if not counterpart:
                    continue

                summary["suspicious_count"] += 1
                
                try:
                    rel_counterpart_str = str(counterpart.relative_to(repo_root))
                except ValueError:
                    rel_counterpart_str = str(counterpart)

                item = {
                    "duplicate_path": rel_str,
                    "counterpart_path": rel_counterpart_str,
                    "classification": "",
                    "duplicate_sha256": None,
                    "counterpart_sha256": None,
                    "duplicate_tracked": rel_str in tracked,
                    "duplicate_untracked": rel_str in untracked,
                    "duplicate_staged": rel_str in staged
                }

                if item["duplicate_tracked"]:
                    summary["tracked_duplicate_count"] += 1
                if item["duplicate_untracked"]:
                    summary["untracked_duplicate_count"] += 1
                if item["duplicate_staged"]:
                    summary["staged_duplicate_count"] += 1

                if not is_path_safe(p, repo_root) or not is_path_safe(counterpart, repo_root):
                    item["classification"] = AMBIGUOUS
                    summary["ambiguous_count"] += 1
                    items.append(item)
                    continue

                if not counterpart.exists():
                    item["classification"] = ORPHAN_NO_CANONICAL_PAIR
                    summary["orphan_count"] += 1
                elif not counterpart.is_file():
                    item["classification"] = AMBIGUOUS
                    summary["ambiguous_count"] += 1
                else:
                    try:
                        dup_sha = get_sha256(p)
                        cp_sha = get_sha256(counterpart)
                        item["duplicate_sha256"] = dup_sha
                        item["counterpart_sha256"] = cp_sha
                        
                        if p.stat().st_size == counterpart.stat().st_size and dup_sha == cp_sha and file_byte_compare(p, counterpart):
                            item["classification"] = EXACT_DUPLICATE
                            summary["exact_duplicate_count"] += 1
                        else:
                            item["classification"] = CONTENT_DIVERGED
                            summary["content_diverged_count"] += 1
                    except Exception as e:
                        errors.append(f"Read failure on {rel_str} or counterpart: {e}")
                        item["classification"] = AMBIGUOUS
                        summary["ambiguous_count"] += 1
                        
                items.append(item)
            
    except Exception as e:
        errors.append(f"Scan failure: {e}")
        if args.json:
            print(json.dumps({"checker": "duplicate_workspace", "final_status": UNKNOWN_BLOCKED, "repository_root": ".", "scan_complete": False, "errors": errors}))
        else:
            print("Final Status:", UNKNOWN_BLOCKED)
            print("Errors:", errors)
        sys.exit(3)

    items.sort(key=lambda x: x["duplicate_path"])

    final_status, exit_code = aggregate_status(summary)
    
    if errors:
        final_status = UNKNOWN_BLOCKED
        exit_code = 3

    if args.json:
        out = {
            "checker": "duplicate_workspace",
            "final_status": final_status,
            "repository_root": ".",
            "scan_complete": len(errors) == 0,
            "errors": errors,
            "summary": summary,
            "items": items
        }
        print(json.dumps(out, indent=2))
    else:
        print(f"Final Status: {final_status}")
        if errors:
            print(f"Errors: {errors}")
        print(f"Suspicious Count: {summary['suspicious_count']}")
        print(f"Exact Duplicate Count: {summary['exact_duplicate_count']}")
        print(f"Content Diverged Count: {summary['content_diverged_count']}")
        print(f"Orphan Count: {summary['orphan_count']}")
        print(f"Ambiguous Count: {summary['ambiguous_count']}")
        print(f"Staged Duplicate Count: {summary['staged_duplicate_count']}")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
