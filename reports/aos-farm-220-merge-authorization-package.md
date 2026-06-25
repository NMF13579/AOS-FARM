```yaml
authorization_type: merge
source_branch: dev
source_ref: origin/dev
target_branch: main
target_ref: origin/main

authorized_now: false
human_authorization_required: true

merge_command_proposed: git checkout main && git merge --no-ff origin/dev
push_after_merge_authorized: false
release_authorized: false
production_use_authorized: false

required_human_checkpoint:
  - reports/human-checkpoints/aos-farm-220-merge-authorization.md
```
