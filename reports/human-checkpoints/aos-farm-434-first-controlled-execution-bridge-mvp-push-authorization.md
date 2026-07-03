checkpoint_status: APPROVED_FOR_PUSH
push_authorized: true
human_decision_required: true

push_target_details:
  - commit_SHA_to_be_pushed: "414637b13f50a93d34228063b9b9385e886b2199"
  - origin_dev_SHA_before_push: "34087dccbbe035cb8bbc6b3289a0d29b8744a7a8"
  - target_branch: "origin/dev"
  - allowed_command: "git push origin HEAD:dev"

authorization_boundaries:
  - push_performed: false
  - force_push: forbidden
  - tag_push: forbidden
  - release: forbidden
  - AOS_FARM_435: not_authorized
  - only_commit_414637b13f50a93d34228063b9b9385e886b2199_may_be_pushed: true
  - unrelated_pre_existing_dirty_worktree_paths: outside_scope
  - local_AOS_FARM_433_push_authorization_artifacts: outside_scope
  - no_additional_stage_commit_push_changes_authorized: true
  - runner_automation_SQLite_RAG_vector_DB_CI_Spec_Kit_execution: not_authorized
