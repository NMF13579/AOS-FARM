# Task-to-Code Execution Bridge

## Status
```yaml
document_type: control_bridge_specification
project: AOS-FARM
status: active
source_pack_role: core_required
language: en
```

## Purpose
This document defines the safe, non-autonomous transition from an approved Task Brief to a Code Execution Package. 

## The Bridge Contract
1. **Task Brief is NOT Execution Authorization**: Having a Task Brief does not grant permission to execute. A separate, explicitly human-assigned Risk Profile and Human Execution Authorization are required.
2. **Task Queue Position is NOT Execution Authorization**: Being next in the queue does not automatically start execution.
3. **Execution Package Valid is NOT Approval**: The creation and validation of an Execution Package do not constitute human approval to commit or merge.
4. **Code Quality Reported is NOT Approval**: Passing quality control only means the report is ready for a human to review.

## Allowed States
- `TASK_TO_CODE_BRIDGE_BLOCKED`
- `CODE_EXECUTION_PACKAGE_CANDIDATE_CREATED_HUMAN_AUTHORIZATION_REQUIRED`

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- Human approval cannot be simulated.
- Skeleton ≠ implementation.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.
