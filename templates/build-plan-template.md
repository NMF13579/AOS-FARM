# Build Plan

## Metadata
- plan_id: [ID]
- related_feature_id: [Feature ID]

## 1. Authorized Scope
[What is within the boundaries of this plan?]

## 2. Implementation Strategy
[High-level approach]

## 3. Artifact Plan
[List of artifacts to be created or modified]

## 4. Allowed Paths
[Strict list of file paths that can be touched]

## 5. Forbidden Paths
[Explicit paths that must not be touched]

## 6. Risk Profile Proposal
[Agent's proposed risk profile. Agent may propose Risk Profile but cannot self-assign LOW_RISK_FAST.]

## 7. Validation Plan
[How will this be tested or verified?]

## 8. Rollback or Stop Conditions
[When should execution halt?]

## Important Notes
Plan is not execution authorization.
Agent may propose Risk Profile but cannot self-assign LOW_RISK_FAST.

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
