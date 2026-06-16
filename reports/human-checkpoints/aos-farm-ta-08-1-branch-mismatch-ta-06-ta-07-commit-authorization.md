checkpoint_id: AOS-FARM.TA-08.1-BRANCH-MISMATCH-TA-06-TA-07-COMMIT-AUTHORIZATION
checkpoint_status: APPROVED
authorization_type: COMMIT_ONLY_WITH_BRANCH_WARNING

expected_branch: dev
actual_branch: main
head_equals_origin_dev: true

commit_authorized: true
branch_warning_accepted: true
push_authorized: false
combined_commit_push_authorized: false

candidate_commit_set_source:
  - reports/aos-farm-ta-08-1-branch-mismatch-ta-06-ta-07-commit-authorization-package.md

proposed_commit_message: "docs: add adaptive technical assignment intake methodology"

required_human_action:
  - review_branch_warning
  - decide whether commit may proceed from current main state because HEAD equals origin/dev
  - verify exact candidate file set
  - verify proposed commit message
  - if acceptable, explicitly set checkpoint_status: APPROVED
  - if acceptable, explicitly set commit_authorized: true
  - if acceptable, explicitly set branch_warning_accepted: true

forbidden:
  - combined_commit_push_authorization
  - push
  - force_push
  - tag_push
  - merge
  - release
  - deploy
  - production_use
  - runtime_implementation
  - json_state_implementation
  - probing_engine_implementation
  - validator_implementation
  - ci_workflow_changes
  - speckit_commands
