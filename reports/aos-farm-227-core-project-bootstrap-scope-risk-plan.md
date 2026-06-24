# AOS-FARM.227 — Scope / Risk Plan for Core Project Bootstrap MVP

## State Verification
- **Required Sources**: Read and verified (`00`, `01`, `02`).
- **Git State**:
  - Branch: `build/core-project-bootstrap-mvp`
  - HEAD: `aaa2af673cb287cd15149b1793192687ca5209ef`
  - origin/dev: `aaa2af673cb287cd15149b1793192687ca5209ef`
  - origin/dev...HEAD divergence: `0 0`
- **Local Uncommitted Evidence Artifacts**: Multiple old uncommitted check/closure reports exist in the tree. These evidence-tail artifacts do not block continuation unless explicitly requested by a human.

## Stage Goal
Create a minimal, safe, non-programmer-friendly bootstrap layer for using AOS-FARM as a project starter template. Provide guidance on what to do in the first 30 minutes after creating a repository.

## Authorized Scope
Allowed Implementation Outputs:
- **Docs**:
  - `docs/user-guide/new-project-bootstrap.md`
  - `docs/user-guide/first-30-minutes.md`
  - `docs/user-guide/template-repository-usage.md`
  - `docs/user-guide/bootstrap-agent-workflow.md`
- **Templates**:
  - `templates/project-bootstrap-checklist.md`
  - `templates/first-agent-session-template.md`
  - `templates/first-task-brief-template.md`
  - `templates/bootstrap-human-checkpoint-template.md`
  - `templates/bootstrap-next-safe-step-template.md`
- **Reports/Checkpoints**:
  - AOS-FARM.229, 230, 231, 233 reports and corresponding human checkpoints.

## Core Safety Boundary
- Manual bootstrap path only.
- No automatic execution, runner, task queue, CLI, or installer scripts.
- No modifications to protected/canonical sources (`00`, `01`, `02`).

## Forbidden Scope
- Install automation / CLI implementation.
- Runner / Task Queue implementations.
- GitHub Actions / CI / Runtime implementations.
- RAG, SQLite, vector DB, retrieval engines, or automatic scanners.
- Automatic commit/push.
- Modifying approval semantics, lifecycle semantics, or Source of Truth rules.

## Proposed Risk Profile
**MEDIUM_RISK_GUIDED**
Reason: The stage only creates documentation and bootstrap templates for new project initialization. It explicitly does not modify runtime code, canonical rules, or CI infrastructure. Human execution authorization with explicit Risk Profile assignment is strictly required before implementation.
