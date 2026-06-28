#!/usr/bin/env python3
import sys
import os
import json
import argparse
from pathlib import Path

# Add project root to sys.path to allow importing aos module
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from aos.tools.optional import task_registry_validator

def print_invariants():
    print("WARNING: PASS ≠ approval.", file=sys.stderr)
    print("WARNING: Evidence ≠ approval.", file=sys.stderr)
    print("WARNING: Queue position ≠ approval.", file=sys.stderr)
    print("WARNING: Next Task Candidate ≠ approved task.", file=sys.stderr)
    print("WARNING: UNKNOWN is treated as BLOCKED.", file=sys.stderr)
    print("WARNING: NOT_RUN is not PASS.", file=sys.stderr)
    print("WARNING: Risk Profile must not be self-assigned by the agent.", file=sys.stderr)
    print("WARNING: This helper is read-only. It does not authorize execution, approve tasks, assign Risk Profiles, or start tasks.", file=sys.stderr)
    print("", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Read-only Inspection CLI for Task Registry and Queue")
    parser.add_argument("command", choices=["validate", "summary", "show-current", "show-next"])
    parser.add_argument("--registry", required=True, help="Path to registry markdown file")
    parser.add_argument("--queue", required=True, help="Path to queue markdown file")

    args = parser.parse_args()

    try:
        with open(args.registry, "r", encoding="utf-8") as f:
            registry_text = f.read()
    except Exception as e:
        print(json.dumps({"ok": False, "final_status": "BLOCKED", "errors": [f"Failed to read registry: {e}"], "warnings": []}))
        sys.exit(1)

    try:
        with open(args.queue, "r", encoding="utf-8") as f:
            queue_text = f.read()
    except Exception as e:
        print(json.dumps({"ok": False, "final_status": "BLOCKED", "errors": [f"Failed to read queue: {e}"], "warnings": []}))
        sys.exit(1)

    print_invariants()

    if args.command == "validate":
        res = task_registry_validator.validate_registry_queue(registry_text, queue_text)
        res["status"] = res.get("final_status", "UNKNOWN")
        res["approval_required"] = True
        res["execution_authorized"] = False
        res["commit_authorized"] = False
        res["push_authorized"] = False
        res["release_authorized"] = False
        res["candidate_only"] = False
        res["unknown_items"] = sum(1 for e in res.get("errors", []) if "UNKNOWN" in e)
        res["not_run_items"] = sum(1 for w in res.get("warnings", []) if "NOT_RUN" in w)
        res["invalid_transitions"] = sum(1 for e in res.get("errors", []) if "invalid transition" in e)
        res["approval_boundary_violations"] = sum(1 for e in res.get("errors", []) if "READY_FOR_EXECUTION" in e)

        print(json.dumps(res, indent=2))
        if not res.get("ok"):
            sys.exit(1)

    elif args.command == "summary":
        res = task_registry_validator.summarize_registry_queue(registry_text, queue_text)
        summary = res.get("summary", {})
        total = sum(summary.values())
        out = {
            "status": "PASS",
            "warnings": res.get("warnings", []),
            "approval_required": True,
            "execution_authorized": False,
            "commit_authorized": False,
            "push_authorized": False,
            "release_authorized": False,
            "candidate_only": False,
            "total_tasks": total,
            "closed": summary.get("CLOSED", 0),
            "queued": summary.get("QUEUED", 0),
            "blocked": summary.get("BLOCKED", 0),
            "deferred": summary.get("DEFERRED", 0),
            "replaced": summary.get("REPLACED", 0)
        }
        print(json.dumps(out, indent=2))

    elif args.command in ("show-current", "show-next"):
        if args.command == "show-current":
            res = task_registry_validator.select_current_task(registry_text, queue_text)
        else:
            res = task_registry_validator.select_next_task(registry_text, queue_text)

        task = res.get("task")
        if task:
            queue_data = task_registry_validator.parse_markdown_yaml(queue_text)
            queue_items = queue_data.get("queue_items", [])
            qid = None
            for q in queue_items:
                if q.get("task_id") == task.get("task_id"):
                    qid = q.get("queue_item_id")
                    break

            out = {
                "status": res.get("final_status", "HUMAN_REVIEW_REQUIRED") if not res.get("ok") else task.get("final_status", "PASS"),
                "warnings": res.get("warnings", []),
                "selected_task_id": task.get("task_id"),
                "selected_queue_item_id": qid,
                "next_action": task.get("next_action"),
                "approval_required": True,
                "execution_authorized": task.get("execution_authorized", False),
                "commit_authorized": False,
                "push_authorized": False,
                "release_authorized": False,
                "candidate_only": True,
                "invariants": {
                    "queue_position_is_not_approval": True,
                    "show_next_is_not_execution": True,
                    "show_current_is_not_execution": True,
                    "next_candidate_is_not_approved": True
                }
            }
        else:
            out = {
                "status": res.get("final_status", "BLOCKED"),
                "warnings": res.get("warnings", []),
                "selected_task_id": None,
                "selected_queue_item_id": None,
                "approval_required": True,
                "execution_authorized": False,
                "commit_authorized": False,
                "push_authorized": False,
                "release_authorized": False,
                "candidate_only": True,
                "invariants": {
                    "queue_position_is_not_approval": True,
                    "show_next_is_not_execution": True,
                    "show_current_is_not_execution": True,
                    "next_candidate_is_not_approved": True
                }
            }
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
