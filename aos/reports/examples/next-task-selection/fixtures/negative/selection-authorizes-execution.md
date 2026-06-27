# Negative Selection Authorizes Execution Fixture

expected_result: BLOCKED
violation: selection artifact claims execution authorization

candidate_task_id: AOS-FARM.FIXTURE.SELECTION.NEGATIVE.EXEC
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: ACCEPT
decision_rationale: Incorrectly treats ACCEPT as execution authorization.
requested_clarification:
replacement_direction:
deferred_reason:
rejected_reason:
execution_authorized: true
task_brief_authorized: false
risk_profile_assigned_by_human: false
next_task_started: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

Why blocked:
- ACCEPT does not authorize execution.
- PASS is not approval.
