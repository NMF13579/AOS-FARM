---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Valid Next Task Candidate Fixture

expected_result: PASS

candidate_task_id: GENERIC-TASK.FIXTURE.NEXT
source_backlog_item: GAP-FIXTURE-001
source_evidence: reports/fixture-evidence.md
candidate_goal: create one post-execution review template
candidate_scope:
- one template
- one example
out_of_scope:
- validator/helper code
- tests
- execution
proposed_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: null
execution_authorized: false
commit_authorized: false
push_authorized: false
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
