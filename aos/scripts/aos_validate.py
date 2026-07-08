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
import re
import aos_architecture_document_check
import aos_task_document_check

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

PASS = "PASS"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"
BLOCKED = "BLOCKED"
NOT_RUN = "NOT_RUN"
FAIL = "FAIL"

STATUS_ALIASES = {
    PASS: PASS,
    "PASS_WITH_WARNINGS": HUMAN_REVIEW_REQUIRED,
    HUMAN_REVIEW_REQUIRED: HUMAN_REVIEW_REQUIRED,
    UNKNOWN_BLOCKED: UNKNOWN_BLOCKED,
    "UNKNOWN": UNKNOWN_BLOCKED,
    BLOCKED: BLOCKED,
    "CONFLICT_BLOCKED": BLOCKED,
    NOT_RUN: NOT_RUN,
    FAIL: FAIL,
    "FAILED": FAIL,
    "FAILED_OR_BLOCKED": FAIL,
    "ERROR": FAIL,
    "INVALID": FAIL,
    "MALFORMED_EXCLUSION": UNKNOWN_BLOCKED,
}

STATUS_FIELD_PATTERNS = [
    re.compile(r"^\s*(?:\*\*)?Final Status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?Overall Status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?final_status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?overall_status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?install_status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?Readiness(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
]
STATUS_FIELD_NAMES = [
    "Final Status",
    "Overall Status",
    "final_status",
    "overall_status",
    "install_status",
    "Readiness",
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

def normalize_status(raw_status):
    if raw_status is None:
        return UNKNOWN_BLOCKED
    status = str(raw_status).strip().replace("*", "").replace("`", "")
    if not status:
        return UNKNOWN_BLOCKED
    return STATUS_ALIASES.get(status, UNKNOWN_BLOCKED)

def aggregate_statuses(statuses):
    normalized = [normalize_status(status) for status in statuses]
    if not normalized:
        return UNKNOWN_BLOCKED
    if UNKNOWN_BLOCKED in normalized:
        return UNKNOWN_BLOCKED
    if HUMAN_REVIEW_REQUIRED in normalized:
        return HUMAN_REVIEW_REQUIRED
    if BLOCKED in normalized:
        return BLOCKED
    if FAIL in normalized:
        return FAIL
    if NOT_RUN in normalized:
        return NOT_RUN
    if all(status == PASS for status in normalized):
        return PASS
    return UNKNOWN_BLOCKED

def collect_json_statuses(payload):
    statuses = []
    if not isinstance(payload, dict):
        return statuses
    specific_status_keys = ["overall_status", "final_status", "install_status", "dry_run_install_status"]
    has_specific_status = any(key in payload for key in specific_status_keys)
    for key in specific_status_keys:
        if key in payload:
            statuses.append(payload.get(key))
    if "status" in payload and not has_specific_status:
        statuses.append(payload.get("status"))
    for key in [
        "package_integrity",
        "target_install_state",
        "installer_dry_run",
        "readiness_audit",
    ]:
        value = payload.get(key)
        if isinstance(value, dict):
            statuses.extend(collect_json_statuses(value))
    return statuses

def extract_json_report(text):
    marker = "--- JSON REPORT ---"
    end_marker = "-------------------"
    if marker not in text:
        return None
    after_marker = text.split(marker, 1)[1]
    json_text = after_marker.split(end_marker, 1)[0].strip()
    if not json_text:
        return None
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return {"status": UNKNOWN_BLOCKED}

def collect_text_statuses(text):
    statuses = []
    if not text:
        return statuses
    json_report = extract_json_report(text)
    if json_report is not None:
        statuses.extend(collect_json_statuses(json_report))
        return statuses
    for line in text.splitlines():
        clean_line = line.replace("*", "").replace("`", "").strip()
        for field_name in STATUS_FIELD_NAMES:
            prefix = f"{field_name}:"
            if clean_line.startswith(prefix):
                status = clean_line[len(prefix):].strip().split()[0] if clean_line[len(prefix):].strip() else ""
                statuses.append(status)
    for pattern in STATUS_FIELD_PATTERNS:
        statuses.extend(pattern.findall(text))
    return statuses

def normalize_child_result(result):
    statuses = [result.get("status")]
    statuses.extend(collect_text_statuses(result.get("stdout", "")))
    statuses.extend(collect_text_statuses(result.get("stderr", "")))
    normalized = aggregate_statuses(statuses)
    return_code = result.get("return_code")
    if return_code not in (None, 0) and normalized == PASS:
        return FAIL
    return normalized

def determine_overall_status(results):
    return aggregate_statuses([normalize_child_result(result) for result in results])


def build_readiness_audit():
    try:
        return aos_task_document_check.build_readiness_report("tasks")
    except Exception as exc:
        return {
            "status": "UNKNOWN_BLOCKED",
            "error": f"readiness_audit_unavailable: {exc}",
            "counts": {
                "active_ready_count": 0,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
            "active_blockers": [],
            "excluded_terminal_tasks": [],
            "excluded_legacy_tasks": [],
            "malformed_exclusions": [],
            "tasks": [],
            "explicit_not_pass_statement": [
                "EXCLUDED_TERMINAL is not PASS",
                "EXCLUDED_LEGACY is not PASS",
                "MALFORMED_EXCLUSION is blocker state",
            ],
        }

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
            
    readiness_audit = build_readiness_audit()
    overall_status = determine_overall_status(results)
    if readiness_audit.get("status") == "UNKNOWN_BLOCKED":
        overall_status = "UNKNOWN_BLOCKED"
    elif readiness_audit.get("status") == "BLOCKED" and overall_status == "PASS":
        overall_status = "BLOCKED"

    output = {
        "command": "aos validate",
        "target": args.target,
        "overall_status": overall_status,
        "readiness_audit": readiness_audit,
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
