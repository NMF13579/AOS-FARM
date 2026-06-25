# TA 21 - Technical Assignment Execution Authorization Package

```yaml
task_id: TA-21
package_type: execution_authorization_preparation
checkpoint_required: true
approval_status: NOT_APPROVED
execution_authorized: false
execution_authorized_now: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
```

## 1. Proposed Execution Scope

This package prepares a future human decision for TA 23 through TA 25 only.

Future target:

```text
Move Technical Assignment intake from STRUCTURAL_MVP_ONLY / smoke-test toward a working gated MVP process.
```

Future process target:

```text
existing brief / user idea
-> route selection
-> intake / review
-> PROJECT_SPEC.draft.md
-> REQUIREMENTS.draft.md
-> problem report
-> checklist
-> bridge to Project Brief / Specification / Task Brief candidate inputs
-> validator evidence
-> Human Review Package
```

Maximum future process status:

```text
READY_FOR_HUMAN_REVIEW
```

Forbidden future meanings:

```text
APPROVED
READY_FOR_EXECUTION
IMPLEMENTATION_AUTHORIZED
PRODUCTION_READY
```

## 2. Proposed Risk Profile

```yaml
risk_profile_proposed_by_agent: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: null
risk_profile_assignment_required_before_execution: true
```

Rationale:

- planned runner behavior changes;
- planned validator status and semantic-boundary changes;
- active methodology and prompt updates;
- bridge contract for lifecycle-adjacent documentation flow;
- dirty worktree handling;
- false PASS and approval-boundary risk.

The agent does not assign the Risk Profile. Human assignment is required.

## 3. Branch Policy Options

Preferred option:

```yaml
branch_creation_authorized: true
authorized_working_branch: build/ta-intake-working-pipeline
work_on_dev_authorized: false
```

Alternative option:

```yaml
branch_creation_authorized: false
authorized_working_branch: dev
work_on_dev_authorized: true
```

If neither option is explicitly approved by human checkpoint:

```yaml
execution_status: BLOCKED
```

Reason: `dev` is preserved as skeleton/reference baseline by the AOS control source, and new work must not accidentally proceed on `dev`.

## 4. Dirty Worktree Handling

Observed:

```yaml
dirty_worktree_detected: true
tracked_modifications_detected: false
staged_changes_detected: false
untracked_files_detected: true
upstream_ahead_behind: "0 0"
```

Required future checkpoint decision:

```yaml
dirty_worktree_handling_confirmed: true
preexisting_untracked_files_must_not_be_touched: true
preexisting_untracked_files_must_not_be_staged: true
preexisting_untracked_files_must_not_be_sourced: true
preexisting_untracked_files_must_not_be_deleted: true
preexisting_untracked_files_must_not_be_committed: true
```

Dirty worktree does not block TA 21. It blocks TA 23 through TA 25 unless explicitly handled in the human checkpoint.

## 5. Proposed Exact Allowed File Set

This file set is a proposal only.

### TA 23 - Honesty Alignment and Bridge Contract

Modify:

```text
agentos/docs/methodology/technical-assignment/README.md
agentos/docs/methodology/technical-assignment/00-overview-and-routing.md
agentos/docs/methodology/technical-assignment/01-human-methodology.md
agentos/docs/methodology/technical-assignment/07-consistency-checklist.md
agentos/docs/prompts/problem-intake-agent.md
```

Create:

```text
agentos/docs/methodology/technical-assignment/10-ta-intake-to-documentation-assembly-bridge.md
reports/ta-23-technical-assignment-honesty-alignment-and-bridge-execution-report.md
reports/ta-23-technical-assignment-honesty-alignment-and-bridge-verification-report.md
```

### TA 24 - Runner v2 and Validator v2

Modify:

```text
agentos/scripts/problem_intake_runner.py
agentos/scripts/problem_intake_output_validator.py
```

Create:

```text
reports/ta-24-technical-assignment-runner-validator-v2-execution-report.md
reports/ta-24-technical-assignment-runner-validator-v2-verification-report.md
```

### TA 25 - Fixtures, Dogfood, Final Audit, Commit Authorization Preparation

Create:

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
agentos/reports/problem-intake/ta-25-dogfood/input.md
agentos/reports/problem-intake/ta-25-dogfood/PROJECT_SPEC.draft.md
agentos/reports/problem-intake/ta-25-dogfood/REQUIREMENTS.draft.md
agentos/reports/problem-intake/ta-25-dogfood/problem-interview-report.md
agentos/reports/problem-intake/ta-25-dogfood/requirements-checklist-draft.md
agentos/reports/problem-intake/ta-25-dogfood/problem-intake-run-report.md
agentos/reports/problem-intake/ta-25-dogfood/validator-report.md
agentos/reports/problem-intake/ta-25-dogfood/documentation-assembly-bridge-output.md
agentos/reports/problem-intake/ta-25-dogfood/human-review-package.md
reports/ta-25-technical-assignment-fixture-dogfood-final-audit.md
reports/ta-25-technical-assignment-process-commit-authorization-package.md
reports/human-checkpoints/ta-25-technical-assignment-process-commit-authorization.md
```

## 6. Explicit Forbidden Operations

- no implementation before human execution authorization;
- no runner changes during TA 21 through TA 23;
- no validator changes during TA 21 through TA 23;
- no bridge implementation during TA 21;
- no fixtures during TA 21 through TA 24;
- no dogfood during TA 21 through TA 24;
- no cleanup;
- no delete / move / rename;
- no branch creation without authorization;
- no protected/canonical changes without checkpoint;
- no runtime enforcement;
- no CI workflow changes;
- no commit;
- no push;
- no release;
- no production use;
- no approval simulation;
- no Risk Profile assignment by agent;
- no use of pre-existing untracked dirty files as source.

## 7. Pending Human Decisions

Human must decide before TA 23:

```yaml
risk_profile_assigned_by_human: required
execution_authorized: required
allowed_file_set_confirmed: required
dirty_worktree_handling_confirmed: required
branch_policy_confirmed: required
branch_creation_authorized: true / false
authorized_working_branch: build/ta-intake-working-pipeline or dev
work_on_dev_authorized: true / false
```

If branch creation is not authorized and work on `dev` is not explicitly authorized, future execution is blocked.

## 8. Authorization Boundary

This package does not authorize execution.

```yaml
execution_authorized_now: false
human_approval_created_by_agent: false
checkpoint_created_as_pending_draft_only: true
next_safe_step: TA 22 - Human Execution Authorization
```
