# AOS-FARM.211 — Scope / Risk Plan for Core Stage / Feature Status Registry MVP

## State Verification
- **Required Sources**: Read and verified (00, 01, 02).
- **Git State**:
  - Branch: `build/core-stage-feature-status-registry-mvp`
  - HEAD: `63c19b1ab43fa4a26b09a4dea93b53c0b43ad38c`
  - origin/dev: `63c19b1ab43fa4a26b09a4dea93b53c0b43ad38c`
  - origin/dev...HEAD: `0 0`
- **Local Uncommitted Evidence Artifacts**: Multiple uncommitted reports/checkpoints exist (e.g. from previous stages). These evidence-tail artifacts do not block continuation unless the human explicitly requests recovery.

## Stage Goal
Create a lightweight human-readable registry for AOS-FARM stages and feature statuses. This improves usability without adding automated scanners or RAG logic.

## Authorized Scope
Allowed Implementation Outputs:
- `docs/project-status/README.md`
- `docs/project-status/stage-registry.md`
- `docs/project-status/feature-status-registry.md`
- `templates/stage-status-record-template.md`
- `templates/feature-status-record-template.md`
- `reports/aos-farm-213-core-stage-feature-status-registry-implementation-report.md`
- `reports/aos-farm-214-core-stage-feature-status-registry-verification.md`
- `reports/aos-farm-215-core-stage-feature-status-registry-commit-authorization-package.md`
- `reports/human-checkpoints/aos-farm-215-core-stage-feature-status-registry-commit-authorization.md`
- `reports/aos-farm-217-core-stage-feature-status-registry-commit-push-authorization-package.md`
- `reports/human-checkpoints/aos-farm-217-core-stage-feature-status-registry-commit-push-authorization.md`

## Core Safety Boundary
The registry records status but **does not approve status**. 
- `UNKNOWN` and `NOT_RUN` must be preserved.
- `APPROVED` requires a specific Human approval checkpoint.
- `PASS` or `Evidence` is NOT approval.

## Forbidden Scope
- RAG / SQLite / embeddings / vector DB / chat / retrieval
- Automatic scanners / automatic status detectors
- Modifying protected/canonical sources
- Modifying approval semantics
- CI / runtime / validator implementation
- Cleanup of old untracked artifacts or destructive operations

## Proposed Risk Profile
**MEDIUM_RISK_GUIDED**
Reason: The stage creates new documentation and templates under `docs/project-status`, `templates`, and `reports`. It does not modify protected/canonical sources, runtime code, or approval semantics. Human Risk Profile assignment is strictly required before implementation.
