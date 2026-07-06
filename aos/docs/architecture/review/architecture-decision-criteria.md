---
task_id: AOS-FARM.621
document_type: architecture_decision_criteria
criteria_status: READY_FOR_HUMAN_WEIGHTING
approval_status: NOT_REQUESTED
human_weight_required: true
human_review_required: true
is_approval: false
---

# Architecture Decision Criteria

This document defines criteria that require future human weighting before stack or pattern decisions can be promoted.
It is not an approval record.

## Criteria

### Markdown-first compatibility

weight: UNASSIGNED_BY_HUMAN
source: ADR-0001 / registry / project constraint
human_weight_required: true

Architecture evidence and decisions should preserve Markdown as the auditable source of truth.

### Validator-first lifecycle

weight: UNASSIGNED_BY_HUMAN
source: ADR-0002 / registry / project constraint
human_weight_required: true

Architecture artifacts should be checkable before canonical promotion.

### Human-gated approval

weight: UNASSIGNED_BY_HUMAN
source: ADR-0005 / project constraint
human_weight_required: true

Architecture selection must remain separated from agent-generated recommendations.

### Local-first operation

weight: UNASSIGNED_BY_HUMAN
source: ADR-0003 / registry / project constraint
human_weight_required: true

Architecture workflow should preserve local operation where possible and avoid unnecessary external runtime authority.

### Non-programmer usability

weight: UNASSIGNED_BY_HUMAN
source: registry / project constraint
human_weight_required: true

Architecture workflow should be understandable and usable by non-programmer owners without hiding approval boundaries.

### Safe installer boundary

weight: UNASSIGNED_BY_HUMAN
source: ADR-0004 / project constraint
human_weight_required: true

Installer-related architecture must preserve safe-create behavior and avoid destructive default actions.

### Low operational burden

weight: UNASSIGNED_BY_HUMAN
source: registry / project constraint
human_weight_required: true

Architecture choices should account for maintenance, deployment, external service, and support burden.

### Extensibility

weight: UNASSIGNED_BY_HUMAN
source: registry / project constraint
human_weight_required: true

Architecture choices should allow future project growth without premature complexity.

### Fail-closed semantics

weight: UNASSIGNED_BY_HUMAN
source: ADR-0002 / project constraint
human_weight_required: true

Architecture workflow should prefer explicit blocked or human-review states over inference.

### Minimal runtime authority

weight: UNASSIGNED_BY_HUMAN
source: ADR-0003 / project constraint
human_weight_required: true

Runtime components should receive no more authority than the workflow needs.

### No autonomous runner by default

weight: UNASSIGNED_BY_HUMAN
source: ADR-0003 / project constraint
human_weight_required: true

Architecture workflow should preserve manual queue semantics unless a future human checkpoint changes scope.

### Product folder boundary preservation

weight: UNASSIGNED_BY_HUMAN
source: registry / project constraint
human_weight_required: true

Architecture choices should preserve project folder boundaries and avoid cross-product mutation by default.

## Non-decision note

These criteria are ready for human weighting only.
No criterion weight has been assigned by agent.
