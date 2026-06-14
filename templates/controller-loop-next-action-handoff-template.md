The handoff is not approval.
The handoff is not Evidence by itself.
The handoff cannot authorize execution, commit, push, release, or production use.
If required approval is missing, next action must be blocked or human review.

```yaml
handoff_id: ""
source_task_id: ""
source_task_final_status: ""
source_task_report_path: ""
current_branch: ""
head: ""
origin_dev: ""
remote_baseline_closed: false

recommended_next_task_id: ""
recommended_next_task_name: ""
recommended_next_task_type: ""

next_action_type: ""
allowed_next_action_types:
  - read_only_verification
  - execution_authorization_preparation
  - human_execution_authorization
  - controlled_execution
  - post_execution_verification
  - commit_authorization_preparation
  - human_commit_authorization
  - controlled_commit_execution
  - push_authorization_preparation
  - human_push_authorization
  - controlled_push_execution
  - remote_baseline_closure
  - blocked_human_review

requires_human_checkpoint: true
required_human_checkpoint_type: ""
risk_profile_required: true
risk_profile_assigned_by_human: ""

execution_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false

authorized_scope: ""
authorized_files: []
forbidden_operations: []

blocking_issue_count: 0
warning_count: 0
carried_warnings: []

approval_simulated: false
UNKNOWN_treated_as_OK: false
NOT_RUN_treated_as_PASS: false

handoff_status: DRAFT
```
