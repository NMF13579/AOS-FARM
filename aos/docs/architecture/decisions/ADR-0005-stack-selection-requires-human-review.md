# ADR-0005 — Stack Selection Requires Human Review
## Status
PROPOSED
## Decision Type
architecture_candidate
## Metadata
adr_id: ADR-0005
title: Stack Selection Requires Human Review
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
AOS-FARM provides stack presets but must not make implicit architectural choices for the user.
## Proposed Decision
AOS may explain and propose stack choices, but must not silently select, approve, or activate a default stack.
## Rationale
To ensure the user is fully aware and explicitly authorizes the architecture stack being used.
## Alternatives Considered
Default active stacks. Rejected as it bypasses user consent and architecture governance.
## Consequences
Stack selection is an explicit gated process requiring human approval.
## Unknowns
None currently identified.
## Human Review Required
Should stack presets be introduced as PROPOSED candidates in a later dedicated stage?
## Traceability
- source_context: Stack selection
- related_workflow: AOS-FARM.619
- related_validator: none
- related_reference: aos/docs/architecture/architecture-anti-pattern-catalog.md
- related_risk_boundary: Stack recommendation ≠ approval. Stack Choice Map ≠ default stack selection. Stack preset PASS ≠ implementation authorization. Human review is required before ACTIVE default use.
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
