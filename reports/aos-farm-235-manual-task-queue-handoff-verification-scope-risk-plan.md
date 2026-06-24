# AOS-FARM.235 — Scope / Risk Plan for Manual Task Queue, Handoff, and Verification Contract

## State Verification
- **Required Sources**: Verified and accessible (`00`, `01`, `02`).
- **Git State**:
  - Branch: `build/manual-task-queue-handoff-verification-contract`
  - HEAD: `b9fec2c8185297551a368b351968d0f1106dd4bd`
  - origin/dev: `b9fec2c8185297551a368b351968d0f1106dd4bd`
  - origin/dev...HEAD: `0 0`
- **Local Evidence**: Multiple uncommitted check/closure reports exist from previous stages; they do not block continuation unless a human requests recovery.

## Stage Goal
Create a manual Markdown-based task queue, agent handoff workflow, and execution verification loop contract. This will define how tasks move from drafting to verification to push, completely manually, without any execution runners, databases, or daemons.

## Authorized Scope
The agent is authorized to create/modify the following files during implementation:

**Documentation**:
- `docs/task-queue/README.md`
- `docs/task-queue/manual-task-queue.md`
- `docs/task-queue/agent-handoff-workflow.md`
- `docs/task-queue/execution-result-verification-loop.md`
- `docs/task-queue/task-status-transition-contract.md`

**Templates**:
- `templates/task-queue-item-template.md`
- `templates/task-batch-plan-template.md`
- `templates/agent-handoff-package-template.md`
- `templates/agent-execution-result-report-template.md`
- `templates/post-execution-verification-template.md`
- `templates/task-queue-status-update-template.md`
- `templates/manual-task-queue-review-template.md`

**Reports/Checkpoints**:
- AOS-FARM.237, 238, 239, 241, 242 reports and checkpoints.

## Forbidden Scope
- No runner, task daemon, CLI, or automatic dispatcher implementation.
- No SQLite, RAG, vector DB, or retrieval engine.
- No automatic status updater or verifier.
- No GitHub Actions / CI workflow changes.
- No runtime orchestration or production workflow implementations.
- No modification of protected/canonical files (`00`, `01`, `02`).
- No changes to approval semantics, lifecycle semantics, or Source of Truth rules.
- No automatic execution of `git commit` or `git push` without human checkpoints.

## Proposed Risk Profile
**MEDIUM_RISK_GUIDED**
Reason: The stage only involves creating Markdown documentation and templates. It explicitly forbids any modification of canonical rules, automation scripts, CI, or runtime components. Human execution authorization with an explicitly assigned risk profile is strictly required.
