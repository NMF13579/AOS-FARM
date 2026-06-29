---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Negative Selection Starts Next Task Fixture

expected_result: BLOCKED
violation: selection artifact claims next task already started

candidate_task_id: GENERIC-TASK.FIXTURE.SELECTION.NEGATIVE.START
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: ACCEPT
decision_rationale: Incorrectly claims next-task start.
requested_clarification:
replacement_direction:
deferred_reason:
rejected_reason:
execution_authorized: false
task_brief_authorized: false
risk_profile_assigned_by_human: false
next_task_started: true
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

Why blocked:
- ACCEPT does not start the next task.
- Human review remains required.
