checkpoint_status: APPROVED_FOR_MERGE
human_decision: APPROVED

merge_authorized: true
aos_farm_222_merge_execution_authorized: true

source_branch: dev
source_ref: origin/dev
source_commit: 3ad31a5715e305e0bb4df7ed7c5f9bacbf27cfd2

target_branch: main
target_ref: origin/main
target_commit_before_merge: 5e2ed9e7d9c8ae4937f54e292971847ee7dd6e51

authorized_merge_command: git checkout main && git merge --no-ff origin/dev

merge_candidate_commit_count: 30
merge_candidate_changed_file_count: 284
large_merge_acknowledged_by_human: true

push_after_merge_authorized: false
release_authorized: false
production_use_authorized: false
tag_push_authorized: false
force_push_authorized: false
destructive_operations_authorized: false

approval_simulated: false