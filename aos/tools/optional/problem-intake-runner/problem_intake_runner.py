#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional


REQUIRED_OUTPUT_FILES = {
    "PROJECT_SPEC.draft.md",
    "REQUIREMENTS.draft.md",
    "problem-interview-report.md",
    "requirements-checklist-draft.md",
    "problem-intake-run-report.md",
}

SUPPORTED_ROUTE = "EXISTING_SPEC_REVIEW"

SECTION_ALIASES = {
    "problem": ("problem statement", "problem", "pain", "issue"),
    "target_user": ("target user", "user", "users", "audience"),
    "current_workflow": ("current workflow", "current process", "workflow", "as is"),
    "target_outcome": ("desired outcome", "target outcome", "goal", "objective"),
    "constraints": ("constraints", "negative constraints", "non-goals", "non goals"),
    "known_risks": ("known risks", "risks", "risk"),
    "open_questions": ("open questions", "unknown", "questions", "gaps"),
    "data_discovery": ("data discovery", "data", "data inventory"),
    "information_flow": ("information flow", "data flow", "flow"),
    "access_permissions": ("access", "permissions", "roles"),
    "acceptance_criteria": ("acceptance criteria", "acceptance", "success criteria"),
    "mvp": ("mvp", "minimum viable", "minimum scope"),
    "implementation_hints": ("implementation hints", "technical notes", "technology"),
    "contradictions": ("contradictions", "conflicts"),
    "requirements": ("requirements", "functional requirements"),
}

CORE_FIELDS = (
    "problem",
    "target_user",
    "current_workflow",
    "target_outcome",
    "constraints",
    "known_risks",
    "open_questions",
)


def check_run_id_safe(run_id: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", run_id))


def normalize_heading(heading: str) -> str:
    heading = heading.strip().lower()
    heading = re.sub(r"^#+\s*", "", heading)
    heading = re.sub(r"^\d+[\.)]\s*", "", heading)
    return heading.strip()


def canonical_field(heading: str) -> Optional[str]:
    normalized = normalize_heading(heading)
    for field, aliases in SECTION_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            return field
    return None


def extract_markdown_sections(content: str) -> dict:
    sections: dict[str, list[str]] = {}
    current_field: Optional[str] = None
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.lstrip().startswith("#"):
            if current_field:
                sections.setdefault(current_field, []).append("\n".join(current_lines).strip())
            current_field = canonical_field(line)
            current_lines = []
            continue
        if current_field:
            current_lines.append(line)

    if current_field:
        sections.setdefault(current_field, []).append("\n".join(current_lines).strip())

    return {
        field: "\n\n".join(part for part in parts if part).strip()
        for field, parts in sections.items()
    }


def compact_text(value: str, limit: int = 1800) -> str:
    value = value.strip()
    if not value:
        return ""
    value = re.sub(r"\n{3,}", "\n\n", value)
    if len(value) <= limit:
        return value
    return value[: limit - 80].rstrip() + "\n\n[TRUNCATED_FOR_DRAFT_REVIEW]"


def fallback_source_excerpt(content: str) -> str:
    text = re.sub(r"\s+", " ", content).strip()
    if not text:
        return "NEEDS_HUMAN_REVIEW: source material is empty."
    if len(text) <= 1200:
        return text
    return text[:1120].rstrip() + " [TRUNCATED_FOR_DRAFT_REVIEW]"


def missing_value(label: str) -> str:
    return f"NEEDS_HUMAN_REVIEW: {label} was not found in the existing material."


def value_or_missing(sections: dict, field: str, label: str, source_excerpt: str = "") -> str:
    value = compact_text(sections.get(field, ""))
    if value:
        return value
    if field == "problem" and source_excerpt:
        return (
            "NEEDS_HUMAN_REVIEW: explicit Problem Statement was not found. "
            "Source excerpt preserved for review:\n\n" + source_excerpt
        )
    return missing_value(label)


def build_unknowns(sections: dict) -> list[str]:
    unknowns: list[str] = []
    labels = {
        "problem": "Problem Statement",
        "target_user": "Target User",
        "current_workflow": "Current Workflow",
        "target_outcome": "Desired Outcome",
        "constraints": "Constraints",
        "known_risks": "Known Risks",
        "open_questions": "Open Questions",
        "data_discovery": "Data Discovery",
        "information_flow": "Information Flow",
        "access_permissions": "Access / Permissions",
        "acceptance_criteria": "Acceptance Criteria",
    }
    for field, label in labels.items():
        if not sections.get(field, "").strip():
            unknowns.append(f"UNKNOWN: {label} missing or insufficient in source material.")

    open_questions = compact_text(sections.get("open_questions", ""))
    if open_questions:
        for line in open_questions.splitlines():
            stripped = line.strip("-* \t")
            if stripped:
                unknowns.append(f"UNKNOWN: {stripped}")

    return unknowns or ["UNKNOWN: No explicit open questions supplied; human review required."]


def build_human_decisions(unknowns: list[str]) -> list[str]:
    decisions = [
        "Assign Risk Profile before any execution.",
        "Confirm whether candidate requirements are in scope.",
        "Confirm exact allowed and forbidden changes before implementation.",
        "Confirm acceptance criteria before execution.",
        "Confirm execution authorization separately; this runner never authorizes execution.",
    ]
    if unknowns:
        decisions.append("Resolve or explicitly accept listed UNKNOWN items before finalization.")
    return decisions


def yaml_block(extra: Optional[dict] = None) -> str:
    fields = {
        "artifact_status": "DRAFT",
        "approval_status": "NOT_APPROVED",
        "automation_status": "RUNNER_V2_EXISTING_SPEC_REVIEW_ONLY",
        "production_status": "NOT_PRODUCTION",
        "intake_route": SUPPORTED_ROUTE,
        "ready_for_execution": "false",
        "execution_authorized": "false",
        "implementation_authorized": "false",
        "commit_authorized": "false",
        "push_authorized": "false",
        "release_authorized": "false",
        "production_use_authorized": "false",
    }
    if extra:
        fields.update(extra)
    lines = ["```yaml"]
    lines.extend(f"{key}: {value}" for key, value in fields.items())
    lines.append("```")
    return "\n".join(lines)


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def final_status_block(sections: dict, unknowns: list[str], final_status: str) -> str:
    critical_failure_count = len(unknowns)
    confidence = "LOW" if critical_failure_count else "MEDIUM"
    return "\n".join(
        [
            "```yaml",
            "artifact_type: technical_assignment_intake_draft",
            f"intake_depth: {SUPPORTED_ROUTE}",
            "problem_interview_status: NOT_REQUIRED_EXISTING_SPEC_REVIEW",
            "problem_evidence_level: UNKNOWN",
            f"data_discovery_depth: {'PARTIAL' if sections.get('data_discovery') else 'MISSING'}",
            f"information_flow_status: {'PARTIAL' if sections.get('information_flow') else 'MISSING'}",
            f"access_permissions_status: {'PARTIAL' if sections.get('access_permissions') else 'MISSING'}",
            f"requirements_confidence: {confidence}",
            f"unknown_count: {len(unknowns)}",
            f"contradiction_count: {1 if sections.get('contradictions') else 0}",
            "inference_count: 0",
            f"implementation_hint_count: {1 if sections.get('implementation_hints') else 0}",
            f"critical_failure_count: {critical_failure_count}",
            "ready_for_requirements_review: true_with_risks",
            "ready_for_execution: false",
            "approval_status: NOT_APPROVED",
            "execution_authorized: false",
            "implementation_authorized: false",
            "commit_authorized: false",
            "push_authorized: false",
            "deploy_authorized: false",
            "production_use_authorized: false",
            f"final_status: {final_status}",
            "```",
        ]
    )


def project_spec_content(sections: dict, unknowns: list[str], human_decisions: list[str], source_excerpt: str, final_status: str) -> str:
    return f"""# PROJECT_SPEC.draft.md

{yaml_block({"final_status": final_status})}

## 1. Source Status

| Field | Value |
|---|---|
| Entry Route | {SUPPORTED_ROUTE} |
| Problem Interview Status | NOT_REQUIRED_EXISTING_SPEC_REVIEW |
| Ready For Execution | false |
| Approval Status | NOT_APPROVED |
| Missing Sections Status | {'NEEDS_HUMAN_REVIEW' if unknowns else 'DRAFT'} |

## 2. User Vision

{value_or_missing(sections, "problem", "User Vision / Problem Statement", source_excerpt)}

## 3. Data Discovery

{value_or_missing(sections, "data_discovery", "Data Discovery")}

## 4. Information Flow

{value_or_missing(sections, "information_flow", "Information Flow")}

## 5. Access / Permissions

{value_or_missing(sections, "access_permissions", "Access / Permissions")}

## 6. Problem Evidence

{value_or_missing(sections, "known_risks", "Problem Evidence / Known Risks")}

## 7. Optional Current Workflow

{value_or_missing(sections, "current_workflow", "Current Workflow")}

## 8. Requirements Draft

{value_or_missing(sections, "requirements", "Requirements Draft")}

## 9. Implementation Hints

{value_or_missing(sections, "implementation_hints", "Implementation Hints")}

## 10. Negative Constraints

{value_or_missing(sections, "constraints", "Negative Constraints / Constraints")}

## 11. Acceptance Criteria

{value_or_missing(sections, "acceptance_criteria", "Acceptance Criteria")}

## 12. MVP

{value_or_missing(sections, "mvp", "MVP")}

## 13. UNKNOWN / Open Questions

{bullets(unknowns)}

## 14. Contradictions

{value_or_missing(sections, "contradictions", "Contradictions")}

## 15. Human Decisions Required

{bullets(human_decisions)}

## 16. Final Status

{final_status_block(sections, unknowns, final_status)}
"""


def requirements_content(sections: dict, unknowns: list[str], human_decisions: list[str], final_status: str) -> str:
    requirement_source = value_or_missing(sections, "requirements", "Functional Requirements")
    data_source = value_or_missing(sections, "data_discovery", "Data Requirements")
    access_source = value_or_missing(sections, "access_permissions", "Access Requirements")
    constraints = value_or_missing(sections, "constraints", "Constraints")
    acceptance = value_or_missing(sections, "acceptance_criteria", "Acceptance Criteria")
    risks = value_or_missing(sections, "known_risks", "Security / Privacy / Known Risks")
    return f"""# REQUIREMENTS.draft.md

{yaml_block({"final_status": final_status})}

## Functional Requirements

- FR-001: Candidate behavior extracted from source material.
  - Source: existing specification review
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
  - Detail: {requirement_source}

## Data Requirements

- DATA-001: Candidate data handling scope.
  - Sensitive: UNKNOWN
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: {data_source}

## Access Requirements

- ACCESS-001: Candidate access / permission scope.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: {access_source}

## Non-Functional Requirements

- NFR-001: Non-functional requirements are not finalized by this runner.
  - Status: NEEDS_HUMAN_REVIEW

## Constraints

- CON-001: Candidate constraints and non-goals.
  - Status: CANDIDATE_CONSTRAINT
  - Detail: {constraints}

## Security / Privacy

- SEC-001: Security, privacy, and risk handling require human review.
  - Status: NEEDS_HUMAN_REVIEW
  - Detail: {risks}

## Acceptance Criteria

- AC-001: Candidate acceptance criteria.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
  - Detail: {acceptance}

## Out of Scope

- Final Task Brief creation.
- Execution authorization.
- Implementation authorization.
- Production use.

## UNKNOWN / Open Questions

{bullets(unknowns)}

## Human Decisions Required

{bullets(human_decisions)}

## Final Status

{final_status_block(sections, unknowns, final_status)}
"""


def problem_report_content(sections: dict, unknowns: list[str], final_status: str) -> str:
    return f"""# Problem Interview Report

{yaml_block({"final_status": final_status})}

## Interview Route

`{SUPPORTED_ROUTE}` only. No interview automation was performed.

## Problem

{value_or_missing(sections, "problem", "Problem Statement")}

## Target User

{value_or_missing(sections, "target_user", "Target User")}

## Current Workflow

{value_or_missing(sections, "current_workflow", "Current Workflow")}

## Target Outcome

{value_or_missing(sections, "target_outcome", "Target Outcome")}

## Risks

{value_or_missing(sections, "known_risks", "Known Risks")}

## UNKNOWN / Open Questions

{bullets(unknowns)}

## Final Status

final_status: {final_status}
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
"""


def checklist_content(sections: dict, unknowns: list[str], human_decisions: list[str], final_status: str) -> str:
    rows = []
    for field in CORE_FIELDS:
        label = field.replace("_", " ").title()
        status = "FOUND" if sections.get(field) else "NEEDS_HUMAN_REVIEW"
        rows.append(f"| {label} | {status} |")

    return f"""# Requirements Checklist Draft

{yaml_block({"final_status": final_status})}

## Field Coverage

| Field | Status |
|---|---|
{chr(10).join(rows)}

## UNKNOWN / Open Questions

{bullets(unknowns)}

## Human Decisions Required

{bullets(human_decisions)}

## Final Status

final_status: {final_status}
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
"""


def run_report_content(run_id: str, output_dir: Path, sections: dict, unknowns: list[str], final_status: str) -> str:
    missing_core = [field.replace("_", " ").title() for field in CORE_FIELDS if not sections.get(field)]
    return f"""# Problem Intake Run Report

{yaml_block({
    "run_status": "DRAFT_ARTIFACTS_CREATED",
    "draft_status": "DRAFT",
    "validator_status": "NOT_RUN",
    "final_status": final_status,
})}

## Run Metadata

- run_id: `{run_id}`
- output_dir: `{output_dir}`
- runner_scope: `{SUPPORTED_ROUTE}_ONLY`
- interview_automation_performed: false
- final_task_brief_created: false

## Created Artifacts

{bullets(sorted(REQUIRED_OUTPUT_FILES))}

## Missing Core Sections

{bullets(missing_core) if missing_core else "- None"}

## UNKNOWN / Open Questions

{bullets(unknowns)}

## Final Status

final_status: {final_status}
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
approval_status: NOT_APPROVED
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Problem Intake Runner v2")
    parser.add_argument("--input", required=True, help="Path to input Markdown file")
    parser.add_argument("--run-id", required=True, help="Unique run identifier")
    parser.add_argument("--output-root", default="agentos/reports/problem-intake", help="Root output directory")
    parser.add_argument("--route", default=SUPPORTED_ROUTE, help="Automation route. Only EXISTING_SPEC_REVIEW is automated.")
    args = parser.parse_args()

    if args.route != SUPPORTED_ROUTE:
        print(f"Error: route '{args.route}' is not automated. Interview routes remain manual/prompt-based.")
        return 1

    input_path = Path(args.input)
    output_root = Path(args.output_root)
    output_dir = output_root / args.run_id

    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist.")
        return 1
    if not input_path.is_file():
        print(f"Error: Input path '{input_path}' is not a file.")
        return 1
    if not check_run_id_safe(args.run_id):
        print(f"Error: Run ID '{args.run_id}' is not filesystem-safe.")
        return 1
    if output_dir.exists():
        print(f"Error: Output directory '{output_dir}' already exists. Overwrite is forbidden.")
        return 1

    try:
        input_content = input_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error reading input file: {exc}")
        return 1

    sections = extract_markdown_sections(input_content)
    source_excerpt = fallback_source_excerpt(input_content)
    unknowns = build_unknowns(sections)
    human_decisions = build_human_decisions(unknowns)
    final_status = "NEEDS_HUMAN_REVIEW" if unknowns else "READY_FOR_HUMAN_REVIEW"

    artifacts = {
        "PROJECT_SPEC.draft.md": project_spec_content(sections, unknowns, human_decisions, source_excerpt, final_status),
        "REQUIREMENTS.draft.md": requirements_content(sections, unknowns, human_decisions, final_status),
        "problem-interview-report.md": problem_report_content(sections, unknowns, final_status),
        "requirements-checklist-draft.md": checklist_content(sections, unknowns, human_decisions, final_status),
        "problem-intake-run-report.md": run_report_content(args.run_id, output_dir, sections, unknowns, final_status),
    }

    try:
        output_dir.mkdir(parents=True, exist_ok=False)
        for filename, content in artifacts.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
    except OSError as exc:
        print(f"Error writing artifacts: {exc}")
        return 1

    print(f"Draft artifacts successfully saved to '{output_dir}'.")
    print(f"runner_scope: {SUPPORTED_ROUTE}_ONLY")
    print(f"final_status: {final_status}")
    print("ready_for_execution: false")
    print("execution_authorized: false")
    print("implementation_authorized: false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
