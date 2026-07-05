# ADR-0004 — Safe Installer Boundary
## Status
PROPOSED
## Decision Type
architecture_candidate
## Metadata
adr_id: ADR-0004
title: Safe Installer Boundary
status: PROPOSED
approval_status: NOT_APPROVED
human_review_required: true
decision_type: architecture_candidate
decided_by: none
technical_assignment_ref: none
architecture_brief_ref: none
related_patterns: none
related_unknowns: none
related_conflicts: none
## Context
AOS-FARM installer interacts with user target projects and must be extremely careful not to overwrite user data.
## Proposed Decision
Installer must stay safe-by-default.
Existing target project files should not be overwritten silently.
AGENTS.md should not be auto-merged during install.
Installer apply behavior must remain explicit and gated.
## Rationale
To prevent destructive operations on user repositories during installation.
## Alternatives Considered
Auto-merging and auto-overwriting for convenience. Rejected because it causes data loss and safety violations.
## Consequences
Installer will prompt or require manual intervention for conflicts.
## Unknowns
None currently identified.
## Human Review Required
Should install/apply behavior remain gated and conflict-aware before any broader automation?
## Traceability
- source_context: installer boundary, first-start workflow, aos/root/AGENTS.md
- related_workflow: AOS-FARM.619
- related_validator: none
- related_risk_boundary: Install dry-run PASS ≠ apply authorization. Installer check ≠ approval. Existing project files must not be silently overwritten. AGENTS.md must not be auto-merged by default.
## Authority Boundary
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
This ADR is not approval.
This ADR does not authorize execution.
This ADR does not authorize commit.
This ADR does not authorize push.
This ADR does not authorize release.
Human approval cannot be simulated.
Human approval is required before promotion.
