# Next Task Selection Accept Example

## Selection Context
candidate_task_id: AOS-FARM.EXAMPLE.NEXT
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: ACCEPT
decision_rationale: Candidate is suitable for Task Brief draft preparation.
requested_clarification:
replacement_direction:
deferred_reason:
rejected_reason:
execution_authorized: false
task_brief_authorized: false
risk_profile_assigned_by_human: false
next_task_started: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

## Decision Semantics
- ACCEPT means candidate accepted for Task Brief draft preparation only.
- ACCEPT is not task approval.
- ACCEPT does not assign Risk Profile.
- ACCEPT does not authorize execution.
- ACCEPT does not authorize commit or push.
- ACCEPT does not start the next task.

## Safety Boundary
- PASS is not approval.
- Evidence is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
