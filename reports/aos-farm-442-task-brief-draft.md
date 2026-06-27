---
task_id: AOS-FARM.442
task_brief_id: AOS-FARM.442-TASK-BRIEF-DRAFT
title: Task Registry and Queue Contract MVP
branch: build/task-registry-queue-contract-mvp
branch_from: origin/dev
baseline_commit: 2440c47cc89d074f459d39f687bb9ef15c9f2b4d
task_brief_status: DRAFT
risk_profile_required: true
risk_profile_assigned_by_human: false
risk_profile_assigned_by_agent: false
minimum_risk_profile_recommended_by_agent: HIGH_RISK_PROTECTED
execution_authorized: false
implementation_allowed: false
commit_authorized: false
push_authorized: false
final_status: HUMAN_REVIEW_REQUIRED

allowed_files_after_human_execution_authorization:
  - aos/docs/workflow/task-registry-and-queue.md
  - aos/templates/tasks/**
  - aos/reports/examples/task-registry/**
  - aos/tools/optional/task_registry_validator.py
  - aos/scripts/aos_tasks.py
  - tests/task_registry/**
  - reports/aos-farm-442-*.md
  - reports/human-checkpoints/aos-farm-442-*.md

forbidden_files:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  - 03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
  - agentos/**
  - .github/**
  - release/**
  - SQLite/RAG-light files
  - reports/aos-farm-441-remote-baseline-closure-report.md unless explicitly authorized

future_sqlite_rag_light_design_considered: true
markdown_yaml_registry_queue: Source of Truth
sqlite: future_derived_index_only
rag_light: future_navigation_search_summary_only
sqlite_implementation_allowed_now: false
rag_light_implementation_allowed_now: false
future_sqlite_may_read: true
future_sqlite_may_index: true
future_sqlite_may_cache: true
future_sqlite_may_report: true
future_sqlite_may_decide: false
future_sqlite_may_approve: false
future_sqlite_may_execute: false
future_sqlite_may_mutate_source_of_truth: false
future_rag_light_may_search: true
future_rag_light_may_summarize: true
future_rag_light_may_link_to_sources: true
future_rag_light_may_report_known_state: true
future_rag_light_may_approve: false
future_rag_light_may_execute: false
future_rag_light_may_assign_risk_profile: false
future_rag_light_may_mutate_lifecycle: false

validation_plan_after_human_execution_authorization:
  - unit tests
  - CLI smoke checks
  - diff check
  - semantic boundary review
  - dirty boundary review
  - no mutation review
  - future SQLite/RAG-light authority boundary review
---

# Task Registry and Queue Contract MVP (DRAFT)

## Purpose
Create a safe task-management control layer for AOS-FARM:
1. Task Registry — state of all known tasks.
2. Task Queue — ordered execution queue.
3. Workflow / State Machine — allowed and forbidden lifecycle transitions.
4. Automation / Validators — read-only validation, summary, show-current, show-next.

## Forbidden Behavior
The following behaviors and actions are strictly forbidden:
- runner
- auto execution
- auto approval
- Risk Profile assignment by agent
- commit automation
- push automation
- lifecycle mutation without explicit rules
- protected/canonical source changes
- agentos/**
- .github/**
- release/**
- SQLite implementation
- RAG-light implementation
- dirty boundary cleanup
- git reset
- git clean
- git stash
- git restore
- file deletion
- file move

## Future-Compatible Fields
This Task Brief requires future registry/queue templates to include the following schema fields:

```yaml
schema_version: 1
task_id: AOS-FARM.442
queue_item_id: AOS-FARM.QUEUE.2026-06-27-01.001
queue_revision: 2026-06-27-01
queue_order: "001"
source_file: null
source_commit: null
source_hash: null
indexed_at: null
registry_status: QUEUED
lifecycle_stage: CANDIDATE
task_brief_status: NOT_CREATED
depends_on:
  - AOS-FARM.441
blocked_by: []
replaces: []
replaced_by: null
risk_profile_assigned_by_human: false
risk_profile: null
execution_authorized: false
commit_authorized: false
push_authorized: false
next_action: PREPARE_TASK_BRIEF
final_status: HUMAN_REVIEW_REQUIRED
```
