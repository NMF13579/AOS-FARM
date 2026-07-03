checkpoint_status: APPROVED_FOR_PUSH
push_authorized: true
human_decision_required: true

push_target_details:
  - commit_SHA_to_be_pushed: "34087dccbbe035cb8bbc6b3289a0d29b8744a7a8"
  - origin_dev_SHA_before_push: "249f1c035a9ed3deda3e18294a227e4a2ad15971"
  - target_branch: "origin/dev"
  - allowed_command: "git push origin HEAD:dev"

authorization_boundaries:
  - push_performed: false
  - force_push: forbidden
  - tag_push: forbidden
  - release: forbidden
  - AOS_FARM_434: not_authorized
  - only_commit_34087dccbbe035cb8bbc6b3289a0d29b8744a7a8_may_be_pushed: true
  - unrelated_pre_existing_dirty_worktree_paths: outside_scope
  - unrelated_dirty_paths_must_not_be_staged_committed_or_pushed_as_new_changes: true
