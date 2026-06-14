# Task Brief Chain

## Metadata
- chain_id: [ID]
- related_plan_id: [Plan ID]

## 1. Task Sequence
[Ordered list of tasks to execute]

## 2. Task Dependencies
[Links between tasks]

## 3. Per-Task Breakdown

### Task: [Task Name]
- per_task_scope: [Scope]
- per_task_allowed_paths: [Allowed Paths]
- per_task_forbidden_paths: [Forbidden Paths]
- per_task_validation: [Validation commands/checks]
- per_task_expected_report: [Expected evidence artifact]

## 4. Human Checkpoint Requirements
[Which tasks require explicit human checkpoints before proceeding]

## Important Notes
Task brief is not approval.
Task chain readiness does not start execution.

## AOS Invariants
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Verification PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
Human approval cannot be simulated.
Execution authorization preparation ≠ execution authorization.
Execution authorization ≠ commit authorization.
Commit authorization ≠ push authorization.
Spec Kit pattern reference ≠ Spec Kit dependency.
Spec Kit guidance ≠ AOS governance authority.
Documentation output ≠ approval.
Documentation output ≠ release.
