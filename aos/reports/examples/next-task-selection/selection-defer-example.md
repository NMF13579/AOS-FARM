---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Next Task Selection Defer Example

## Selection Context
candidate_task_id: GENERIC-TASK.EXAMPLE.NEXT
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: DEFER
decision_rationale: Candidate is useful but not the current priority.
requested_clarification:
replacement_direction:
deferred_reason: Postpone until earlier backlog items are reviewed.
rejected_reason:
execution_authorized: false
task_brief_authorized: false
risk_profile_assigned_by_human: false
next_task_started: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

## Decision Semantics
- DEFER means candidate postponed.
- DEFER does not authorize Task Brief drafting, execution, commit, or push.

## Safety Boundary
- PASS is not approval.
- Evidence is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
