task_id: AOS-FARM.443
stage: local_reconciliation
implementation_started: false
commit_authorized: false
push_authorized: false
current_branch: build/task-registry-queue-contract-mvp
target_branch: build/task-quality-acceptance-gate-mvp
head: f1afce93a60ab050f65adb236095a5db0b9ba9b2
origin_dev: f1afce93a60ab050f65adb236095a5db0b9ba9b2
ahead_behind: 0 0
local_target_branch_status: LOCAL_TARGET_BRANCH_MISSING
remote_target_branch_status: REMOTE_TARGET_BRANCH_MISSING
dirty_worktree: true
dirty_deleted_files: true
dirty_modified_files: false
dirty_untracked_files: true
forbidden_path_touched_by_current_dirty_state:
  - agentos/**
443_task_brief_present: false
443_execution_checkpoint_present: false
safe_next_options:
  - option_id: HUMAN_DECISION_REQUIRED
    description: "Human must decide how to handle dirty worktree before branch switch."
blocked_operations:
  - git clean
  - git reset
  - restore/delete/move/rename without explicit human authorization
  - checkout target branch while dirty state unresolved
final_status: HUMAN_REVIEW_REQUIRED
