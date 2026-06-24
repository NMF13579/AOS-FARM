# AOS-FARM.243 — Scope / Risk Plan for Thin Task Queue Helper / Dry-Run Runner MVP

## State Verification
- **Required Sources**: Verified and accessible (`00`, `01`, `02`).
- **Git State**:
  - Branch: `build/thin-task-queue-helper-dry-run-runner-mvp`
  - HEAD: `23ff371b02051098dd840ba4a0dbe5efc7fd6660`
  - origin/dev: `23ff371b02051098dd840ba4a0dbe5efc7fd6660`
  - origin/dev...HEAD: `0 0`
- **Local Evidence**: Multiple uncommitted check/closure reports exist from previous stages; they do not block continuation unless a human requests recovery.

## Stage Goal
Create a thin local helper script for the manual task queue. This helper acts as a dry-run / generator-only runner to validate tasks, detect unsafe transitions or missing approvals, and generate handoff/verification templates. It must not execute code, mutate state, or authorize anything.

## Authorized Scope
The agent is authorized to create/modify the following files during implementation:

**Documentation**:
- `docs/task-queue/thin-task-queue-helper.md`
- `docs/task-queue/dry-run-runner-boundary.md`

**Scripts**:
- `agentos/scripts/task_queue_helper.py`

**Templates**:
- `templates/task-queue-helper-output-template.md`
- `templates/task-queue-helper-next-safe-step-template.md`

**Fixtures**:
- `fixtures/task-queue-helper/valid-task-queue-item.md`
- `fixtures/task-queue-helper/missing-approval-task-queue-item.md`
- `fixtures/task-queue-helper/unsafe-transition-task-queue-item.md`
- `fixtures/task-queue-helper/unknown-blocked-task-queue-item.md`
- `fixtures/task-queue-helper/not-run-task-queue-item.md`

**Reports/Checkpoints**:
- AOS-FARM.245, 246, 247, 249, 250 reports and checkpoints.

## Forbidden Scope
- No autonomous runner implementation.
- No agent launcher or execution authority.
- No automatic status updater or lifecycle mutation.
- No automatic approval authority.
- No automatic commit, push, merge, or release.
- No RAG, SQLite, vector DB, chat-with-docs, retrieval system.
- No runtime orchestration or CI workflow.
- No modification of protected/canonical files (`00`, `01`, `02`).
- No destruction or deletion of existing files.

## Proposed Risk Profile
**MEDIUM_RISK_GUIDED**
Reason: The stage introduces a Python script (`task_queue_helper.py`) but explicitly confines it to dry-run validation and template generation. The script will not have execution or network privileges and will strictly parse Markdown. Human execution authorization with an explicitly assigned risk profile is required before writing any code.
