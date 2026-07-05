# ADR-0001 — Markdown-first Source of Truth
## Status
PROPOSED
## Decision Type
architecture_candidate
## Metadata
adr_id: ADR-0001
title: Markdown-first Source of Truth
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
AOS-FARM requires a clear definition of where the definitive truth of its architecture and state lives.
## Proposed Decision
Markdown/YAML documents are the primary Source of Truth.
Generated indexes, JSON, caches, SQLite, helper outputs and reports are derived or supporting artifacts unless explicitly promoted by human approval.
## Rationale
To ensure human readability, version control history, and clear boundaries between generated artifacts and authoritative decisions.
## Alternatives Considered
Using a database or strictly structured JSON for all architectural state. Rejected because it reduces human readability.
## Consequences
All automated tools must treat Markdown/YAML documents as the source and only generate derived artifacts from them.
## Unknowns
None currently identified.
## Human Review Required
Should Markdown-first remain the default Source of Truth model for AOS-FARM?
## Traceability
- source_context: 00_AOS_Core_Control.md, 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md, 02_AOS_Governance_Control_Module_and_Safety_Rules.md
- related_workflow: AOS-FARM.619
- related_validator: none
- related_risk_boundary: Generated artifact ≠ Source of Truth unless explicitly promoted. Evidence ≠ approval. PASS ≠ approval.
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
