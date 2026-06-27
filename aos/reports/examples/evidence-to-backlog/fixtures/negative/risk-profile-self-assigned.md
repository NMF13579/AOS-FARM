# Negative Fixture: Risk Profile Self-Assigned

expected_result: HUMAN_REVIEW_REQUIRED
violation: Risk Profile assigned by a non-human actor

candidate_task_id: AOS-FARM.NEGATIVE.RISK
source_backlog_item: GAP-NEGATIVE-002
source_evidence: reports/negative-evidence.md
candidate_goal: implement follow-up work
candidate_scope:
- update templates
out_of_scope:
- commit
- push
proposed_risk_profile: LOW_RISK_FAST
risk_profile_assigned_by: agent
execution_authorized: false
commit_authorized: false
push_authorized: false
approval_claimed: false
status: DRAFT

Why blocked:
- Agent must not self-assign LOW_RISK_FAST.
- Human unavailable for required decision → BLOCKED or HUMAN_REVIEW_REQUIRED.
- Next Task Candidate ≠ approved task.
