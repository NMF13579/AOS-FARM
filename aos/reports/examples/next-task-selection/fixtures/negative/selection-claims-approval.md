# Negative Selection Claims Approval Fixture

expected_result: BLOCKED
violation: selection artifact claims approved lifecycle state

candidate_task_id: AOS-FARM.FIXTURE.SELECTION.NEGATIVE.APPROVAL
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: ACCEPT
decision_rationale: Incorrectly claims approval.
requested_clarification:
replacement_direction:
deferred_reason:
rejected_reason:
execution_authorized: false
task_brief_authorized: false
risk_profile_assigned_by_human: false
next_task_started: false
human_review_required: true
approval_status: APPROVED
final_status: HUMAN_REVIEW_REQUIRED

Why blocked:
- Human approval cannot be simulated.
- ACCEPT is not task approval.
