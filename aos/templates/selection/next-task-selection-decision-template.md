# Next Task Selection Decision Template

Use this template to record one human decision for one `Next Task Candidate`.

## Selection Context
candidate_task_id:
candidate_source_file:
candidate_status: DRAFT
selection_decision:
decision_rationale:
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
- `ACCEPT` means candidate accepted for Task Brief draft preparation only.
- `ACCEPT` is not task approval.
- `ACCEPT` does not assign Risk Profile.
- `ACCEPT` does not authorize execution.
- `ACCEPT` does not authorize commit.
- `ACCEPT` does not authorize push.
- `ACCEPT` does not start the next task.
- `CLARIFY` means more human or user clarification is required.
- `DEFER` means candidate postponed.
- `REJECT` means candidate rejected and must not be compiled.
- `REPLACE` means a different candidate is requested.

## Safety Boundary
- PASS is not approval.
- Evidence is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
