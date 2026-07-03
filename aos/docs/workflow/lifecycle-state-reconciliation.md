# Lifecycle State Reconciliation

## Purpose

Lifecycle State Reconciliation defines a read-only interpretation layer for task lifecycle signals that may otherwise be displayed differently by queue helpers, dashboards, validators, or next-task utilities.

The reconciler exists to prevent silent disagreement from becoming false readiness.

## Source Inputs

The reconciler may inspect:

- task files under `tasks/`
- task registry or queue metadata when present in task frontmatter
- queue helper derived ranking
- dashboard derived view
- validator summaries
- git branch, HEAD, and working tree status

The reconciler must not write these inputs.

## Source Precedence

Precedence follows the AOS-FARM control model:

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
4. task files and registries as repository Source of Truth for task state
5. generated or derived helper output

For safety and control semantics, `02_AOS_Governance_Control_Module_and_Safety_Rules.md` has domain authority over `01` unless `00` explicitly says otherwise.

## Source of Truth Boundary

Task files, registries, and canonical docs remain Source of Truth.

Lifecycle Reconciler is only the authoritative read-only interpreter of lifecycle signals.

Lifecycle Reconciler does not create, replace, or mutate Source of Truth.

If interpretation conflicts with Source of Truth, Source of Truth wins and the reconciler must fail-closed.

Reports, dashboards, JSON snapshots, and queue summaries are derived outputs. They do not approve, authorize, or mutate lifecycle state.

## Lifecycle States

The reconciler may report these lifecycle states:

- `DRAFT`
- `READY_FOR_HUMAN_REVIEW`
- `READY_FOR_EXECUTION`
- `EXECUTION_REPORTED`
- `EVIDENCE_RECORDED`
- `HUMAN_REVIEW_REQUIRED`
- `APPROVED`
- `REJECTED`
- `NEEDS_CHANGES`
- `BLOCKED`
- `UNKNOWN_BLOCKED`
- `NOT_RUN`

The state is interpretation, not mutation. If task metadata is absent, invalid, ambiguous, or contradictory, the reconciler reports `UNKNOWN_BLOCKED`.

## Current and Next Task Selection Rule

The current next candidate is the first ranked task that satisfies all of these:

- `queue_status` is `BACKLOG`, `NEXT`, or `IN_PROGRESS`
- lifecycle status is not `BLOCKED`, `CLOSED`, or `REJECTED`
- the task file can be read
- the task id and path can be interpreted

Tasks with `queue_status: DONE` are not next candidates. If a `DONE` task is surfaced as current or next by a derived tool, the reconciler must report a conflict or blocker unless the output explicitly states it was skipped as a non-candidate.

Multiple explicit `queue_status: NEXT` candidates are an ambiguous state and must be reported as `UNKNOWN_BLOCKED`.

No next candidate is `NONE` or `UNKNOWN_BLOCKED`, depending on whether absence is expected or caused by missing/invalid state.

## Conflict Behavior

The reconciler must fail-closed when:

- queue helper and dashboard disagree on current or next task
- a `DONE` task appears as current or next without explicit skip rationale
- task file metadata conflicts with derived tool output
- multiple explicit next tasks exist
- required task file cannot be read
- git state, validation state, or lifecycle authority is unknown

Fail-closed means:

- no approval
- no execution authorization
- no commit authorization
- no push authorization
- no lifecycle mutation
- next safe action is human review or blocker resolution

## Blocker Taxonomy

Blockers include:

- `missing_task`
- `missing_required_field`
- `invalid_task_id`
- `source_conflict`
- `queue_dashboard_disagreement`
- `done_task_surfaced_as_next`
- `multiple_next_tasks`
- `missing_human_risk_profile`
- `missing_execution_authorization`
- `approval_missing`
- `validator_not_run`
- `evidence_not_run`
- `unknown_git_state`
- `temp_boundary_risk`

`UNKNOWN` is not OK. `NOT_RUN` is not PASS.

## Permission Flags

The reconciler must default all permission flags to false:

```yaml
execution_allowed: false
approval_granted: false
commit_allowed: false
push_allowed: false
merge_allowed: false
release_allowed: false
```

Permission flags may only become true from explicit Source of Truth fields or human authorization records. Derived PASS, Evidence, CI PASS, queue position, or dashboard visibility must not set them.

## Output Format

The canonical CLI JSON shape is:

```yaml
schema_version: 1
source: aos_lifecycle_state
repo_state:
  branch: string
  head: string
  working_tree_clean: true|false|unknown
current_task:
  id: string|null
  path: string|null
  selection_status: SELECTED|CONFLICT|NONE|UNKNOWN_BLOCKED
  selection_reason:
    - string
lifecycle:
  state: DRAFT|READY_FOR_HUMAN_REVIEW|READY_FOR_EXECUTION|EXECUTION_REPORTED|EVIDENCE_RECORDED|HUMAN_REVIEW_REQUIRED|APPROVED|REJECTED|NEEDS_CHANGES|BLOCKED|UNKNOWN_BLOCKED|NOT_RUN
  blockers:
    - string
  unknowns:
    - string
permissions:
  execution_allowed: false
  approval_granted: false
  commit_allowed: false
  push_allowed: false
  merge_allowed: false
  release_allowed: false
evidence:
  validation_status: PASS|FAIL|NOT_RUN|UNKNOWN_BLOCKED
  evidence_status: PRESENT|MISSING|NOT_RUN|UNKNOWN_BLOCKED
human:
  risk_profile_status: ASSIGNED_BY_HUMAN|MISSING|AMBIGUOUS|UNKNOWN_BLOCKED
  execution_authorization_status: AUTHORIZED|NOT_AUTHORIZED|UNKNOWN_BLOCKED
  acceptance_status: APPROVED|REJECTED|NEEDS_CHANGES|NOT_REVIEWED|UNKNOWN_BLOCKED
conflicts:
  - source: string
    value: string
    reason: string
next_safe_action: string
```

Text output is a human-readable view of the same interpretation.

## Relationship to Queue Helper and Dashboard

The queue helper remains a derived queue utility and does not approve or authorize execution.

The dashboard remains a derived readability view and does not approve or authorize execution.

The dashboard should use the same next-candidate boundary as the queue helper, or explicitly surface disagreement as a conflict.

The Lifecycle Reconciler is the unified read-only interpreter used to compare these signals. It does not replace task files, registries, or human checkpoints.

## Explicit Non-Goals

Lifecycle Reconciler does not approve.

Lifecycle Reconciler does not mutate task files.

Lifecycle Reconciler does not assign Risk Profile.

Lifecycle Reconciler does not authorize execution.

Lifecycle Reconciler does not authorize commit/push/release.

Lifecycle Reconciler does not replace human checkpoint.

Lifecycle Reconciler does not produce Evidence.

Lifecycle Reconciler does not treat Evidence as approval.

Lifecycle Reconciler does not treat NOT_RUN as PASS.

Lifecycle Reconciler does not write reports, checkpoints, Evidence, or temporary files into `/.aos-tmp/`.
