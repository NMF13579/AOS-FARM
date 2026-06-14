PASS or PASS_WITH_WARNINGS may recommend a next action but does not authorize it.
BLOCKED must route to human review.
UNKNOWN must route to blocked or human review.
NOT_RUN must not be treated as PASS.
Commit/push/release/production actions require explicit human checkpoint.

```yaml
task_id: ""
final_status: ""
report_path: ""
created_files: []
modified_files: []

execution_performed: false
staging_performed: false
commit_performed: false
push_performed: false
release_performed: false
production_use_performed: false

approval_simulated: false
risk_profile_self_assigned_by_agent: false
UNKNOWN_treated_as_OK: false
NOT_RUN_treated_as_PASS: false

blocking_issue_count: 0
warning_count: 0
carried_warnings: []

may_recommend_next_action: false
recommended_next_action_type: ""
recommended_next_task_id: ""
recommended_next_task_name: ""
requires_human_checkpoint: true
handoff_file_required: true
handoff_file_path: ""

routing_status: DRAFT
```
