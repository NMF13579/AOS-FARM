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
import aos_architecture_document_check

VALIDATION_COMMANDS = [
    ["python3", "aos/scripts/aos_install.py", "--dry-run"],
    ["python3", "aos/scripts/aos_consumer_self_test.py"],
    ["python3", "aos/scripts/aos_task_document_check.py", "task", "--validate-all"],
    ["python3", "aos/scripts/aos_task_document_check.py", "queue", "--list"],
    ["python3", "aos/scripts/aos_task_document_check.py", "queue", "--next"],
    ["python3", "aos/scripts/aos_task_document_check.py", "task", "--readiness-all"],
    # Do not include aos_doctor.py here because doctor runs broad unittest discover and can recursively re-enter tests/test_aos_validate.py through aos_validate.py.
    ["python3", "aos/scripts/aos_queue_dashboard.py"],
    ["python3", "aos/scripts/aos_next_task_selection.py", "--json"]
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
    has_blocked = False
    has_unknown = False
    
    for r in results:
        status = r.get("status")
        stdout = r.get("stdout", "")
        stderr = r.get("stderr", "")
        
        if status == "UNKNOWN_BLOCKED" or "UNKNOWN_BLOCKED" in stdout or "UNKNOWN_BLOCKED" in stderr:
            has_unknown = True
        elif status in ["BLOCKED", "CONFLICT_BLOCKED", "HUMAN_REVIEW_REQUIRED"] or "BLOCKED" in stdout or "BLOCKED" in stderr:
            has_blocked = True
        elif status == "FAILED":
            has_failed = True
        elif status == "NOT_RUN":
            has_not_run = True
            
    if has_unknown:
        return "UNKNOWN_BLOCKED"
    if has_blocked:
        return "BLOCKED"
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
        
    if args.target == "all" or args.target == "architecture":
        try:
            arch_report = aos_architecture_document_check.get_validate_all_report()
            results.append({
                "command": "aos_architecture_document_check.get_validate_all_report",
                "status": arch_report.get("status", "UNKNOWN_BLOCKED"),
                "source": "aos_architecture_document_check.get_validate_all_report",
                "approval_claimed": False,
                "execution_authorized": False,
                "implementation_authorized": False,
                "release_authorized": False,
                "report": arch_report
            })
        except Exception as e:
            results.append({
                "command": "aos_architecture_document_check.get_validate_all_report",
                "status": "UNKNOWN_BLOCKED",
                "reason": f"architecture_validation_unavailable: {e}",
                "counted_as_pass": False,
                "approval_claimed": False,
                "execution_authorized": False,
                "implementation_authorized": False,
                "release_authorized": False
            })
            
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
