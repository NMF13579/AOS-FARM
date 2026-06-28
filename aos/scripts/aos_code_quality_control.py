#!/usr/bin/env python3
import json
import sys
import argparse
import re
from pathlib import Path

def parse_pseudo_yaml(content):
    # A simple parser that extracts key-value pairs and lists.
    data = {}
    lines = content.split('\n')
    current_key = None
    for line in lines:
        if line.strip().startswith('#') or not line.strip():
            continue
        if ':' in line and not line.startswith(' '):
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            if val == '':
                data[key] = []
                current_key = key
            else:
                data[key] = val
                current_key = None
        elif line.strip().startswith('-') and current_key:
            val = line.strip()[1:].strip()
            data[current_key].append(val)
    return data

def validate_package(file_path: Path) -> dict:
    if not file_path.exists():
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "File not found"}

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"status": "CODE_QUALITY_BLOCKED", "reason": f"Could not read file: {e}"}

    # 1. Never emit forbidden approvals anywhere. We prevent them from even being in output.
    forbidden_emits = ["APPROVED", "READY_FOR_RELEASE", "READY_FOR_MERGE", "PASS-as-approval"]
    for term in forbidden_emits:
        if term in content:
            return {"status": "CODE_QUALITY_BLOCKED", "reason": f"Forbidden term found in content: {term}"}

    data = parse_pseudo_yaml(content)

    # Required fields presence
    if 'risk_profile' not in data:
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "Missing risk_profile"}
    if 'risk_profile_assigned_by' not in data or data['risk_profile_assigned_by'] != 'human':
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "Risk profile not assigned by human"}

    if data.get('execution_authorized') != 'true':
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "execution_authorized is false or missing"}
    if data.get('candidate_only') == 'true':
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "candidate_only is true"}

    if 'allowed_files' not in data or not data['allowed_files']:
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "allowed_files empty or missing"}
    if 'forbidden_files' not in data:
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "forbidden_files missing"}

    if 'required_tests' not in data or not data['required_tests']:
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "required_tests missing"}
    if 'required_checks' not in data or not data['required_checks']:
        return {"status": "CODE_QUALITY_BLOCKED", "reason": "required_checks missing"}

    # Check for UNKNOWN / NOT_RUN
    for val in data.values():
        val_str = str(val).upper()
        if 'UNKNOWN' in val_str:
            return {"status": "CODE_QUALITY_BLOCKED", "reason": "UNKNOWN in required fields"}
        if 'NOT_RUN' in val_str:
            return {"status": "CODE_QUALITY_BLOCKED", "reason": "NOT_RUN in required checks"}

    # Check authorizations
    auth_fields = [
        'commit_authorized', 'push_authorized', 'merge_authorized',
        'release_authorized', 'approval_record_creation_allowed',
        'lifecycle_mutation_authorized'
    ]
    for field in auth_fields:
        if data.get(field) == 'true':
            return {"status": "CODE_QUALITY_BLOCKED", "reason": f"{field} is true"}

    # Check file modifications against allowed/forbidden
    planned_changes = data.get('planned_changes', [])
    allowed = data.get('allowed_files', [])
    forbidden = data.get('forbidden_files', [])
    protected_patterns = ['00_', '01_', '02_', 'README', 'AGENTS', 'START_HERE']

    for changed_file in planned_changes:
        # Protected check
        for pat in protected_patterns:
            if pat in changed_file:
                return {"status": "CODE_QUALITY_BLOCKED", "reason": f"Protected/canonical planned change: {changed_file}"}

        if changed_file in forbidden:
            return {"status": "CODE_QUALITY_BLOCKED", "reason": f"Planned change inside forbidden_files: {changed_file}"}

        # Must be in allowed
        is_allowed = False
        for a in allowed:
            if a == '*' or a == changed_file or changed_file.startswith(a.replace('*', '')):
                is_allowed = True
                break
        if not is_allowed:
            return {"status": "CODE_QUALITY_BLOCKED", "reason": f"Planned change outside allowed_files: {changed_file}"}

    # Unsafe commands
    commands = data.get('commands', [])
    unsafe = ['git push', 'git commit', 'rm -rf']
    for cmd in commands:
        for u in unsafe:
            if u in cmd:
                return {"status": "CODE_QUALITY_BLOCKED", "reason": f"Unsafe command pattern: {u}"}

    # Overengineering risk
    overengineering = ['new dependency', 'runtime expansion', 'future only code']
    notes = data.get('notes', '')
    for risk in overengineering:
        if risk in notes.lower():
            return {"status": "CODE_QUALITY_BLOCKED", "reason": f"Overengineering risk: {risk}"}

    return {
        "status": "CODE_QUALITY_REPORTED_HUMAN_REVIEW_REQUIRED",
        "reason": "Package meets quality control standards. No approval granted."
    }

def summarize(file_path: Path) -> dict:
    res = validate_package(file_path)
    is_blocked = (res['status'] == 'CODE_QUALITY_BLOCKED')

    summary = f"Summary: blocked" if is_blocked else "Summary: human review required"
    blocked_reasons = [res['reason']] if is_blocked else []

    return {
        "status": res['status'],
        "summary": summary,
        "package": str(file_path),
        "human_review_required": True,
        "approval_granted": False,
        "commit_authorized": False,
        "push_authorized": False,
        "release_authorized": False,
        "blocked_reasons_count": len(blocked_reasons),
        "blocked_reasons": blocked_reasons,
        "unknown_count": 0,
        "not_run_count": 0
    }

def main():
    parser = argparse.ArgumentParser(description="Code Quality Control Validator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    val_parser = subparsers.add_parser("validate-package")
    val_parser.add_argument("--package", required=True)

    sum_parser = subparsers.add_parser("summarize")
    sum_parser.add_argument("--package", required=True)

    args = parser.parse_args()

    if args.command == "validate-package":
        print(json.dumps(validate_package(Path(args.package)), indent=2))
    elif args.command == "summarize":
        print(json.dumps(summarize(Path(args.package)), indent=2))

if __name__ == "__main__":
    main()
