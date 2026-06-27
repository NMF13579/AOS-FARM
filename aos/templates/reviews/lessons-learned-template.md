# Lessons Learned Template

Use this template to record one lesson from a completed controlled task.
Lessons Learned are review material only. They do not approve work, authorize
execution, authorize commit, authorize push, authorize merge, authorize
release, assign a Risk Profile, or start the next task.

## Status
source_task_id:
source_evidence:
lesson_type:
problem_observed:
what_worked:
what_failed:
what_was_manual:
what_was_ambiguous:
recommendation:
requires_backlog_item:
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

## Next Safe Step
If this lesson implies future work, create or review a separate Pipeline
Hardening Backlog Item. Do not treat this lesson as authorization.
