# Forbidden Behavior Evidence Mapping

## Task identity
- **Task ID**: [TASK_ID]
- **Related Task Quality Package**: [PATH_TO_QUALITY_PACKAGE]
- **Functional Intent Reference**: [PATH_TO_FUNCTIONAL_INTENT_SOURCE]

## Forbidden behaviors list
- [FB_001]: [Statement of forbidden behavior]
- [FB_002]: [Statement of forbidden behavior]

## Evidence mapping table

| forbidden_behavior_id | forbidden_behavior_statement | evidence_item | evidence_path_or_command | verification_method | verification_status | human_review_note |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FB_001 | No automatic approval | EV_001 | `reports/evidence.md` | `manual_review` | `VERIFIED` | Reviewed by human |

## Verification method definitions

### Code-backed checks
Checks performed automatically by validators or tests.

### Manual checks
Checks requiring explicit human inspection.

## NOT_RUN items
Items that were intentionally skipped. (Must be justified).

## UNKNOWN items
Items whose status could not be determined. (Requires human review).

## Human Review boundary
- PASS is not approval.
- Evidence is not approval.
- Mapping validation is not approval.
- Human approval cannot be simulated.
- Human Review required.
- This mapping does not grant commit/push/merge/release authorization.

## Final mapping status
[STATUS]
