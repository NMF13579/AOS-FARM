#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional


REQUIRED_FILES = {
    "PROJECT_SPEC.draft.md",
    "REQUIREMENTS.draft.md",
    "problem-interview-report.md",
    "requirements-checklist-draft.md",
    "problem-intake-run-report.md",
}

PROJECT_SPEC_REQUIRED_SECTIONS = {
    "source status": "source_status",
    "user vision": "user_vision",
    "data discovery": "data_discovery",
    "information flow": "information_flow",
    "access / permissions": "access_permissions",
    "problem evidence": "problem_evidence_if_applicable",
    "optional current workflow": "optional_current_workflow_if_applicable",
    "requirements draft": "requirements_draft",
    "implementation hints": "implementation_hints",
    "negative constraints": "negative_constraints",
    "acceptance criteria": "acceptance_criteria",
    "mvp": "mvp",
    "unknown / open questions": "unknown_open_questions",
    "contradictions": "contradictions",
    "human decisions required": "human_decisions_required",
    "final status": "final_status",
}

REQUIREMENTS_REQUIRED_SECTIONS = {
    "functional requirements",
    "data requirements",
    "access requirements",
    "non-functional requirements",
    "constraints",
    "security / privacy",
    "acceptance criteria",
    "out of scope",
    "unknown / open questions",
    "human decisions required",
    "final status",
}

SAFETY_FIELD_PATTERNS = {
    "approval_status_not_approved": r"(?m)^\s*approval_status:\s*NOT_APPROVED\s*$",
    "ready_for_execution_false": r"(?m)^\s*ready_for_execution:\s*false\s*$",
    "execution_authorized_false": r"(?m)^\s*execution_authorized:\s*false\s*$",
    "implementation_authorized_false": r"(?m)^\s*implementation_authorized:\s*false\s*$",
    "final_status_present": r"(?m)^\s*final_status:\s*(DRAFT|NEEDS_HUMAN_REVIEW|UNKNOWN_BLOCKED|READY_FOR_HUMAN_REVIEW|STRUCTURAL_MVP_ONLY)\s*$",
}

FORBIDDEN_STATUS_VALUES = {
    "APPROVED",
    "READY_FOR_EXECUTION",
    "IMPLEMENTATION_AUTHORIZED",
    "PRODUCTION_READY",
    "EXECUTION_AUTHORIZED",
    "HUMAN_APPROVED",
}

AUTHORIZED_TRUE_FIELDS = {
    "ready_for_execution",
    "execution_authorized",
    "implementation_authorized",
    "commit_authorized",
    "push_authorized",
    "deploy_authorized",
    "release_authorized",
    "production_use_authorized",
}

SUCCESS_STATUSES = {"STRUCTURAL_CONTRACT_VALIDATED", "NEEDS_HUMAN_REVIEW"}


def normalize_heading(line: str) -> str:
    text = line.strip().lower()
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^\d+[\.)]\s*", "", text)
    return text.strip()


def headings(content: str) -> set[str]:
    return {normalize_heading(line) for line in content.splitlines() if line.lstrip().startswith("#")}


def has_section(content: str, expected: str) -> bool:
    normalized_headings = headings(content)
    return any(expected in heading for heading in normalized_headings)


def check_required_sections(filename: str, content: str) -> list[str]:
    errors: list[str] = []
    if filename == "PROJECT_SPEC.draft.md":
        for heading_text, section_id in PROJECT_SPEC_REQUIRED_SECTIONS.items():
            if not has_section(content, heading_text):
                errors.append(f"{filename} missing required section from 02-agent-contract.md: {section_id}")
    elif filename == "REQUIREMENTS.draft.md":
        for heading_text in REQUIREMENTS_REQUIRED_SECTIONS:
            if not has_section(content, heading_text):
                errors.append(f"{filename} missing required requirements section: {heading_text}")
    return errors


def check_safety_fields(filename: str, content: str) -> list[str]:
    errors: list[str] = []
    for field_name, pattern in SAFETY_FIELD_PATTERNS.items():
        if not re.search(pattern, content):
            errors.append(f"{filename} missing or invalid safety field: {field_name}")
    return errors


def status_value(line: str) -> Optional[tuple[str, str]]:
    match = re.match(r"^\s*([A-Za-z0-9_ -]+)\s*:\s*['\"]?([^'\"#\n]+)", line)
    if not match:
        return None
    key = match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
    value = match.group(2).strip().strip(",")
    return key, value


def table_status_value(line: str) -> Optional[tuple[str, str]]:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    if len(cells) < 2:
        return None
    key = cells[0].lower().replace(" ", "_").replace("-", "_")
    value = cells[1].strip()
    return key, value


def is_actual_status_key(key: str) -> bool:
    return any(
        marker in key
        for marker in (
            "status",
            "authorized",
            "authorization",
            "ready_for_execution",
            "decision",
            "approval",
            "production",
        )
    )


def check_forbidden_promotions(filename: str, content: str) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        parsed = status_value(line) or table_status_value(line)
        if not parsed:
            continue
        key, value = parsed
        normalized_value = value.strip().strip("`").upper()
        normalized_key = key.lower()

        if normalized_key in AUTHORIZED_TRUE_FIELDS and normalized_value == "TRUE":
            errors.append(f"{filename}:{line_number} forbidden authorization value: {key}: {value}")
            continue

        if is_actual_status_key(normalized_key) and normalized_value in FORBIDDEN_STATUS_VALUES:
            errors.append(f"{filename}:{line_number} forbidden status promotion: {key}: {value}")
    return errors


def read_required_files(run_dir: Path) -> tuple[dict[str, str], list[str], list[str]]:
    actual_files = {path.name for path in run_dir.iterdir() if path.is_file()}
    missing = sorted(REQUIRED_FILES - actual_files)
    unexpected = sorted(actual_files - REQUIRED_FILES)
    contents: dict[str, str] = {}

    for filename in sorted(REQUIRED_FILES & actual_files):
        file_path = run_dir / filename
        try:
            contents[filename] = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise OSError(f"Error reading {filename}: {exc}") from exc

    return contents, missing, unexpected


def analyze(run_dir: Path) -> dict:
    contents, missing_files, unexpected_files = read_required_files(run_dir)
    section_errors: list[str] = []
    safety_errors: list[str] = []
    forbidden_promotions: list[str] = []

    for filename, content in contents.items():
        section_errors.extend(check_required_sections(filename, content))
        safety_errors.extend(check_safety_fields(filename, content))
        forbidden_promotions.extend(check_forbidden_promotions(filename, content))

    combined_content = "\n".join(contents.values())
    unknown_visible = bool(re.search(r"\bUNKNOWN\b|NEEDS_HUMAN_REVIEW|UNKNOWN_BLOCKED", combined_content))
    human_decisions_visible = "Human Decisions Required" in combined_content
    approval_simulation_detected = bool(forbidden_promotions)

    if forbidden_promotions:
        validator_status = "FORBIDDEN_PROMOTION_DETECTED"
    elif missing_files or unexpected_files or section_errors or safety_errors:
        validator_status = "CONTRACT_VIOLATION"
    elif not unknown_visible:
        validator_status = "UNKNOWN_BLOCKED"
    elif not human_decisions_visible:
        validator_status = "NEEDS_HUMAN_REVIEW"
    else:
        validator_status = "NEEDS_HUMAN_REVIEW"

    return {
        "validator_status": validator_status,
        "found_files": sorted(contents),
        "missing_files": missing_files,
        "unexpected_files": unexpected_files,
        "section_errors": section_errors,
        "safety_errors": safety_errors,
        "forbidden_promotions": forbidden_promotions,
        "unknown_visible": unknown_visible,
        "human_decisions_visible": human_decisions_visible,
        "approval_simulation_detected": approval_simulation_detected,
        "ready_for_execution_authorized": False,
        "execution_authorized": False,
        "implementation_authorized": False,
    }


def generate_report(args, results: dict, report_path: Path) -> None:
    lines = [
        "# Problem Intake Output Validator v2 Report",
        "",
        "## 1. Task Metadata",
        f"- run_directory: `{args.run_dir}`",
        "- validator_scope: structural_contract_only",
        "- semantic_product_quality_validated: false",
        "- approval_declared: false",
        "- execution_authorized: false",
        "- implementation_authorized: false",
        "",
        "## 2. Required File Inventory",
    ]
    for filename in sorted(REQUIRED_FILES):
        status = "found" if filename in results["found_files"] else "missing"
        lines.append(f"- {filename}: {status}")

    lines.extend(["", "## 3. Unexpected File Inventory"])
    lines.extend([f"- {name}" for name in results["unexpected_files"]] or ["- none"])

    lines.extend(["", "## 4. Contract Checks"])
    for key in ("section_errors", "safety_errors", "forbidden_promotions"):
        lines.append(f"### {key}")
        lines.extend([f"- {item}" for item in results[key]] or ["- none"])

    lines.extend(
        [
            "",
            "## 5. Visibility Checks",
            f"- unknown_visible: {str(results['unknown_visible']).lower()}",
            f"- human_decisions_visible: {str(results['human_decisions_visible']).lower()}",
            "",
            "## 6. Final Validator Status",
            "```yaml",
            f"validator_status: {results['validator_status']}",
            "approval_status: NOT_APPROVED",
            "ready_for_execution: false",
            "execution_authorized: false",
            "implementation_authorized: false",
            "semantic_product_quality_validated: false",
            "```",
        ]
    )

    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Error writing report: {exc}")
        sys.exit(2)


def print_results(results: dict) -> None:
    print(f"validator_status: {results['validator_status']}")
    print(f"required_files_found: {len(results['found_files'])}/{len(REQUIRED_FILES)}")
    print(f"missing_required_files: {len(results['missing_files'])}")
    print(f"section_errors: {len(results['section_errors'])}")
    print(f"safety_errors: {len(results['safety_errors'])}")
    print(f"forbidden_promotions: {len(results['forbidden_promotions'])}")
    print(f"unknown_visible: {str(results['unknown_visible']).lower()}")
    print(f"human_decisions_visible: {str(results['human_decisions_visible']).lower()}")
    print("approval_status: NOT_APPROVED")
    print("ready_for_execution: false")
    print("execution_authorized: false")
    print("implementation_authorized: false")


def main() -> int:
    parser = argparse.ArgumentParser(description="Problem Intake Output Validator v2")
    parser.add_argument("--run-dir", required=True, help="Path to the problem intake run directory")
    parser.add_argument("--report", help="Path to output markdown report")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        print(f"validator_status: TOOL_ERROR")
        print(f"error: Run directory '{run_dir}' does not exist.")
        return 2
    if not run_dir.is_dir():
        print("validator_status: TOOL_ERROR")
        print(f"error: Run directory '{run_dir}' is not a directory.")
        return 2

    try:
        results = analyze(run_dir)
    except OSError as exc:
        print("validator_status: TOOL_ERROR")
        print(f"error: {exc}")
        return 2
    except Exception as exc:
        print("validator_status: VALIDATOR_ERROR")
        print(f"error: {exc}")
        return 2

    if args.report:
        generate_report(args, results, Path(args.report))

    print_results(results)
    return 0 if results["validator_status"] in SUCCESS_STATUSES else 1


if __name__ == "__main__":
    sys.exit(main())
