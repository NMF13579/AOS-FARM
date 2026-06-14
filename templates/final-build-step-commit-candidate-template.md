# Final Build Step Commit Candidate

## Metadata
- build_step_id: [ID]
- final_verification_report: [Path]

## 1. Candidate Files
- candidate_file_count: [Number]
- candidate_files:
  - [File 1]
  - [File 2]

## 2. Excluded Files
- excluded_files: [List]

## 3. Issues
- blocking_issues: [List]
- warnings: [List]

## 4. Authorizations
- human_commit_authorization_required: true
- commit_authorized_now: false
- push_authorized_now: false
- release_authorized_now: false
- production_use_authorized_now: false

## 5. Proposed Commit
- recommended_commit_message: [Message]

## Important Notes
Final Build Step verification ≠ commit authorization.
Commit authorization ≠ push authorization.
Commit ≠ release.
Push ≠ release.
Human Commit Authorization is required before git add / commit.
Human Push Authorization is required before git push.

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
