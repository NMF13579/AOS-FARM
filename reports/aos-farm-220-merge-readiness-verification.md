```yaml
task_id: AOS-FARM.220
task_name: Merge Readiness Verification / Merge Authorization Preparation

mode: read_only_verification

source_branch: dev
source_remote_ref: origin/dev
target_remote_ref: origin/main

head: 3ad31a5715e305e0bb4df7ed7c5f9bacbf27cfd2
origin_dev: 3ad31a5715e305e0bb4df7ed7c5f9bacbf27cfd2
origin_main: 5e2ed9e7d9c8ae4937f54e292971847ee7dd6e51

head_equals_origin_dev: true
remote_baseline_closed: true

origin_main_origin_dev_left_right_counts: "0 30"
merge_candidate_commit_count: 30
merge_candidate_commits:
  - 3ad31a5 docs: add evidence-based hardening review
  - (and 29 prior commits representing Build Steps 2-12 on dev)

merge_candidate_changed_files:
  - (284 changed files representing all Build Steps 2-12 on dev)

tracked_worktree_clean: true
untracked_artifacts_present: true
untracked_artifacts:
  - path: "reports/human-checkpoints/*.md"
    classification: evidence_tail
    merge_blocking: false
  - path: "reports/*.md"
    classification: evidence_tail
    merge_blocking: false

step_12_closure_report_exists: true

merge_performed: false
commit_performed: false
push_performed: false
force_push_performed: false
tag_push_performed: false
release_performed: false
production_use_performed: false
destructive_operations_performed: false
approval_simulated: false

blocking_issue_count: 0
warning_count: 0

may_prepare_human_merge_authorization: true

final_status: AOS_FARM_220_MERGE_READINESS_VERIFICATION_PASS
```
