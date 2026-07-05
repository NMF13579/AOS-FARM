# ADR-0002 — Validator Before Canonical Promotion
## Status
PROPOSED
## Decision Type
architecture_candidate
## Metadata
adr_id: ADR-0002
title: Validator Before Canonical Promotion
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
AOS-FARM needs a way to ensure architectural documents are correctly structured before they reach a human for review and eventual promotion.
## Proposed Decision
Architecture documents should be validator-checkable before any future protected/canonical promotion checkpoint.
## Rationale
To prevent malformed or unsafe architecture documents from being manually reviewed or accidentally promoted.
## Alternatives Considered
Manual structural review only. Rejected as error-prone and unscalable.
## Consequences
All architecture documents must pass the validator script. Validator PASS only means structural/safety validation passed.
## Unknowns
None currently identified.
## Human Review Required
Should validator PASS be required before any future protected/canonical promotion checkpoint?
## Traceability
- source_context: AOS-FARM.618, AOS-FARM.619
- related_workflow: AOS-FARM.619
- related_validator: aos/scripts/aos_architecture_document_check.py, tests/test_aos_architecture_document_check.py
- related_risk_boundary: Validator PASS ≠ approval. Validator PASS only means structural/safety validation passed. Validator PASS does not authorize canonical promotion.
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
