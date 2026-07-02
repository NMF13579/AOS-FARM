#!/usr/bin/env python3
"""
Review & Handoff Package Generator
Read-only git/package inspection.
Never outputs APPROVED.
"""

import argparse
import subprocess
import json
import sys

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(description="AOS Review & Handoff Package Generator")
    parser.add_argument("--since", default="origin/dev", help="Git ref to compare against")
    parser.add_argument("--include-validation", action="store_true", help="Run read-only validation commands")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    # Git inspection
    branch = run_command(["git", "branch", "--show-current"]) or "UNKNOWN"
    head = run_command(["git", "rev-parse", "HEAD"]) or "UNKNOWN"
    diff_stat = run_command(["git", "diff", "--stat", args.since]) or ""
    untracked = run_command(["git", "status", "--short", "--untracked-files=all"]) or ""

    validation_status = "NOT_RUN"
    validation_results = []

    if args.include_validation:
        try:
            val_result = subprocess.run(["python3", "aos/scripts/aos_validate.py", "all", "--json"], capture_output=True, text=True)
            if val_result.returncode == 0:
                try:
                    val_data = json.loads(val_result.stdout)
                    validation_status = val_data.get("overall_status", "UNKNOWN")
                    validation_results = val_data.get("results", [])
                except json.JSONDecodeError:
                    validation_status = "FAILED"
            else:
                validation_status = "FAILED"
        except Exception:
            validation_status = "FAILED"

    # Determine status
    if branch == "UNKNOWN" or head == "UNKNOWN":
        package_status = "UNKNOWN_BLOCKED"
    elif validation_status in ["FAILED", "BLOCKED", "FAILED_OR_BLOCKED", "UNKNOWN_BLOCKED"]:
        package_status = "CHANGES_REQUIRED"
    elif validation_status == "NOT_RUN":
        package_status = "READY_FOR_HUMAN_REVIEW"
    else:
        package_status = "READY_FOR_HUMAN_REVIEW"

    # Hardcoded safety fields
    approval_claimed = False
    commit_authorized = False
    push_authorized = False
    release_authorized = False

    if args.json:
        output = {
            "package_status": package_status,
            "branch": branch,
            "head": head,
            "since": args.since,
            "validation_status": validation_status,
            "approval_claimed": approval_claimed,
            "commit_authorized": commit_authorized,
            "push_authorized": push_authorized,
            "release_authorized": release_authorized,
            "diff_stat": diff_stat.split('\n') if diff_stat else [],
            "untracked_files": untracked.split('\n') if untracked else []
        }
        if args.include_validation:
            output["validation_results"] = validation_results
            
        print(json.dumps(output, indent=2))
    else:
        print("=== Review & Handoff Package ===")
        print(f"Status: {package_status}")
        print(f"Branch: {branch}")
        print(f"HEAD: {head}")
        print(f"Since: {args.since}")
        print(f"Validation Status: {validation_status}")
        print("---")
        print(f"Approval Claimed: {approval_claimed}")
        print(f"Commit Authorized: {commit_authorized}")
        print(f"Push Authorized: {push_authorized}")
        print(f"Release Authorized: {release_authorized}")
        print("---")
        print("Diff Stat:")
        print(diff_stat)
        print("---")
        print("Untracked Files:")
        print(untracked)

if __name__ == "__main__":
    main()
