#!/usr/bin/env python3
"""
AOS Doctor
Read-only validation aggregator.
Not validator authority. Not approval authority. Not lifecycle authority. Not Source of Truth.
"""

import subprocess
import json
import sys
import argparse

COMMANDS_TO_AGGREGATE = [
    ["python3", "aos/scripts/aos_install.py", "--dry-run"],
    ["python3", "aos/scripts/aos_consumer_self_test.py"],
    ["python3", "-m", "py_compile", "aos/scripts/aos_install.py"],
    ["python3", "-m", "py_compile", "aos/scripts/aos_consumer_self_test.py"],
    ["python3", "-m", "py_compile", "aos/scripts/aos_task_document_check.py"],
    ["python3", "-m", "py_compile", "aos/scripts/aos_doctor.py"],
    ["python3", "aos/scripts/aos_task_document_check.py", "task", "--validate-all"],
    ["python3", "aos/scripts/aos_task_document_check.py", "queue", "--list"],
    ["python3", "aos/scripts/aos_task_document_check.py", "queue", "--next"],
    ["python3", "aos/scripts/aos_task_document_check.py", "task", "--readiness-all"],
    ["python3", "-m", "unittest", "discover"]
]

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
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
        
        # Check for specific outputs in stdout/stderr if we want to be more granular,
        # but relying on return code for basic PASS/FAILED.
        if status == "FAILED":
            if "UNKNOWN_BLOCKED" in stdout or "UNKNOWN_BLOCKED" in stderr:
                return "UNKNOWN_BLOCKED"
            if "BLOCKED" in stdout or "BLOCKED" in stderr:
                return "BLOCKED"
            has_failed = True
        elif status == "NOT_RUN":
            has_not_run = True
            
        if "HUMAN_REVIEW_REQUIRED" in stdout or "HUMAN_REVIEW_REQUIRED" in stderr:
            # Not a failure if human review is expected, but if there's a hard block, that wins.
            pass
            
    if has_failed:
        return "FAILED_OR_BLOCKED"
    if has_not_run:
        return "PASS_WITH_NOT_RUN"
    return "PASS"

def main():
    parser = argparse.ArgumentParser(description="AOS Doctor")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    results = []
    for cmd in COMMANDS_TO_AGGREGATE:
        res = run_command(cmd)
        results.append(res)
        
    overall_status = determine_overall_status(results)
    
    if args.json:
        output = {
            "command": "aos doctor",
            "overall_status": overall_status,
            "approval_claimed": False,
            "execution_authorized": False,
            "commit_authorized": False,
            "push_authorized": False,
            "release_authorized": False,
            "boundary_note": "Doctor PASS is not approval. Doctor PASS is not execution/commit/push/release authorization.",
            "results": results
        }
        print(json.dumps(output, indent=2))
    else:
        print("=== AOS Doctor ===")
        print("Read-only validation aggregator. Not validator authority.")
        print("Doctor PASS is not approval. Doctor PASS is not execution authorization.\n")
        
        for r in results:
            print(f"Command: {r['command']}")
            print(f"Status:  {r['status']}")
            if r.get("reason"):
                print(f"Reason:  {r['reason']}")
            if r.get("return_code", 0) != 0:
                print(f"Code:    {r['return_code']}")
                if r.get("stderr"):
                    print("Stderr excerpt:")
                    # just print first lines
                    print("\n".join(r['stderr'].split('\n')[:3]))
            print("-" * 40)
            
        print(f"Overall Status: {overall_status}")
        print("\nNote: BLOCKED beats HUMAN_REVIEW_REQUIRED. UNKNOWN_BLOCKED beats PASS.")
        print("NOT_RUN is reported, never converted to PASS.")

if __name__ == "__main__":
    main()
