# AOS-FARM.314 — First Consumer Workflow Dogfood Report

## Usability Findings
- **Could a first user understand what to do?** Yes, the `docs/user-guide/first-consumer-workflow.md` explicitly lists a 10-step process that requires creating a task brief from a template.
- **Could a first user find the right template?** Yes, the workflow doc points directly to `templates/first-controlled-task-brief-template.md`.
- **Could a first user understand what needs human approval?** Yes, the template clearly highlights sections like `Human Risk Profile Assignment` and explicit statements that `Commit and Push require explicit, separate Human Checkpoints.`
- **Could a first user avoid accidental commit/push/release?** Yes, the `aos-farm-core-loop-ready.md` explicitly warns against self-approval and explicitly forbids agent autonomy.
- **Where would a non-programmer likely get confused?** A non-programmer might struggle with terms like "canonical sources" or the difference between local staging and pushing to a remote branch, though the workflow document breaks it down into simple steps.
- **Did the workflow avoid runner/autonomy assumptions?** Yes, the documents clearly state the agent cannot execute without a human-in-the-loop and runner autonomy is strictly disabled.
