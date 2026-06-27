# Human Result Acceptance Decision Contract

This document defines the contract for recording a human's decision regarding the result of a completed task.

## Rules
- Markdown/YAML remains the Source of Truth.
- JSON decision package is derived check input only.
- JSON package/checker output is Evidence / validation signal only.
- Package/checker must not approve task result, close task, authorize commit, authorize push, mutate lifecycle, or start next task.

## Required Fields

### Task Context
- `task_id`: String identifier of the task.
- `task_title`: Title of the task.

### Quality and Evidence
- `task_quality_package_path`: Path to the Task Quality package.
- `task_quality_result_path`: Path to the Task Quality result JSON.
- `task_quality_status`: Status from the Task Quality Gate (e.g., PASS, PASS_WITH_WARNINGS).
- `task_quality_known_limits`: List of known limits or caveats identified during quality checks.
- `acceptance_summary_path`: Path to the user-facing acceptance summary.

### Human Decision
- `human_decision`: Must be `ACCEPT_RESULT`, `NEEDS_CHANGES`, or `REJECT_RESULT`.
- `human_decision_reason`: Explanation for the decision.
- `human_acknowledges_known_limits`: Boolean indicating the human has read and accepts the known limits.
- `result_accepted_by_human`: Boolean, must be true if `human_decision` is `ACCEPT_RESULT`.
- `requires_follow_up_task`: Boolean, true if `NEEDS_CHANGES`.
- `follow_up_task_candidate`: Path to follow-up task candidate (required if `NEEDS_CHANGES`).
- `rejection_reason`: Explanation (required if `REJECT_RESULT`).

### Forbidden Automation Boundries
- `commit_authorized`: Must be false.
- `push_authorized`: Must be false.
- `merge_authorized`: Must be false.
- `release_authorized`: Must be false.
- `next_task_started`: Must be false.
- `lifecycle_mutation_authorized`: Must be false.
