#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aos.scripts.aos_task_document_check import calculate_queue, load_all_tasks, select_next_candidate


def _load_module():
    script_path = Path(__file__).resolve()
    module_path = script_path.parent.parent / "tools" / "optional" / "next_task_selection_validator.py"
    spec = importlib.util.spec_from_file_location("aos_next_task_selection_validator_core", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load next-task selection validator module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def reconciliation_snapshot() -> dict[str, object]:
    tasks = load_all_tasks("tasks")
    queue = calculate_queue(tasks)
    candidate = select_next_candidate(queue)
    ranked_first = queue[0] if queue else None
    ranked_first_task_id = ranked_first.get("task_id") if ranked_first else None
    candidate_task_id = candidate.get("task_id") if candidate else None
    selection_status = "RECONCILED" if ranked_first_task_id == candidate_task_id else "RECONCILED_WITH_SKIPPED_NON_CANDIDATE"
    final_status = "HUMAN_REVIEW_REQUIRED" if candidate_task_id else "UNKNOWN_BLOCKED"

    return {
        "mode": "read_only_lifecycle_reconciliation",
        "final_status": final_status,
        "selection_status": selection_status,
        "ranked_first_task_id": ranked_first_task_id,
        "next_candidate": candidate_task_id,
        "candidate_queue_status": candidate.get("queue_status") if candidate else None,
        "candidate_lifecycle_status": candidate.get("status") if candidate else None,
        "approval_claimed": False,
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "release_authorized": False,
        "boundary_note": "Derived read-only reconciliation only. Task files remain Source of Truth. Next candidate is not approval or execution authorization.",
    }

def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv == ["--json"]:
        print(json.dumps(reconciliation_snapshot(), indent=2))
        return 0

    module = _load_module()
    return module.main(argv)


if __name__ == "__main__":
    sys.exit(main())
