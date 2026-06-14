# Verification / Evidence Report

## Metadata
- verification_id: [ID]
- verified_task: [Task ID]

## 1. Commands Run
[Exact list of commands executed]

## 2. Files Created
[Exact list of files created]

## 3. Files Modified
[Exact list of files modified]

## 4. Allowed Scope Check
[Did the execution stay within allowed paths?]

## 5. Forbidden Scope Check
[Did the execution touch any forbidden paths?]

## 6. Evidence Items
[Verifiable outputs and logs]

## 7. Unknown or Not Run Items
[List of skipped checks or unresolved UNKNOWNs]

## 8. Blocking Issues
[Issues that prevent marking this as a PASS]

## 9. Warnings
[Non-blocking anomalies]

## 10. Final Status
- final_status: [PASS | PASS_WITH_WARNINGS | BLOCKED | HUMAN_REVIEW_REQUIRED]

## Important Notes
Evidence ≠ approval.
Verification PASS ≠ approval.
NOT_RUN ≠ PASS.
UNKNOWN ≠ OK.

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
