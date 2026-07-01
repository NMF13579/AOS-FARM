---
task_id: AOS-FARM-TASK-0524
title: Validator Readiness/Approval Semantics Design
type: design_task
status: READY_FOR_EXECUTION
approval_status: NOT_REQUESTED
risk_profile: HIGH_RISK_PROTECTED
risk_profile_proposed: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: HIGH_RISK_PROTECTED
risk_assigned_by: human
validator_status: PENDING
log_status: NOT_RUN
log_uri: .aos-tmp/tasks/AOS-FARM-TASK-0524/log.txt
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
source_reports:
  - reports/aos-farm-523-readiness-vs-approval-validator-semantics-conflict-review.md
  - reports/aos-farm-522-task-canonical-schema-completion-report.md
  - reports/aos-farm-521-third-pass-report-only-package-closure-rereview.md
target_validator: aos/scripts/aos_task_document_check.py
target_issue: readiness_vs_approval_semantics_conflict
ready_for_execution: true
execution_authorized: true
approval_granted: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
allowed_future_files:
  - reports/validator-readiness-approval-semantics-design.md
forbidden_files:
  - aos/scripts/aos_task_document_check.py
  - tasks/AOS-FARM-TASK-0509.md
  - tasks/AOS-FARM-TASK-0513.md
  - tasks/AOS-FARM-TASK-0516.md
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  - /aos/**
  - aos/templates/**
  - aos/schemas/**
  - .github/workflows/**
stop_if:
  - human_decision_required
  - validator_change_required
  - canonical_change_required
  - task_migration_required
  - approval_status_approved_required
  - scope_unclear
  - execution_requested
  - commit_requested
  - push_requested
---

## Задача
Create a design report for safely separating readiness, execution authorization, and approval semantics in AOS-FARM task validation.

This task draft does not authorize validator implementation.
This task draft does not authorize migration of existing task files.
This task draft does not authorize adding approval_status: APPROVED to any task.

## Context
AOS-FARM.521 exposed that task validation still fails after YAML frontmatter correction.
AOS-FARM.522 identified that completing task schema would require an unsafe approval_status decision.
AOS-FARM.523 classified the issue as MIXED: TASK_SCHEMA_GAP + APPROVAL_SEMANTICS_CONFLICT.

## Problem
Current validator readiness logic appears to require approval_status: APPROVED for status: READY_FOR_EXECUTION.
This conflicts with the AOS-FARM invariant READY_FOR_EXECUTION ≠ approval.

## Scope
The future execution of this task, if separately authorized later, may only create:
reports/validator-readiness-approval-semantics-design.md

The future design report should define:
* current validator behavior;
* target semantics;
* proposed schema fields;
* migration strategy;
* validator update strategy;
* task fixture strategy;
* backward compatibility;
* safety gates;
* Risk Profile requirements;
* human checkpoint requirements.

## Non-goals
* no validator implementation;
* no validator patch;
* no migration script;
* no task migration;
* no canonical source change;
* no /aos/ change;
* no schema file change;
* no workflow change;
* no approval assignment;
* no commit/push/merge/release.

## Target model to design
```yaml
target_task_authority_model:
  readiness_status:
    meaning: "Task is structurally ready and execution has been separately authorized."
    approval_implication: false
  approval_status:
    allowed_values:
      - NOT_REQUESTED
      - HUMAN_REVIEW_REQUIRED
      - APPROVED
      - REJECTED
    approval_implication:
      APPROVED: true
      NOT_REQUESTED: false
      HUMAN_REVIEW_REQUIRED: false
      REJECTED: false
  execution_authorized:
    meaning: "Human authorized execution of the task scope."
    approval_implication: false
  approval_granted:
    meaning: "Explicit human approval."
    must_not_be_inferred_from:
      - validator PASS
      - Evidence
      - READY_FOR_EXECUTION
      - execution_authorized
```

## Validator behavior to design
```yaml
validator_readiness_should_check:
  - required_yaml_fields_present
  - required_sections_present
  - risk_profile_assigned_by_human_not_null
  - execution_authorized_true
  - approval_granted_not_required_for_readiness
  - approval_status_approved_not_required_for_readiness
  - no_blocked_status
  - no_unknown_blocked

validator_readiness_should_not_require:
  - approval_status_APPROVED
  - approval_granted_true
```

## Risk
HIGH_RISK_PROTECTED
Future implementation may affect validator behavior, task schema semantics, lifecycle boundaries, approval semantics, and migration of existing task files.

## Done когда
The future task will be done when a design report exists that:
* identifies current validator behavior;
* defines target readiness/approval separation;
* defines safe approval_status values;
* defines migration strategy;
* defines validator change strategy;
* defines test fixture strategy;
* preserves PASS ≠ approval;
* preserves Evidence ≠ approval;
* preserves READY_FOR_EXECUTION ≠ approval;
* does not authorize implementation by itself.

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
- AOS-FARM.524: Created DRAFT task for validator readiness/approval semantics design. No execution authorized.

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
