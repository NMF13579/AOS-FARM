# Clarification Gate

## Metadata
- clarification_id: [ID]
- related_feature_id: [Feature ID]
- resolution_status: [READY_FOR_PLAN | BLOCKED | HUMAN_REVIEW_REQUIRED]

## 1. Blocking Questions
[Questions that prevent planning or execution]

## 2. Non-Blocking Questions
[Questions that can be deferred]

## 3. Assumptions Prohibited
[List of assumptions that the agent is not allowed to make autonomously]

## 4. Unknown Items
[List of unknowns. Must be cleared before READY_FOR_PLAN.]

## 5. Human Answers Required
[Explicit questions directed at the human owner]

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
