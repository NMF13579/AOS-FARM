# Build Step Batch Scope Proposal

## Metadata
- build_step_id: [ID]
- batch_id: [ID]
- batch_name: [Name]
- batch_type: [Type]

## 1. Goal
- batch_goal: [Goal]

## 2. Non-Goals
- batch_non_goals: [Non-Goals]

## 3. Allowed Paths
- allowed_paths:
  - [Path 1]
  - [Path 2]

## 4. Forbidden Paths
- forbidden_paths:
  - [Path 1]
  - [Path 2]

## 5. Output Files
- proposed_output_files:
  - [Path 1]
- proposed_output_count: [Number]

## 6. Dependencies
- dependencies: [List]

## 7. Risk Profile
- risk_profile_proposal: [Profile]

## 8. Verification and Checkpoints
- human_checkpoint_required: true
- verification_required: true

## 9. Strategy
- commit_strategy: [Strategy]
- push_strategy: [Strategy]

## 10. Unknowns and Blocking Conditions
- unknowns: [List]
- blocking_conditions: [List]

## Important Notes
Scope proposal ≠ execution authorization.
Risk Profile proposal ≠ Risk Profile assignment.
Agent may propose Risk Profile but cannot self-assign LOW_RISK_FAST.

## Required Invariants
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
Final Build Step verification ≠ commit authorization.
Documentation output ≠ approval.
Documentation output ≠ release.
Commit ≠ release.
Push ≠ release.
