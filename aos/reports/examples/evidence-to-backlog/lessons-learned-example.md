---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Lessons Learned Example

## Status
source_task_id: GENERIC-TASK.EXAMPLE
source_evidence: reports/example-controlled-execution-evidence.md
lesson_type: workflow_gap
problem_observed: evidence review found a manual checklist that could be made clearer
what_worked: guard results and evidence boundaries were explicit
what_failed: follow-up hardening was not easy to capture in a consistent shape
what_was_manual: converting the finding into a backlog item
what_was_ambiguous: whether the finding should become a task or remain parked
recommendation: create a backlog item and a next-task candidate for human review
requires_backlog_item: true
approval_claimed: false
status: DRAFT

## Safety Boundary
- Evidence Review ≠ approval.
- Lessons Learned ≠ approval.
- Pipeline Hardening Backlog Item ≠ execution authorization.
- Next Task Candidate ≠ approved task.
- Validator PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Human unavailable for required decision → BLOCKED or HUMAN_REVIEW_REQUIRED.
