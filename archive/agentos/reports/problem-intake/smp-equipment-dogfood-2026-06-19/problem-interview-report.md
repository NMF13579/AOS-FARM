# Problem Interview Report

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

## Interview Route

`PROBLEM_INTERVIEW` performed manually in chat and preserved as dogfood evidence.

## Problem

The station cannot reliably determine the factual availability, condition, location, and accountable holder of equipment because the formal accounting loop diverges from real operational movement.

## Target User

- Ambulance crews.
- Duty room.
- Senior feldsher.
- Station manager.
- Material support department.
- Higher medical management.

## Current Workflow

Equipment enters through a centralized health department intake, is documented and distributed, then moves between substations, crews, the duty room, repair, and calibration loops. The formal handover ritual exists, but factual equipment verification is incomplete and secondary records are inconsistent.

## Target Outcome

A draft technical assignment for a system that preserves factual movement and condition history while keeping crew operations moving even when mismatches or missing replacements exist.

## Key Findings

- The main breakdown is `shift -> shift` handover.
- Paper checklists and journals do not preserve factual state reliably.
- Duty room replacement issuance is a major traceability gap.
- Material support department is the primary control point for repair, calibration, and write-off.
- Brigade continuity is operationally prioritized over perfect compliance.

## Risks

- Formal accountability differs from factual accountability.
- Loss is often discovered later than it happened.
- Repair return quality is verified too late, often by the receiving brigade.
- Expired calibration or imperfect equipment may still stay in use when replacement is unavailable.
- A naive "record everything" workflow could become too heavy for crews.

## UNKNOWN / Open Questions

- UNKNOWN: Exact role-based access matrix is not finalized.
- UNKNOWN: The formal definition of significant interaction versus ordinary use is not finalized.
- UNKNOWN: Inter-substation exception handling needs more detail.
- UNKNOWN: Required management reports and escalation thresholds are not finalized.

## Final Status

final_status: NEEDS_HUMAN_REVIEW
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
