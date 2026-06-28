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
        
    if args.command == "validate":
        res = task_registry_validator.validate_registry_queue(registry_text, queue_text)
        print(json.dumps(res, indent=2))
        if not res.get("ok"):
            sys.exit(1)
            
    elif args.command == "summary":
        res = task_registry_validator.summarize_registry_queue(registry_text, queue_text)
        summary = res.get("summary", {})
        total = sum(summary.values())
        out = {
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
                "selected_task_id": task.get("task_id"),
                "selected_queue_item_id": qid,
                "next_action": task.get("next_action"),
                "execution_authorized": task.get("execution_authorized", False),
                "final_status": res.get("final_status", "HUMAN_REVIEW_REQUIRED") if not res.get("ok") else task.get("final_status", "PASS"),
                "invariants": {
                    "queue_position_is_not_approval": True,
                    "show_next_is_not_execution": True,
                    "show_current_is_not_execution": True
                }
            }
        else:
            out = {
                "selected_task_id": None,
                "selected_queue_item_id": None,
                "final_status": res.get("final_status", "BLOCKED"),
                "invariants": {
                    "queue_position_is_not_approval": True,
                    "show_next_is_not_execution": True,
                    "show_current_is_not_execution": True
                }
            }
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
