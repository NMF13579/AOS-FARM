---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Next Task Selection Clarify Example

## Selection Context
candidate_task_id: GENERIC-TASK.EXAMPLE.NEXT
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: CLARIFY
decision_rationale: Candidate scope is promising but still ambiguous.
requested_clarification: Clarify exact allowed files and non-goals before any Task Brief drafting.
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
- CLARIFY means more human or user clarification is required.
- CLARIFY does not authorize Task Brief drafting, execution, commit, or push.

## Safety Boundary
- PASS is not approval.
- Evidence is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
