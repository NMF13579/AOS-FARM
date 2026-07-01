---
task_id: AOS-FARM-TASK-0513
title: Problem Intake To Technical Assignment Traceability Task Draft
status: READY_FOR_EXECUTION
source_candidate_id: AOS-FARM-DRAFT-CANDIDATE-0002
source_cycle: AOS-FARM-CYCLE-0001
source_cycle_artifacts:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
  - reports/aos-farm-505-draft-task-candidates.md
  - reports/aos-farm-506-draft-task-traceability-validation-report.md
  - reports/aos-farm-507-planning-cycle-final-review-package.md
  - reports/aos-farm-508-pre-existing-untracked-task-duplicate-cleanup-review.md
  - reports/candidate-promotion-checkpoint-draft.md
  - reports/aos-farm-512-task-0509-execution-report.md
risk_profile_proposed: MEDIUM_RISK_GUIDED
risk_profile_escalation_rule: "If future execution touches aos/scripts/, validators, lifecycle semantics, protected/canonical files, approval semantics, Evidence semantics, or workflow enforcement, Risk Profile must be escalated to HIGH_RISK_PROTECTED before execution."
risk_profile_assigned_by_human: MEDIUM_RISK_GUIDED
requires_human_review: true
ready_for_execution: true
execution_authorized: true
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
approval_granted: false
allowed_files:
  - reports/problem-intake-to-ta-traceability-draft.md
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
  - risk_profile_escalation_needed
  - execution_requested
  - commit_requested
  - push_requested
type: implementation_task
approval_status: NOT_REQUESTED
risk_assigned_by: human
validator_status: PENDING
log_status: NOT_RUN
log_uri: .aos-tmp/tasks/AOS-FARM-TASK-0513/log.txt
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
risk_profile: MEDIUM_RISK_GUIDED
---
# AOS-FARM-TASK-0513: Problem Intake To Technical Assignment Traceability Task Draft

## 7.1. Purpose

This task will draft a traceability format tracing requirements from Problem Intake to Technical Assignment and later DRAFT task candidates.

It must make explicit:
- Problem Intake output is not automatically a Technical Assignment.
- Technical Assignment is not implementation approval.
- Traceability PASS is not approval.
- UNKNOWN in intake must remain visible.
- Human decisions must be explicit.

## 7.2. Problem

The path from interview output to Technical Assignment can easily lose critical information, such as:
- assumptions;
- UNKNOWNs;
- user constraints;
- source anchors;
- safety blockers;
- human decisions;
- unresolved scope boundaries.

This loss of traceability can create false confidence before task decomposition begins.

## 7.3. Scope

The scope is strictly limited to drafting a report/checkpoint format.

Allowed future output if this task is later executed after explicit human authorization:
- `reports/problem-intake-to-ta-traceability-draft.md`

No `/aos/` changes.
No `aos/scripts/` changes.
No validator implementation.
No lifecycle automation.
No canonical source changes.
No task execution beyond drafting the traceability report.

## 7.4. Non-goals

This task explicitly will not include:
- no implementation pipeline;
- no automated Technical Assignment generation;
- no auto-approval;
- no Risk Profile assignment by agent;
- no READY_FOR_EXECUTION;
- no helper/validator code;
- no `/aos/` changes;
- no canonical source changes;
- no commit;
- no push;
- no merge;
- no release.

## 7.5. Proposed traceability fields

The future traceability draft should define fields for:

```yaml
traceability_record_id: null
source_problem_intake:
  source_file: null
  source_sections: []
  intake_status: null
problem_brief:
  source_file: null
  source_sections: []
  assumptions: []
  unknowns: []
  user_constraints: []
technical_assignment:
  source_file: null
  source_sections: []
  claims: []
  implementation_scope: []
  non_goals: []
mapping:
  intake_to_brief: []
  brief_to_ta: []
  ta_to_draft_candidates: []
human_decisions:
  required: true
  decisions: []
risk_and_safety:
  proposed_risk_profile: null
  assigned_risk_profile_by_human: null
  blockers: []
  unknown_blocked: []
validation:
  every_ta_claim_has_source: false
  unknowns_preserved: false
  human_decisions_explicit: false
  ready_for_execution: false
```

## 7.6. Required traceability rules

- every Technical Assignment claim must map to a Problem Intake source, Problem Brief source, or explicit human decision;
- every implementation scope item must have a source reference;
- every non-goal must remain visible;
- every UNKNOWN must remain visible until resolved by human decision or documented evidence;
- unsupported scope must be UNKNOWN_BLOCKED;
- external references are not Source of Truth;
- traceability PASS is not approval;
- traceability report is not execution authorization;
- Risk Profile proposal is not Risk Profile assignment.

## 7.7. Risk escalation rule

If future execution touches aos/scripts/, validators, lifecycle semantics, protected/canonical files, approval semantics, Evidence semantics, or workflow enforcement, Risk Profile must be escalated to HIGH_RISK_PROTECTED before execution.

## 7.8. Validation requirements

- task document validator;
- forbidden status scan;
- forbidden file scan;
- check that no `READY_FOR_EXECUTION` appears unless explicitly authorized later;
- check that no `execution_authorized: true` appears;
- check that `risk_profile_assigned_by_human` remains `null`;
- check that reports are not treated as approval;
- check that PASS/Evidence are not approval;
- check that every source reference is present;
- check that UNKNOWN/NOT_RUN are preserved.

## 7.9. Evidence requirements

The required future Evidence (for future execution only, not claiming it exists now):
- generated traceability draft;
- source candidate reference;
- source report references;
- diff stat;
- validator output;
- UNKNOWN / NOT_RUN list;
- human decision status.

## 7.10. Human checkpoint

This task cannot become READY_FOR_EXECUTION until a human explicitly assigns Risk Profile and authorizes execution in a separate step.

If HIGH_RISK escalation is triggered, human must assign:
`HIGH_RISK_PROTECTED`
before execution.

## 7.11. Current lifecycle status

```yaml
current_lifecycle_status:
  status: READY_FOR_EXECUTION
  ready_for_execution: true
  execution_authorized: true
  approval_granted: false
  human_review_required: true
```

## Задача
Create and govern the Candidate 0002 promotion task draft for Problem Intake to Technical Assignment traceability.

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
