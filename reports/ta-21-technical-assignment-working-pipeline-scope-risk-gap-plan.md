# TA 21 - Technical Assignment Working Pipeline Scope / Risk / Gap Plan

```yaml
task_id: TA-21
mode: authorization-prep / report-writing
repository: AOS-FARM
final_status: TA_21_EXECUTION_AUTHORIZATION_PREPARED
approval_status: NOT_APPROVED
execution_authorized: false
implementation_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
```

## 1. Scope Boundary

TA 21 prepares authorization materials only.

Allowed in TA 21:

- read required AOS sources;
- inspect repository state;
- inspect technical-assignment methodology, scripts, templates, reports, and checkpoints;
- identify gaps;
- propose a future exact allowed file set for TA 23 through TA 25;
- propose branch and dirty-worktree policy;
- propose Risk Profile;
- create this report, the TA 21 execution authorization package, and the pending human checkpoint draft.

Forbidden in TA 21:

- no implementation;
- no runner changes;
- no validator changes;
- no bridge implementation;
- no fixtures;
- no dogfood;
- no cleanup;
- no delete / move / rename;
- no branch creation;
- no staging;
- no commit;
- no push;
- no release;
- no production use;
- no approval simulation.

## 2. Repository State

Required read-only commands were run.

```yaml
branch: dev
HEAD: 20959c41dd836a78b456ab1d66bc32ded7396b32
origin_dev: 20959c41dd836a78b456ab1d66bc32ded7396b32
upstream_ahead_behind: "0 0"
dirty_worktree_detected: true
tracked_modifications_detected: false
staged_changes_detected: false
untracked_files_detected: true
```

Required commands:

```text
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse origin/dev
git rev-list --left-right --count origin/dev...HEAD
git status --short
git status -sb
```

Observed dirty worktree inventory:

```text
?? "docs/assembly/aos-native-build-step-batch-strategy-mvp 2.md"
?? "docs/assembly/aos-native-spec-to-execution-pattern-pack-mvp 2.md"
?? "docs/assembly/code-assembly-pipeline-contract 2.md"
?? "docs/assembly/code-assembly-pipeline-mvp 2.md"
?? "docs/assembly/code-diff-evidence-expectations 2.md"
?? "docs/assembly/documentation-assembly-pipeline-mvp 2.md"
?? "docs/assembly/documentation-assembly-pipeline-skeleton 2.md"
?? "docs/assembly/task-brief-to-scoped-code-change 2.md"
?? "docs/governance/governance-control-module-contract 2.md"
?? "docs/governance/human-checkpoint-boundary 2.md"
?? "docs/governance/minimal-safety-floor 2.md"
?? "docs/governance/pass-evidence-approval-boundary 2.md"
?? "docs/governance/unknown-not-run-pass-semantics 2.md"
?? "docs/operations/agent-routing-policy 2.md"
?? "docs/operations/ide-architect-controller-mode 2.md"
?? "docs/operations/multi-environment-agent-workflow 2.md"
?? "docs/operations/token-budget-and-model-routing-policy 2.md"
?? "docs/validation/aos-farm-task-verification-checker-contract 2.md"
?? "reports/aos-farm-100-step-3-batch-1-post-execution-verification 2.md"
?? "reports/aos-farm-101-final-step-3-verification 2.md"
?? "reports/aos-farm-102-final-step-3-commit-authorization-package 2.md"
?? reports/aos-farm-104-step-3-commit-push-authorization-package.md
?? reports/aos-farm-108-step-3-post-push-remote-baseline-closure.md
?? "reports/aos-farm-109-build-step-4-scope-risk-batch-plan 2.md"
?? "reports/aos-farm-109-step-4-batch-1-execution-authorization-package 2.md"
?? "reports/aos-farm-112-step-4-batch-and-final-verification 2.md"
?? "reports/aos-farm-113-final-step-4-commit-authorization-package 2.md"
?? reports/aos-farm-115-step-4-commit-push-authorization-package.md
?? reports/aos-farm-117-step-4-push-and-remote-baseline-closure.md
?? "reports/aos-farm-118-build-step-5-scope-risk-batch-plan 2.md"
?? "reports/aos-farm-118-step-5-batch-1-execution-authorization-package 2.md"
?? "reports/aos-farm-121-step-5-batch-and-final-verification 2.md"
?? "reports/aos-farm-122-deep-step-5-audit 2.md"
?? "reports/aos-farm-123-final-step-5-commit-authorization-package 2.md"
?? reports/aos-farm-125-step-5-commit-push-authorization-package.md
?? reports/aos-farm-127-3-closure-evidence-commit-push-authorization-package.md
?? "reports/aos-farm-127-closure-evidence-recovery-commit-authorization-package 2.md"
?? "reports/aos-farm-127-step-5-push-and-remote-baseline-closure 2.md"
?? "reports/aos-farm-128-multi-environment-ide-controller-token-routing-implementation-report 2.md"
?? "reports/aos-farm-129-multi-environment-controller-commit-authorization-package 2.md"
?? reports/aos-farm-131-multi-environment-controller-commit-push-authorization-package.md
?? "reports/aos-farm-134-build-step-6-dogfood-scope-risk-batch-plan 2.md"
?? "reports/aos-farm-134-step-6-batch-1-execution-authorization-package 2.md"
?? "reports/aos-farm-135-build-step-6-controller-review-report 2.md"
?? "reports/aos-farm-135-build-step-6-dogfood-evidence-report 2.md"
?? "reports/aos-farm-135-build-step-6-dogfood-session-start 2.md"
?? "reports/aos-farm-135-build-step-6-model-routing-decision 2.md"
?? "reports/aos-farm-136-build-step-6-dogfood-batch-1-post-execution-verification 2.md"
?? "reports/aos-farm-137-build-step-6-commit-authorization-package 2.md"
?? "reports/aos-farm-137-final-build-step-6-dogfood-verification 2.md"
?? reports/aos-farm-139-build-step-6-dogfood-commit-push-authorization-package.md
?? "reports/aos-farm-142-1-task-verification-checker-contract-report 2.md"
?? "reports/aos-farm-142-build-step-7-controller-loop-scope-risk-batch-plan 2.md"
?? reports/aos-farm-167-controller-loop-handoff-commit-push-authorization-package.md
?? reports/aos-farm-172-controller-loop-handoff-closure-evidence-commit-push-authorization-package.md
?? reports/aos-farm-174-controller-loop-handoff-final-remote-baseline-closure.md
?? reports/aos-farm-181-step-8-commit-push-authorization-package.md
?? reports/aos-farm-183-step-8-push-and-remote-baseline-closure.md
?? reports/aos-farm-190-step-9-commit-push-authorization-package.md
?? reports/aos-farm-192-step-9-push-and-remote-baseline-closure.md
?? reports/aos-farm-199-step-10-commit-push-authorization-package.md
?? reports/aos-farm-201-step-10-push-and-remote-baseline-closure.md
?? reports/aos-farm-208-step-11-commit-push-authorization-package.md
?? reports/aos-farm-210-step-11-push-and-remote-baseline-closure.md
?? reports/aos-farm-217-step-12-commit-push-authorization-package.md
?? reports/aos-farm-219-step-12-push-and-remote-baseline-closure.md
?? reports/aos-farm-220-merge-authorization-package.md
?? reports/aos-farm-220-merge-readiness-verification.md
?? reports/aos-farm-222-merge-execution-report.md
?? reports/aos-farm-223-merge-push-authorization-package.md
?? reports/aos-farm-224-merge-push-and-remote-baseline-closure.md
?? reports/aos-farm-84-commit-post-push-remote-baseline-closure.md
?? reports/aos-farm-84-commit-push-authorization-package.md
?? reports/aos-farm-85-88-evidence-artifacts-commit-authorization-package.md
?? reports/aos-farm-96-14-final-build-step-2-push-authorization-package.md
?? reports/aos-farm-96-17-build-step-2-post-push-remote-baseline-closure.md
?? reports/aos-farm-build-step-2-planning-artifacts-push-authorization-package.md
?? reports/aos-farm-post-skeleton-push-authorization-package.md
?? reports/aos-farm-ta-06-commit-push-authorization-package.md
?? reports/aos-farm-ta-08-2-ta-06-ta-07-push-authorization-package.md
?? reports/aos-farm-ta-08-3-ta-06-ta-07-push-and-remote-baseline-closure.md
?? reports/aos-farm-ta-09-push-and-remote-baseline-closure.md
?? reports/aos-farm-ta-09-push-authorization-package.md
?? reports/aos-farm-ta-10-push-and-remote-baseline-closure.md
?? reports/aos-farm-ta-10-push-authorization-package.md
?? reports/aos-farm-ta-20-problem-intake-mvp-commit-push-authorization-package.md
?? "reports/human-checkpoints/aos-farm-102-final-step-3-commit-authorization 2.md"
?? reports/human-checkpoints/aos-farm-104-step-3-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-115-step-4-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-125-step-5-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-127-3-closure-evidence-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-131-multi-environment-controller-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-139-build-step-6-dogfood-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-167-controller-loop-handoff-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-172-controller-loop-handoff-closure-evidence-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-181-step-8-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-190-step-9-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-199-step-10-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-208-step-11-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-217-step-12-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-220-merge-authorization.md
?? reports/human-checkpoints/aos-farm-223-merge-push-authorization.md
?? reports/human-checkpoints/aos-farm-84-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-85-88-evidence-artifacts-commit-authorization.md
?? reports/human-checkpoints/aos-farm-96-14-final-build-step-2-push-authorization.md
?? reports/human-checkpoints/aos-farm-build-step-2-planning-artifacts-push-authorization.md
?? "reports/human-checkpoints/aos-farm-commit-authorization 2.md"
?? "reports/human-checkpoints/aos-farm-constitution-alignment-approval 2.md"
?? "reports/human-checkpoints/aos-farm-documentation-assembly-mvp-execution-authorization 2.md"
?? "reports/human-checkpoints/aos-farm-first-controlled-implementation-authorization 2.md"
?? "reports/human-checkpoints/aos-farm-implementation-readiness-authorization 2.md"
?? "reports/human-checkpoints/aos-farm-post-skeleton-commit-authorization 2.md"
?? reports/human-checkpoints/aos-farm-post-skeleton-push-authorization.md
?? "reports/human-checkpoints/aos-farm-push-authorization 2.md"
?? "reports/human-checkpoints/aos-farm-push-evidence-commit-authorization 2.md"
?? reports/human-checkpoints/aos-farm-push-evidence-push-authorization.md
?? reports/human-checkpoints/aos-farm-push-evidence-working-tree-addendum.md
?? "reports/human-checkpoints/aos-farm-push-working-tree-addendum 2.md"
?? reports/human-checkpoints/aos-farm-ta-06-commit-push-authorization.md
?? reports/human-checkpoints/aos-farm-ta-08-2-ta-06-ta-07-push-authorization.md
?? reports/human-checkpoints/aos-farm-ta-09-push-authorization.md
?? reports/human-checkpoints/aos-farm-ta-10-push-authorization.md
?? reports/human-checkpoints/aos-farm-ta-20-problem-intake-mvp-commit-push-authorization.md
?? "templates/allowed-forbidden-code-change-template 2.md"
?? "templates/aos-farm-task-verification-input-template 2.md"
?? "templates/aos-farm-task-verification-output-template 2.md"
?? "templates/build-plan-template 2.md"
?? "templates/build-step-batch-scope-template 2.md"
?? "templates/build-step-batch-verification-template 2.md"
?? "templates/clarification-gate-template 2.md"
?? "templates/code-assembly-mvp-evidence-report-template 2.md"
?? "templates/code-assembly-mvp-execution-report-template 2.md"
?? "templates/code-assembly-mvp-human-review-template 2.md"
?? "templates/code-assembly-mvp-input-template 2.md"
?? "templates/code-assembly-traceability-matrix-template 2.md"
?? "templates/code-assembly-verification-report-template 2.md"
?? "templates/code-change-scope-template 2.md"
?? "templates/code-diff-evidence-template 2.md"
?? "templates/code-execution-package-template 2.md"
?? "templates/documentation-assembly-input-template 2.md"
?? "templates/documentation-assembly-output-template 2.md"
?? "templates/documentation-assembly-report-template 2.md"
?? "templates/execution-authorization-package-template 2.md"
?? "templates/feature-intake-template 2.md"
?? "templates/feature-spec-template 2.md"
?? "templates/final-build-step-commit-candidate-template 2.md"
?? "templates/governance-control-gate-matrix-template 2.md"
?? "templates/governance-control-module-contract-template 2.md"
?? "templates/human-approval-boundary-template 2.md"
?? "templates/ide-controller-next-task-template 2.md"
?? "templates/ide-controller-review-report-template 2.md"
?? "templates/manual-code-review-checkpoint-template 2.md"
?? "templates/minimal-safety-floor-checklist-template 2.md"
?? "templates/model-routing-decision-template 2.md"
?? "templates/multi-environment-handoff-template 2.md"
?? "templates/multi-environment-session-start-template 2.md"
?? "templates/safety-gate-matrix-template 2.md"
?? "templates/session-limit-handoff-template 2.md"
?? "templates/spec-to-execution-traceability-matrix-template 2.md"
?? "templates/step-safety-verification-report-template 2.md"
?? "templates/task-brief-chain-template 2.md"
?? "templates/token-budget-task-header-template 2.md"
?? "templates/unknown-not-run-pass-semantics-template 2.md"
?? "templates/verification-evidence-report-template 2.md"
```

Dirty inventory categories:

- untracked duplicate docs with ` 2.md` suffix under `docs/assembly`, `docs/governance`, `docs/operations`, `docs/validation`, and `templates`;
- untracked duplicate and closure reports under `reports`;
- untracked human-checkpoint files under `reports/human-checkpoints`;
- untracked TA push/authorization files such as `reports/aos-farm-ta-20-problem-intake-mvp-commit-push-authorization-package.md` and `reports/human-checkpoints/aos-farm-ta-20-problem-intake-mvp-commit-push-authorization.md`.

TA 21 does not modify, delete, stage, source, or rely on any pre-existing untracked dirty files.

## 3. Required Source Availability

```yaml
required_sources_available: true
sources_read_in_required_order:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
blocked_required_source_missing: false
```

## 4. Current TA Package Inventory

Methodology docs:

```text
agentos/docs/methodology/technical-assignment/README.md
agentos/docs/methodology/technical-assignment/00-overview-and-routing.md
agentos/docs/methodology/technical-assignment/01-human-methodology.md
agentos/docs/methodology/technical-assignment/02-agent-contract.md
agentos/docs/methodology/technical-assignment/03-data-discovery-and-access.md
agentos/docs/methodology/technical-assignment/04-draft-artifact-templates.md
agentos/docs/methodology/technical-assignment/05-safety-gates-and-statuses.md
agentos/docs/methodology/technical-assignment/06-domain-extension-interface.md
agentos/docs/methodology/technical-assignment/07-consistency-checklist.md
agentos/docs/methodology/technical-assignment/08-interview-depth-loop-and-entity-process-traversal.md
agentos/docs/methodology/technical-assignment/09-adaptive-elicitation-method-selector.md
agentos/docs/methodology/technical-assignment/runbooks/*.md
agentos/docs/methodology/technical-assignment/extensions/*.md
```

Prompt:

```text
agentos/docs/prompts/problem-intake-agent.md
```

Scripts:

```text
agentos/scripts/problem_intake_runner.py
agentos/scripts/problem_intake_output_validator.py
```

Current example run:

```text
agentos/reports/problem-intake/examples/ta-14-example-input.md
agentos/reports/problem-intake/ta-14-example-run/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-14-example-run/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-14-example-run/problem-interview-report.md
agentos/reports/problem-intake/ta-14-example-run/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-14-example-run/problem-intake-run-report.md
```

Relevant AOS templates:

```text
agentos/templates/project-brief.md
agentos/templates/specification.md
agentos/templates/task-brief.md
agentos/templates/execution-report.md
agentos/templates/evidence-report.md
agentos/templates/human-review.md
templates/documentation-assembly-input-template.md
templates/documentation-assembly-output-template.md
templates/spec-to-execution-traceability-matrix-template.md
templates/task-brief-chain-template.md
templates/verification-evidence-report-template.md
templates/human-approval-boundary-template.md
templates/minimal-safety-floor-checklist-template.md
```

Relevant prior TA reports/checkpoints:

```text
reports/aos-farm-ta-11-problem-intake-automation-gap-recovery-plan.md
reports/aos-farm-ta-12-minimal-problem-intake-runner-mvp-design.md
reports/aos-farm-ta-14-problem-intake-example-run-evidence.md
reports/aos-farm-ta-15-problem-intake-runner-output-validator-design.md
reports/aos-farm-ta-16-problem-intake-output-validator-implementation-report.md
reports/aos-farm-ta-16-problem-intake-output-validator-run-report.md
reports/aos-farm-ta-17-problem-intake-output-validator-evidence-review.md
reports/aos-farm-ta-18-problem-intake-mvp-batch-commit-authorization-package.md
reports/human-checkpoints/aos-farm-ta-18-problem-intake-mvp-batch-commit-authorization.md
```

## 5. Gap Analysis

### GAP-01 - Misleading or overbroad status language

Current validator emits `VALIDATION_COMPLETE` when only file inventory, required status fields, and simple unsafe-claim scanning pass. This can be read too broadly unless renamed or contextualized as structural validation only.

Evidence:

- `agentos/scripts/problem_intake_output_validator.py` sets `validator_status = "VALIDATION_COMPLETE"` when structural checks pass.
- `reports/aos-farm-ta-16-problem-intake-output-validator-run-report.md` records `validator_status: VALIDATION_COMPLETE`.
- Prior evidence also records `semantic_quality_status: NOT_VALIDATED`.

### GAP-02 - Contract reference mismatch

Several methodology docs still reference `02-agent-contract.yaml`, but the tracked file is `02-agent-contract.md`.

Evidence paths include:

```text
agentos/docs/methodology/technical-assignment/README.md
agentos/docs/methodology/technical-assignment/00-overview-and-routing.md
agentos/docs/methodology/technical-assignment/01-human-methodology.md
agentos/docs/methodology/technical-assignment/07-consistency-checklist.md
reports/aos-farm-ta-11-problem-intake-automation-gap-recovery-plan.md
```

### GAP-03 - Missing TA Intake to Documentation Assembly bridge

The TA package outputs `PROJECT_SPEC.draft.md`, `REQUIREMENTS.draft.md`, problem report, and checklist. The active Documentation Assembly Pipeline expects Project Brief, Specification, Task Brief, Execution/Evidence, and Human Review Package. A deterministic bridge contract is missing or insufficient.

Required future bridge boundary:

- bridge output is not approval;
- bridge output is not execution authorization;
- bridge output is not final Task Brief;
- Task Brief output is candidate only;
- `risk_profile_assigned_by_human` remains missing until human assignment;
- `execution_authorized: false`.

### GAP-04 - Runner creates placeholders or insufficient artifacts

Current runner detects a small set of required input sections, then writes base skeleton content for all output artifacts. `PROJECT_SPEC.draft.md` and `REQUIREMENTS.draft.md` currently contain status YAML plus a generic sentence, not the required contract sections.

Evidence:

- `agentos/scripts/problem_intake_runner.py` uses `get_base_content(...)` for output artifacts.
- Generated `PROJECT_SPEC.draft.md` and `REQUIREMENTS.draft.md` in `agentos/reports/problem-intake/ta-14-example-run/` have only a title, status YAML, and one generic line.

### GAP-05 - Validator is not contract-aware enough

Current validator checks required files, required status fields, and simple unsafe literal claims. It does not check required sections from `02-agent-contract.md`, final status, UNKNOWN visibility, Human Decisions Required, or contextual forbidden promotions in actual output/status fields.

Also, forbidden claim detection is literal text oriented and should become contextual to avoid false positives when a document safely says a forbidden status is forbidden.

### GAP-06 - Missing fixture matrix

No current fixture matrix covers:

1. complete brief;
2. weak brief;
3. missing data discovery;
4. sensitive/high-impact case;
5. contradiction / skip case.

### GAP-07 - Missing dogfood evidence for the working gated MVP process

Current TA-14 example run proves only a controlled structural example, not the full gated MVP process:

```text
input -> generated drafts -> bridge output -> validator report -> Human Review Package
```

### GAP-08 - Missing final audit for the completed working pipeline

No current final audit verifies the future v2 runner, v2 validator, bridge, fixtures, dogfood, dirty-worktree boundaries, and false-PASS controls as one scoped pipeline.

### GAP-09 - Dirty worktree creates implementation risk

The current dirty worktree is acceptable for TA 21 report-writing, but it blocks implementation unless explicitly handled by the future human execution checkpoint. Pre-existing untracked files must not be touched, staged, sourced, deleted, renamed, or committed by TA 23 through TA 25.

## 6. Proposed Risk Profile

```yaml
risk_profile_proposed_by_agent: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: null
assignment_status: HUMAN_REQUIRED
```

Rationale:

- runner behavior changes are planned in TA 24;
- validator semantics and status language changes are planned in TA 24;
- methodology and bridge documents are lifecycle-adjacent and control-adjacent;
- false PASS / approval boundary risks are present;
- dirty worktree and branch policy require explicit human handling.

The agent proposes `HIGH_RISK_PROTECTED` only. A human must assign the Risk Profile.

## 7. Branch / Worktree Policy Proposal

Preferred future policy:

```yaml
preferred_working_branch: build/ta-intake-working-pipeline
branch_creation_required_for_execution: true
```

If branch creation is not authorized:

```yaml
execution_status: BLOCKED
```

unless the human explicitly authorizes work on `dev` in the TA 22 checkpoint.

Required TA 22 branch fields:

```yaml
branch_policy:
  branch_creation_authorized: true / false
  authorized_working_branch: build/ta-intake-working-pipeline or dev
  work_on_dev_authorized: true / false
```

Dirty worktree policy:

- dirty worktree does not block TA 21;
- dirty worktree blocks TA 23 through TA 25 unless the human checkpoint explicitly confirms handling;
- pre-existing untracked dirty files must not be touched, staged, sourced, deleted, renamed, or committed;
- TA 23 through TA 25 may only touch their exact authorized file set.

## 8. Exact Allowed File Set Proposal for TA 23 through TA 25

This is a proposal only. It is not authorized until a human checkpoint confirms it.

### TA 23 - Honesty Alignment and Bridge Contract

May modify:

```text
agentos/docs/methodology/technical-assignment/README.md
agentos/docs/methodology/technical-assignment/00-overview-and-routing.md
agentos/docs/methodology/technical-assignment/01-human-methodology.md
agentos/docs/methodology/technical-assignment/07-consistency-checklist.md
agentos/docs/prompts/problem-intake-agent.md
```

May create:

```text
agentos/docs/methodology/technical-assignment/10-ta-intake-to-documentation-assembly-bridge.md
reports/ta-23-technical-assignment-honesty-alignment-and-bridge-execution-report.md
reports/ta-23-technical-assignment-honesty-alignment-and-bridge-verification-report.md
```

Protected/canonical note:

- the methodology docs and prompt are active operational/control-adjacent sources;
- changes require explicit human execution checkpoint and exact file-set confirmation;
- no source-precedence, approval, or execution authority may be changed except to clarify safe boundaries.

### TA 24 - Runner v2 and Validator v2

May modify:

```text
agentos/scripts/problem_intake_runner.py
agentos/scripts/problem_intake_output_validator.py
```

May create:

```text
reports/ta-24-technical-assignment-runner-validator-v2-execution-report.md
reports/ta-24-technical-assignment-runner-validator-v2-verification-report.md
```

Protected/canonical note:

- validator semantics are HIGH_RISK_PROTECTED;
- runner must remain existing-spec-review MVP only;
- interview route automation is out of scope;
- no runtime enforcement or CI workflow may be introduced.

### TA 25 - Fixtures, Dogfood, Final Audit, and Commit Authorization Preparation

May create fixture inputs and expected-result notes:

```text
agentos/reports/problem-intake/ta-25-fixtures/complete-brief/input.md
agentos/reports/problem-intake/ta-25-fixtures/complete-brief/expected-validator-status.md
agentos/reports/problem-intake/ta-25-fixtures/weak-brief/input.md
agentos/reports/problem-intake/ta-25-fixtures/weak-brief/expected-validator-status.md
agentos/reports/problem-intake/ta-25-fixtures/missing-data-discovery/input.md
agentos/reports/problem-intake/ta-25-fixtures/missing-data-discovery/expected-validator-status.md
agentos/reports/problem-intake/ta-25-fixtures/sensitive-high-impact/input.md
agentos/reports/problem-intake/ta-25-fixtures/sensitive-high-impact/expected-validator-status.md
agentos/reports/problem-intake/ta-25-fixtures/contradiction-skip/input.md
agentos/reports/problem-intake/ta-25-fixtures/contradiction-skip/expected-validator-status.md
```

May create generated fixture outputs:

```text
agentos/reports/problem-intake/ta-25-fixture-runs/complete-brief/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/complete-brief/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/complete-brief/problem-interview-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/complete-brief/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/complete-brief/problem-intake-run-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/complete-brief/validator-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/weak-brief/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/weak-brief/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/weak-brief/problem-interview-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/weak-brief/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/weak-brief/problem-intake-run-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/weak-brief/validator-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/missing-data-discovery/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/missing-data-discovery/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/missing-data-discovery/problem-interview-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/missing-data-discovery/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/missing-data-discovery/problem-intake-run-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/missing-data-discovery/validator-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/sensitive-high-impact/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/sensitive-high-impact/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/sensitive-high-impact/problem-interview-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/sensitive-high-impact/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/sensitive-high-impact/problem-intake-run-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/sensitive-high-impact/validator-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/contradiction-skip/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/contradiction-skip/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/contradiction-skip/problem-interview-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/contradiction-skip/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-25-fixture-runs/contradiction-skip/problem-intake-run-report.md
agentos/reports/problem-intake/ta-25-fixture-runs/contradiction-skip/validator-report.md
```

May create dogfood outputs:

```text
agentos/reports/problem-intake/ta-25-dogfood/input.md
agentos/reports/problem-intake/ta-25-dogfood/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-25-dogfood/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-25-dogfood/problem-interview-report.md
agentos/reports/problem-intake/ta-25-dogfood/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-25-dogfood/problem-intake-run-report.md
agentos/reports/problem-intake/ta-25-dogfood/validator-report.md
agentos/reports/problem-intake/ta-25-dogfood/documentation-assembly-bridge-output.md
agentos/reports/problem-intake/ta-25-dogfood/human-review-package.md
```

May create final TA 25 reports/checkpoint:

```text
reports/ta-25-technical-assignment-fixture-dogfood-final-audit.md
reports/ta-25-technical-assignment-process-commit-authorization-package.md
reports/human-checkpoints/ta-25-technical-assignment-process-commit-authorization.md
```

Protected/canonical note:

- generated reports and fixture outputs are Evidence/drafts only;
- they do not authorize execution, implementation, commit, push, release, or production use.

## 9. Explicit Forbidden Operations for TA 23 through TA 25

- no cleanup;
- no delete / move / rename;
- no branch creation without explicit human authorization;
- no protected/canonical changes without exact human checkpoint;
- no runtime enforcement;
- no CI workflow changes;
- no branch protection changes;
- no required-check changes;
- no broad validator suite;
- no hidden auto-fix;
- no final Task Brief;
- no Risk Profile assignment by agent;
- no approval simulation;
- no staging;
- no commit;
- no push;
- no force push;
- no tag push;
- no merge;
- no release;
- no production use;
- no use of dirty/untracked `* 2.md` files as source;
- no staging or committing pre-existing unrelated dirty files.

## 10. BLOCKED Conditions

Future execution must stop if any of these is true:

- required sources missing or unreadable;
- branch policy ambiguous;
- branch creation not authorized and work on `dev` not explicitly authorized;
- dirty worktree handling not confirmed;
- dirty worktree conflicts with any output path;
- target file conflicts exist;
- exact file set missing or unconfirmed;
- Risk Profile not assigned by human for execution;
- human execution checkpoint missing;
- protected/canonical scope involved without checkpoint;
- validator status or evidence state unknown;
- UNKNOWN is being treated as OK;
- NOT_RUN is being treated as PASS;
- Evidence is being treated as approval.

## 11. Recommended Next Step

Next safe step:

```text
TA 22 - Human Execution Authorization
```

Do not execute TA 23 until TA 22 has explicit human authorization, exact file-set confirmation, branch/worktree decision, and human-assigned Risk Profile.

## 12. TA 21 Final Boundary

TA 21 prepared authorization materials only.

```yaml
implementation_performed: false
runner_modified: false
validator_modified: false
bridge_implemented: false
fixtures_created: false
dogfood_performed: false
commit_performed: false
push_performed: false
release_performed: false
production_use_performed: false
human_approval_simulated: false
```
