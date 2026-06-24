# AOS-FARM.290 — Human Checkpoint: Batch 3 Destructive Template Cleanup

## Checkpoint Status
checkpoint_status: APPROVED_FOR_EXECUTION

## Human Decision
execution_authorized: true
human_decision_required: false

## Risk Profile
risk_profile_assigned_by_human: HIGH_RISK_PROTECTED
agent_proposed_risk_profile: HIGH_RISK_PROTECTED

## Authorized Target
authorized_task: AOS-FARM.291
authorized_operation: destructive_template_cleanup
git_rm_authorized: true

## Authorized Files
authorized_files:
  - "templates/allowed-forbidden-code-change-template 2.md"
  - "templates/aos-farm-task-verification-input-template 2.md"
  - "templates/aos-farm-task-verification-output-template 2.md"
  - "templates/build-plan-template 2.md"
  - "templates/build-step-batch-scope-template 2.md"
  - "templates/build-step-batch-verification-template 2.md"
  - "templates/clarification-gate-template 2.md"
  - "templates/code-assembly-mvp-evidence-report-template 2.md"
  - "templates/code-assembly-mvp-execution-report-template 2.md"
  - "templates/code-assembly-mvp-human-review-template 2.md"
  - "templates/code-assembly-mvp-input-template 2.md"
  - "templates/code-assembly-traceability-matrix-template 2.md"
  - "templates/code-assembly-verification-report-template 2.md"
  - "templates/code-change-scope-template 2.md"
  - "templates/code-diff-evidence-template 2.md"
  - "templates/code-execution-package-template 2.md"
  - "templates/documentation-assembly-input-template 2.md"
  - "templates/documentation-assembly-output-template 2.md"
  - "templates/documentation-assembly-report-template 2.md"
  - "templates/execution-authorization-package-template 2.md"
  - "templates/feature-intake-template 2.md"
  - "templates/feature-spec-template 2.md"
  - "templates/final-build-step-commit-candidate-template 2.md"
  - "templates/governance-control-gate-matrix-template 2.md"
  - "templates/governance-control-module-contract-template 2.md"
  - "templates/human-approval-boundary-template 2.md"
  - "templates/ide-controller-next-task-template 2.md"
  - "templates/ide-controller-review-report-template 2.md"
  - "templates/manual-code-review-checkpoint-template 2.md"
  - "templates/minimal-safety-floor-checklist-template 2.md"
  - "templates/model-routing-decision-template 2.md"
  - "templates/multi-environment-handoff-template 2.md"
  - "templates/multi-environment-session-start-template 2.md"
  - "templates/safety-gate-matrix-template 2.md"
  - "templates/session-limit-handoff-template 2.md"
  - "templates/spec-to-execution-traceability-matrix-template 2.md"
  - "templates/step-safety-verification-report-template 2.md"
  - "templates/task-brief-chain-template 2.md"
  - "templates/token-budget-task-header-template 2.md"
  - "templates/unknown-not-run-pass-semantics-template 2.md"
  - "templates/verification-evidence-report-template 2.md"

## Boundaries
git_rm_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false

## Important Safety Rules
- No deletion is authorized until Human updates this checkpoint.
- Agent cannot assign LOW_RISK_FAST.
- Destructive operations require explicit Human approval.
- Only exact listed duplicate files may be removed in AOS-FARM.291.

## Human Approval Notes
human_approval_notes: Approved destructive cleanup of exactly the listed duplicate template files only. No other deletion, rename, move, edit, commit, push, release, or production use is authorized.
