# Negative Selection Assigns Risk Profile Without Human Fixture

expected_result: BLOCKED
violation: selection artifact assigns Risk Profile without human checkpoint

candidate_task_id: AOS-FARM.FIXTURE.SELECTION.NEGATIVE.RISK
candidate_source_file: aos/reports/examples/evidence-to-backlog/next-task-candidate-example.md
candidate_status: DRAFT
selection_decision: ACCEPT
decision_rationale: Incorrectly claims Risk Profile assignment.
requested_clarification:
replacement_direction:
deferred_reason:
rejected_reason:
execution_authorized: false
task_brief_authorized: false
risk_profile_assigned_by: agent
risk_profile_assigned_by_human: true
next_task_started: false
human_review_required: true
final_status: HUMAN_REVIEW_REQUIRED

Why blocked:
- ACCEPT does not assign Risk Profile.
- Risk Profile assignment must stay human-controlled.
