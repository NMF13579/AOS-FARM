#!/usr/bin/env python3
"""
Unified AOS Validate
Validation orchestration only.
It must not: create tasks, mutate queue, write Evidence, claim approval, commit, push, release, change lifecycle state, assign Risk Profile.
"""

import subprocess
import json
import sys
import argparse

VALIDATION_COMMANDS = [
    ["python3", "aos/scripts/aos_install.py", "--dry-run"],
    ["python3", "aos/scripts/aos_consumer_self_test.py"],
    ["python3", "aos/scripts/aos_task_document_check.py", "task", "--validate-all"],
    ["python3", "aos/scripts/aos_task_document_check.py", "queue", "--list"],
    ["python3", "aos/scripts/aos_task_document_check.py", "queue", "--next"],
    ["python3", "aos/scripts/aos_task_document_check.py", "task", "--readiness-all"],
    ["python3", "aos/scripts/aos_doctor.py"],
    ["python3", "aos/scripts/aos_queue_dashboard.py"]
]

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return {
            "command": " ".join(cmd),
            "status": "PASS" if result.returncode == 0 else "FAILED",
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except FileNotFoundError:
        return {
            "command": " ".join(cmd),
            "status": "NOT_RUN",
            "reason": "Command or script not found"
        }
    except subprocess.TimeoutExpired:
        return {
            "command": " ".join(cmd),
            "status": "NOT_RUN",
            "reason": "Timeout expired"
        }
    except Exception as e:
        return {
            "command": " ".join(cmd),
            "status": "NOT_RUN",
            "reason": str(e)
        }

def determine_overall_status(results):
    has_failed = False
    has_not_run = False
    
    for r in results:
        status = r.get("status")
        stdout = r.get("stdout", "")
        stderr = r.get("stderr", "")
        
        if status == "FAILED":
            if "UNKNOWN_BLOCKED" in stdout or "UNKNOWN_BLOCKED" in stderr:
                return "UNKNOWN_BLOCKED"
            if "BLOCKED" in stdout or "BLOCKED" in stderr:
                return "BLOCKED"
            has_failed = True
        elif status == "NOT_RUN":
            has_not_run = True
            
    if has_failed:
        return "FAILED_OR_BLOCKED"
    if has_not_run:
        return "PASS_WITH_NOT_RUN"
    return "PASS"

def main():
    parser = argparse.ArgumentParser(description="Unified AOS Validate")
    parser.add_argument("target", nargs="?", default="all", help="Target to validate (e.g. 'all')")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    results = []
    
    commands_to_run = VALIDATION_COMMANDS
    if args.target != "all":
        # Extend to support specific targets if needed later
        pass

    for cmd in commands_to_run:
        res = run_command(cmd)
        results.append(res)
        
    overall_status = determine_overall_status(results)
    
    output = {
        "command": "aos validate",
        "target": args.target,
        "overall_status": overall_status,
        "approval_claimed": False,
        "commit_authorized": False,
        "push_authorized": False,
        "release_authorized": False,
        "results": results
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("=== Unified AOS Validate ===")
        print("Validation orchestration only.")
        print("PASS is not approval. PASS is not execution authorization.\n")
        
        for r in results:
            print(f"Command: {r['command']}")
            print(f"Status:  {r['status']}")
            if r.get("reason"):
                print(f"Reason:  {r['reason']}")
            if r.get("return_code", 0) != 0:
                print(f"Code:    {r['return_code']}")
                if r.get("stderr"):
                    print("Stderr excerpt:")
                    print("\n".join(r['stderr'].split('\n')[:3]))
            print("-" * 40)
            
        print(f"Overall Status: {overall_status}")
        print("\nNote: BLOCKED beats HUMAN_REVIEW_REQUIRED. UNKNOWN_BLOCKED beats PASS.")
        print("NOT_RUN is reported, never converted to PASS.")

if __name__ == "__main__":
    main()
