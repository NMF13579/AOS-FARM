# REQUIREMENTS.draft.md

```yaml
artifact_status: DRAFT
approval_status: NOT_APPROVED
automation_status: MANUAL_CHAT_DOGFOOD_ONLY
production_status: NOT_PRODUCTION
intake_route: PROBLEM_INTERVIEW
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
final_status: NEEDS_HUMAN_REVIEW
```

## Functional Requirements

- FR-001: The system must preserve a factual history of significant equipment interactions.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-002: The system must support `shift -> shift` handover as a single acceptance act based on factual inspection by the receiving shift.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-003: The system must preserve the declared handover list from the giving shift and the factual acceptance result from the receiving shift.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-004: The system must record mismatches as `nonconformity` without blocking crew work when replacement is unavailable.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-005: The system must support replacement issue and return tracking.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-006: The system must support repair, calibration, write-off, and donor-for-parts lifecycle handling.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true
- FR-007: The system must preserve the minimum significant transfer event fields: who gave, who received, when, which unit, condition, where, and participant confirmation.
  - Status: CANDIDATE_REQUIREMENT
  - Human review required: true

## Data Requirements

- DATA-001: Each equipment unit must have a factual current state distinct from expected assigned state.
  - Status: CANDIDATE_REQUIREMENT
- DATA-002: Equipment condition at transfer must support at least: `working`, `not_working_with_reason`, `working_with_defects`, `incomplete_set`.
  - Status: CANDIDATE_REQUIREMENT
- DATA-003: Equipment lifecycle states must support at least: `with_brigade`, `with_unit`, `in_repair`, `in_calibration`, `lost`, `written_off`, `for_parts`.
  - Status: CANDIDATE_REQUIREMENT

## Access Requirements

- ACCESS-001: Receiving shift must confirm factual acceptance.
  - Status: CANDIDATE_REQUIREMENT
- ACCESS-002: Giving shift must leave a trace of the handed-over equipment list.
  - Status: CANDIDATE_REQUIREMENT
- ACCESS-003: Every employee participating in significant movement must leave an electronic trace.
  - Status: CANDIDATE_REQUIREMENT
- ACCESS-004: Final role-based access matrix remains unresolved and requires human review.
  - Status: NEEDS_HUMAN_REVIEW

## Non-Functional Requirements

- NFR-001: A significant recording action should fit into approximately 5 minutes under real shift conditions.
  - Status: CANDIDATE_REQUIREMENT
- NFR-002: Mobile usage on personal phone or tablet must be a first-class operating scenario.
  - Status: CANDIDATE_REQUIREMENT
- NFR-003: The workflow must preserve brigade continuity and avoid blocking emergency work because of accounting incompleteness alone.
  - Status: CANDIDATE_REQUIREMENT

## Constraints

- CON-001: The system must preserve electronic traceability for significant interactions.
  - Status: CANDIDATE_CONSTRAINT
- CON-002: When replacement is unavailable, brigade work continues with visible exception rather than operational stop.
  - Status: CANDIDATE_CONSTRAINT
- CON-003: Inventory number alone is not a reliable practical verification mechanism.
  - Status: CANDIDATE_CONSTRAINT

## Security / Privacy

- SEC-001: Medical context and accountability handling require later human review for security, privacy, and audit boundaries.
  - Status: NEEDS_HUMAN_REVIEW

## Acceptance Criteria

- AC-001: It is possible to determine factual equipment location and condition for a unit over time.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
- AC-002: It is possible to reconstruct who last transferred and who accepted a unit.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
- AC-003: Replacement issue and return history is preserved.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION
- AC-004: Repair, calibration, and write-off visibility no longer stays only in a disconnected departmental loop.
  - Status: CANDIDATE_ACCEPTANCE_CRITERION

## Out of Scope

- Execution authorization.
- Implementation authorization.
- Final role authorization semantics.
- Production release or deploy decisions.

## UNKNOWN / Open Questions

- UNKNOWN: Exact role-based access matrix is not finalized.
- UNKNOWN: Significant interaction boundaries are not finalized.
- UNKNOWN: Inter-substation exception handling is not finalized.
- UNKNOWN: Reporting and escalation requirements are not finalized.

## Human Decisions Required

- Confirm MVP equipment coverage.
- Confirm significant interaction boundaries.
- Confirm role permissions and escalation chain.
- Confirm reporting package for management.
- Assign Risk Profile before any implementation.
- Authorize any later execution separately.

## Final Status

```yaml
artifact_type: technical_assignment_intake_draft
intake_depth: PROBLEM_INTERVIEW
problem_interview_status: COMPLETED_MANUAL_DOGFOOD
problem_evidence_level: MEDIUM
data_discovery_depth: MEDIUM
information_flow_status: MEDIUM
access_permissions_status: PARTIAL
requirements_confidence: MEDIUM
unknown_count: 4
contradiction_count: 2
inference_count: 1
implementation_hint_count: 2
critical_failure_count: 0
ready_for_requirements_review: true_with_risks
ready_for_execution: false
approval_status: NOT_APPROVED
execution_authorized: false
implementation_authorized: false
commit_authorized: false
push_authorized: false
deploy_authorized: false
production_use_authorized: false
final_status: NEEDS_HUMAN_REVIEW
```
