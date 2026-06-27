# AOS Project Map

The `aos/` directory is designed to be a self-contained kit.

- `aos/root/`: Contains templates for files that belong in your project root (like `AGENTS.md`).
- `aos/docs/`: Core framework documentation and user guides.
- `aos/templates/`: Blank templates for tasks, checkpoints, and reports.
- `aos/prompts/`: Standardized system and tutor prompts.
- `aos/reports/examples/`: Sample workflow artifacts such as controlled execution guard example fixtures.
- `aos/reports/`: Default directory for execution reports.
- `aos/config/`: Policies and configuration for the framework.
- `aos/tools/`: Safe, dry-run utility scripts.

Typical user path:

`README -> START_HERE -> aos/START_HERE -> Problem Intake -> Technical Assignment -> Task Breakdown -> Controlled Task Brief -> Human Execution Authorization -> Controlled Execution Guard -> Execution / Evidence Review -> Evidence-to-Backlog Loop -> Human Review`

The Evidence-to-Backlog Loop is documented at `aos/docs/workflow/evidence-to-backlog-loop.md`.
It records lessons learned and follow-up candidates after evidence review, but it does not approve work or authorize the next task.
