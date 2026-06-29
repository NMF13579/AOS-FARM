---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Valid Post-Execution Review Fixture

expected_result: HUMAN_REVIEW_REQUIRED

source_task_id: GENERIC-TASK.FIXTURE
source_evidence_report: reports/fixture-evidence.md
source_execution_report: reports/fixture-execution.md
guard_results:
  precheck: PASS
  scopecheck: PASS
  postcheck: PASS
goal_result: completed
evidence_sufficiency: sufficient_for_human_review
NOT_RUN:
- markdown linter
UNKNOWN:
- none
BLOCKED:
- none
new_gaps_found:
- manual review step should be templated
lessons_learned_created:
- fixtures/valid/lessons-learned.md
backlog_items_created:
- fixtures/valid/backlog-item.md
next_task_candidates_created:
- fixtures/valid/next-task-candidate.md
approval_claimed: false
execution_authorized: false
commit_authorized: false
push_authorized: false
next_task_started: false
human_review_required: true
status: HUMAN_REVIEW_REQUIRED

Safety:
- Evidence Review ≠ approval.
- Lessons Learned ≠ approval.
- Pipeline Hardening Backlog Item ≠ execution authorization.
- Next Task Candidate ≠ approved task.
- Validator PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Human unavailable for required decision → BLOCKED or HUMAN_REVIEW_REQUIRED.
