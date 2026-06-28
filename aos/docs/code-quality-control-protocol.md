# Code Quality Control Protocol

## Status
```yaml
document_type: control_protocol_specification
project: AOS-FARM
status: active
source_pack_role: core_required
language: en
```

## Purpose
Defines the code quality requirements, forbidden operations, and deterministic validation criteria for a Code Execution Package in the `AOS-FARM.451` controlled corridor.

## Required Invariants
The protocol guarantees that:
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Code Quality reported ≠ approval.

## Overengineering Gate
The validator ensures the package does not exhibit:
- Autonomous runner behaviors
- Auto-fix or auto-commit behaviors
- Release automation
- Lifecycle mutation automation
- Risk Profile auto-assignment
- Approval automation
- Next task auto-start

## Allowed Validation Statuses
- `CODE_QUALITY_BLOCKED`
- `CODE_QUALITY_REPORTED_HUMAN_REVIEW_REQUIRED`
- `CODE_QUALITY_VALIDATION_REPORTED_NO_APPROVAL`

**Validator must never emit:** `APPROVED`, `READY_FOR_RELEASE`, `READY_FOR_MERGE`, or `PASS-as-approval`.
