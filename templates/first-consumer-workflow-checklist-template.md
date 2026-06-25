---
version: draft-1
status: first consumer workflow checklist template
last_reviewed: 2026-06-25
lifecycle: "Template/reference. Use a fresh copy or embed checklist answers into the task report for each real task. This file is not approval and does not authorize execution, commit, push, release, or production use."
source_priority_note: "If this checklist conflicts with canonical sources 00/01/02, the canonical sources win."
---

# First Consumer Workflow Checklist

## Before Execution
- [ ] Task brief created from template.
- [ ] Allowed/forbidden scope explicitly defined.
- [ ] Human assigned Risk Profile.
- [ ] Human authorized execution.

## During Execution
- [ ] Agent adheres strictly to allowed file list.
- [ ] Agent stops and asks for clarification if ambiguous.

## After Execution
- [ ] Agent generates execution report.
- [ ] Agent generates verification report (confirming no boundary violations).

## Before Commit
- [ ] Human reviews verification report.
- [ ] Human updates Commit Checkpoint to `APPROVED_FOR_COMMIT`.
- [ ] Agent stages and commits ONLY the authorized files.

## Before Push
- [ ] Human reviews post-commit state.
- [ ] Human updates Push Checkpoint to `APPROVED_FOR_PUSH`.
- [ ] Agent pushes to remote.

## Final Closure
- [ ] Remote baseline closed.
- [ ] Agent generates final closure report.

## Stop Conditions (Fail-Closed)
Stop immediately if:
- [ ] Agent attempts to self-approve.
- [ ] Agent attempts to change canonical files without explicit protected authorization.
- [ ] Agent attempts to commit, push, or release autonomously.
- [ ] Unclear instructions cause ambiguity (`HUMAN_REVIEW_REQUIRED`).

## Checklist Lifecycle
- This file is a template/reference.
- A checked item is Evidence, not approval.
- The checklist does not replace Human Checkpoint.
- The checklist does not authorize execution, commit, push, release, protected/canonical changes, or production use.
