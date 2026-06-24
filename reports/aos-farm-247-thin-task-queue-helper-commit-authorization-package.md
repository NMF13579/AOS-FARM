# AOS-FARM.247 — Commit Authorization Package

## Target Task
AOS-FARM.249 — Controlled Commit + Push Authorization Preparation

## Preconditions Verified
- Implementation (AOS-FARM.245) was completed inside authorized scope.
- Post-execution verification (AOS-FARM.246) passed successfully.
- No protected/canonical changes made.
- Strict dry-run helper boundary preserved (no runner, CI, automation, or RAG).

## Proposed Commit Message
`feat: add thin task queue dry-run helper`

## Candidate Set for Commit
The following exact files are proposed for commit:
- `docs/task-queue/thin-task-queue-helper.md`
- `docs/task-queue/dry-run-runner-boundary.md`
- `agentos/scripts/task_queue_helper.py`
- `templates/task-queue-helper-output-template.md`
- `templates/task-queue-helper-next-safe-step-template.md`
- `fixtures/task-queue-helper/valid-task-queue-item.md`
- `fixtures/task-queue-helper/missing-approval-task-queue-item.md`
- `fixtures/task-queue-helper/unsafe-transition-task-queue-item.md`
- `fixtures/task-queue-helper/unknown-blocked-task-queue-item.md`
- `fixtures/task-queue-helper/not-run-task-queue-item.md`
- `reports/aos-farm-243-thin-task-queue-helper-scope-risk-plan.md`
- `reports/aos-farm-243-thin-task-queue-helper-execution-authorization-package.md`
- `reports/human-checkpoints/aos-farm-243-thin-task-queue-helper-execution-authorization.md`
- `reports/aos-farm-245-thin-task-queue-helper-implementation-report.md`
- `reports/aos-farm-246-thin-task-queue-helper-verification.md`
- `reports/aos-farm-247-thin-task-queue-helper-commit-authorization-package.md`
- `reports/human-checkpoints/aos-farm-247-thin-task-queue-helper-commit-authorization.md`

## Required Action
To authorize this commit, update `reports/human-checkpoints/aos-farm-247-thin-task-queue-helper-commit-authorization.md` with:
- `checkpoint_status`: APPROVED_FOR_COMMIT
- `commit_authorized`: true
- `authorized_commit_message`: feat: add thin task queue dry-run helper
- `authorized_files`: [exact candidate set]
- `authorized_target_task`: AOS-FARM.249
