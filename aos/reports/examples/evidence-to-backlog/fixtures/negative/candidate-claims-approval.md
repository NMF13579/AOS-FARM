# Negative Fixture: Candidate Claims Approval

expected_result: BLOCKED
violation: Next Task Candidate claims approved-task status

candidate_task_id: AOS-FARM.NEGATIVE.NEXT
source_backlog_item: GAP-NEGATIVE-001
source_evidence: reports/negative-evidence.md
candidate_goal: implement follow-up work
candidate_scope:
- change workflow files
out_of_scope:
- none listed
proposed_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: null
execution_authorized: false
commit_authorized: false
push_authorized: false
approval_claimed: true
status: DRAFT
claim: this candidate is an approved task

Why blocked:
- Next Task Candidate ≠ approved task.
- Human approval cannot be simulated.
- Pipeline Hardening Backlog Item ≠ execution authorization.
