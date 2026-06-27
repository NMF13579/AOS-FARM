# Post-Execution Review Template

Use this template after Evidence Review to decide what should be learned from a
completed controlled task. This review does not approve work, authorize
execution, authorize commit, authorize push, authorize merge, authorize
release, assign a Risk Profile, or start the next task.

## Status
source_task_id:
source_evidence_report:
source_execution_report:
guard_results:
  precheck:
  scopecheck:
  postcheck:
goal_result:
evidence_sufficiency:
approval_claimed: false
execution_authorized: false
commit_authorized: false
push_authorized: false
next_task_started: false
human_review_required: true
status: HUMAN_REVIEW_REQUIRED

## Review Findings
NOT_RUN:

UNKNOWN:

BLOCKED:

new_gaps_found:

lessons_learned_created:

backlog_items_created:

next_task_candidates_created:

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
Stop at human review unless a human explicitly authorizes a later lifecycle
transition in a separate checkpoint.
