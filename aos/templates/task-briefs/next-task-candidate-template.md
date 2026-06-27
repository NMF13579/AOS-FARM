# Next Task Candidate Template

Use this template to frame a possible follow-up task from post-execution
evidence. A Next Task Candidate is not an approved task, not a Controlled Task
Brief, and not execution authorization.

## Status
candidate_task_id:
source_backlog_item:
source_evidence:
candidate_goal:
candidate_scope:
out_of_scope:
proposed_risk_profile:
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

## Next Safe Step
Human review is required before this candidate can become a real Task Brief,
receive a human-assigned Risk Profile, or move toward execution authorization.
