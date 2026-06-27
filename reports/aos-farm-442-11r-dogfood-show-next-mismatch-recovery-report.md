task_id: AOS-FARM.442.11R
parent_task_id: AOS-FARM.442
title: Dogfood Show-Next Mismatch Recovery
branch: build/task-registry-queue-contract-mvp
execution_authorized_by_human: true
risk_profile: HIGH_RISK_PROTECTED
previous_step: AOS-FARM.442.11
previous_status: BLOCKED
previous_reason: dogfood_failed
previous_expected_show_next_matched: false
diagnosis_performed: true
root_cause: "Validator selection logic for show-next simply fell back to the exact same logic as show-current, finding the first eligible task in the queue (AOS-FARM.442), instead of advancing to the next eligible task after the currently selected task."
changed_files:
  - aos/tools/optional/task_registry_validator.py
dogfood_fixture_modified: false
validator_modified: true
cli_modified: false
tests_modified: false
unit_tests_passed: true
dogfood_validate_passed: true
expected_summary_matched: true
expected_show_current_matched: true
expected_show_next_matched: true
runner_behavior_introduced: false
auto_approval_introduced: false
auto_execution_introduced: false
sqlite_implementation_introduced: false
rag_light_implementation_introduced: false
commit_performed: false
push_performed: false
next_allowed_step: AOS-FARM.442.12 Final Review
final_status: PASS
