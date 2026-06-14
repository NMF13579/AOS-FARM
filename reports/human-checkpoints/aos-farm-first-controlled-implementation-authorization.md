# AOS-FARM.35 — Human Authorization for First Controlled Implementation Candidate

## 1. Checkpoint Metadata

```yaml
checkpoint_id: AOS-FARM.35-FIRST-CONTROLLED-IMPLEMENTATION-CANDIDATE-AUTHORIZATION
checkpoint_type: human_authorization
repository: NMF13579/AOS-FARM
branch: dev
base_branch: main
created_by_human: true
agent_created_approval: false
human_approval_simulated: false
```

## 2. Human Decision

```yaml
human_decision: APPROVED
human_author: "Muhammed"
human_author_is_human: true
human_author_date: "2026-06-14"
human_signature_token: "APPROVED_AOS_FARM_35_FIRST_CONTROLLED_IMPLEMENTATION_BY_MUHAMMED_2026-06-14"
```

Required human approval token if approved:

```text
APPROVED_AOS_FARM_35_FIRST_CONTROLLED_IMPLEMENTATION_BY_MUHAMMED_2026-06-14
```

If the human decision is not `APPROVED`, AOS-FARM.36 is BLOCKED.

## 3. Authorization Scope

```yaml
authorized_future_task: AOS-FARM.36
authorized_future_task_name: "First Controlled Implementation: Documentation Assembly Pipeline Skeleton"
authorized_candidate: "Documentation Assembly Pipeline skeleton only"
candidate_type: docs-or-validation-skeleton-only
single_workstream: true
small_scope: true
skeleton_only: true
runtime_execution_required: false
spec_kit_command_required: false
protected_canonical_change_required: false
```

## 4. Human-Assigned Risk Profile

```yaml
risk_profile_assigned_by_human: true
risk_profile_assigned_by_agent: false
low_risk_fast_assigned_by_agent: false
risk_profile: MEDIUM_RISK_GUIDED
```

The agent may not downgrade this to `LOW_RISK_FAST`.

## 5. Exact Authorized Files for AOS-FARM.36

AOS-FARM.36 may create or modify only these files:

```yaml
authorized_files:
  - docs/assembly/documentation-assembly-pipeline-skeleton.md
  - templates/documentation-assembly-input-template.md
  - templates/documentation-assembly-output-template.md
  - reports/aos-farm-documentation-assembly-pipeline-skeleton-report.md
```

No other files are authorized.

## 6. Exact Forbidden Files and Paths

```yaml
forbidden_files_and_paths:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  - 03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
  - .specify/memory/constitution.md
  - constitution.md
  - .github/
  - scripts/
  - src/
  - app/
  - packages/
  - tests/
  - reports/human-checkpoints/
  - any file not listed in authorized_files
```

## 7. Allowed Commands for AOS-FARM.36

```yaml
allowed_commands:
  - git branch --show-current
  - git status --short
  - git status -sb
  - git diff --name-status
  - git diff -- docs/assembly/documentation-assembly-pipeline-skeleton.md templates/documentation-assembly-input-template.md templates/documentation-assembly-output-template.md reports/aos-farm-documentation-assembly-pipeline-skeleton-report.md
  - test -f 00_AOS_Core_Control.md
  - test -f 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - test -f 02_AOS_Governance_Control_Module_and_Safety_Rules.md
```

## 8. Forbidden Commands for AOS-FARM.36

```yaml
forbidden_commands:
  - /speckit.implement
  - /specify
  - /plan
  - git add
  - git commit
  - git push
  - git pull
  - git fetch
  - git merge
  - git rebase
  - git reset
  - git clean
  - rm
  - mv
  - cp over protected/canonical files
  - chmod
  - workflow creation
  - CI activation
  - branch protection changes
```

## 9. Explicit Non-Authorization

```yaml
implementation_execution_beyond_authorized_skeleton: false
broad_implementation_authorized: false
source_code_modification_authorized: false
runtime_execution_authorized: false
speckit_implement_authorized: false
specify_authorized: false
plan_authorized: false
workflow_creation_authorized: false
ci_activation_authorized: false
branch_protection_change_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
destructive_operations_authorized: false
protected_canonical_changes_authorized: false
```

## 10. Required Behavior for AOS-FARM.36

AOS-FARM.36 must create a minimal Documentation Assembly Pipeline skeleton only.

The skeleton may define:

```yaml
allowed_content:
  - pipeline purpose
  - input artifact categories
  - output artifact categories
  - assembly stages as placeholders
  - evidence requirements
  - safety boundaries
  - non-approval semantics
  - future validation placeholders
```

The skeleton must preserve:

```text
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
Human approval cannot be simulated.
Skeleton ≠ implementation.
Scope must not expand without explicit human permission.
Protected/canonical changes require human checkpoint.
Destructive operations are forbidden by default.
Minimal Safety Floor is always-on.
```

## 11. AOS-FARM.36 Stop Conditions

AOS-FARM.36 must stop as BLOCKED if any condition is true:

```yaml
stop_conditions:
  - required source file missing
  - this checkpoint file missing
  - human_decision is not APPROVED
  - human approval token missing
  - risk_profile_assigned_by_human is not true
  - risk_profile_assigned_by_agent is true
  - low_risk_fast_assigned_by_agent is true
  - current branch is not dev
  - unexpected local delta exists outside known authorization evidence and authorized files
  - any file outside authorized_files would be created or modified
  - any protected/canonical file would be changed
  - any forbidden command is needed
  - /speckit.implement is needed
  - /specify is needed
  - /plan is needed
  - implementation scope expands beyond skeleton-only
  - commit is requested
  - push is requested
  - release or production use is requested
```

## 12. Validation Requirements for AOS-FARM.36

AOS-FARM.36 final report must include:

```yaml
required_final_report_fields:
  - current_branch
  - head_sha
  - origin_dev_sha
  - head_equals_origin_dev
  - required_sources_available
  - aos_farm_35_checkpoint_validated
  - human_decision
  - human_signature_token_present
  - risk_profile
  - risk_profile_assigned_by_human
  - risk_profile_assigned_by_agent
  - low_risk_fast_assigned_by_agent
  - files_created
  - files_modified
  - unauthorized_files_touched
  - forbidden_commands_run
  - speckit_implement_run
  - specify_run
  - plan_run
  - stage_performed
  - commit_created
  - push_performed
  - workflow_created
  - ci_activated
  - branch_protection_changed
  - release_authorized
  - production_use_authorized
  - final_status
```

Allowed final statuses:

```yaml
allowed_final_statuses:
  - AOS_FARM_36_DOCUMENTATION_ASSEMBLY_PIPELINE_SKELETON_CREATED
  - AOS_FARM_36_DOCUMENTATION_ASSEMBLY_PIPELINE_SKELETON_CREATED_WITH_WARNINGS
  - AOS_FARM_36_BLOCKED
```

## 13. Final Authorization Boundary

```yaml
aos_farm_36_authorized_only_if_human_decision_approved: true
aos_farm_36_authorized_scope: "Documentation Assembly Pipeline skeleton only"
aos_farm_37_authorized: false
implementation_beyond_skeleton_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
```

Final rule:

```text
This checkpoint may authorize only AOS-FARM.36 skeleton-only execution if manually approved by the human. It does not authorize broad implementation, Spec Kit commands, commit, push, release, production use, lifecycle mutation, protected/canonical changes, or any future task.
```
