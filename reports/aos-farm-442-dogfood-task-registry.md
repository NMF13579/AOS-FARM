schema_version: 1
tasks:
  - task_id: AOS-FARM.441
    title: Remote Baseline Closure
    source_file: reports/aos-farm-441-remote-baseline-closure-report.md
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
  - task_id: AOS-FARM.442
    title: Task Registry and Queue Contract MVP
    source_file: reports/aos-farm-442-task-brief-draft.md
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: HUMAN_REVIEW_REQUIRED
    lifecycle_stage: IN_PROGRESS
    depends_on:
      - AOS-FARM.441
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
  - task_id: AOS-FARM.443
    title: Next Task Candidate
    source_file: null
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: QUEUED
    lifecycle_stage: CANDIDATE
    depends_on:
      - AOS-FARM.442
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
  - task_id: AOS-FARM.444
    title: Optional Dirty Boundary Cleanup Candidate
    source_file: null
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: BLOCKED
    lifecycle_stage: CANDIDATE
    depends_on:
      - AOS-FARM.442
    blocked_by:
      - HUMAN_DECISION_REQUIRED
    replaces: []
    replaced_by: null
    task_brief_status: NOT_CREATED
    risk_profile_assigned_by_human: false
    risk_profile: null
    execution_authorized: false
    commit_authorized: false
    push_authorized: false
    next_action: HUMAN_REVIEW_REQUIRED
    final_status: BLOCKED
  - task_id: AOS-FARM.445
    title: Deferred Task Candidate
    source_file: null
    source_commit: null
    source_hash: null
    indexed_at: null
    registry_status: DEFERRED
    lifecycle_stage: CANDIDATE
    depends_on:
      - AOS-FARM.442
    blocked_by: []
    replaces: []
    replaced_by: null
    task_brief_status: NOT_CREATED
    risk_profile_assigned_by_human: false
    risk_profile: null
    execution_authorized: false
    commit_authorized: false
    push_authorized: false
    next_action: REACTIVATE_BEFORE_SELECTION
    final_status: HUMAN_REVIEW_REQUIRED
