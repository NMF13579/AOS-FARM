package_id: AOS-FARM.440.PA
package_name: Push Authorization Package
source_commit: 9ca21bb1bc04fcb0380ca058d550addf666e66e9
source_post_commit_verification_report: reports/aos-farm-440-post-commit-verification-report.md
branch: build/evidence-to-backlog-loop-mvp
HEAD: 9ca21bb1bc04fcb0380ca058d550addf666e66e9
origin/dev: d612284028fea7984f3d8833a2b2b427c47e8d99
ahead_behind: 0 1
push_authorization_status: NOT_AUTHORIZED
human_push_authorization_required: true
proposed_push_target: origin dev
proposed_push_command: git push origin HEAD:dev
force_push: false
tag_push: false
release: false
merge: false
next_task_started: false
committed_file_count: 42
tests_run:
  - python3 -m unittest discover -s tests/evidence_to_backlog -p 'test_evidence_to_backlog_validator.py'
  - python3 aos/scripts/aos_evidence_to_backlog.py validate-chain --review reports/aos-farm-440-dogfood-post-execution-review.md --lessons reports/aos-farm-440-dogfood-lessons-learned.md --item reports/aos-farm-440-dogfood-pipeline-hardening-backlog-item.md --candidate reports/aos-farm-440-dogfood-next-task-candidate.md
test_result: PASS
dogfood_chain_result: PASS
safety_invariants_preserved:
  - PASS does not equal approval
  - Evidence does not equal approval
  - Validator PASS does not equal approval
  - Commit PASS does not equal push authorization
  - Commit does not authorize push
dirty_worktree_boundary: pre-existing unrelated dirty state preserved; no cleanup, reset, stash, delete, restore, chmod, or chown performed
out_of_scope_dirty_state:
  - agentos/reports/problem-intake/**
  - reports/** unrelated pre-existing artifacts
  - reports/human-checkpoints/** unrelated pre-existing artifacts
UNKNOWN:
  - none
NOT_RUN:
  - none
BLOCKED:
  - none
remaining_gaps: none
push_performed: false
final_status: HUMAN_REVIEW_REQUIRED
This package does not authorize push.
Human push authorization is required.
Commit does not authorize push.
PASS does not equal approval.
Evidence does not equal approval.
Validator PASS does not equal approval.
Push must not occur until the human checkpoint explicitly sets push_authorized: true.
