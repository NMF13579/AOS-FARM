---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Negative Fixture: Execution Authorized Inside Candidate

expected_result: BLOCKED
violation: Next Task Candidate claims execution authorization

candidate_task_id: GENERIC-TASK.NEGATIVE.EXECUTION
source_backlog_item: GAP-NEGATIVE-003
source_evidence: reports/negative-evidence.md
candidate_goal: implement follow-up work
candidate_scope:
- update workflow docs
out_of_scope:
- commit
- push
proposed_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: null
execution_authorized: true
commit_authorized: false
push_authorized: false
approval_claimed: false
status: DRAFT

Why blocked:
- Pipeline Hardening Backlog Item ≠ execution authorization.
- Next Task Candidate ≠ approved task.
- Human approval cannot be simulated.
