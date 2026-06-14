# AOS-FARM.96.5 — Build Step 2 Next Bounded Batch Scope Proposal

## 1. Why Step 2 Should Continue
The deferred commit strategy explicitly permits extending the uncommitted Step 2 workspace using bounded execution batches. Step 2 currently defines documentation structure and spec-to-execution templates. A missing structural link is the strategy for organizing future execution batches and Build Steps themselves.

## 2. Why Final Step 2 Verification is Premature
Step 2 scope is not yet complete. The operational rules for how batches within a Build Step are authorized and verified have not been explicitly codified into AOS-native templates. Final verification should occur only when no more execution batches are planned for Step 2.

## 3. Why Final Step 2 Commit Authorization is Premature
Commit authorization follows final verification. Because final verification is premature, preparing commit authorization now would violate the dependency chain established in AOS-FARM.95.1.

## 4. Proposed Next Bounded Batch
**AOS-native Build Step Batch Strategy MVP**

Future sequence:
- AOS-FARM.96.6 — Build Step 2 Batch Strategy Execution Authorization Preparation
- AOS-FARM.96.7 — Human Execution Authorization for Build Step 2 Batch Strategy MVP
- AOS-FARM.96.8 — Build Step 2 Batch Strategy MVP Execution
- AOS-FARM.96.9 — Post-Execution Verification for Build Step Batch Strategy MVP

## 5. Proposed Future Output Files
- docs/assembly/aos-native-build-step-batch-strategy-mvp.md
- templates/build-step-batch-scope-template.md
- templates/build-step-batch-verification-template.md
- templates/final-build-step-commit-candidate-template.md
- reports/aos-farm-build-step-batch-strategy-mvp-report.md

## 6. Proposed Allowed Paths
```text
docs/assembly/aos-native-build-step-batch-strategy-mvp.md
templates/build-step-batch-scope-template.md
templates/build-step-batch-verification-template.md
templates/final-build-step-commit-candidate-template.md
reports/aos-farm-build-step-batch-strategy-mvp-report.md
```

## 7. Proposed Forbidden Paths
```text
All existing core governance files
All existing MVP files
All executable scripts, workflow files, and runtime enforcement artifacts
Code Assembly artifacts
```

## 8. Risk Rationale
The proposed batch is strictly limited to creating 5 new markdown documentation and template files. It carries no risk of executable deployment, repository corruption, or unapproved commits, remaining completely bounded and fail-closed.

## 9. Step 3 Carry-Forward Policy
Step 3 may reuse the same deferred commit/push strategy as Step 2.

However, Step 3 batch size must be smaller if it touches scripts, runtime, validators, workflows, generated code, or protected/canonical sources.

Step 3 must not inherit Step 2 documentation-batch size automatically.

Step 3 must define its own allowed paths, forbidden paths, Risk Profile, execution authorization, and verification boundary.

## 10. Decision Fields
```yaml
task_id: AOS-FARM.96.5
stage_type: next_bounded_batch_scope_proposal

current_branch: "dev"
head_sha: "1f3fb3a6ec0387a1eb7648270700fd0b9ed031eb"
origin_dev_sha: "1f3fb3a6ec0387a1eb7648270700fd0b9ed031eb"
head_equals_origin_dev: true
dev_ahead_origin_dev_by: 0

deferred_step_2_commit_strategy_active: true
may_continue_step_2_with_next_bounded_batch: true
may_prepare_final_step_2_verification: false
may_prepare_final_step_2_commit_authorization: false

proposed_next_batch: "AOS-native Build Step Batch Strategy MVP"
proposed_future_output_count: 5
proposed_next_task: "AOS-FARM.96.6 — Build Step 2 Batch Strategy Execution Authorization Preparation"

execution_authorized_now: false
commit_authorized_now: false
push_authorized_now: false
release_authorized_now: false
production_use_authorized_now: false

blocking_issue_count: 0
warning_count: 0
```

## 11. Invariants Confirmation
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Verification PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
Human approval cannot be simulated.
Scope proposal ≠ execution authorization.
Execution authorization ≠ commit authorization.
Commit authorization ≠ push authorization.
Final Build Step verification ≠ commit authorization.
Documentation output ≠ approval.
Documentation output ≠ release.

## 12. Final Status
AOS_FARM_96_5_NEXT_BOUNDED_BATCH_SCOPE_PROPOSED
