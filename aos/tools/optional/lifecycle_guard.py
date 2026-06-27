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

COMMIT_REQUIRED_FIELDS = [
    "checkpoint_type",
    "commit_authorized",
    "human_decision_required",
    "commit_performed",
    "push_performed",
    "merge_performed",
    "release_performed",
    "next_task_started",
]
PUSH_REQUIRED_FIELDS = [
    "checkpoint_type",
    "push_authorized",
    "human_decision_required",
    "force_push_authorized",
    "tag_push_authorized",
    "merge_authorized",
    "release_authorized",
    "next_task_authorized",
    "push_performed",
]


class InputError(ValueError):
    """Raised when a lifecycle checkpoint artifact cannot be read safely."""


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


def validate_commit_checkpoint(path: str | Path) -> ValidationResult:
    return _validate_checkpoint("commit", path)


def validate_push_checkpoint(path: str | Path) -> ValidationResult:
    return _validate_checkpoint("push", path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate lifecycle commit/push human checkpoint artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commit_parser = subparsers.add_parser(
        "validate-commit-checkpoint",
        help="Validate one commit authorization checkpoint artifact",
    )
    commit_parser.add_argument("--checkpoint", required=True, help="Path to the commit checkpoint artifact")

    push_parser = subparsers.add_parser(
        "validate-push-checkpoint",
        help="Validate one push authorization checkpoint artifact",
    )
    push_parser.add_argument("--checkpoint", required=True, help="Path to the push checkpoint artifact")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "validate-commit-checkpoint":
            result = validate_commit_checkpoint(args.checkpoint)
        elif args.command == "validate-push-checkpoint":
            result = validate_push_checkpoint(args.checkpoint)
        else:
            raise InputError(f"unsupported command: {args.command}")
    except InputError as exc:
        print(json.dumps({"final_status": BLOCKED, "summary": str(exc)}, indent=2))
        return 2

    print(json.dumps(result.to_dict(), indent=2))
    return result.exit_code()


def _validate_checkpoint(kind: str, path: str | Path) -> ValidationResult:
    parser_module = _load_markdown_field_parser()
    parse_markdown_file = parser_module.parse_markdown_file

    checkpoint_path = _resolve_file(path)
    raw_text = checkpoint_path.read_text(encoding="utf-8")
    required_fields = COMMIT_REQUIRED_FIELDS if kind == "commit" else PUSH_REQUIRED_FIELDS
    parsed = parse_markdown_file(checkpoint_path, required_fields=required_fields)
    fields = parsed.fields

    blocked: list[str] = []
    unknown: list[str] = []
    passed: list[str] = []

    blocked.extend(
        f"missing required field: {field_name}"
        for field_name in parsed.missing_required_fields
    )
    if parsed.duplicate_keys:
        blocked.extend(f"duplicate key present: {key}" for key in parsed.duplicate_keys)

    checkpoint_type = _normalized_string(fields.get("checkpoint_type"))
    approval_status = _normalized_string(fields.get("approval_status"))

    if _field_is_true(fields, "human_approval_simulated"):
        blocked.append("human_approval_simulated must be false")
    if _field_is_true(fields, "force_push_performed"):
        blocked.append("force_push_performed must be false")
    if _field_is_true(fields, "tag_push_performed"):
        blocked.append("tag_push_performed must be false")
    if _field_is_true(fields, "merge_performed"):
        blocked.append("merge_performed must be false")
    if _field_is_true(fields, "release_performed"):
        blocked.append("release_performed must be false")
    if _field_is_true(fields, "next_task_started"):
        blocked.append("next_task_started must be false")

    if approval_status == "APPROVED":
        blocked.append("approval_status must not be APPROVED")

    if "UNKNOWN is OK" in raw_text:
        blocked.append("UNKNOWN must not be treated as OK")
    if "NOT_RUN is PASS" in raw_text:
        blocked.append("NOT_RUN must not be treated as PASS")
    if "PASS is approval" in raw_text:
        blocked.append("PASS must not be treated as approval")

    if kind == "commit":
        if checkpoint_type != "COMMIT_AUTHORIZATION":
            blocked.append("checkpoint_type must be commit_authorization")
        if not _field_is_true(fields, "commit_authorized"):
            blocked.append("commit_authorized must be true")
        if _field_is_true(fields, "human_decision_required"):
            blocked.append("human_decision_required must be false when commit authorization is expected")
        if _field_is_true(fields, "commit_performed"):
            blocked.append("commit_performed must be false")
        if _field_is_true(fields, "push_performed"):
            blocked.append("push_performed must be false")
    else:
        if checkpoint_type != "PUSH_AUTHORIZATION":
            blocked.append("checkpoint_type must be push_authorization")
        if not _field_is_true(fields, "push_authorized"):
            blocked.append("push_authorized must be true")
        if _field_is_true(fields, "human_decision_required"):
            blocked.append("human_decision_required must be false when push authorization is expected")
        if _field_is_true(fields, "force_push_authorized"):
            blocked.append("force_push_authorized must be false")
        if _field_is_true(fields, "tag_push_authorized"):
            blocked.append("tag_push_authorized must be false")
        if _field_is_true(fields, "merge_authorized"):
            blocked.append("merge_authorized must be false")
        if _field_is_true(fields, "release_authorized"):
            blocked.append("release_authorized must be false")
        if _field_is_true(fields, "next_task_authorized"):
            blocked.append("next_task_authorized must be false")
        if _field_is_true(fields, "push_performed"):
            blocked.append("push_performed must be false")

    status_fields = parsed.status_fields
    if any(value == UNKNOWN_BLOCKED for value in status_fields.values()):
        unknown.extend(
            f"status field requires blocked unknown handling: {key}"
            for key, value in status_fields.items()
            if value == UNKNOWN_BLOCKED
        )

    if blocked:
        return ValidationResult(
            mode=f"validate-{kind}-checkpoint",
            final_status=BLOCKED,
            summary="lifecycle checkpoint violates commit/push authorization rules",
            blocked_items=blocked,
            unknown_items=unknown,
        )

    if unknown:
        return ValidationResult(
            mode=f"validate-{kind}-checkpoint",
            final_status=UNKNOWN_BLOCKED,
            summary="lifecycle checkpoint contains unknown-blocked state",
            unknown_items=unknown,
        )

    passed.append("required checkpoint fields present")
    passed.append("authorization flags match review-only lifecycle rules")
    passed.append("no forbidden approval, force-push, merge, release, or next-task claims")
    return ValidationResult(
        mode=f"validate-{kind}-checkpoint",
        final_status=PASS,
        summary="lifecycle checkpoint passed deterministic validation",
        pass_items=passed,
    )


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
