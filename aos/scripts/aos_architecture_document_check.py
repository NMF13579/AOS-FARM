import argparse
import json
import os
import sys
import re

def build_report_dict(status, target_type, file_path, errors=None, warnings=None,
                blocked_reasons=None, authority_findings=None,
                traceability_findings=None, unknown_findings=None,
                conflict_findings=None, human_review_findings=None,
                document_type=None, checks=None):
    summary = {
        "passed": 0,
        "warnings": 0,
        "failed": 0,
        "blocked": 0,
        "not_run": 0
    }
    for c in (checks or []):
        c_status = c.get("status") or c.get("result", "UNKNOWN_BLOCKED")
        if c_status == "PASS": summary["passed"] += 1
        elif c_status == "WARNING": summary["warnings"] += 1
        elif c_status == "FAILED": summary["failed"] += 1
        elif c_status in ["BLOCKED", "UNKNOWN_BLOCKED", "CONFLICT_BLOCKED", "HUMAN_REVIEW_REQUIRED"]: summary["blocked"] += 1
        elif c_status == "NOT_RUN": summary["not_run"] += 1

    return {
        "status": status,
        "target_type": target_type,
        "document_type": document_type or target_type,
        "file": file_path,
        "approval_claimed": False,
        "execution_authorized": False,
        "implementation_authorized": False,
        "release_authorized": False,
        "human_review_required": True,
        "summary": summary,
        "checks": checks or [],
        "errors": errors or [],
        "warnings": warnings or [],
        "blocked_reasons": blocked_reasons or [],
        "authority_findings": authority_findings or [],
        "traceability_findings": traceability_findings or [],
        "unknown_findings": unknown_findings or [],
        "conflict_findings": conflict_findings or [],
        "human_review_findings": human_review_findings or []
    }

def emit_report(status, target_type, file_path, errors=None, warnings=None,
                blocked_reasons=None, authority_findings=None,
                traceability_findings=None, unknown_findings=None,
                conflict_findings=None, human_review_findings=None,
                document_type=None, checks=None):
    report = build_report_dict(
        status=status, target_type=target_type, file_path=file_path,
        errors=errors, warnings=warnings, blocked_reasons=blocked_reasons,
        authority_findings=authority_findings, traceability_findings=traceability_findings,
        unknown_findings=unknown_findings, conflict_findings=conflict_findings,
        human_review_findings=human_review_findings, document_type=document_type,
        checks=checks
    )
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

    evidence_parser = subparsers.add_parser("evidence", help="Check an architecture evidence packet")
    evidence_parser.add_argument("--file", required=True, help="Path to evidence packet file")

    criteria_parser = subparsers.add_parser("criteria", help="Check architecture decision criteria")
    criteria_parser.add_argument("--file", required=True, help="Path to criteria file")

    task_parser = subparsers.add_parser("task-breakdown", help="Check a task breakdown")
    task_parser.add_argument("--file", required=True, help="Path to task breakdown file")

    registry_parser = subparsers.add_parser("registry", help="Check the architecture registry")
    registry_group = registry_parser.add_mutually_exclusive_group(required=True)
    registry_group.add_argument("--validate", action="store_true", help="Validate the full registry")
    registry_group.add_argument("--file", help="Path to registry file")

    validate_all_parser = subparsers.add_parser("validate-all", help="Run all architecture checks")
    validate_all_parser.add_argument("--json", action="store_true", help="Output JSON")

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
        "release_authorized: true",
        "default_stack: true"
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

FORBIDDEN_AUTHORITY_MARKERS = [
    "default_stack: true",
    "status: ACTIVE",
    "approval_status: APPROVED",
    "is_approval: true",
    "is_execution_authorized: true",
    "execution_authorized: true",
    "is_implementation_authorized: true",
    "implementation_authorized: true",
    "is_release_authorized: true",
    "release_authorized: true",
]

FORBIDDEN_WEIGHT_MARKERS = [
    "weight: MUST",
    "weight: SHOULD",
    "weight: NICE_TO_HAVE",
    "matrix_status: COMPLETE",
]

def normalize_value(value):
    if value is None:
        return None
    return value.strip().strip('"').strip("'")

def find_exact_markers(text, markers):
    findings = []
    for i, line in enumerate(text.splitlines()):
        for marker in markers:
            if marker in line:
                findings.append(f"Line {i+1}: {line.strip()}")
    return findings

def require_field_value(text, field, expected, errors):
    actual = normalize_value(extract_field_value(text, field))
    if actual is None:
        errors.append(f"Missing required field: {field}")
    elif actual != expected:
        errors.append(f"{field} must be {expected}, found {actual}")

def require_field_in_values(text, field, allowed, human_review_findings):
    actual = normalize_value(extract_field_value(text, field))
    if actual is None:
        human_review_findings.append(f"Missing required field: {field}")
    elif actual not in allowed:
        human_review_findings.append(f"{field} must be one of {allowed}, found {actual}")

def validate_evidence(text):
    errors = []
    blocked_reasons = []
    human_review_findings = []

    authority_findings = find_exact_markers(text, FORBIDDEN_AUTHORITY_MARKERS)
    if authority_findings:
        blocked_reasons.append("Forbidden authority marker found in targeted evidence file.")

    require_field_value(text, "document_type", "architecture_decision_evidence_packet", errors)
    require_field_value(text, "packet_status", "READY_FOR_HUMAN_REVIEW", errors)
    require_field_value(text, "recommendation_status", "CANDIDATE_ONLY", errors)
    require_field_value(text, "approval_status", "NOT_REQUESTED", errors)
    require_field_value(text, "is_approval", "false", errors)
    require_field_value(text, "is_execution_authorized", "false", errors)
    require_field_value(text, "is_implementation_authorized", "false", errors)
    require_field_value(text, "is_release_authorized", "false", errors)
    require_field_value(text, "human_review_required", "true", errors)
    require_field_in_values(text, "recommendation_confidence", ["LOW", "MEDIUM", "HIGH"], human_review_findings)

    if blocked_reasons or errors:
        return "BLOCKED", errors, blocked_reasons, authority_findings, human_review_findings
    if human_review_findings:
        return "HUMAN_REVIEW_REQUIRED", errors, blocked_reasons, authority_findings, human_review_findings
    return "PASS", errors, blocked_reasons, authority_findings, human_review_findings

def validate_review_matrix(text):
    errors = []
    blocked_reasons = []

    authority_findings = find_exact_markers(text, FORBIDDEN_AUTHORITY_MARKERS)
    weight_findings = find_exact_markers(text, FORBIDDEN_WEIGHT_MARKERS)
    if authority_findings:
        blocked_reasons.append("Forbidden authority marker found in targeted matrix file.")
    if weight_findings:
        blocked_reasons.append("Forbidden matrix completion or human-weight marker found.")

    document_type = normalize_value(extract_field_value(text, "document_type"))
    require_field_value(text, "matrix_status", "INCOMPLETE_WEIGHTS", errors)
    require_field_value(text, "approval_status", "NOT_REQUESTED", errors)
    require_field_value(text, "human_weight_required", "true", errors)
    require_field_value(text, "human_review_required", "true", errors)

    if document_type == "stack_fit_matrix":
        require_field_value(text, "default_stack_selected", "false", errors)
    elif document_type == "pattern_fit_matrix":
        require_field_value(text, "active_patterns_selected", "false", errors)
    else:
        errors.append(f"Unsupported review matrix document_type: {document_type}")

    criteria_rows = []
    in_weights_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## Criteria weights":
            in_weights_section = True
            continue
        if in_weights_section and stripped.startswith("## "):
            break
        if in_weights_section and stripped.startswith("|") and "UNASSIGNED_BY_HUMAN" in stripped:
            criteria_rows.append(stripped)
        elif in_weights_section and stripped.startswith("|") and stripped not in [
            "| Criterion | Weight | Human weight required | Evidence source |",
            "|---|---|---|---|",
        ]:
            errors.append(f"Criterion row missing weight field: {stripped}")

    if not criteria_rows:
        errors.append("No criteria rows with UNASSIGNED_BY_HUMAN found.")

    if blocked_reasons or errors:
        return "BLOCKED", errors, blocked_reasons, authority_findings + weight_findings
    return "PASS", errors, blocked_reasons, authority_findings + weight_findings

def validate_criteria(text):
    errors = []
    blocked_reasons = []

    authority_findings = find_exact_markers(text, FORBIDDEN_AUTHORITY_MARKERS)
    weight_findings = find_exact_markers(text, FORBIDDEN_WEIGHT_MARKERS)
    if authority_findings:
        blocked_reasons.append("Forbidden authority marker found in targeted criteria file.")
    if weight_findings:
        blocked_reasons.append("Forbidden human-weight marker found.")

    require_field_value(text, "document_type", "architecture_decision_criteria", errors)
    require_field_value(text, "criteria_status", "READY_FOR_HUMAN_WEIGHTING", errors)
    require_field_value(text, "approval_status", "NOT_REQUESTED", errors)
    require_field_value(text, "human_weight_required", "true", errors)
    require_field_value(text, "human_review_required", "true", errors)
    require_field_value(text, "is_approval", "false", errors)

    criteria_sections = re.findall(r'^###\s+(.+)$', text, re.MULTILINE)
    if not criteria_sections:
        errors.append("No criteria sections found.")

    section_blocks = re.split(r'^###\s+.+$', text, flags=re.MULTILINE)[1:]
    for criterion, block in zip(criteria_sections, section_blocks):
        if "weight: UNASSIGNED_BY_HUMAN" not in block:
            errors.append(f"Criterion missing unassigned human weight: {criterion}")
        if "human_weight_required: true" not in block:
            errors.append(f"Criterion missing human_weight_required: {criterion}")

    if blocked_reasons or errors:
        return "BLOCKED", errors, blocked_reasons, authority_findings + weight_findings
    return "PASS", errors, blocked_reasons, authority_findings + weight_findings

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
    document_type = normalize_value(extract_field_value(text, "document_type"))
    if document_type in ["stack_fit_matrix", "pattern_fit_matrix"]:
        return validate_review_matrix(text)

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

    return status_code, errors, blocked_reasons, []

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
        if re.search(r'^\s*(?:-\s*)?status\s*[:=]\s*ACTIVE\b', line) and not is_negative_invariant_line(line):
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
        "origin_conflict_resolution",
        "architecture_decision_evidence",
        "human_architecture_checkpoint",
        "unresolved_unknowns",
        "downstream_scope_boundary",
        "risk_profile_handling",
        "approval_boundary",
        "build_step_boundary"
    ]
    missing = contains_required_fields(text, required)
    if missing:
        errors.append(f"Missing required origins: {missing}")
        if "origin_unknown_resolution" in missing or "unresolved_unknowns" in missing or "architecture_decision_evidence" in missing:
            status_code = "UNKNOWN_BLOCKED"
        elif "origin_conflict_resolution" in missing and status_code == "PASS":
            status_code = "CONFLICT_BLOCKED"
        elif "human_architecture_checkpoint" in missing and status_code == "PASS":
            status_code = "HUMAN_REVIEW_REQUIRED"
        else:
            status_code = "BLOCKED"

    text_lower = text.lower()
    unsafe_contract_claims = [
        "pass is approval",
        "evidence is approval",
        "validator pass is execution authority",
        "task brief readiness is build step authorization",
        "aos-farm.633 execution claimed",
        "agent assigns low_risk_fast"
    ]
    for claim in unsafe_contract_claims:
        if claim in text_lower:
            errors.append(f"Unsafe contract claim found: {claim}")
            if status_code in ["PASS", "HUMAN_REVIEW_REQUIRED"]:
                status_code = "FAILED"

    return status_code, errors, blocked_reasons

def process_file_validation(file_path, command):
    text, err = read_text(file_path)
    if err:
        return "BLOCKED", [f"File missing or unreadable: {file_path}"], [], [], []

    authority_findings = find_positive_authority(text)
    unsafe_status_findings = find_unsafe_status_language(text)
    all_auth_findings = authority_findings + unsafe_status_findings

    if all_auth_findings:
        return "BLOCKED", [], ["Safety scanner blocked positive authority or unsafe status."], all_auth_findings, []

    status = "PASS"
    errors = []
    blocked_reasons = []
    human_review_findings = []

    if command == "brief":
        status, errors, blocked_reasons = validate_brief(text)
    elif command == "adr":
        status, errors, blocked_reasons = validate_adr(text)
    elif command == "matrix":
        status, errors, blocked_reasons, all_auth_findings = validate_matrix(text)
    elif command == "evidence":
        status, errors, blocked_reasons, all_auth_findings, human_review_findings = validate_evidence(text)
    elif command == "criteria":
        status, errors, blocked_reasons, all_auth_findings = validate_criteria(text)
    elif command == "registry":
        status, errors, blocked_reasons = validate_registry(text)
    elif command == "task-breakdown":
        status, errors, blocked_reasons = validate_task_breakdown(text)

    return status, errors, blocked_reasons, all_auth_findings, human_review_findings

def aggregate_status(current, new):
    hierarchy = {
        "BLOCKED": 6,
        "CONFLICT_BLOCKED": 5,
        "UNKNOWN_BLOCKED": 4,
        "HUMAN_REVIEW_REQUIRED": 3,
        "FAILED": 2,
        "NOT_RUN": 1,
        "PASS": 0
    }
    cur_val = hierarchy.get(current, 0)
    new_val = hierarchy.get(new, 0)
    return current if cur_val >= new_val else new


def check_result(id_str, status, severity, file_path, message):
    return {
        "id": id_str,
        "status": status,
        "severity": severity,
        "file": file_path,
        "message": message,
        # Keep backwards compatibility for old checks model if needed
        "checker": id_str,
        "result": status
    }

def run_structural_checks():
    results = []

    # 1. Required Architecture File Presence
    REQUIRED_ARCHITECTURE_FILES = [
        "aos/docs/workflow/architecture-input-intake.md",
        "aos/docs/workflow/architecture-decision-layer.md",
        "aos/docs/architecture/review/architecture-decision-evidence-packet.md",
        "aos/docs/architecture/review/human-architecture-checkpoint-template.md",
        "aos/docs/architecture/review/pattern-fit-matrix.md",
        "aos/docs/architecture/review/stack-fit-matrix.md",
        "aos/docs/architecture/decisions/README.md"
    ]
    for f in REQUIRED_ARCHITECTURE_FILES:
        if not os.path.exists(f):
            results.append(check_result("ARCH-REQ-FILE", "UNKNOWN_BLOCKED", "error", f, "required architecture artifact missing"))
        else:
            results.append(check_result("ARCH-REQ-FILE", "PASS", "info", f, "required file present"))

    # 2. Cross-Reference Diagnostics
    def require_link(source_file, target_string, ref_id):
        text, err = read_text(source_file)
        if err:
            results.append(check_result(ref_id, "WARNING", "warning", source_file, f"Could not read source file for cross-reference check: {source_file}"))
            return
        if target_string.lower() not in text.lower():
            results.append(check_result(ref_id, "WARNING", "warning", source_file, f"Missing cross-reference to: {target_string}"))
        else:
            results.append(check_result(ref_id, "PASS", "info", source_file, f"Found cross-reference to: {target_string}"))

    require_link("aos/START_HERE.md", "architecture input", "ARCH-REF-START-HERE")
    require_link("aos/START_HERE.md", "architecture decision layer", "ARCH-REF-INPUT-TO-DECISION")

    require_link("aos/docs/ROUTES.md", "architecture route", "ARCH-REF-ROUTES")
    require_link("aos/docs/ROUTES.md", "human checkpoint", "ARCH-REF-ROUTES")
    require_link("aos/docs/ROUTES.md", "no automatic execution authority", "ARCH-REF-ROUTES")

    require_link("aos/docs/workflow/architecture-decision-layer.md", "architecture-decision-evidence-packet.md", "ARCH-REF-DECISION-TO-EVIDENCE")
    require_link("aos/docs/workflow/architecture-decision-layer.md", "human-architecture-checkpoint-template.md", "ARCH-REF-EVIDENCE-TO-HUMAN-CHECKPOINT")
    require_link("aos/docs/workflow/architecture-decision-layer.md", "task brief", "ARCH-REF-HUMAN-CHECKPOINT-TO-TASK-BRIEF")

    # 3. Marker Groups & Unsafe Claims
    MARKER_GROUPS = {
        "hard_safety_boundary": [
            ("PASS ≠ approval", "PASS != approval", "PASS not approval", "Validation PASS ≠ approval", "Architecture validator PASS ≠ approval", "validator PASS ≠ approval"),
            ("Evidence ≠ approval", "Evidence != approval", "Evidence not approval", "Evidence Packet ≠ approval", "Evidence Packet != approval"),
            ("CI PASS ≠ approval", "CI PASS != approval", "CI PASS not approval"),
            ("UNKNOWN ≠ OK", "UNKNOWN != OK", "UNKNOWN not OK"),
            ("NOT_RUN ≠ PASS", "NOT_RUN != PASS", "NOT_RUN not PASS"),
            ("Human approval cannot be simulated", "human approval cannot be simulated"),
            ("approval_claimed: false", "approval not claimed", "approval_status: NOT_APPROVED", "not approved", "does not grant approval", "no approval record is created", "is_approval: false", "approval_status: NOT_REQUESTED"),
            ("implementation_authorized: false", "implementation not authorized", "does not authorize implementation", "is_implementation_authorized: false", "implementation was not authorized", "no implementation is authorized"),
            ("release_authorized: false", "release not authorized", "does not authorize release", "is_release_authorized: false", "release was not authorized", "no release is authorized"),
            ("human_review_required: true", "human review required", "human checkpoint", "human review is required")
        ],
        "aos/docs/workflow/architecture-input-intake.md": [
            ("purpose", "input"), "constraints", "assumptions", "UNKNOWN", "non-goals", ("human review", "checkpoint")
        ],
        "aos/docs/workflow/architecture-decision-layer.md": [
            "decision question", "options", "recommended option", "rejected options", "Evidence", "human review", "approval boundary"
        ],
        "aos/docs/architecture/review/architecture-decision-evidence-packet.md": [
            "Evidence summary", "inspected files", "validation results", "assumptions", "UNKNOWNs", "rejected options", "human questions", "approval not claimed"
        ]
    }

    for doc_path in REQUIRED_ARCHITECTURE_FILES:
        text, err = read_text(doc_path)
        if err:
            continue

        text_lower = text.lower()

        # Hard Safety Boundary for specific files (e.g. decision layer, evidence packet)
        if doc_path in [
            "aos/docs/workflow/architecture-decision-layer.md",
            "aos/docs/architecture/review/architecture-decision-evidence-packet.md"
        ]:
            for marker_group in MARKER_GROUPS["hard_safety_boundary"]:
                if not any(m.lower() in text_lower for m in marker_group):
                    results.append(check_result("ARCH-MARKER-HARD", "WARNING", "warning", doc_path, f"canonical doc alignment required outside current AOS-FARM.627 write scope: missing hard safety boundary marker from group: {marker_group[0]}"))
                else:
                    results.append(check_result("ARCH-MARKER-HARD", "PASS", "info", doc_path, f"Found hard safety boundary marker from group: {marker_group[0]}"))

        # Recommended Structure
        if doc_path in MARKER_GROUPS:
            for marker_spec in MARKER_GROUPS[doc_path]:
                if isinstance(marker_spec, tuple):
                    found = any(m.lower() in text_lower for m in marker_spec)
                    name = " or ".join(marker_spec)
                else:
                    found = marker_spec.lower() in text_lower
                    name = marker_spec

                if not found:
                    results.append(check_result("ARCH-MARKER-REC", "WARNING", "warning", doc_path, f"Missing recommended structural marker: {name}"))
                else:
                    results.append(check_result("ARCH-MARKER-REC", "PASS", "info", doc_path, f"Found recommended structural marker: {name}"))

        # Unsafe Claims Classifier
        unsafe_phrases = [
            "architecture approved", "approval granted", "automatically approved",
            "validator approves", "pass approves", "ready_for_execution",
            "implementation authorized", "release authorized", "human approval simulated",
            "validator pass authorizes execution", "task brief authorizes build step",
            "aos-farm.633 execution claimed", "pass is approval", "evidence is approval",
            "evidence proves approval", "pass proves approval",
            "validator pass is execution authority",
            "task brief readiness is build step authorization",
            "agent assigns low_risk_fast", "agent self-assigns low_risk_fast"
        ]
        allowed_assertions = [
            "approval_claimed: false", "approval granted: no", "not approved",
            "not automatically approved", "does not approve", "does not authorize",
            "pass ≠ approval", "converted to approval: no", "implementation_authorized: false",
            "release_authorized: false", "human approval cannot be simulated"
        ]
        negation_markers = [
            "not", "no", "false", "cannot", "must not", "does not", "do not",
            "≠", "!=", "not approved", "not authorized", "not claimed",
            "without approval", "approval not claimed", "implementation_authorized: false",
            "release_authorized: false", "approval_claimed: false", "forbidden example",
            "unsafe example", "should reject", "negative test"
        ]

        ambiguous_markers = ["unclear", "maybe", "unsure", "pending", "might", "could", "possibly", "assume"]
        lines = text.splitlines()
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for unsafe in unsafe_phrases:
                if unsafe.lower() in line_lower:
                    is_explicitly_allowed = any(allowed.lower() in line_lower for allowed in allowed_assertions)
                    if is_explicitly_allowed:
                        continue

                    has_negation = any(neg.lower() in line_lower for neg in negation_markers)
                    if has_negation:
                        # Negative context explicitly negates the unsafe phrase
                        continue

                    has_ambiguous = any(amb.lower() in line_lower for amb in ambiguous_markers)

                    if has_ambiguous:
                        results.append(check_result("ARCH-UNSAFE-CLAIM", "UNKNOWN_BLOCKED", "error", doc_path, f"Ambiguous approval wording on line {i+1}: '{unsafe}'"))
                    else:
                        results.append(check_result("ARCH-UNSAFE-CLAIM", "FAILED", "error", doc_path, f"Unsafe positive approval wording on line {i+1}: '{unsafe}'"))

    return results


def get_validate_all_report():
    known_targets = [
        ("evidence", "aos/docs/architecture/review/architecture-decision-evidence-packet.md"),
        ("matrix", "aos/docs/architecture/review/stack-fit-matrix.md"),
        ("matrix", "aos/docs/architecture/review/pattern-fit-matrix.md"),
        ("criteria", "aos/docs/architecture/review/architecture-decision-criteria.md"),
        ("task-breakdown", "tests/fixtures/architecture/valid_task_breakdown_traced.md")
    ]

    registry_files = [
        "aos/docs/architecture/pattern-registry.md",
        "aos/docs/architecture/stack-preset-registry.md"
    ]

    overall_status = "PASS"
    all_errors = []
    all_blocked = []
    all_auth = []
    all_human_review = []
    checks_report = []

    for reg_file in registry_files:
        status, errors, blocked_reasons, auth_findings, human_review_findings = process_file_validation(reg_file, "registry")
        overall_status = aggregate_status(overall_status, status)
        checks_report.append({"file": reg_file, "checker": "registry", "result": status})
        all_errors.extend(errors)
        all_blocked.extend(blocked_reasons)
        all_auth.extend(auth_findings)
        all_human_review.extend(human_review_findings)

    for cmd, path in known_targets:
        status, errors, blocked_reasons, auth_findings, human_review_findings = process_file_validation(path, cmd)
        overall_status = aggregate_status(overall_status, status)
        checks_report.append({"file": path, "checker": cmd, "result": status})
        all_errors.extend(errors)
        all_blocked.extend(blocked_reasons)
        all_auth.extend(auth_findings)
        all_human_review.extend(human_review_findings)

    structural_results = run_structural_checks()
    for res in structural_results:
        status = res.get("status")
        # Do not aggregate WARNING or PASS or NOT_RUN into overall failure unnecessarily, but FAILED, BLOCKED, UNKNOWN_BLOCKED affect overall
        if status in ["BLOCKED", "UNKNOWN_BLOCKED", "FAILED"]:
            overall_status = aggregate_status(overall_status, status)
        checks_report.append(res)

    return build_report_dict(
        status=overall_status,
        target_type="validate-all",
        file_path="aggregate",
        errors=all_errors,
        blocked_reasons=all_blocked,
        authority_findings=all_auth,
        human_review_findings=all_human_review,
        checks=checks_report
    )

def run_validate_all():
    report = get_validate_all_report()
    print(json.dumps(report, indent=2))
    exit_for_status(report["status"])

def main():
    parser = build_parser()
    args = parser.parse_args()

    command = args.command

    if command == "validate-all":
        run_validate_all()
        return

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
            status, errors, blocked_reasons, auth_findings, _human_review_findings = process_file_validation(reg_file, "registry")
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
        status, errors, blocked_reasons, auth_findings, human_review_findings = process_file_validation(file_path, command)
        document_type = None
        text, _err = read_text(file_path)
        if text:
            document_type = normalize_value(extract_field_value(text, "document_type"))
        emit_report(
            status=status,
            target_type=command,
            file_path=file_path,
            errors=errors,
            blocked_reasons=blocked_reasons,
            authority_findings=auth_findings,
            human_review_findings=human_review_findings,
            document_type=document_type
        )
        exit_for_status(status)

if __name__ == "__main__":
    main()
