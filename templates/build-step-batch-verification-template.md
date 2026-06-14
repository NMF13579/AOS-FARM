# Build Step Batch Verification

## Metadata
- verification_id: [ID]
- verified_build_step: [Build Step ID]
- verified_batch_id: [Batch ID]
- verified_execution_task: [Task ID]

## 1. Authorized Scope Check
- authorized_output_count: [Number]
- actual_output_files_present: [true/false]
- created_files: [List]
- modified_files: [List]
- unauthorized_file_modifications_detected: [true/false]
- forbidden_scope_expansion_detected: [true/false]

## 2. Issues and Warnings
- unknown_or_not_run_in_critical_checks: [true/false]
- blocking_issue_count: [Number]
- warning_count: [Number]

## 3. Authorizations
- may_continue_with_next_bounded_batch: [true/false]
- may_prepare_final_build_step_verification: [true/false]
- may_prepare_final_commit_authorization: [true/false]
- commit_authorized_now: false
- push_authorized_now: false

## 4. Status
- final_status: [Status]

## Important Notes
Verification PASS ≠ approval.
Evidence ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.

## Required Invariants
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
