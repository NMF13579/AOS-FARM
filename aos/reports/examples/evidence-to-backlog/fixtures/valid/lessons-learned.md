# Valid Lessons Learned Fixture

expected_result: PASS

source_task_id: AOS-FARM.FIXTURE
source_evidence: reports/fixture-evidence.md
lesson_type: safety_boundary
problem_observed: users need a place to record post-execution learning
what_worked: evidence boundaries stayed explicit
what_failed: no standard learning artifact existed
what_was_manual: converting review notes into follow-up work
what_was_ambiguous: none
recommendation: create a backlog item for human review
requires_backlog_item: true
approval_claimed: false
status: DRAFT

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
