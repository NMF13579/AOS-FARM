checkpoint_id: AOS-FARM.TA-09-PROBLEM-INTAKE-AGENT-COMMIT-AUTHORIZATION
checkpoint_status: APPROVED
authorization_type: COMMIT_ONLY

expected_branch: dev
actual_branch: dev
head_equals_origin_dev: true

commit_authorized: true
push_authorized: false
combined_commit_push_authorized: false

candidate_commit_set_source:
  - reports/aos-farm-ta-09-problem-intake-agent-commit-authorization-package.md

proposed_commit_message: "docs: update problem intake agent prompt for adaptive TA methodology"

required_human_action:
  - verify exact candidate file set
  - verify proposed commit message
  - if acceptable, explicitly set checkpoint_status: APPROVED
  - if acceptable, explicitly set commit_authorized: true

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
