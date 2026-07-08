#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aos.scripts.aos_task_document_check import calculate_queue, load_all_tasks, parse_yaml_frontmatter, select_next_candidate


VALID_LIFECYCLE_STATES = {
    "DRAFT",
    "READY_FOR_HUMAN_REVIEW",
    "READY_FOR_EXECUTION",
    "EXECUTION_REPORTED",
    "EVIDENCE_RECORDED",
    "HUMAN_REVIEW_REQUIRED",
    "APPROVED",
    "REJECTED",
    "CLOSED",
    "NEEDS_CHANGES",
    "BLOCKED",
    "UNKNOWN_BLOCKED",
    "NOT_RUN",
}


def run_git(args: list[str]) -> str:
    try:
        result = subprocess.run(["git"] + args, capture_output=True, text=True, timeout=10)
    except Exception:
        return "unknown"
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def repo_state() -> dict[str, Any]:
    status = run_git(["status", "--short", "--untracked-files=all"])
    if status == "unknown":
        clean: bool | str = "unknown"
    else:
        clean = status == ""
    return {
        "branch": run_git(["branch", "--show-current"]),
        "head": run_git(["rev-parse", "HEAD"]),
        "working_tree_clean": clean,
    }


def read_task(path: str | Path) -> tuple[dict[str, Any] | None, str | None]:
    task_path = Path(path)
    if not task_path.exists() or not task_path.is_file():
        return None, f"missing task: {task_path}"
    try:
        content = task_path.read_text(encoding="utf-8")
    except Exception as exc:
        return None, f"failed to read task: {exc}"
    data, _ = parse_yaml_frontmatter(content)
    if not data:
        return None, "missing or invalid task frontmatter"
    data["_filepath"] = str(task_path)
    return data, None


def normalize_validation_status(value: Any) -> str:
    if value == "NOT_RUN":
        return "NOT_RUN"
    if value in ("PASS", "VALIDATION_COMPLETE"):
        return "PASS"
    if value in ("FAIL", "FAILED", "BLOCKED"):
        return "FAIL"
    if value in (None, "", "UNKNOWN", "UNKNOWN_BLOCKED"):
        return "UNKNOWN_BLOCKED"
    return "UNKNOWN_BLOCKED"


def normalize_evidence_status(value: Any) -> str:
    if value == "NOT_RUN":
        return "NOT_RUN"
    if value in ("PRESENT", "EVIDENCE_COLLECTED", "RECORDED", "EVIDENCE_RECORDED"):
        return "PRESENT"
    if value in ("MISSING", "FAIL", "FAILED"):
        return "MISSING"
    if value in (None, "", "UNKNOWN", "UNKNOWN_BLOCKED"):
        return "UNKNOWN_BLOCKED"
    return "UNKNOWN_BLOCKED"


def risk_status(task: dict[str, Any] | None) -> str:
    if not task:
        return "UNKNOWN_BLOCKED"
    risk = task.get("risk_profile")
    assigned_by = task.get("risk_assigned_by") or task.get("risk_profile_assigned_by_human")
    if risk == "UNKNOWN_BLOCKED":
        return "UNKNOWN_BLOCKED"
    if not risk:
        return "MISSING"
    if assigned_by == "human" or task.get("risk_profile_assigned_by_human"):
        return "ASSIGNED_BY_HUMAN"
    if assigned_by in (None, "", "none"):
        return "MISSING"
    return "AMBIGUOUS"


def acceptance_status(task: dict[str, Any] | None) -> str:
    if not task:
        return "UNKNOWN_BLOCKED"
    approval = task.get("approval_status")
    if approval == "APPROVED":
        return "APPROVED"
    if approval == "REJECTED":
        return "REJECTED"
    if approval == "NEEDS_CHANGES":
        return "NEEDS_CHANGES"
    if approval in ("NOT_APPROVED", "NOT_REQUESTED", None, ""):
        return "NOT_REVIEWED"
    return "UNKNOWN_BLOCKED"


def explicit_next_conflicts(queue: list[dict[str, Any]]) -> list[dict[str, str]]:
    explicit_next = [
        task for task in queue
        if task.get("queue_status") == "NEXT" and task.get("status") not in {"BLOCKED", "CLOSED", "REJECTED"}
    ]
    if len(explicit_next) <= 1:
        return []
    return [
        {
            "source": "task_queue",
            "value": ", ".join(str(task.get("task_id")) for task in explicit_next),
            "reason": "multiple explicit queue_status NEXT candidates",
        }
    ]


def dashboard_signal(queue: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = select_next_candidate(queue)
    return {
        "source": "dashboard_shared_selector",
        "value": candidate.get("task_id") if candidate else None,
        "reason": "dashboard uses shared next-candidate boundary",
    }


def build_state(task_path: str | None = None) -> dict[str, Any]:
    tasks = load_all_tasks("tasks")
    queue = calculate_queue(tasks)
    queue_candidate = select_next_candidate(queue)
    conflicts = explicit_next_conflicts(queue)
    selection_reason: list[str] = []
    unknowns: list[str] = []
    blockers: list[str] = []

    dashboard = dashboard_signal(queue)
    queue_candidate_id = queue_candidate.get("task_id") if queue_candidate else None
    if dashboard["value"] != queue_candidate_id:
        conflicts.append({
            "source": "dashboard",
            "value": str(dashboard["value"]),
            "reason": f"dashboard disagrees with queue helper candidate {queue_candidate_id}",
        })

    ranked_first = queue[0] if queue else None
    if ranked_first and ranked_first.get("queue_status") == "DONE" and queue_candidate_id != ranked_first.get("task_id"):
        conflicts.append({
            "source": "ranked_queue",
            "value": str(ranked_first.get("task_id")),
            "reason": "ranked first task has queue_status DONE and was skipped as non-candidate",
        })
        selection_reason.append(f"skipped ranked first non-candidate {ranked_first.get('task_id')} with queue_status DONE")

    if task_path:
        task, read_error = read_task(task_path)
        if read_error:
            task = None
            unknowns.append(read_error)
            selection_status = "UNKNOWN_BLOCKED"
        else:
            selection_status = "SELECTED"
            selection_reason.append(f"explicit task path selected: {task_path}")
    else:
        task = queue_candidate
        if conflicts:
            selection_status = "CONFLICT" if not queue_candidate else "SELECTED"
        elif queue_candidate:
            selection_status = "SELECTED"
        elif queue:
            selection_status = "UNKNOWN_BLOCKED"
            unknowns.append("no eligible next task candidate")
        else:
            selection_status = "NONE"
        if queue_candidate:
            selection_reason.append("selected first ranked eligible task")

    if conflicts and not task:
        unknowns.append("selection conflict has no usable task candidate")

    task_id = task.get("task_id") if task else None
    path = task.get("_filepath") if task else None
    raw_state = task.get("status") if task else "UNKNOWN_BLOCKED"
    lifecycle_state = raw_state if raw_state in VALID_LIFECYCLE_STATES else "UNKNOWN_BLOCKED"

    if not task:
        blockers.append("missing_task")
    else:
        if risk_status(task) in {"MISSING", "AMBIGUOUS", "UNKNOWN_BLOCKED"}:
            blockers.append(f"risk_profile_status: {risk_status(task)}")
        if task.get("execution_authorized") is not True:
            blockers.append("execution_authorized is not true")
        if acceptance_status(task) != "APPROVED":
            blockers.append(f"acceptance_status: {acceptance_status(task)}")
        if normalize_validation_status(task.get("validator_status")) == "NOT_RUN":
            blockers.append("validator_status is NOT_RUN")
        if normalize_evidence_status(task.get("evidence_status")) == "NOT_RUN":
            blockers.append("evidence_status is NOT_RUN")
        if task.get("queue_status") == "DONE" and not task_path:
            blockers.append("DONE task cannot be current next candidate")

    if lifecycle_state == "READY_FOR_EXECUTION" and task and task.get("execution_authorized") is not True:
        lifecycle_state = "UNKNOWN_BLOCKED"
        unknowns.append("READY_FOR_EXECUTION without execution authorization")

    approval_granted = acceptance_status(task) == "APPROVED" if task else False
    execution_allowed = bool(task and task.get("execution_authorized") is True and approval_granted and not conflicts)

    result = {
        "schema_version": 1,
        "source": "aos_lifecycle_state",
        "repo_state": repo_state(),
        "current_task": {
            "id": task_id,
            "path": path,
            "selection_status": selection_status,
            "selection_reason": selection_reason,
        },
        "lifecycle": {
            "state": lifecycle_state,
            "blockers": blockers,
            "unknowns": unknowns,
        },
        "permissions": {
            "execution_allowed": execution_allowed,
            "approval_granted": approval_granted,
            "commit_allowed": bool(task and task.get("commit_authorized") is True and approval_granted),
            "push_allowed": bool(task and task.get("push_authorized") is True and approval_granted),
            "merge_allowed": bool(task and task.get("merge_authorized") is True and approval_granted),
            "release_allowed": bool(task and task.get("release_authorized") is True and approval_granted),
        },
        "evidence": {
            "validation_status": normalize_validation_status(task.get("validator_status") if task else None),
            "evidence_status": normalize_evidence_status(task.get("evidence_status") if task else None),
        },
        "human": {
            "risk_profile_status": risk_status(task),
            "execution_authorization_status": "AUTHORIZED" if task and task.get("execution_authorized") is True else "NOT_AUTHORIZED" if task else "UNKNOWN_BLOCKED",
            "acceptance_status": acceptance_status(task),
        },
        "conflicts": conflicts,
        "next_safe_action": "HUMAN_REVIEW_REQUIRED" if blockers or conflicts or unknowns else "READY_FOR_HUMAN_REVIEW",
    }
    return result


def render_text(state: dict[str, Any]) -> str:
    lines = [
        "=== AOS Lifecycle State ===",
        "Read-only interpreter. Not Source of Truth. Not approval.",
        f"Task: {state['current_task']['id']}",
        f"Selection: {state['current_task']['selection_status']}",
        f"Lifecycle: {state['lifecycle']['state']}",
        f"Execution Allowed: {state['permissions']['execution_allowed']}",
        f"Approval Granted: {state['permissions']['approval_granted']}",
        f"Commit Allowed: {state['permissions']['commit_allowed']}",
        f"Push Allowed: {state['permissions']['push_allowed']}",
        f"Next Safe Action: {state['next_safe_action']}",
        "",
        "Blockers:",
    ]
    lines.extend(f"- {item}" for item in state["lifecycle"]["blockers"] or ["none"])
    lines.append("Unknowns:")
    lines.extend(f"- {item}" for item in state["lifecycle"]["unknowns"] or ["none"])
    lines.append("Conflicts:")
    if state["conflicts"]:
        lines.extend(f"- {c['source']}: {c['value']} ({c['reason']})" for c in state["conflicts"])
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only AOS lifecycle state reconciler")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--json", action="store_true", help="Output JSON")
    mode.add_argument("--text", action="store_true", help="Output text")
    mode.add_argument("--explain", action="store_true", help="Explain reconciliation rules")
    mode.add_argument("--check-consistency", action="store_true", help="Check queue/dashboard/next-task consistency")
    parser.add_argument("--task", help="Task file to interpret directly")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.explain:
        print("Lifecycle Reconciler is read-only. Task files, registries, and canonical docs remain Source of Truth.")
        print("It selects the first ranked eligible task and fails closed on conflicts, UNKNOWN, NOT_RUN, or missing human decisions.")
        print("It does not approve, assign Risk Profile, authorize execution, create Evidence, commit, push, merge, or release.")
        return 0

    state = build_state(args.task)
    if args.check_consistency:
        print(json.dumps({
            "schema_version": 1,
            "source": "aos_lifecycle_state",
            "selection_status": state["current_task"]["selection_status"],
            "current_task": state["current_task"]["id"],
            "conflicts": state["conflicts"],
            "next_safe_action": state["next_safe_action"],
        }, indent=2))
        return 1 if state["current_task"]["selection_status"] in {"CONFLICT", "UNKNOWN_BLOCKED"} else 0

    if args.text:
        print(render_text(state), end="")
    else:
        print(json.dumps(state, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
