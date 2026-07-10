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
    [sys.executable, "aos/scripts/aos_install.py", "--dry-run"],
    [sys.executable, "aos/scripts/aos_consumer_self_test.py"],
    [sys.executable, "-m", "py_compile", "aos/scripts/aos_install.py"],
    [sys.executable, "-m", "py_compile", "aos/scripts/aos_consumer_self_test.py"],
    [sys.executable, "-m", "py_compile", "aos/scripts/aos_task_document_check.py"],
    [sys.executable, "aos/scripts/aos_duplicate_workspace_check.py", "--json"],
    [sys.executable, "-m", "py_compile", "aos/scripts/aos_doctor.py"],
    [sys.executable, "aos/scripts/aos_task_document_check.py", "task", "--validate-all"],
    [sys.executable, "aos/scripts/aos_task_document_check.py", "queue", "--list"],
    [sys.executable, "aos/scripts/aos_task_document_check.py", "queue", "--next"],
    [sys.executable, "aos/scripts/aos_task_document_check.py", "task", "--readiness-all"],
    [sys.executable, "-c", "import pytest"],
    [sys.executable, "-m", "pytest"]
]

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
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
        cmd_str = r.get("command", "")
        
        if ("unittest" in cmd_str or "pytest" in cmd_str) and status == "PASS":
            if "Ran 0 tests" in stdout or "Ran 0 tests" in stderr or "collected 0 items" in stdout or "collected 0 items" in stderr:
                r["status"] = "FAILED"
                r["reason"] = "0 tests executed is not a strong PASS"
                has_failed = True
                status = "FAILED"
                
        if "aos_duplicate_workspace_check.py" in cmd_str:
            try:
                import json
                data = json.loads(stdout)
                dup_status = data.get("final_status", "UNKNOWN_BLOCKED")
                r["status"] = dup_status
                status = dup_status
                r["checker"] = data.get("checker", "duplicate_workspace")
            except Exception:
                r["status"] = "UNKNOWN_BLOCKED"
                status = "UNKNOWN_BLOCKED"
                r["reason"] = "Execution or JSON parse failure"
                
        if status == "UNKNOWN_BLOCKED":
            return "UNKNOWN_BLOCKED"
        if status == "BLOCKED":
            return "BLOCKED"
        if status in ("FAILED_OR_BLOCKED", "HUMAN_REVIEW_REQUIRED"):
            has_failed = True
            
        if status == "FAILED":
            if "UNKNOWN_BLOCKED" in stdout or "UNKNOWN_BLOCKED" in stderr:
                return "UNKNOWN_BLOCKED"
            if "BLOCKED" in stdout or "BLOCKED" in stderr:
                return "BLOCKED"
            has_failed = True
        elif status == "NOT_RUN":
            has_not_run = True
            
        if "HUMAN_REVIEW_REQUIRED" in stdout or "HUMAN_REVIEW_REQUIRED" in stderr:
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
    pytest_available = True
    for cmd in COMMANDS_TO_AGGREGATE:
        if "-m" in cmd and "pytest" in cmd:
            if not pytest_available:
                results.append({
                    "command": " ".join(cmd),
                    "status": "NOT_RUN",
                    "reason": "Skipped due to missing pytest dependency"
                })
                continue
                
        res = run_command(cmd)
        
        if len(cmd) == 3 and cmd[1] == "-c" and cmd[2] == "import pytest":
            if res.get("status") == "FAILED":
                pytest_available = False
                res["reason"] = f"Missing required development dependency: pytest. Interpreter: {sys.executable}. Authoritative dependency declaration: requirements-dev.txt. Run: {sys.executable} -m pip install -r requirements-dev.txt"
                
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
