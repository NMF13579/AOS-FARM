# AOS-FARM.441 Push Authorization Package

task_id: AOS-FARM.441.15
related_commit: 2440c47cc89d074f459d39f687bb9ef15c9f2b4d
proposed_push_command: git push origin HEAD:dev
push_type: normal
force_push_required: false
tag_push_required: false
merge_required: false
release_required: false
post_commit_verification: reports/aos-farm-441-post-commit-verification-report.md
git_mutation_performed: false
staging_performed: false
commit_performed_by_this_task: false
push_authorized: false
push_performed: false
force_push_authorized: false
tag_push_authorized: false
merge_authorized: false
release_authorized: false
next_task_authorized: false
aos_farm_442_authorized: false
final_status: HUMAN_REVIEW_REQUIRED

## Boundary
- This package proposes one normal push only: `git push origin HEAD:dev`.
- Force-push, tag push, merge, release, and AOS-FARM.442 remain unauthorized.
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
