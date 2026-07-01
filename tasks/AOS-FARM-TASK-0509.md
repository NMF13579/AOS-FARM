---
task_id: AOS-FARM-TASK-0509
title: Candidate 0004 Promotion Human Checkpoint Task Draft
status: READY_FOR_EXECUTION
source_candidate_id: AOS-FARM-DRAFT-CANDIDATE-0004
source_cycle: AOS-FARM-CYCLE-0001
source_cycle_artifacts:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
  - reports/aos-farm-505-draft-task-candidates.md
  - reports/aos-farm-506-draft-task-traceability-validation-report.md
  - reports/aos-farm-507-planning-cycle-final-review-package.md
  - reports/aos-farm-508-pre-existing-untracked-task-duplicate-cleanup-review.md
risk_profile_proposed: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: HIGH_RISK_PROTECTED
requires_human_review: true
ready_for_execution: true
execution_authorized: true
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
approval_granted: false
allowed_files:
  - reports/candidate-promotion-checkpoint-draft.md
forbidden_files:
  - /aos/**
  - aos/scripts/**
  - aos/templates/**
  - aos/schemas/**
  - .github/workflows/**
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
stop_if:
  - scope_unclear
  - source_refs_missing
  - protected_canonical_change_needed
  - human_decision_required
  - execution_requested
  - commit_requested
  - push_requested
type: implementation_task
approval_status: NOT_REQUESTED
risk_assigned_by: human
validator_status: PENDING
log_status: NOT_RUN
log_uri: .aos-tmp/tasks/AOS-FARM-TASK-0509/log.txt
template_level: task
owner: human
queue_position: 1
queue_mode: MANUAL
queue_priority: NORMAL
queue_status: DONE
human_checkpoint_required: true
created_at: null
updated_at: null
evidence_status: PENDING
risk_profile: HIGH_RISK_PROTECTED
---
# AOS-FARM-TASK-0509: Candidate 0004 Promotion Human Checkpoint Task Draft

## 7.1. Purpose

This task will draft a human checkpoint format for the promotion from a DRAFT candidate to a real task file that remains non-executable until separate human Risk Profile assignment and execution authorization.

It is critical to explicitly recognize that:
- DRAFT_CANDIDATE ≠ real task
- real task DRAFT ≠ READY_FOR_EXECUTION
- Risk Profile proposal ≠ Risk Profile assignment
- human review ≠ approval
- approval ≠ execution authorization unless explicitly stated

## 7.2. Problem

Candidate review can easily be mistaken for approval or execution readiness.
The transition from a DRAFT candidate to a real task needs a clear, unambiguous human checkpoint.

## 7.3. Scope

The scope is strictly limited to drafting a report/checkpoint format.

Allowed future output (if this task is later executed after explicit human authorization):
- `reports/candidate-promotion-checkpoint-draft.md`

No changes to `/aos/`. No validator implementation. No lifecycle automation. No canonical source changes.

## 7.4. Non-goals

This task will absolutely not include:
- no execution pipeline;
- no automated promotion;
- no auto-approval;
- no Risk Profile assignment by agent;
- no READY_FOR_EXECUTION;
- no commit;
- no push;
- no merge;
- no release.

## 7.5. Proposed checkpoint fields

The future checkpoint draft should define fields for:
```yaml
candidate_id: null
source_reports: []
promotion_decision:
  status: PENDING
  allowed_options:
    - REJECT
    - REQUEST_FIX
    - ACCEPT_AS_REPORT_ONLY
    - PROMOTE_TO_REAL_TASK_DRAFT
risk_profile:
  proposed_by_agent: null
  assigned_by_human: null
execution:
  ready_for_execution: false
  execution_authorized: false
git_authority:
  commit_authorized: false
  push_authorized: false
release_authority:
  merge_authorized: false
  release_authorized: false
required_human_statement: null
```

## 7.6. Validation requirements

The future implementation must include validation rules:
- task document validator;
- forbidden status scan;
- forbidden file scan;
- check that no `READY_FOR_EXECUTION` appears;
- check that no `execution_authorized: true` appears;
- check that no `risk_profile_assigned_by_human` is non-null unless human explicitly supplied it;
- check that reports are not treated as approval;
- check that PASS/Evidence are not treated as approval.

## 7.7. Evidence requirements

The required future Evidence (for future execution only, not claiming it exists now):
- generated checkpoint draft;
- source candidate reference;
- diff stat;
- validator output;
- NOT_RUN/UNKNOWN list;
- human decision status.

## 7.8. Human checkpoint

This task cannot become READY_FOR_EXECUTION until a human explicitly assigns Risk Profile and authorizes execution in a separate step.

## 7.9. Current lifecycle status

```yaml
current_lifecycle_status:
  status: READY_FOR_EXECUTION
  ready_for_execution: true
  execution_authorized: true
  approval_granted: false
  human_review_required: true
```

## Задача
Create and govern the candidate promotion human checkpoint draft for Candidate 0004.

## Done когда
Done when the task artifact/report exists, required validator checks have been run, Evidence is recorded in permitted Source of Truth locations, and the task is ready for human review. Done does not mean approval.

## История
- AOS-FARM.533 added canonical schema fields/sections.
- AOS-FARM.534 requested semantic correction because Evidence wording pointed to log_uri/.aos-tmp.
- AOS-FARM.535 corrected Evidence and placeholder section wording without changing lifecycle authority.

## Evidence
Evidence status: PENDING.
Current Evidence is limited to this task file lifecycle state and related reports listed in the task context.
Local log_uri is not Evidence and not Source of Truth.
Evidence is stored in the task file and referenced reports only.
.aos-tmp is disposable and not Source of Truth.
Evidence is not approval.
Validator PASS is not approval.

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
