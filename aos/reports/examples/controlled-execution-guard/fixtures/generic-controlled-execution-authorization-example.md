> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Controlled Execution Authorization Example

```yaml
checkpoint_id: GENERIC-TASK-438-CONTROLLED-EXECUTION-AUTHORIZATION-EXAMPLE
task_id: GENERIC-TASK.438
task_title: Controlled Execution Guard MVP Example
human_execution_authorized: true
authorized_by: human
authorization_scope: exact_task_only
risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by: human
authorized_branch: build/controlled-execution-guard-mvp
base_branch: origin/dev
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
next_task_authorized: false
```

This example records execution authorization only. It is not approval for commit, push, merge, release, or any other lifecycle transition.
