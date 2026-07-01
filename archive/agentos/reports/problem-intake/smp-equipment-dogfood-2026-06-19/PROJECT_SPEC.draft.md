# PROJECT_SPEC.draft.md

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

## 1. Source Status

| Field | Value |
|---|---|
| Entry Route | PROBLEM_INTERVIEW |
| Problem Interview Status | COMPLETED_MANUAL_DOGFOOD |
| Ready For Execution | false |
| Approval Status | NOT_APPROVED |
| Missing Sections Status | NEEDS_HUMAN_REVIEW |

## 2. User Vision

The station needs to know what equipment factually exists, what condition it is in, where it is at a given time, and who last interacted with it.

## 3. Data Discovery

Relevant data includes equipment identity, assigned unit, factual location, current condition, completeness, repair state, calibration state, write-off state, donor-for-parts state, and accountable transfer history.

## 4. Information Flow

Central intake -> station documentation -> substation distribution -> brigade assignment -> shift handover / duty room issuance / inter-substation transfer / repair / calibration / write-off -> factual state recovery and accountability trace.

## 5. Access / Permissions

Operational visibility and escalation involve brigades, duty room, senior feldsher, station manager, and material support department. Human approval remains required for any execution, implementation, commit, push, or production use decision.

## 6. Problem Evidence

- Shift handover is frequently formal rather than factual.
- Duty room and Excel tracking do not preserve the real state consistently.
- Loss and mismatch responsibility are often inferred from discovery time rather than factual transfer chain.
- Repair and calibration loops are visible mainly to the material support department.

## 7. Optional Current Workflow

The current workflow is partially formalized but operationally reactive. Brigades often discover issues first, the duty room finds replacements, and management or material support reconstructs responsibility after the fact.

## 8. Requirements Draft

- Preserve factual history for significant equipment interactions.
- Support shift handover as a single acceptance act centered on factual inspection by the receiving shift.
- Preserve replacement issue and return history.
- Preserve repair, calibration, write-off, and donor-for-parts lifecycle transitions.
- Keep the brigade working even when mismatch or expired service state exists and no replacement is available.

## 9. Implementation Hints

The operating surface should be mobile-first and optimized for short event capture. Inventory numbers alone are not sufficient as the practical verification mechanism.

## 10. Negative Constraints

- The system must not simulate approval.
- The system must not imply execution authorization.
- The system must not block emergency work solely because the accounting loop is incomplete.
- UNKNOWN items must remain visible.

## 11. Acceptance Criteria

- Draft material captures `as-is` and `to-be` process logic for equipment control.
- Required transfer facts are explicit.
- Significant operational exceptions remain visible.
- No output declares approval or execution authorization.

## 12. MVP

Initial scope should center on expensive equipment and the highest-friction flows: shift handover, replacement issue/return, factual location tracking, and visibility into repair and calibration status.

## 13. UNKNOWN / Open Questions

- UNKNOWN: Exact role-based access matrix is not finalized.
- UNKNOWN: Significant interaction boundaries are not finalized.
- UNKNOWN: Inter-substation exceptions need more detail.
- UNKNOWN: Reporting and escalation requirements are not finalized.

## 14. Contradictions

- Formal checklist completion does not guarantee factual equipment verification.
- Service-expired or defective equipment may remain in operational use when no replacement exists.

## 15. Human Decisions Required

- Confirm role boundaries and access rights.
- Confirm which interactions must be mandatory in MVP.
- Confirm which equipment categories are in first implementation scope.
- Confirm management reporting requirements.
- Assign downstream Risk Profile before any implementation task.
- Authorize execution separately if a future scoped task is prepared.

## 16. Final Status

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
