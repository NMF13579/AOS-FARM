checkpoint_id: AOS-FARM.TA-08.2-TA-06-TA-07-PUSH-AUTHORIZATION
checkpoint_status: APPROVED
authorization_type: PUSH_ONLY_WITH_BRANCH_WARNING

current_branch: main
push_target: origin/dev
commit_sha: b8a03c1edf0375fc1b1cc89dcf8917a996fe579c
proposed_push_command: "git push origin b8a03c1edf0375fc1b1cc89dcf8917a996fe579c:dev"

push_authorized: true
branch_warning_accepted: true
force_push_authorized: false
tag_push_authorized: false
release_authorized: false
deploy_authorized: false
production_use_authorized: false

required_human_action:
  - review_push_authorization_package
  - verify_commit_sha
  - verify_push_target
  - verify_exact_push_command
  - explicitly accept branch warning for pushing current main HEAD to origin/dev
  - if acceptable, explicitly set checkpoint_status: APPROVED
  - if acceptable, explicitly set push_authorized: true
  - if acceptable, explicitly set branch_warning_accepted: true

forbidden:
  - force_push
  - tag_push
  - push_to_origin_main
  - ambiguous_git_push_origin_dev_from_main
  - merge
  - release
  - deploy
  - production_use
  - commit
  - runtime_implementation
  - validator_implementation
  - ci_workflow_changes
  - speckit_commands
