# Human Result Acceptance Decision Contract

This document defines the contract for recording a human's decision regarding the result of a completed task.

## Rules
- Markdown/YAML remains the Source of Truth.
- JSON decision package is derived check input only.
- JSON package/checker output is Evidence / validation signal only.
- Package/checker must not approve task result, close task, authorize commit, authorize push, mutate lifecycle, or start next task.
- Task Quality PASS is not Human Result Acceptance.
- Human Result Acceptance is not commit authorization.
- Commit authorization is not push authorization.
- Push authorization is not release authorization.

## Required Fields

### Task Context
- `task_id`: String identifier of the task.
- `task_title`: Title of the task.

### Quality and Evidence
- `task_quality_package_path`: Path to the Task Quality package.
- `task_quality_result_path`: Path to the Task Quality result JSON.
- `task_quality_status`: Status from the Task Quality Gate (e.g., PASS, PASS_WITH_WARNINGS).
- `acceptance_summary_path`: Path to the user-facing acceptance summary.

### Human Decision
- `human_decision`: Must be `ACCEPT_RESULT`, `NEEDS_CHANGES`, or `REJECT_RESULT`.
- `human_decision_reason`: Explanation for the decision.
- `result_accepted_by_human`: Boolean, must be true if `human_decision` is `ACCEPT_RESULT`.
- `human_acknowledges_known_limits`: Boolean indicating the human has read and accepts the known limits.

### Forbidden Automation Boundaries
- `commit_authorized`: Must be false.
- `push_authorized`: Must be false.
- `merge_authorized`: Must be false.
- `release_authorized`: Must be false.
- `next_task_started`: Must be false.
- `lifecycle_mutation_authorized`: Must be false.
- `auto_approval_claim`: Must be missing or false.
- `auto_closure_claim`: Must be missing or false.

## Required Decision Rules

**ACCEPT_RESULT:**
- Requires `result_accepted_by_human` to be `true`.
- Blocks if `task_quality_status` is `BLOCKED`.
- Blocks if required `UNKNOWN` or `NOT_RUN` values exist in the decision.

**NEEDS_CHANGES:**
- Requires `follow_up_task_candidate` to be provided.

**REJECT_RESULT:**
- Requires `human_decision_reason` to be provided.

**Forbidden Claims:**
- `auto_approval_claim` -> BLOCKED
- `auto_closure_claim` -> BLOCKED
- `commit_authorized: true` -> BLOCKED
- `push_authorized: true` -> BLOCKED
- `next_task_started: true` -> BLOCKED
