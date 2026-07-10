#!/usr/bin/env python3
"""
Unified AOS Validate
Validation orchestration only.
It must not: create tasks, mutate queue, write Evidence, claim approval, commit, push, release, change lifecycle state, assign Risk Profile.
"""

import subprocess
import json
import sys
import os
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
    ["python3", "aos/scripts/aos_next_task_selection.py", "--json"],
    [sys.executable, "aos/scripts/aos_duplicate_workspace_check.py", "--json"]
]

PASS = "PASS"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"
BLOCKED = "BLOCKED"
NOT_RUN = "NOT_RUN"
FAIL = "FAIL"
BLOCKED_REQUIRED_SOURCES_MISSING = "BLOCKED_REQUIRED_SOURCES_MISSING"

REQUIRED_ROOT_SOURCES = [
    "00_AOS_Core_Control.md",
    "01_AOS_Assembly_Pipelines_and_Build_Roadmap.md",
    "02_AOS_Governance_Control_Module_and_Safety_Rules.md"
]

def check_required_root_sources():
    missing = [src for src in REQUIRED_ROOT_SOURCES if not os.path.exists(src)]
    if missing:
        return {"status": "FAIL", "missing": missing}
    return {"status": "PASS", "missing": []}

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

def process_exit_status(return_code=None, process_error=None):
    if process_error == "timeout":
        return "TIMEOUT"
    if process_error == "not_run":
        return "NOT_RUN"
    if process_error:
        return "PROCESS_ERROR"
    if return_code is None:
        return "NOT_RUN"
    if return_code == 0:
        return "EXIT_ZERO"
    return "EXIT_NON_ZERO"

BASE_STATUS_FIELD_PATTERNS = [
    re.compile(r"^\s*(?:\*\*)?Final Status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?Overall Status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?final_status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?overall_status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
    re.compile(r"^\s*(?:\*\*)?install_status(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE),
]
BASE_STATUS_FIELD_NAMES = [
    "Final Status",
    "Overall Status",
    "final_status",
    "overall_status",
    "install_status",
]
READINESS_STATUS_PATTERN = re.compile(r"^\s*(?:\*\*)?Readiness(?:\*\*)?\s*:\s*(?:\*\*)?`?([A-Z_]+)", re.MULTILINE)
READINESS_STATUS_FIELD_NAME = "Readiness"
NONE = "NONE"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return {
            "command": " ".join(cmd),
            "raw_status": "PASS" if result.returncode == 0 else "FAILED",
            "status": "PASS" if result.returncode == 0 else "FAILED",
            "raw_exit_code": result.returncode,
            "exit_code": result.returncode,
            "process_exit_status": process_exit_status(result.returncode),
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except FileNotFoundError:
        return {
            "command": " ".join(cmd),
            "raw_status": "NOT_RUN",
            "status": "NOT_RUN",
            "raw_exit_code": None,
            "exit_code": None,
            "process_exit_status": process_exit_status(process_error="not_run"),
            "reason": "Command or script not found"
        }
    except subprocess.TimeoutExpired:
        return {
            "command": " ".join(cmd),
            "raw_status": "NOT_RUN",
            "status": "NOT_RUN",
            "raw_exit_code": None,
            "exit_code": None,
            "process_exit_status": process_exit_status(process_error="timeout"),
            "reason": "Timeout expired"
        }
    except Exception as e:
        return {
            "command": " ".join(cmd),
            "raw_status": "NOT_RUN",
            "status": "NOT_RUN",
            "raw_exit_code": None,
            "exit_code": None,
            "process_exit_status": process_exit_status(process_error="error"),
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

def extract_json_stdout(text):
    if not text:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"status": UNKNOWN_BLOCKED, "schema_error": "malformed_json_stdout"}
    if not isinstance(payload, dict):
        return {"status": UNKNOWN_BLOCKED, "schema_error": "json_stdout_not_object"}
    return payload

def is_next_task_selection_command(command):
    return "aos_next_task_selection.py" in command and "--json" in command

def is_installer_dry_run_command(command):
    return "aos_install.py" in command and "--dry-run" in command

def is_consumer_self_test_command(command):
    return "aos_consumer_self_test.py" in command

def _section_items(text, heading):
    lines = text.splitlines()
    heading_line = f"### {heading}"
    for idx, line in enumerate(lines):
        if line.strip() != heading_line:
            continue
        items = []
        for item_line in lines[idx + 1:]:
            stripped = item_line.strip()
            if stripped.startswith("### ") or stripped == "---":
                break
            if stripped.startswith("- "):
                items.append(stripped[2:].strip())
        return items
    return []

def installer_blocked_reasons(stdout):
    return [item for item in _section_items(stdout, "blocked_reasons") if item != "[none]"]

def installer_existing_targets(stdout):
    return [item for item in _section_items(stdout, "existing_targets") if item != "[none]"]

def installer_conflicts(stdout):
    return [item for item in _section_items(stdout, "conflicts") if item != "[none]"]

def has_process_failure(result):
    if result.get("process_exit_status") in {"PROCESS_ERROR", "TIMEOUT", "NOT_RUN"}:
        return True
    return result.get("return_code") not in (None, 0)

def selector_payload(result):
    if not is_next_task_selection_command(result.get("command", "")):
        return None
    return extract_json_stdout(result.get("stdout", ""))

def valid_selector_advisory(result):
    payload = selector_payload(result)
    if not isinstance(payload, dict):
        return False
    if payload.get("schema_error"):
        return False
    return (
        not has_process_failure(result)
        and payload.get("final_status") == HUMAN_REVIEW_REQUIRED
        and bool(payload.get("next_candidate"))
        and not payload.get("runtime_error")
        and not payload.get("schema_error")
    )

def valid_installer_dry_run_advisory(result):
    command = result.get("command", "")
    stdout = result.get("stdout", "")
    statuses = collect_text_statuses(stdout, command=command)
    return (
        is_installer_dry_run_command(command)
        and not has_process_failure(result)
        and HUMAN_REVIEW_REQUIRED in [normalize_status(status) for status in statuses]
        and not installer_blocked_reasons(stdout)
        and bool(installer_existing_targets(stdout) or installer_conflicts(stdout))
    )

def consumer_self_test_report(result):
    if not is_consumer_self_test_command(result.get("command", "")):
        return None
    return extract_json_report(result.get("stdout", ""))

def valid_consumer_self_test_advisory(result):
    report = consumer_self_test_report(result)
    if not isinstance(report, dict):
        return False
    installer_dry_run = report.get("installer_dry_run", {})
    return (
        not has_process_failure(result)
        and report.get("final_status") == PASS
        and report.get("package_integrity", {}).get("status") == PASS
        and report.get("target_install_state", {}).get("status") == PASS
        and installer_dry_run.get("status") == "COMPLETED"
        and installer_dry_run.get("dry_run_install_status") == HUMAN_REVIEW_REQUIRED
        and not report.get("runtime_error")
        and not report.get("schema_error")
    )

def build_advisory(result):
    command = result.get("command", "")
    if valid_selector_advisory(result):
        payload = selector_payload(result)
        return {
            "source": "aos_next_task_selection.py",
            "status": HUMAN_REVIEW_REQUIRED,
            "advisory": True,
            "blocking_technical_health": False,
            "next_candidate": payload.get("next_candidate"),
            "selector_status": payload.get("final_status"),
            "selection_status": payload.get("selection_status"),
            "approval_granted": False,
            "execution_authorized": False,
            "reason": "next candidate requires human review",
        }
    if valid_installer_dry_run_advisory(result):
        return {
            "source": "aos_install.py --dry-run",
            "status": HUMAN_REVIEW_REQUIRED,
            "advisory": True,
            "blocking_technical_health": False,
            "dry_run": True,
            "approval_granted": False,
            "execution_authorized": False,
            "reason": "existing target requires human review",
        }
    if valid_consumer_self_test_advisory(result):
        report = consumer_self_test_report(result)
        embedded_status = report.get("installer_dry_run", {}).get("dry_run_install_status")
        return {
            "source": "aos_consumer_self_test.py",
            "status": report.get("final_status"),
            "advisory": True,
            "blocking_technical_health": False,
            "embedded_advisory_status": embedded_status,
            "approval_granted": False,
            "execution_authorized": False,
            "reason": "consumer self-test passed while installer dry-run requires human review",
        }
    return None

def collect_advisories(results):
    advisories = []
    for result in results:
        advisory = build_advisory(result)
        if advisory:
            advisories.append(advisory)
    return advisories

def determine_control_status(advisories):
    for advisory in advisories:
        if advisory.get("status") == HUMAN_REVIEW_REQUIRED or advisory.get("embedded_advisory_status") == HUMAN_REVIEW_REQUIRED:
            return HUMAN_REVIEW_REQUIRED
    return NONE

def command_uses_display_readiness_field(command):
    return "aos_queue_dashboard.py" in command

def collect_text_statuses(text, command=""):
    statuses = []
    if not text:
        return statuses
    json_report = extract_json_report(text)
    if json_report is not None:
        statuses.extend(collect_json_statuses(json_report))
        return statuses
    status_field_names = list(BASE_STATUS_FIELD_NAMES)
    status_field_patterns = list(BASE_STATUS_FIELD_PATTERNS)
    if not command_uses_display_readiness_field(command):
        status_field_names.append(READINESS_STATUS_FIELD_NAME)
        status_field_patterns.append(READINESS_STATUS_PATTERN)
    for line in text.splitlines():
        clean_line = line.replace("*", "").replace("`", "").strip()
        for field_name in status_field_names:
            prefix = f"{field_name}:"
            if clean_line.startswith(prefix):
                status = clean_line[len(prefix):].strip().split()[0] if clean_line[len(prefix):].strip() else ""
                statuses.append(status)
    for pattern in status_field_patterns:
        statuses.extend(pattern.findall(text))
    return statuses

def normalize_child_result(result):
    if result.get("process_exit_status") in {"PROCESS_ERROR", "TIMEOUT"}:
        return FAIL if result.get("process_exit_status") == "PROCESS_ERROR" else NOT_RUN
    command = result.get("command", "")
    if is_next_task_selection_command(command):
        payload = selector_payload(result)
        if not isinstance(payload, dict) or payload.get("schema_error"):
            return UNKNOWN_BLOCKED
        status = normalize_status(payload.get("final_status"))
        if status == HUMAN_REVIEW_REQUIRED:
            return PASS if valid_selector_advisory(result) else UNKNOWN_BLOCKED
        return status
    if valid_installer_dry_run_advisory(result):
        return PASS
    if valid_consumer_self_test_advisory(result):
        return PASS
    statuses = [result.get("status")]
    statuses.extend(collect_text_statuses(result.get("stdout", ""), command=command))
    statuses.extend(collect_text_statuses(result.get("stderr", ""), command=command))
    normalized = aggregate_statuses(statuses)
    return_code = result.get("return_code")
    stdout = result.get("stdout", "")
    if return_code not in (None, 0) and "aos_task_document_check.py task --readiness-all" in command:
        malformed_count_present = (
            "malformed_exclusion_count: " in stdout
            and "malformed_exclusion_count: 0" not in stdout
        )
        human_review_count_present = (
            "active_human_review_required_count: " in stdout
            and "active_human_review_required_count: 0" not in stdout
        )
        if "MALFORMED_EXCLUSION" in stdout or malformed_count_present:
            return UNKNOWN_BLOCKED
        if "UNKNOWN_BLOCKED" in stdout:
            return UNKNOWN_BLOCKED
        if "HUMAN_REVIEW_REQUIRED" in stdout or human_review_count_present:
            return HUMAN_REVIEW_REQUIRED
        if "FAIL:" in stdout or "FAIL:" in result.get("stderr", ""):
            return FAIL
        return BLOCKED
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
    technical_status = determine_overall_status(results)
    if readiness_audit.get("status") == "UNKNOWN_BLOCKED":
        technical_status = "UNKNOWN_BLOCKED"
    elif readiness_audit.get("status") == "HUMAN_REVIEW_REQUIRED" and technical_status == "PASS":
        technical_status = "HUMAN_REVIEW_REQUIRED"
    elif readiness_audit.get("status") == "BLOCKED" and technical_status == "PASS":
        technical_status = "BLOCKED"

    required_sources_check = check_required_root_sources()
    if required_sources_check["status"] != "PASS":
        technical_status = BLOCKED_REQUIRED_SOURCES_MISSING

    advisories = collect_advisories(results)
    control_status = determine_control_status(advisories)
    human_review_required = control_status == HUMAN_REVIEW_REQUIRED


    duplicate_workspace_status = "NOT_RUN"
    duplicate_workspace_summary = {}
    for r in results:
        if "aos_duplicate_workspace_check.py" in r.get("command", ""):
            # It outputs JSON, let's parse stdout

            try:
                data = json.loads(r.get("stdout", "{}"))
                duplicate_workspace_status = data.get("final_status", r.get("status", "UNKNOWN_BLOCKED"))
                duplicate_workspace_summary = data.get("summary", {})
                
                if duplicate_workspace_status != "PASS":
                    technical_status = duplicate_workspace_status
            except:
                duplicate_workspace_status = "UNKNOWN_BLOCKED"
                technical_status = "UNKNOWN_BLOCKED"

    output = {
        "duplicate_workspace_status": duplicate_workspace_status,
        "duplicate_workspace_summary": duplicate_workspace_summary,
        "command": "aos validate",
        "target": args.target,
        "overall_status": technical_status,
        "technical_status": technical_status,
        "control_status": control_status,
        "human_review_required": human_review_required,
        "approval_granted": False,
        "execution_authorized": False,
        "advisories": advisories,
        "readiness_audit": readiness_audit,
        "required_sources": required_sources_check,
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
            
        if required_sources_check["status"] != "PASS":
            print("ERROR: Required Root Sources Missing:")
            for m in required_sources_check["missing"]:
                print(f"  - {m}")
            print("-" * 40)

        print(f"Overall Status: {technical_status}")
        print("\nNote: BLOCKED beats HUMAN_REVIEW_REQUIRED. UNKNOWN_BLOCKED beats PASS.")
        print("NOT_RUN is reported, never converted to PASS.")

if __name__ == "__main__":
    main()
