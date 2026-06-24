# AOS-FARM.231 — Commit Authorization Package

## Target Task
AOS-FARM.233 — Controlled Commit + Push Authorization Preparation

## Preconditions Verified
- Implementation (AOS-FARM.229) was completed inside authorized scope.
- Post-execution verification (AOS-FARM.230) passed successfully.
- No protected/canonical changes made.
- Strictly pure documentation and templates (no runner, CI, automation, or RAG).

## Proposed Commit Message
`docs: add core project bootstrap workflow`

## Candidate Set for Commit
The following exact files are proposed for commit:
- `docs/user-guide/new-project-bootstrap.md`
- `docs/user-guide/first-30-minutes.md`
- `docs/user-guide/template-repository-usage.md`
- `docs/user-guide/bootstrap-agent-workflow.md`
- `templates/project-bootstrap-checklist.md`
- `templates/first-agent-session-template.md`
- `templates/first-task-brief-template.md`
- `templates/bootstrap-human-checkpoint-template.md`
- `templates/bootstrap-next-safe-step-template.md`
- `reports/aos-farm-227-core-project-bootstrap-scope-risk-plan.md`
- `reports/aos-farm-227-core-project-bootstrap-execution-authorization-package.md`
- `reports/human-checkpoints/aos-farm-227-core-project-bootstrap-execution-authorization.md`
- `reports/aos-farm-229-core-project-bootstrap-implementation-report.md`
- `reports/aos-farm-230-core-project-bootstrap-verification.md`
- `reports/aos-farm-231-core-project-bootstrap-commit-authorization-package.md`
- `reports/human-checkpoints/aos-farm-231-core-project-bootstrap-commit-authorization.md`

## Required Action
To authorize this commit, update `reports/human-checkpoints/aos-farm-231-core-project-bootstrap-commit-authorization.md` with:
- `checkpoint_status`: APPROVED_FOR_COMMIT
- `commit_authorized`: true
- `authorized_commit_message`: docs: add core project bootstrap workflow
- `authorized_files`: [exact candidate set]
- `authorized_target_task`: AOS-FARM.233
