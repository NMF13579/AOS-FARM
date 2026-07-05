# ADR-0003 — Manual Queue Over Autonomous Runner
## Status
PROPOSED
## Decision Type
architecture_candidate
## Metadata
adr_id: ADR-0003
title: Manual Queue Over Autonomous Runner
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
AOS-FARM needs to decide how tasks are picked up and executed in the first-start workflow.
## Proposed Decision
AOS-FARM prefers manual task queue and thin helpers over autonomous execution runner by default.
## Rationale
To maintain explicit human control and safety over the execution flow.
## Alternatives Considered
Fully autonomous runner. Rejected because it violates the safe-by-default control model.
## Consequences
Users must manually approve and advance tasks in the queue.
## Unknowns
None currently identified.
## Human Review Required
Should autonomous runner behavior remain out of the default first-start workflow?
## Traceability
- source_context: manual task queue, thin helper, first-start workflow
- related_workflow: AOS-FARM.619
- related_validator: none
- related_risk_boundary: Queue readiness ≠ execution authorization. Task candidate ≠ execution authorization. Agent helper ≠ autonomous runner.
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
