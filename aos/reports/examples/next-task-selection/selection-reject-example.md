---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Next Task Selection Reject Example

## Selection Context
candidate_task_id: GENERIC-TASK.EXAMPLE.NEXT
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: REJECT
decision_rationale: Candidate does not fit the desired direction.
requested_clarification:
replacement_direction:
deferred_reason:
rejected_reason: Do not compile this candidate into a Task Brief draft.
execution_authorized: false
task_brief_authorized: false
risk_profile_assigned_by_human: false
next_task_started: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

## Decision Semantics
- REJECT means candidate rejected and it must not be compiled.
- REJECT does not authorize any later execution step.

## Safety Boundary
- PASS is not approval.
- Evidence is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
