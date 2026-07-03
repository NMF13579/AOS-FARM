checkpoint_status: APPROVED_FOR_PUSH
push_authorized: true
human_decision_required: false

push_target_details:
  - commit_SHA_to_be_pushed: HEAD
  - origin_dev_SHA_before_push: origin/dev
  - target_branch: origin/dev
  - allowed_command: "git push origin HEAD:dev"

authorization_boundaries:
  - force_push: forbidden
  - tag_push: forbidden
  - merge: forbidden
  - release: forbidden
  - production_use: forbidden
