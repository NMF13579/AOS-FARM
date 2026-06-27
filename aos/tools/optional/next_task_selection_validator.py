from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import argparse
import importlib.util
import json
import sys


PASS = "PASS"
BLOCKED = "BLOCKED"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"

EXIT_CODES = {
    PASS: 0,
    BLOCKED: 1,
    HUMAN_REVIEW_REQUIRED: 1,
    UNKNOWN_BLOCKED: 1,
}
ALLOWED_DECISIONS = {"ACCEPT", "CLARIFY", "DEFER", "REJECT", "REPLACE"}
REQUIRED_FIELDS = [
    "candidate_task_id",
    "candidate_source_file",
    "candidate_status",
    "selection_decision",
    "execution_authorized",
    "task_brief_authorized",
    "risk_profile_assigned_by_human",
    "next_task_started",
    "human_review_required",
    "final_status",
]


class InputError(ValueError):
    """Raised when a selection artifact cannot be read or parsed safely."""


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


def validate_selection(path: str | Path) -> ValidationResult:
    parser_module = _load_markdown_field_parser()
    parse_markdown_file = parser_module.parse_markdown_file

    selection_path = _resolve_file(path)
    raw_text = selection_path.read_text(encoding="utf-8")
    parsed = parse_markdown_file(selection_path, required_fields=REQUIRED_FIELDS)
    fields = parsed.fields

    blocked: list[str] = []
    human_review: list[str] = []
    unknown: list[str] = []
    passed: list[str] = []

    blocked.extend(
        f"missing required field: {field_name}"
        for field_name in parsed.missing_required_fields
    )

    decision = _normalized_string(fields.get("selection_decision"))
    candidate_status = _normalized_string(fields.get("candidate_status"))
    final_status = _normalized_string(fields.get("final_status"))
    approval_status = _normalized_string(fields.get("approval_status"))
    risk_profile_assigned_by = _normalized_string(fields.get("risk_profile_assigned_by"))

    if decision is None:
        blocked.append("selection_decision is required")
    elif decision not in ALLOWED_DECISIONS:
        blocked.append("selection_decision must be one of ACCEPT, CLARIFY, DEFER, REJECT, REPLACE")

    if candidate_status is None:
        blocked.append("candidate_status is required")
    elif candidate_status == "READY_FOR_EXECUTION":
        blocked.append("candidate_status must not be READY_FOR_EXECUTION")
    elif candidate_status != "DRAFT":
        blocked.append("candidate_status must be DRAFT")

    if _field_is_true(fields, "execution_authorized"):
        blocked.append("execution_authorized must be false")
    if _field_is_true(fields, "task_brief_authorized"):
        blocked.append("task_brief_authorized must be false")
    if _field_is_true(fields, "next_task_started"):
        blocked.append("next_task_started must be false")
    if _field_is_true(fields, "human_approval_simulated"):
        blocked.append("human_approval_simulated must be false")

    if risk_profile_assigned_by == "AGENT":
        blocked.append("risk_profile_assigned_by must not be agent")
    if _field_is_true(fields, "risk_profile_assigned_by_human"):
        blocked.append("risk_profile_assigned_by_human must be false until a separate human checkpoint exists")

    if final_status == "APPROVED":
        blocked.append("final_status must not be APPROVED")
    elif final_status is None:
        blocked.append("final_status is required")
    elif final_status != HUMAN_REVIEW_REQUIRED:
        blocked.append("final_status must be HUMAN_REVIEW_REQUIRED")

    if approval_status == "APPROVED":
        blocked.append("approval_status must not be APPROVED")

    if "UNKNOWN is OK" in raw_text:
        blocked.append("UNKNOWN must not be treated as OK")
    if "NOT_RUN is PASS" in raw_text:
        blocked.append("NOT_RUN must not be treated as PASS")
    if "PASS is approval" in raw_text:
        blocked.append("PASS must not be treated as approval")
    if "Evidence is approval" in raw_text:
        blocked.append("Evidence must not be treated as approval")
    if "CI PASS is approval" in raw_text:
        blocked.append("CI PASS must not be treated as approval")
    if "ACCEPT authorizes execution" in raw_text:
        blocked.append("ACCEPT must not be treated as execution authorization")
    if "ACCEPT assigns Risk Profile" in raw_text:
        blocked.append("ACCEPT must not be treated as Risk Profile assignment")
    if "ACCEPT starts the next task" in raw_text:
        blocked.append("ACCEPT must not be treated as next-task start")

    status_fields = parsed.status_fields
    if any(value == UNKNOWN_BLOCKED for value in status_fields.values()):
        unknown.extend(
            f"status field requires blocked unknown handling: {key}"
            for key, value in status_fields.items()
            if value == UNKNOWN_BLOCKED
        )

    if parsed.duplicate_keys:
        blocked.extend(f"duplicate key present: {key}" for key in parsed.duplicate_keys)

    if blocked:
        return ValidationResult(
            mode="validate-selection",
            final_status=BLOCKED,
            summary="selection artifact violates selection gate rules",
            blocked_items=blocked,
            human_review_items=human_review,
            unknown_items=unknown,
        )

    if unknown:
        return ValidationResult(
            mode="validate-selection",
            final_status=UNKNOWN_BLOCKED,
            summary="selection artifact contains unknown-blocked state",
            unknown_items=unknown,
        )

    if _field_is_true(fields, "human_review_required"):
        passed.append("selection artifact preserves human review boundary")
    else:
        blocked.append("human_review_required must be true")
        return ValidationResult(
            mode="validate-selection",
            final_status=BLOCKED,
            summary="selection artifact violates selection gate rules",
            blocked_items=blocked,
        )

    passed.append("required control fields present")
    passed.append("no forbidden approval, execution, or lifecycle claims")
    passed.append("selection decision stays review-only")

    return ValidationResult(
        mode="validate-selection",
        final_status=PASS,
        summary="selection artifact passed deterministic validation",
        pass_items=passed,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate next-task selection artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate-selection",
        help="Validate one next-task selection decision artifact",
    )
    validate_parser.add_argument("--selection", required=True, help="Path to the selection artifact")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "validate-selection":
            result = validate_selection(args.selection)
        else:
            raise InputError(f"unsupported command: {args.command}")
    except InputError as exc:
        print(json.dumps({"final_status": BLOCKED, "summary": str(exc)}, indent=2))
        return 2

    print(json.dumps(result.to_dict(), indent=2))
    return result.exit_code()


def _field_is_true(fields: dict[str, object], key: str) -> bool:
    return fields.get(key) is True


def _normalized_string(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if stripped == "":
        return None
    return stripped.upper()


def _resolve_file(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.exists() or not candidate.is_file():
        raise InputError(f"file not found or unreadable: {candidate}")
    return candidate


def _load_markdown_field_parser():
    module_path = Path(__file__).with_name("markdown_field_parser.py")
    spec = importlib.util.spec_from_file_location("aos_markdown_field_parser_core", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load markdown field parser module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(main())
