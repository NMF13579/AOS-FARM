# Execution Authorization Package

## Metadata
- package_id: [ID]
- package_type: [Type]
- package_status: [Status]
- target_execution_task: [Target Task]

## 1. Authorized Scope Proposal
[What is being proposed for authorization?]

## 2. Allowed Paths
[Strict list of allowed paths]

## 3. Forbidden Paths
[Strict list of forbidden paths]

## 4. Risk Profile for Human Review
[Proposed risk profile requiring human sign-off]

## 5. Required Preconditions
[What must be true before execution can start?]

## 6. Non-Authorizations
[What is explicitly NOT authorized (e.g. push, commit, Spec Kit)]

## 7. Human Checkpoint Path
- human_checkpoint_path: [Path to the corresponding checkpoint file]

## Important Notes
Execution authorization package is not approval.
Human Checkpoint is required before execution.

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
