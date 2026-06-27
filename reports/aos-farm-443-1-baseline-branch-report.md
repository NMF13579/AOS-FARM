task_id: AOS-FARM.443
stage: baseline_branch_preparation
branch: build/task-quality-acceptance-gate-mvp
base_branch: dev
expected_head: f1afce93a60ab050f65adb236095a5db0b9ba9b2
head_equals_origin_dev: true
ahead_behind: "0 0"
tracked_dirty_files: false
untracked_reports_present: true
implementation_started: false
commit_authorized: false
push_authorized: false
final_status: BRANCH_READY_WITH_UNTRACKED_REPORTS

```shell
$ git branch --show-current
build/task-quality-acceptance-gate-mvp

$ git status --short
<untracked reports present>

$ git status -sb
## build/task-quality-acceptance-gate-mvp

$ git rev-parse HEAD
f1afce93a60ab050f65adb236095a5db0b9ba9b2

$ git rev-parse origin/dev
f1afce93a60ab050f65adb236095a5db0b9ba9b2

$ git rev-list --left-right --count origin/dev...HEAD
0	0
```
