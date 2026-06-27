from __future__ import annotations

from pathlib import Path
import argparse
import importlib.util
import json
import re
import subprocess
import sys


UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"
CLOSED_REPORT_STATUSES = {"REMOTE_BASELINE_CLOSED", "CLOSED"}


class InputError(ValueError):
    """Raised when the scanner cannot read required local state."""


def scan_project_state(
    project_root: str | Path = ".",
    run_command=None,
) -> dict[str, object]:
    root = Path(project_root).resolve()
    if not root.exists():
        raise InputError(f"project root not found: {root}")

    command_runner = run_command or _run_command
    parser_module = _load_markdown_field_parser()
    parse_markdown_file = parser_module.parse_markdown_file

    branch = _safe_command(command_runner, ["git", "branch", "--show-current"])
    head = _safe_command(command_runner, ["git", "rev-parse", "HEAD"])
    origin_dev = _safe_command(command_runner, ["git", "rev-parse", "origin/dev"])
    ahead_behind = None
    remote_probe_status = None

    if origin_dev is None:
        remote_probe_status = UNKNOWN_BLOCKED
    else:
        ahead_behind = _safe_command(
            command_runner,
            ["git", "rev-list", "--left-right", "--count", "origin/dev...HEAD"],
        )
        if ahead_behind is None:
            remote_probe_status = UNKNOWN_BLOCKED

    latest_closed_task = _find_latest_441_report(root / "reports")
    latest_draft = root / "reports" / "aos-farm-441-7-dogfood-task-brief-draft.md"
    latest_candidate = None
    candidate_status = None
    next_required_action = "HUMAN_REVIEW_REQUIRED"

    if latest_draft.exists():
        latest_draft_fields = parse_markdown_file(latest_draft).fields
        latest_candidate = _string_or_none(latest_draft_fields.get("source_candidate"))
        draft_status = _string_or_none(latest_draft_fields.get("final_status"))
        if latest_candidate:
            candidate_file = root / latest_candidate
            if candidate_file.exists():
                candidate_fields = parse_markdown_file(candidate_file).fields
                candidate_status = _string_or_none(candidate_fields.get("status"))
        if draft_status == "HUMAN_REVIEW_REQUIRED":
            next_required_action = "HUMAN_REVIEW_TASK_BRIEF_DRAFT"
    elif latest_candidate is not None and candidate_status == "DRAFT":
        next_required_action = "HUMAN_SELECT_NEXT_CANDIDATE"

    return {
        "branch": branch,
        "head": head,
        "origin_dev": origin_dev,
        "ahead_behind": ahead_behind,
        "remote_probe_status": remote_probe_status,
        "latest_closed_task": latest_closed_task,
        "latest_candidate": latest_candidate,
        "candidate_status": candidate_status,
        "next_required_action": next_required_action,
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only project state scanner.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Print compact project state")
    status_parser.add_argument("--json", action="store_true", help="Print JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "status":
        raise InputError(f"unsupported command: {args.command}")

    state = scan_project_state()
    print(json.dumps(state, indent=2))
    return 0


def _run_command(command: list[str]) -> str:
    process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise InputError(process.stderr.strip() or process.stdout.strip() or "command failed")
    return process.stdout.strip()


def _safe_command(run_command, command: list[str]) -> str | None:
    try:
        value = run_command(command)
    except Exception:
        return None
    value = value.strip()
    return value or None


def _find_latest_441_report(reports_dir: Path) -> str | None:
    if not reports_dir.exists():
        return None
    latest: tuple[int, str] | None = None
    pattern = re.compile(r"aos-farm-441-(\d+)[^/]*report\.md$")
    for path in reports_dir.iterdir():
        match = pattern.match(path.name)
        if not match:
            continue
        if not _report_is_explicitly_closed(path):
            continue
        number = int(match.group(1))
        task_id = f"AOS-FARM.441.{number}"
        if latest is None or number > latest[0]:
            latest = (number, task_id)
    return None if latest is None else latest[1]


def _report_is_explicitly_closed(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    for status in CLOSED_REPORT_STATUSES:
        if f"final_status: {status}" in text:
            return True
    return False


def _string_or_none(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


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
