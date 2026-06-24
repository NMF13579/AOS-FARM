# Thin Task Queue Helper

## What is the Helper?
The `task_queue_helper.py` is a minimal, dry-run CLI tool that reads Markdown files in the task queue and helps validate them.

## Why it exists
A manual queue requires strict adherence to templates and transition rules. Humans or Agent Tutors can make mistakes. The helper provides an automated way to **check** rules without giving an agent the power to **execute** them.

## How to run it
```bash
python agentos/scripts/task_queue_helper.py --task <path_to_task.md> --mode dry-run
```

Allowed modes:
- `dry-run`: Validates the task and outputs a status.
- `validate`: Alias for dry-run.
- `next-safe-step`: Summarizes what should happen next.
- `generate-handoff`: Creates a draft handoff package (requires `--output`).
- `generate-verification`: Creates a draft verification checklist (requires `--output`).

## What it CANNOT do
- It cannot execute the task.
- It cannot update the status field in the Markdown file.
- It cannot commit or push.
- It cannot launch agents.

## Why Dry-Run PASS is not Approval
A `HELPER_DRY_RUN_PASS` only means the Markdown file is formatted correctly and doesn't violate any transition rules. It **does not** mean the execution is approved. The human must still explicitly approve execution/commit/push.
