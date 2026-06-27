# Next Task Candidate Example

## Status
candidate_task_id: AOS-FARM.EXAMPLE.NEXT
source_backlog_item: GAP-EXAMPLE-001
source_evidence: reports/example-controlled-execution-evidence.md
candidate_goal: add a review template for post-execution learning
candidate_scope:
- create one review template
- create one example
out_of_scope:
- validator/helper implementation
- tests
- commit
- push
proposed_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: null
execution_authorized: false
commit_authorized: false
push_authorized: false
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
