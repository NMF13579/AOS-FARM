```yaml
task_id: AOS-FARM.222
task_name: Merge Execution

mode: execution

source_branch: dev
source_ref: origin/dev
target_branch: main
target_ref: origin/main

authorized_merge_command: "git checkout main && git merge --no-ff origin/dev"

execution_status:
  merge_performed: true
  merge_commit: 9fc5c78abaf13ed328b190a8a38dbdec78b8fa97
  conflicts_encountered: false
  push_performed: false

push_after_merge_authorized: false

next_step: Prepare push authorization package (AOS-FARM.223).
```
