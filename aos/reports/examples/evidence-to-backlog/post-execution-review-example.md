---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Post-Execution Review Example

## Status
source_task_id: GENERIC-TASK.EXAMPLE
source_evidence_report: reports/example-controlled-execution-evidence.md
source_execution_report: reports/example-execution-report.md
guard_results:
  precheck: PASS
  scopecheck: PASS
  postcheck: PASS
goal_result: completed_with_reviewable_evidence
evidence_sufficiency: sufficient_for_human_review
approval_claimed: false
execution_authorized: false
commit_authorized: false
push_authorized: false
next_task_started: false
human_review_required: true
status: HUMAN_REVIEW_REQUIRED

## Review Findings
NOT_RUN:
- no CI check existed for this task

UNKNOWN:
- none

BLOCKED:
- none

new_gaps_found:
- evidence review used manual checklist steps

lessons_learned_created:
- lessons-learned-example.md

backlog_items_created:
- pipeline-hardening-backlog-item-example.md

next_task_candidates_created:
- next-task-candidate-example.md

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
