import argparse
import datetime
import json
import subprocess
import sys
import os

SCHEMA_VERSION = "1.0"
PROJECT = "AOS-FARM"

def main():
    parser = argparse.ArgumentParser(description="AOS Handoff Summary Helper")
    parser.add_argument("--markdown", action="store_true", help="Output in Markdown format")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--compact", action="store_true", help="Compact output mode")
    parser.add_argument("--summary", action="store_true", help="Summary output mode")
    parser.add_argument("--write", help="Write Markdown to a file under reports/")
    parser.add_argument("--task-id", help="Task ID for semantic context")
    parser.add_argument("--stage-title", help="Stage title for semantic context")
    parser.add_argument("--context", help="Additional semantic context")
    args = parser.parse_args()

    if not args.json and not args.markdown and not args.write:
        args.markdown = True

    if args.write:
        write_path = os.path.abspath(args.write)
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "reports"))
        if not write_path.startswith(reports_dir):
            if args.json:
                print(json.dumps({"analysis_status": "BLOCKED", "reason": "output path outside reports/"}))
            else:
                print("analysis_status: BLOCKED\nreason: output path outside reports/")
            sys.exit(0)

    # Reuse lifecycle_status script to get baseline info
    lifecycle_data = {}
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lifecycle_script = os.path.join(base_dir, "aos_lifecycle_status.py")
        res = subprocess.run([sys.executable, lifecycle_script, "--json"], capture_output=True, text=True, check=True)
        lifecycle_data = json.loads(res.stdout)
    except Exception as e:
        pass

    notes = [
        "Generated summary.",
        "Not Source of Truth.",
        "Not approval.",
        "Not execution authorization.",
        "Not commit authorization.",
        "Not push authorization.",
        "UNKNOWN is not OK.",
        "NOT_RUN is not PASS.",
        "PASS is not approval.",
        "Evidence is not approval.",
        "Local trace boundary: /.aos-tmp/logs/ is local-only, ignored, disposable, not Evidence, not approval, not Source of Truth."
    ]

    analysis_status = "HANDOFF_COLLECTED"

    data = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": PROJECT,
        "current_state": lifecycle_data.get("branch", "UNKNOWN"),
        "last_completed_work": lifecycle_data.get("last_completed_task", "UNKNOWN"),
        "what_was_done": ["Collected handoff summary"],
        "what_was_not_done": [],
        "evidence_reports": [],
        "validation_snapshot": "NOT_RUN",
        "open_unknowns": lifecycle_data.get("open_unknowns", []),
        "current_workspace": lifecycle_data.get("working_tree", "UNKNOWN"),
        "next_safe_step": "Human Checkpoint",
        "forbidden_actions": ["Commit", "Push", "Merge", "Release", "Mutate Lifecycle"],
        "human_checkpoint_required": "Yes",
        "analysis_status": analysis_status,
        "notes": notes
    }

    if args.task_id:
        data["task_id"] = args.task_id
    if args.stage_title:
        data["stage_title"] = args.stage_title
    if args.context:
        data["semantic_context"] = args.context

    markdown_out = f"# AOS Handoff Summary\n\n"

    if args.task_id or args.stage_title or args.context:
        markdown_out += "## Semantic Context\n"
        if args.task_id:
            markdown_out += f"- Task ID: {args.task_id}\n"
        if args.stage_title:
            markdown_out += f"- Stage: {args.stage_title}\n"
        if args.context:
            markdown_out += f"- Context: {args.context}\n"
        markdown_out += "\n"

    markdown_out += f"""## Current State
{data['current_state']}

## Last Completed Work
{data['last_completed_work']}

## What Was Done
- {data['what_was_done'][0]}

## What Was Not Done
No execution

## Evidence / Reports
None

## Validation Snapshot
{data['validation_snapshot']}

## Open UNKNOWNs
None

## Current Workspace
```
{data['current_workspace']}
```

## Next Safe Step
{data['next_safe_step']}

## Forbidden Actions
{', '.join(data['forbidden_actions'])}

## Human Checkpoint Required
{data['human_checkpoint_required']}

## Safety Notes
"""
    for n in data['notes']:
        markdown_out += f"- {n}\n"

    markdown_out += f"\n## Analysis Status\n**{data['analysis_status']}**\n"
    markdown_out += "\nGenerated handoff summary is not approval.\n"
    markdown_out += "Generated handoff summary is not Source of Truth.\n"
    markdown_out += "Semantic context is not Source of Truth.\n"

    if args.compact:
        compact_out = f"**AOS Handoff: {data['analysis_status']}**\n"
        if args.task_id:
            compact_out += f"Task: {args.task_id}\n"
        compact_out += f"State: {data['current_state']}\n"
        compact_out += f"Done: {data['what_was_done'][0]}\n"
        compact_out += f"Next: {data['next_safe_step']}\n"
        compact_out += "Safety Notes:\n"
        for n in data['notes']:
            compact_out += f"- {n}\n"
        markdown_out = compact_out

    if args.summary:
        summary_out = f"# AOS Handoff Summary: {data['analysis_status']}\n\n"
        if args.task_id or args.stage_title or args.context:
            summary_out += "## Semantic Context\n"
            if args.task_id:
                summary_out += f"- Task ID: {args.task_id}\n"
            if args.stage_title:
                summary_out += f"- Stage: {args.stage_title}\n"
            if args.context:
                summary_out += f"- Context: {args.context}\n"
            summary_out += "\n"
        summary_out += f"**State:** {data['current_state']}\n"
        summary_out += f"**Done:** {data['what_was_done'][0]}\n"
        summary_out += f"**Next Safe Step:** {data['next_safe_step']}\n"
        summary_out += "\n**Forbidden Actions:** " + ", ".join(data['forbidden_actions']) + "\n"
        summary_out += "\n**Safety Notes:**\n"
        for n in data['notes']:
            summary_out += f"- {n}\n"
        markdown_out = summary_out

    if args.json:
        print(json.dumps(data, indent=2))
    if args.markdown:
        print(markdown_out)

    if args.write:
        with open(args.write, "w") as f:
            f.write(markdown_out)
        print(f"Wrote handoff summary to {args.write}")

if __name__ == '__main__':
    main()
