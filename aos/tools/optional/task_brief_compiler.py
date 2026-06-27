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
REQUIRED_CANDIDATE_FIELDS = [
    "candidate_task_id",
    "candidate_goal",
    "candidate_scope",
    "out_of_scope",
    "allowed_files",
    "forbidden_files",
    "validation_plan",
    "proposed_risk_profile",
    "status",
]


class InputError(ValueError):
    """Raised when the compiler receives unreadable file inputs."""


@dataclass
class CompilationResult:
    mode: str
    final_status: str
    summary: str
    output_path: str | None = None
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
            "output_path": self.output_path,
            "pass": self.pass_items,
            "blocked": self.blocked_items,
            "human_review": self.human_review_items,
            "unknown": self.unknown_items,
        }


def compile_task_brief(
    candidate_path: str | Path,
    selection_path: str | Path,
    output_path: str | Path,
) -> CompilationResult:
    parser_module = _load_module("markdown_field_parser.py", "aos_markdown_field_parser_core")
    validator_module = _load_module(
        "next_task_selection_validator.py",
        "aos_next_task_selection_validator_core",
    )

    parse_markdown_file = parser_module.parse_markdown_file
    validate_selection = validator_module.validate_selection

    candidate_file = _resolve_file(candidate_path)
    selection_file = _resolve_file(selection_path)
    output_file = Path(output_path)

    candidate_raw = candidate_file.read_text(encoding="utf-8")
    selection_raw = selection_file.read_text(encoding="utf-8")
    candidate_parsed = parse_markdown_file(candidate_file, required_fields=REQUIRED_CANDIDATE_FIELDS)
    selection_result = validate_selection(selection_file)

    blocked: list[str] = []
    human_review: list[str] = []
    unknown: list[str] = []
    passed: list[str] = []

    blocked.extend(
        f"missing required candidate field: {field_name}"
        for field_name in candidate_parsed.missing_required_fields
    )
    if candidate_parsed.duplicate_keys:
        blocked.extend(f"duplicate candidate key present: {key}" for key in candidate_parsed.duplicate_keys)

    candidate_fields = candidate_parsed.fields
    candidate_status = _normalized_string(candidate_fields.get("status"))
    if candidate_status is None:
        blocked.append("candidate status is required")
    elif candidate_status != "DRAFT":
        blocked.append("candidate_status must be DRAFT")

    if selection_result.final_status != PASS:
        blocked.append(f"selection artifact must pass validator before compile: {selection_result.final_status}")

    selection_parsed = parse_markdown_file(selection_file)
    selection_fields = selection_parsed.fields
    selection_decision = _normalized_string(selection_fields.get("selection_decision"))
    if selection_decision is None:
        blocked.append("selection_decision is required")
    elif selection_decision != "ACCEPT":
        blocked.append("selection_decision must be ACCEPT for compile")

    if _field_is_true(selection_fields, "execution_authorized"):
        blocked.append("selection execution_authorized must be false")
    if _field_is_true(selection_fields, "task_brief_authorized"):
        blocked.append("selection task_brief_authorized must be false")
    if _field_is_true(selection_fields, "risk_profile_assigned_by_human"):
        blocked.append("selection risk_profile_assigned_by_human must be false")
    if _field_is_true(selection_fields, "next_task_started"):
        blocked.append("selection next_task_started must be false")
    if not _field_is_true(selection_fields, "human_review_required"):
        blocked.append("selection human_review_required must be true")

    selection_final_status = _normalized_string(selection_fields.get("final_status"))
    if selection_final_status != HUMAN_REVIEW_REQUIRED:
        blocked.append("selection final_status must be HUMAN_REVIEW_REQUIRED")

    if "ACCEPT authorizes execution" in selection_raw:
        blocked.append("selection artifact must not treat ACCEPT as execution authorization")
    if "ACCEPT assigns Risk Profile" in selection_raw:
        blocked.append("selection artifact must not treat ACCEPT as Risk Profile assignment")
    if "ACCEPT starts the next task" in selection_raw:
        blocked.append("selection artifact must not treat ACCEPT as next-task start")
    if "PASS is approval" in selection_raw:
        blocked.append("selection artifact must not treat PASS as approval")
    if "Evidence is approval" in selection_raw:
        blocked.append("selection artifact must not treat Evidence as approval")
    if "CI PASS is approval" in selection_raw:
        blocked.append("selection artifact must not treat CI PASS as approval")
    if "UNKNOWN is OK" in selection_raw:
        blocked.append("selection artifact must not treat UNKNOWN as OK")
    if "NOT_RUN is PASS" in selection_raw:
        blocked.append("selection artifact must not treat NOT_RUN as PASS")

    if "PASS is approval" in candidate_raw:
        blocked.append("candidate artifact must not treat PASS as approval")
    if "Evidence is approval" in candidate_raw:
        blocked.append("candidate artifact must not treat Evidence as approval")

    if blocked:
        return CompilationResult(
            mode="compile",
            final_status=BLOCKED,
            summary="task brief compilation blocked by precondition or boundary violations",
            blocked_items=blocked,
            human_review_items=human_review,
            unknown_items=unknown,
        )

    output_text = _build_task_brief_draft(
        candidate_file=candidate_file,
        selection_file=selection_file,
        candidate_fields=candidate_fields,
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(output_text, encoding="utf-8")

    passed.append("candidate remained DRAFT")
    passed.append("selection decision remained ACCEPT and review-only")
    passed.append("generated draft keeps execution, commit, push, and risk flags false")
    passed.append("generated draft ends at HUMAN_REVIEW_REQUIRED")

    return CompilationResult(
        mode="compile",
        final_status=PASS,
        summary="task brief draft compiled successfully",
        output_path=str(output_file),
        pass_items=passed,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile review-only Task Brief drafts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compile_parser = subparsers.add_parser("compile", help="Compile one candidate plus selection into a Task Brief draft")
    compile_parser.add_argument("--candidate", required=True, help="Path to the source next-task candidate")
    compile_parser.add_argument("--selection", required=True, help="Path to the ACCEPT selection artifact")
    compile_parser.add_argument("--output", required=True, help="Path to the output Task Brief draft")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "compile":
            result = compile_task_brief(args.candidate, args.selection, args.output)
        else:
            raise InputError(f"unsupported command: {args.command}")
    except InputError as exc:
        print(json.dumps({"final_status": BLOCKED, "summary": str(exc)}, indent=2))
        return 2

    print(json.dumps(result.to_dict(), indent=2))
    return result.exit_code()


def _build_task_brief_draft(
    candidate_file: Path,
    selection_file: Path,
    candidate_fields: dict[str, object],
) -> str:
    lines = [
        "# Compiled Task Brief Draft",
        "",
        "task_brief_draft_status: DRAFT",
        f"source_candidate: {candidate_file.as_posix()}",
        f"source_selection_decision: {selection_file.as_posix()}",
        f"candidate_goal: {_string_field(candidate_fields, 'candidate_goal')}",
        f"scope: {_string_field(candidate_fields, 'candidate_scope')}",
        f"out_of_scope: {_string_field(candidate_fields, 'out_of_scope')}",
        f"allowed_files: {_string_field(candidate_fields, 'allowed_files')}",
        f"forbidden_files: {_string_field(candidate_fields, 'forbidden_files')}",
        f"validation_plan: {_string_field(candidate_fields, 'validation_plan')}",
        f"proposed_risk_profile: {_string_field(candidate_fields, 'proposed_risk_profile')}",
        "risk_profile_assigned_by_human: false",
        "execution_authorized: false",
        "commit_authorized: false",
        "push_authorized: false",
        "human_review_required: true",
        "final_status: HUMAN_REVIEW_REQUIRED",
        "",
        "## Safety Boundary",
        "- This draft is review-only.",
        "- This draft is not executable until human review and explicit authorization.",
        "- This draft does not assign Risk Profile.",
        "- This draft does not authorize execution.",
        "- This draft does not authorize commit or push.",
        "- This draft does not start the next task.",
        "- PASS is validation result only, not approval.",
        "- Evidence is not approval.",
        "- CI PASS is not approval.",
        "- UNKNOWN is not OK.",
        "- NOT_RUN is not PASS.",
        "- Human approval cannot be simulated.",
    ]
    return "\n".join(lines) + "\n"


def _string_field(fields: dict[str, object], key: str) -> str:
    value = fields.get(key)
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


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


def _load_module(filename: str, module_name: str):
    module_path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(main())
