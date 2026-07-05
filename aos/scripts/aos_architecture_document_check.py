import argparse
import json
import os
import sys
import re

def emit_report(status, target_type, file_path, errors=None, warnings=None,
                blocked_reasons=None, authority_findings=None,
                traceability_findings=None, unknown_findings=None,
                conflict_findings=None, human_review_findings=None):
    report = {
        "status": status,
        "target_type": target_type,
        "file": file_path,
        "errors": errors or [],
        "warnings": warnings or [],
        "blocked_reasons": blocked_reasons or [],
        "authority_findings": authority_findings or [],
        "traceability_findings": traceability_findings or [],
        "unknown_findings": unknown_findings or [],
        "conflict_findings": conflict_findings or [],
        "human_review_findings": human_review_findings or []
    }
    print(json.dumps(report, indent=2))

def exit_for_status(status):
    if status == "PASS":
        sys.exit(0)
    elif status == "CLI_USAGE_ERROR":
        sys.exit(2)
    else:
        sys.exit(1)

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        emit_report("CLI_USAGE_ERROR", "unknown", None, errors=[message])
        sys.exit(2)

def build_parser():
    parser = CustomArgumentParser(description="AOS Architecture Document Check CLI Skeleton")
    subparsers = parser.add_subparsers(dest="command", required=True)

    brief_parser = subparsers.add_parser("brief", help="Check an architecture brief")
    brief_parser.add_argument("--file", required=True, help="Path to brief file")

    adr_parser = subparsers.add_parser("adr", help="Check an architecture decision record")
    adr_parser.add_argument("--file", required=True, help="Path to ADR file")

    matrix_parser = subparsers.add_parser("matrix", help="Check an architecture matrix")
    matrix_parser.add_argument("--file", required=True, help="Path to matrix file")

    task_parser = subparsers.add_parser("task-breakdown", help="Check a task breakdown")
    task_parser.add_argument("--file", required=True, help="Path to task breakdown file")

    registry_parser = subparsers.add_parser("registry", help="Check the architecture registry")
    registry_group = registry_parser.add_mutually_exclusive_group(required=True)
    registry_group.add_argument("--validate", action="store_true", help="Validate the full registry")
    registry_group.add_argument("--file", help="Path to registry file")

    return parser

def read_text(path):
    if not os.path.exists(path):
        return None, "File missing"
    if not os.path.isfile(path):
        return None, "Path is not a file"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read(), None
    except Exception as e:
        return None, f"Unreadable file: {e}"

def contains_required_fields(text, fields):
    missing = []
    for field in fields:
        if f"{field}:" not in text and f"{field} =" not in text and f"{field}" not in text:
            missing.append(field)
    return missing

def is_negative_invariant_line(line):
    markers = [
        "≠",
        "does not",
        "must not",
        "cannot",
        "не является",
        "не даёт",
        "не дает",
        "не авторизует",
        "не разрешает"
    ]
    line_lower = line.lower()
    for marker in markers:
        if marker in line_lower:
            return True
    if re.search(r'\bnot\b', line_lower):
        return True
    return False

def find_positive_authority(text):
    findings = []
    lines = text.splitlines()
    authorities = [
        "approval_authority: true",
        "execution_authority: true",
        "commit_authority: true",
        "push_authority: true",
        "release_authority: true",
        "execution_authorized: true",
        "commit_authorized: true",
        "push_authorized: true",
        "release_authorized: true"
    ]
    for i, line in enumerate(lines):
        for auth in authorities:
            if auth in line:
                if not is_negative_invariant_line(line):
                    findings.append(f"Line {i+1}: {line.strip()}")
    return findings

def find_unsafe_status_language(text):
    findings = []
    lines = text.splitlines()
    unsafe_tokens = [
        "APPROVED",
        "READY_FOR_EXECUTION",
        "RELEASE_READY"
    ]
    import re
    for i, line in enumerate(lines):
        for token in unsafe_tokens:
            if re.search(rf'(?<![a-zA-Z0-9_]){token}(?![a-zA-Z0-9_])', line):
                if not is_negative_invariant_line(line):
                    findings.append(f"Line {i+1}: contains unsafe status '{token}' - {line.strip()}")
    return findings

def extract_field_value(text, field):
    match = re.search(rf'^{field}[:=]\s*(.+)$', text, re.MULTILINE | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def validate_brief(text):
    errors = []
    blocked_reasons = []
    status_code = "PASS"
    
    required = [
        "architecture_brief_id",
        "version",
        "status",
        "technical_assignment_ref",
        "pattern_refs",
        "stack_preset_refs",
        "unknown_records",
        "conflict_records",
        "human_checkpoints"
    ]
    missing = contains_required_fields(text, required)
    if missing:
        errors.append(f"Missing required fields: {missing}")
        if "unknown_records" in missing:
            status_code = "UNKNOWN_BLOCKED"
        elif "conflict_records" in missing and status_code == "PASS":
            status_code = "CONFLICT_BLOCKED"
        else:
            status_code = "BLOCKED"
            
    status_val = extract_field_value(text, "status")
    if status_val:
        allowed_statuses = ["DRAFT", "HUMAN_REVIEW_REQUIRED", "READY_FOR_TASK_BREAKDOWN", 
                            "UNKNOWN_BLOCKED", "CONFLICT_BLOCKED", "REJECTED", "SUPERSEDED"]
        if status_val not in allowed_statuses:
            errors.append(f"Unknown status value: {status_val}")
            status_code = "BLOCKED"

    if "READY_FOR_TASK_BREAKDOWN = approval" in text or "READY_FOR_TASK_BREAKDOWN: approval" in text or "READY_FOR_TASK_BREAKDOWN == approval" in text:
        blocked_reasons.append("READY_FOR_TASK_BREAKDOWN treated as approval")
        status_code = "BLOCKED"
    if "READY_FOR_TASK_BREAKDOWN = READY_FOR_EXECUTION" in text or "READY_FOR_TASK_BREAKDOWN: READY_FOR_EXECUTION" in text:
        blocked_reasons.append("READY_FOR_TASK_BREAKDOWN treated as READY_FOR_EXECUTION")
        status_code = "BLOCKED"

    return status_code, errors, blocked_reasons

def validate_adr(text):
    errors = []
    blocked_reasons = []
    status_code = "PASS"
    
    required = [
        "adr_id",
        "title",
        "status",
        "decided_by",
        "technical_assignment_ref",
        "architecture_brief_ref",
        "related_patterns",
        "related_unknowns",
        "related_conflicts"
    ]
    missing = contains_required_fields(text, required)
    if missing:
        errors.append(f"Missing required fields: {missing}")
        if "related_unknowns" in missing:
            status_code = "UNKNOWN_BLOCKED"
        elif "related_conflicts" in missing and status_code == "PASS":
            status_code = "CONFLICT_BLOCKED"
        else:
            status_code = "BLOCKED"
            
    status_val = extract_field_value(text, "status")
    if status_val:
        allowed = ["PROPOSED", "HUMAN_REVIEW_REQUIRED", "ACCEPTED_BY_HUMAN", 
                   "REJECTED", "SUPERSEDED", "UNKNOWN_BLOCKED", "CONFLICT_BLOCKED"]
        if status_val not in allowed:
            errors.append(f"Unknown status value: {status_val}")
            status_code = "BLOCKED"
            
    return status_code, errors, blocked_reasons

def validate_matrix(text):
    errors = []
    blocked_reasons = []
    status_code = "PASS"
    
    required = [
        "constraint",
        "candidate_pattern",
        "fit",
        "decision",
        "reason",
        "risk",
        "unknowns",
        "conflicts",
        "human_review"
    ]
    missing = contains_required_fields(text, required)
    if missing:
        errors.append(f"Missing required fields: {missing}")
        if "unknowns" in missing:
            status_code = "UNKNOWN_BLOCKED"
        elif "conflicts" in missing and status_code == "PASS":
            status_code = "CONFLICT_BLOCKED"
        else:
            status_code = "BLOCKED"
            
    decision_val = extract_field_value(text, "decision")
    if decision_val:
        allowed = ["SELECTED", "REJECTED", "NEEDS_HUMAN", "UNKNOWN_BLOCKED", "CONFLICT_BLOCKED"]
        if decision_val not in allowed:
            errors.append(f"Unknown decision value: {decision_val}")
            status_code = "BLOCKED"
            
    return status_code, errors, blocked_reasons

def validate_registry(text):
    errors = []
    blocked_reasons = []
    status_code = "PASS"
    
    for line in text.splitlines():
        if "EXECUTION_AUTHORIZED" in line and not is_negative_invariant_line(line):
            errors.append("EXECUTION_AUTHORIZED found")
            status_code = "BLOCKED"
            
    has_active = False
    for line in text.splitlines():
        if re.search(r'\bACTIVE\b', line) and not is_negative_invariant_line(line):
            has_active = True
            break
            
    if has_active:
        checkpoint_fields = ["human_checkpoint", "approved_by", "approved_at"]
        missing_markers = contains_required_fields(text, checkpoint_fields)
        if missing_markers:
            errors.append(f"ACTIVE entry missing checkpoint markers: {missing_markers}")
            status_code = "BLOCKED"
        elif status_code == "PASS":
            status_code = "HUMAN_REVIEW_REQUIRED"
            
    return status_code, errors, blocked_reasons

def validate_task_breakdown(text):
    errors = []
    blocked_reasons = []
    status_code = "PASS"
    
    required = [
        "origin_technical_assignment",
        "origin_architecture_brief",
        "origin_adr",
        "origin_pattern",
        "origin_stack_preset",
        "origin_unknown_resolution",
        "origin_conflict_resolution"
    ]
    missing = contains_required_fields(text, required)
    if missing:
        errors.append(f"Missing required origins: {missing}")
        if "origin_unknown_resolution" in missing:
            status_code = "UNKNOWN_BLOCKED"
        elif "origin_conflict_resolution" in missing and status_code == "PASS":
            status_code = "CONFLICT_BLOCKED"
        else:
            status_code = "BLOCKED"
            
    return status_code, errors, blocked_reasons

def process_file_validation(file_path, command):
    text, err = read_text(file_path)
    if err:
        return "BLOCKED", [f"File missing or unreadable: {file_path}"], [], []
        
    authority_findings = find_positive_authority(text)
    unsafe_status_findings = find_unsafe_status_language(text)
    all_auth_findings = authority_findings + unsafe_status_findings
    
    if all_auth_findings:
        return "BLOCKED", [], ["Safety scanner blocked positive authority or unsafe status."], all_auth_findings
        
    status = "PASS"
    errors = []
    blocked_reasons = []
    
    if command == "brief":
        status, errors, blocked_reasons = validate_brief(text)
    elif command == "adr":
        status, errors, blocked_reasons = validate_adr(text)
    elif command == "matrix":
        status, errors, blocked_reasons = validate_matrix(text)
    elif command == "registry":
        status, errors, blocked_reasons = validate_registry(text)
    elif command == "task-breakdown":
        status, errors, blocked_reasons = validate_task_breakdown(text)

    return status, errors, blocked_reasons, []

def main():
    parser = build_parser()
    args = parser.parse_args()

    command = args.command
    
    if command == "registry" and getattr(args, 'validate', False):
        registry_files = [
            "aos/docs/architecture/pattern-registry.md",
            "aos/docs/architecture/stack-preset-registry.md"
        ]
        overall_status = "PASS"
        all_errors = []
        all_blocked = []
        all_auth = []
        
        for reg_file in registry_files:
            status, errors, blocked_reasons, auth_findings = process_file_validation(reg_file, "registry")
            if status == "BLOCKED":
                overall_status = "BLOCKED"
            elif status == "HUMAN_REVIEW_REQUIRED" and overall_status == "PASS":
                overall_status = "HUMAN_REVIEW_REQUIRED"
            elif status == "UNKNOWN_BLOCKED" and overall_status in ["PASS", "HUMAN_REVIEW_REQUIRED"]:
                overall_status = "UNKNOWN_BLOCKED"
            elif status == "CONFLICT_BLOCKED" and overall_status in ["PASS", "HUMAN_REVIEW_REQUIRED", "UNKNOWN_BLOCKED"]:
                overall_status = "CONFLICT_BLOCKED"
                
            all_errors.extend(errors)
            all_blocked.extend(blocked_reasons)
            all_auth.extend(auth_findings)
            
        emit_report(
            status=overall_status,
            target_type=command,
            file_path="full_registry",
            errors=all_errors,
            blocked_reasons=all_blocked,
            authority_findings=all_auth
        )
        exit_for_status(overall_status)
        
    file_path = getattr(args, 'file', None)
    if file_path:
        status, errors, blocked_reasons, auth_findings = process_file_validation(file_path, command)
        emit_report(
            status=status,
            target_type=command,
            file_path=file_path,
            errors=errors,
            blocked_reasons=blocked_reasons,
            authority_findings=auth_findings
        )
        exit_for_status(status)

if __name__ == "__main__":
    main()
