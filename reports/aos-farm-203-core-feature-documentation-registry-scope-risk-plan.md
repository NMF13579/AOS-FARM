# AOS-FARM.203 — Scope / Risk Plan for Core Feature Documentation Registry MVP

## State Verification
- **Required Sources**: Read and verified (00, 01, 02).
- **Git State**:
  - Branch: `build/core-feature-documentation-registry-mvp`
  - HEAD: `e80746f3fa96dfac6a71c104d57fba20832b56ea`
  - origin/dev: `e80746f3fa96dfac6a71c104d57fba20832b56ea`
  - origin/dev...HEAD: `0 0`
- **Local Uncommitted Closure Reports**: Exist (e.g., AOS-FARM.202 closure report). Local evidence-tail artifacts do not block continuation unless explicitly requested by the human.

## Stage Goal
Create a manual Core Feature Documentation Registry MVP to help a non-programmer understand what features exist in AOS-FARM, without relying on automated RAG or scanning.

## Authorized Scope
Allowed Implementation Outputs:
- `docs/features/README.md`
- `docs/features/feature-documentation-registry.md`
- `templates/feature-documentation-template.md`
- `templates/feature-documentation-update-request-template.md`
- `reports/aos-farm-205-core-feature-documentation-registry-implementation-report.md`
- `reports/aos-farm-206-core-feature-documentation-registry-verification.md`
- `reports/aos-farm-207-core-feature-documentation-registry-commit-authorization-package.md`
- `reports/human-checkpoints/aos-farm-207-core-feature-documentation-registry-commit-authorization.md`
- `reports/aos-farm-209-core-feature-documentation-registry-push-and-remote-closure.md`

## Forbidden Scope
- RAG / SQLite / embeddings / vector DB / chat / retrieval
- Automatic scanners / feature detectors
- Modifying protected/canonical sources
- CI / runtime / validator implementation
- Cleanup of old untracked artifacts or destructive operations

## Proposed Risk Profile
**MEDIUM_RISK_GUIDED**
Reason: The stage creates new documentation and templates under `docs/features`, `templates`, and `reports`. It does not modify protected/canonical sources or runtime code. Human Risk Profile assignment is strictly required before implementation.
