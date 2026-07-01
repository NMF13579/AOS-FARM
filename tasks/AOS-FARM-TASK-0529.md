---
task_id: AOS-FARM-TASK-0529
title: Validator Readiness/Approval Semantics Implementation
type: implementation_task
status: READY_FOR_EXECUTION
approval_status: NOT_REQUESTED
risk_profile: HIGH_RISK_PROTECTED
risk_profile_proposed: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: HIGH_RISK_PROTECTED
risk_assigned_by: human
validator_status: PENDING
log_status: NOT_RUN
log_uri: .aos-tmp/tasks/AOS-FARM-TASK-0529/log.txt
template_level: task
owner: human
queue_position: 1
queue_mode: MANUAL
queue_priority: NORMAL
queue_status: IN_PROGRESS
human_checkpoint_required: true
created_at: null
updated_at: null
evidence_status: PENDING
source_design: reports/validator-readiness-approval-semantics-design.md
source_review: reports/aos-farm-528-validator-readiness-approval-semantics-design-review.md
source_reports:
  - reports/aos-farm-523-readiness-vs-approval-validator-semantics-conflict-review.md
  - reports/validator-readiness-approval-semantics-design.md
  - reports/aos-farm-528-validator-readiness-approval-semantics-design-review.md
target_validator: aos/scripts/aos_task_document_check.py
target_issue: readiness_requires_approval_status_approved
ready_for_execution: true
execution_authorized: true
approval_granted: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
allowed_future_files:
  - aos/scripts/aos_task_document_check.py
  - tests/fixtures/validator-readiness-approval-semantics/**
  - reports/aos-farm-530-validator-readiness-approval-semantics-implementation-report.md
forbidden_files:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  - /aos/**
  - aos/templates/**
  - aos/schemas/**
  - .github/workflows/**
stop_if:
  - human_decision_required
  - source_design_missing
  - source_review_missing
  - validator_scope_unclear
  - canonical_change_required
  - task_migration_required
  - approval_status_approved_required_for_unapproved_task
  - approval_simulation_required
  - execution_requested
  - commit_requested
  - push_requested
---

## Задача
Implement the approved report-only design for separating validator readiness and approval semantics in `aos/scripts/aos_task_document_check.py`.

This task draft does not authorize implementation.
This task draft does not authorize validator changes.
This task draft does not authorize task migration.
This task draft does not authorize adding `approval_status: APPROVED` to any unapproved task.

## Context
AOS-FARM.523 classified a validator conflict where `READY_FOR_EXECUTION` is coupled to `approval_status: APPROVED`.
AOS-FARM.526 produced a report-only design for separating readiness and approval semantics.
AOS-FARM.528 accepted that design as report-only.

## Problem
Current validator readiness logic blocks `READY_FOR_EXECUTION` unless `approval_status` is `APPROVED`.
This violates `READY_FOR_EXECUTION ≠ approval` and creates pressure to simulate approval.

## Scope
The future implementation, if separately authorized later, may only:
* update validator readiness logic in `aos/scripts/aos_task_document_check.py`;
* add focused fixtures/tests for readiness vs approval semantics;
* create implementation report;
* run validator checks;
* verify 0509/0513/0516/0524 no longer fail for the wrong approval reason.

The future implementation must not:
* grant approval;
* set `approval_status: APPROVED` on unapproved tasks;
* migrate task files unless separately authorized;
* change canonical sources;
* change `/aos/`;
* change workflows;
* broaden validator semantics beyond accepted design.

## Target implementation behavior
```yaml
target_validator_behavior:
  readiness_should_require:
    - required_yaml_fields_present
    - required_sections_present
    - status_is_READY_FOR_EXECUTION
    - risk_profile_assigned_by_human_not_null
    - execution_authorized_true
    - approval_status_present
    - approval_status_not_REJECTED
    - no_blocked_status
    - no_unknown_blocked
  readiness_should_not_require:
    - approval_status_APPROVED
    - approval_granted_true
    - commit_authorized_true
    - push_authorized_true
    - release_authorized_true
  approval_checks_should_remain_separate:
    - approval_status_APPROVED_requires_explicit_human_decision
    - approval_granted_true_requires_explicit_human_decision
```

## Future test/fixture requirements
```yaml
required_future_test_cases:
  - name: ready_for_execution_without_approval_is_valid_readiness
    status: READY_FOR_EXECUTION
    approval_status: NOT_REQUESTED
    execution_authorized: true
    approval_granted: false
    expected_readiness: PASS
  - name: approved_task_requires_explicit_approval
    status: READY_FOR_EXECUTION
    approval_status: APPROVED
    approval_granted: true
    expected_approval_check: PASS
  - name: rejected_approval_blocks_readiness
    status: READY_FOR_EXECUTION
    approval_status: REJECTED
    execution_authorized: true
    expected_readiness: BLOCKED
  - name: execution_not_authorized_blocks_readiness
    status: READY_FOR_EXECUTION
    approval_status: NOT_REQUESTED
    execution_authorized: false
    expected_readiness: BLOCKED
```

## Risk
HIGH_RISK_PROTECTED

Future implementation touches validator behavior, lifecycle readiness semantics, approval semantics, and task validation gates.

## Non-goals
* no implementation in this stage;
* no validator patch in this stage;
* no fixtures in this stage;
* no task migration in this stage;
* no canonical source change;
* no `/aos/` change;
* no schema file change;
* no workflow change;
* no approval assignment;
* no commit/push/merge/release.

## Done когда
The future implementation task will be done only when, after separate human authorization:
* validator no longer requires `approval_status: APPROVED` for readiness;
* validator still blocks `approval_status: REJECTED`;
* validator still requires explicit human decision for actual approval;
* fixtures/tests cover readiness without approval;
* fixtures/tests cover approval-specific checks separately;
* 0509/0513/0516/0524 no longer fail due to the obsolete `READY_FOR_EXECUTION`/`APPROVED` coupling;
* no task receives fake approval;
* validation output and Evidence are recorded;
* implementation report is created.

## Evidence
For this task draft stage, Evidence is limited to:
* created task draft file;
* created task draft report;
* validator output if run;
* git status;
* git diff stat.

Evidence is not approval.
Validator PASS is not approval.

Evidence is stored in the task file and referenced reports only.
log_uri is local-only scratch/log pointer and is not Evidence.
.aos-tmp is disposable and not Source of Truth.

## История
- AOS-FARM.529: Created DRAFT implementation task for validator readiness/approval semantics. No implementation authorized.

## ⛔ Решение
```yaml
decision_status: READY_FOR_HUMAN_REVIEW
approval_granted: false
execution_authorized: true
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```
