---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Task Registry Example

```yaml
schema_version: 1
tasks:
  - task_id: GENERIC-TASK.441
    title: Remote Baseline Closure
    source_file: reports/generic-task-441-remote-baseline-closure-report.md
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: CLOSED
    lifecycle_stage: CLOSED
    depends_on: []
    blocked_by: []
    replaces: []
    replaced_by: null
    task_brief_status: CLOSED
    risk_profile_assigned_by_human: true
    risk_profile: HIGH_RISK_PROTECTED
    execution_authorized: true
    commit_authorized: true
    push_authorized: true
    next_action: NONE
    final_status: REMOTE_BASELINE_CLOSED

  - task_id: GENERIC-TASK.442
    title: Task Registry and Queue Contract MVP
    source_file: reports/generic-task-442-task-brief-draft.md
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: HUMAN_REVIEW_REQUIRED
    lifecycle_stage: IN_PROGRESS
    depends_on:
      - GENERIC-TASK.441
    blocked_by: []
    replaces: []
    replaced_by: null
    task_brief_status: DRAFT
    risk_profile_assigned_by_human: true
    risk_profile: HIGH_RISK_PROTECTED
    execution_authorized: true
    commit_authorized: false
    push_authorized: false
    next_action: CONTINUE_IMPLEMENTATION
    final_status: HUMAN_REVIEW_REQUIRED

  - task_id: GENERIC-TASK.443
    title: Next Task Candidate
    source_file: null
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: QUEUED
    lifecycle_stage: CANDIDATE
    depends_on:
      - GENERIC-TASK.442
    blocked_by: []
    replaces: []
    replaced_by: null
    task_brief_status: NOT_CREATED
    risk_profile_assigned_by_human: false
    risk_profile: null
    execution_authorized: false
    commit_authorized: false
    push_authorized: false
    next_action: PREPARE_TASK_BRIEF
    final_status: HUMAN_REVIEW_REQUIRED

  - task_id: GENERIC-TASK.444
    title: Blocked Example Task
    source_file: null
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: BLOCKED
    lifecycle_stage: HUMAN_REVIEW_REQUIRED
    depends_on: []
    blocked_by:
      - GENERIC-TASK.441
    replaces: []
    replaced_by: null
    task_brief_status: DRAFT
    risk_profile_assigned_by_human: false
    risk_profile: null
    execution_authorized: false
    commit_authorized: false
    push_authorized: false
    next_action: RESOLVE_BLOCKER
    final_status: BLOCKED

  - task_id: GENERIC-TASK.445
    title: Deferred Example Task
    source_file: null
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: DEFERRED
    lifecycle_stage: HUMAN_REVIEW_REQUIRED
    depends_on: []
    blocked_by: []
    replaces: []
    replaced_by: null
    task_brief_status: DRAFT
    risk_profile_assigned_by_human: false
    risk_profile: null
    execution_authorized: false
    commit_authorized: false
    push_authorized: false
    next_action: NONE
    final_status: HUMAN_REVIEW_REQUIRED
```
