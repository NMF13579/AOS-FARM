from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import argparse
import json
import re


PASS = "PASS"
BLOCKED = "BLOCKED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"

EXIT_CODES = {PASS: 0, BLOCKED: 1, UNKNOWN_BLOCKED: 1, HUMAN_REVIEW_REQUIRED: 1}
ALLOWED_STATUSES = {PASS, BLOCKED, UNKNOWN_BLOCKED, HUMAN_REVIEW_REQUIRED}


class InputError(ValueError):
    """Raised when a requested artifact cannot be read."""


@dataclass
class ValidationResult:
    mode: str
    final_status: str
    summary: str
    pass_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    human_review_items: list[str] = field(default_factory=list)
    unknown_items: list[str] = field(default_factory=list)

    def exit_code(self) -> int:
        return EXIT_CODES[self.final_status]

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "final_status": self.final_status,
            "summary": self.summary,
            "pass": self.pass_items,
            "blocked": self.blocked_items,
            "human_review": self.human_review_items,
            "unknown": self.unknown_items,
        }


REQUIRED_FIELDS = {
    "review": [
        "source_task_id",
        "source_evidence_report",
        "source_execution_report",
        "guard_results",
        "goal_result",
        "evidence_sufficiency",
        "NOT_RUN",
        "UNKNOWN",
        "BLOCKED",
        "new_gaps_found",
        "lessons_learned_created",
        "backlog_items_created",
        "next_task_candidates_created",
        "approval_claimed: false",
        "execution_authorized: false",
        "commit_authorized: false",
        "push_authorized: false",
        "next_task_started: false",
        "human_review_required: true",
        "status: HUMAN_REVIEW_REQUIRED",
    ],
    "lessons": [
        "source_task_id",
        "source_evidence",
        "lesson_type",
        "problem_observed",
        "what_worked",
        "what_failed",
        "what_was_manual",
        "what_was_ambiguous",
        "recommendation",
        "requires_backlog_item",
        "approval_claimed: false",
        "status: DRAFT",
    ],
    "backlog_item": [
        "gap_id",
        "source_evidence",
        "problem",
        "impact",
        "affected_surface",
        "risk",
        "candidate_fix",
        "protected_or_canonical_impact",
        "requires_human_review",
        "recommended_next_step",
        "execution_authorized: false",
        "commit_authorized: false",
        "push_authorized: false",
        "status: DRAFT",
    ],
    "candidate": [
        "candidate_task_id",
        "source_backlog_item",
        "source_evidence",
        "candidate_goal",
        "candidate_scope",
        "out_of_scope",
        "proposed_risk_profile",
        "risk_profile_assigned_by: null",
        "execution_authorized: false",
        "commit_authorized: false",
        "push_authorized: false",
        "approval_claimed: false",
        "status: DRAFT",
    ],
}


def validate_review(path: str | Path) -> ValidationResult:
    return _validate_artifact("review", path)


def validate_lessons(path: str | Path) -> ValidationResult:
    return _validate_artifact("lessons", path)


def validate_backlog_item(path: str | Path) -> ValidationResult:
    return _validate_artifact("backlog_item", path)


def validate_next_task_candidate(path: str | Path) -> ValidationResult:
    return _validate_artifact("candidate", path)


def validate_chain(
    review_path: str | Path,
    lessons_path: str | Path,
    item_path: str | Path,
    candidate_path: str | Path,
) -> ValidationResult:
    results = [
        validate_review(review_path),
        validate_lessons(lessons_path),
        validate_backlog_item(item_path),
        validate_next_task_candidate(candidate_path),
    ]
    blocked: list[str] = []
    human_review: list[str] = []
    unknown: list[str] = []
    passed: list[str] = []
    for result in results:
        if result.final_status == PASS:
            passed.append(f"{result.mode}: PASS")
        blocked.extend(f"{result.mode}: {item}" for item in result.blocked_items)
        human_review.extend(f"{result.mode}: {item}" for item in result.human_review_items)
        unknown.extend(f"{result.mode}: {item}" for item in result.unknown_items)

    if human_review:
        return ValidationResult(
            mode="validate-chain",
            final_status=HUMAN_REVIEW_REQUIRED,
            summary="chain requires human review",
            pass_items=passed,
            blocked_items=blocked,
            human_review_items=human_review,
            unknown_items=unknown,
        )
    if unknown:
        return ValidationResult(
            mode="validate-chain",
            final_status=UNKNOWN_BLOCKED,
            summary="chain contains unknown state",
            pass_items=passed,
            blocked_items=blocked,
            unknown_items=unknown,
        )
    if blocked:
        return ValidationResult(
            mode="validate-chain",
            final_status=BLOCKED,
            summary="chain contains blocked artifact",
            pass_items=passed,
            blocked_items=blocked,
        )
    return ValidationResult(
        mode="validate-chain",
        final_status=PASS,
        summary="all evidence-to-backlog artifacts passed",
        pass_items=passed,
    )


def _validate_artifact(kind: str, path: str | Path) -> ValidationResult:
    artifact_path = _resolve_file(path)
    text = artifact_path.read_text(encoding="utf-8")
    blocked: list[str] = []
    human_review: list[str] = []
    unknown: list[str] = []
    passed: list[str] = []

    missing = _missing_required_fields(text, REQUIRED_FIELDS[kind])
    blocked.extend(f"missing required field: {field}" for field in missing)

    if _missing_source_evidence(kind, text):
        blocked.append("missing source evidence reference")

    blocked.extend(_find_blocked_semantics(kind, text))
    human_review.extend(_find_human_review_semantics(kind, text))
    unknown.extend(_find_unknown_semantics(text))

    if human_review:
        return ValidationResult(
            mode=f"validate-{kind}",
            final_status=HUMAN_REVIEW_REQUIRED,
            summary="artifact requires human review",
            blocked_items=blocked,
            human_review_items=human_review,
            unknown_items=unknown,
        )
    if unknown:
        return ValidationResult(
            mode=f"validate-{kind}",
            final_status=UNKNOWN_BLOCKED,
            summary="artifact contains unknown state",
            blocked_items=blocked,
            unknown_items=unknown,
        )
    if blocked:
        return ValidationResult(
            mode=f"validate-{kind}",
            final_status=BLOCKED,
            summary="artifact violates evidence-to-backlog safety rules",
            blocked_items=blocked,
        )

    passed.append("required fields present")
    passed.append("no forbidden approval or authorization claims")
    return ValidationResult(
        mode=f"validate-{kind}",
        final_status=PASS,
        summary="artifact passed evidence-to-backlog validation",
        pass_items=passed,
    )


def _resolve_file(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.exists() or not candidate.is_file():
        raise InputError(f"file not found or unreadable: {candidate}")
    return candidate


def _missing_required_fields(text: str, fields: list[str]) -> list[str]:
    return [field for field in fields if field not in text]


def _missing_source_evidence(kind: str, text: str) -> bool:
    field = "source_evidence_report" if kind == "review" else "source_evidence"
    value = _field_value(text, field)
    return value is None or value == "" or value == "null"


def _find_blocked_semantics(kind: str, text: str) -> list[str]:
    claim_text = "\n".join(_claim_lines(text))
    lowered_claim_text = claim_text.lower()
    blocked: list[str] = []
    for field in [
        "approval_claimed",
        "execution_authorized",
        "commit_authorized",
        "push_authorized",
        "next_task_started",
    ]:
        if re.search(rf"(?im)^\s*{re.escape(field)}\s*:\s*true\s*$", text):
            blocked.append(f"forbidden true claim: {field}")

    if re.search(r"(?im)^\s*status\s*:\s*APPROVED\s*$", text):
        blocked.append("forbidden lifecycle status")
    if kind in {"candidate", "backlog_item", "lessons"}:
        status = _field_value(text, "status")
        if status is not None and status not in {"DRAFT"}:
            blocked.append(f"{kind} status must be DRAFT")
    if kind == "review":
        status = _field_value(text, "status")
        if status is not None and status != HUMAN_REVIEW_REQUIRED:
            blocked.append("review status must be HUMAN_REVIEW_REQUIRED")

    if "not_run" in lowered_claim_text and re.search(
        r"(?i)(not_run.*pass|all validation pass|validation pass)",
        claim_text,
    ):
        blocked.append("NOT_RUN treated as PASS")
    if "unknown" in lowered_claim_text and re.search(
        r"(?i)(unknowns? (are|is) (acceptable|ok)|unknown.* ok)",
        claim_text,
    ):
        blocked.append("UNKNOWN treated as OK")
    if re.search(r"(?i)evidence review.*approval|approval.*evidence review", claim_text):
        blocked.append("Evidence Review claiming approval")
    if re.search(r"(?i)lessons learned.*approval|approval.*lessons learned", claim_text):
        blocked.append("Lessons Learned claiming approval")
    if re.search(r"(?i)backlog item.*execution authorization|execution authorization.*backlog item", claim_text):
        blocked.append("Pipeline Hardening Backlog Item claiming execution authorization")
    if re.search(r"(?i)(approved[- ]task|candidate.*approval|approval.*candidate)", claim_text):
        blocked.append("Next Task Candidate claiming approved-task status")
    if re.search(r"(?i)validator pass.*approval|approval.*validator pass", claim_text):
        blocked.append("Validator PASS claimed as approval")
    return blocked


def _claim_lines(text: str) -> list[str]:
    claim_lines: list[str] = []
    ignored_prefixes = ("safety:", "why blocked:")
    ignored_tokens = ("≠", "!=", " cannot ", " must not ", " does not ", " not ")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        lowered = line.lower()
        if not line or lowered.startswith(ignored_prefixes):
            continue
        if any(token in lowered for token in ignored_tokens):
            continue
        claim_lines.append(line)
    return claim_lines


def _find_human_review_semantics(kind: str, text: str) -> list[str]:
    human_review: list[str] = []
    assigned_by = _field_value(text, "risk_profile_assigned_by")
    if kind == "candidate" and assigned_by not in {None, "", "null"}:
        if assigned_by.lower() not in {"human"}:
            human_review.append("Risk Profile assigned by non-human actor")
    return human_review


def _find_unknown_semantics(text: str) -> list[str]:
    if re.search(r"(?im)^\s*final_status\s*:\s*APPROVED\s*$", text):
        return ["forbidden final_status detected"]
    return []


def _field_value(text: str, field: str) -> str | None:
    match = re.search(rf"(?im)^[ \t]*{re.escape(field)}[ \t]*:[ \t]*([^\n]*)$", text)
    if not match:
        return None
    return match.group(1).strip()


def _print_result(result: ValidationResult) -> None:
    payload = result.to_dict()
    print(json.dumps(payload, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Evidence-to-Backlog artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    review_parser = subparsers.add_parser("validate-review")
    review_parser.add_argument("--review", required=True)

    lessons_parser = subparsers.add_parser("validate-lessons")
    lessons_parser.add_argument("--lessons", required=True)

    item_parser = subparsers.add_parser("validate-backlog-item")
    item_parser.add_argument("--item", required=True)

    candidate_parser = subparsers.add_parser("validate-next-task-candidate")
    candidate_parser.add_argument("--candidate", required=True)

    chain_parser = subparsers.add_parser("validate-chain")
    chain_parser.add_argument("--review", required=True)
    chain_parser.add_argument("--lessons", required=True)
    chain_parser.add_argument("--item", required=True)
    chain_parser.add_argument("--candidate", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "validate-review":
            result = validate_review(args.review)
        elif args.command == "validate-lessons":
            result = validate_lessons(args.lessons)
        elif args.command == "validate-backlog-item":
            result = validate_backlog_item(args.item)
        elif args.command == "validate-next-task-candidate":
            result = validate_next_task_candidate(args.candidate)
        elif args.command == "validate-chain":
            result = validate_chain(args.review, args.lessons, args.item, args.candidate)
        else:
            result = ValidationResult(
                mode="invalid-arguments",
                final_status=BLOCKED,
                summary="unsupported command",
                blocked_items=[str(args.command)],
            )
    except InputError as exc:
        result = ValidationResult(
            mode="input",
            final_status=BLOCKED,
            summary="input error",
            blocked_items=[str(exc)],
        )
    _print_result(result)
    return result.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
