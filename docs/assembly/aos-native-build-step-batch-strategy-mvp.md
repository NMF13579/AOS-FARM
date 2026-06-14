# AOS-native Build Step Batch Strategy MVP

## 1. Purpose
Defines the reusable execution boundary and commit strategy for AOS-FARM / AgentOS Next Build Steps.

## 2. Non-Goals
This document does not authorize any specific execution.
It does not dictate business logic.
It does not replace core governance rules.

## 3. Build Step Batch Model
One Build Step may contain multiple bounded execution batches.

## 4. Execution Batch Lifecycle
Build Step scope
→ batch scope proposal
→ execution authorization package
→ Human Execution Checkpoint
→ bounded execution
→ post-execution verification
→ next bounded batch or final Build Step verification
→ final commit candidate preparation
→ Human Commit Authorization
→ commit
→ push authorization package
→ Human Push Authorization
→ push
→ remote baseline closure

## 5. Batch Size Policy
Batch sizing depends on the risk and artifact type.

## 6. Documentation / Template Batch Rules
Documentation/template batches may be larger.

## 7. Scripts / Runtime / Validator Batch Rules
Scripts/runtime/validators/workflows batches must be smaller.

## 8. Protected / Canonical Change Rules
Protected/canonical changes require separate human checkpoint.

## 9. Deferred Commit / Push Strategy
Intermediate commit/push is deferred by default inside a Build Step.
Final commit candidate set is prepared only after final Build Step verification.
Push remains separate from commit.

## 10. Final Build Step Verification Boundary
Final Build Step verification ensures that all batches executed within the Build Step adhere to their authorized scope.

## 11. Final Commit Candidate Boundary
The final commit candidate set bundles the entire verified outcome of the Build Step for final commit authorization.

## 12. Step 3 Carry-Forward Policy
Step 3 may reuse deferred commit/push strategy but must not inherit Step 2 documentation-batch size automatically.

## 13. Forbidden Expansions
UNKNOWN / NOT_RUN / BLOCKED remain fail-closed.
Each execution batch requires Human Execution Authorization.
Each execution batch requires post-execution verification.

## 14. Required Invariants
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Verification PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
Human approval cannot be simulated.
Scope proposal ≠ execution authorization.
Execution authorization preparation ≠ execution authorization.
Execution authorization ≠ commit authorization.
Commit authorization ≠ push authorization.
Final Build Step verification ≠ commit authorization.
Documentation output ≠ approval.
Documentation output ≠ release.
Commit ≠ release.
Push ≠ release.

## 15. Minimal Example Flow
1. Propose scope.
2. Prepare execution authorization.
3. Obtain human execution approval.
4. Execute batch.
5. Verify batch.
6. If Build Step is done, perform final verification.
7. Prepare commit candidate.
8. Obtain human commit approval.
9. Commit.
10. Prepare push authorization.
11. Obtain human push approval.
12. Push.
