# AOS-FARM.505 DRAFT Task Candidates

```yaml
report_id: AOS-FARM.505
cycle: AOS-FARM-CYCLE-0001
report_type: draft_task_candidates
status: READY_FOR_HUMAN_REVIEW
contains_executable_tasks: false
approval_granted: false
execution_authorized: false
```

These are DRAFT task candidates in a report. They are not files under `tasks/`, not executable tasks, not approved work, and not lifecycle mutations.

## Candidate 0001 - Planning Cycle Package Templates

```yaml
task_candidate_id: AOS-FARM-DRAFT-CANDIDATE-0001
status: DRAFT_CANDIDATE
source_cycle: AOS-FARM-CYCLE-0001
source_reports:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
requires_human_review: true
risk_profile_proposed: MEDIUM_RISK_GUIDED
risk_profile_proposal_reason: "Creates non-canonical planning/report templates; no protected change unless promoted separately."
risk_profile_assigned_by_human: null
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
scope_type: planning_or_code_candidate
ready_for_execution: false
allowed_files_proposed_for_future_task:
  - reports/planning-cycle-template-draft.md
  - templates/planning-cycle-report-template.md
actual_files_changed_in_this_cycle:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
  - reports/aos-farm-505-draft-task-candidates.md
  - reports/aos-farm-506-draft-task-traceability-validation-report.md
  - reports/aos-farm-507-planning-cycle-final-review-package.md
forbidden_files:
  - /aos/**
  - aos/scripts/**
  - aos/templates/**
  - aos/schemas/**
  - .github/workflows/**
  - tasks/**
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
```

- Problem found: planning-cycle artifacts are currently produced ad hoc.
- Why it matters: repeatability and review quality depend on fixed fields and explicit boundaries.
- Source refs: `AOS-FARM.502 / Gaps`, `AOS-FARM.504 / Requires Template / Report`.
- Proposed fix: draft templates for the six-report package and final review package.
- Code translation candidate: no for first pass; template/report only.
- Proposed files if later promoted: report/template paths only, not `/aos/` unless a separate checkpoint allows it.
- Required validation: path-scoped diff, forbidden-status scan, source-ref check.
- Evidence requirements: created template list, diff stat, validation output, NOT_RUN list.
- Human checkpoint needed: yes, before any template becomes canonical or enters `/aos/`.
- Reason it remains DRAFT_CANDIDATE: no human promotion, no Risk Profile assignment, no execution authorization.

## Candidate 0002 - Problem Intake To Technical Assignment Traceability

```yaml
task_candidate_id: AOS-FARM-DRAFT-CANDIDATE-0002
status: DRAFT_CANDIDATE
source_cycle: AOS-FARM-CYCLE-0001
source_reports:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
requires_human_review: true
risk_profile_proposed: MEDIUM_RISK_GUIDED
risk_profile_proposal_reason: "Strengthens planning traceability; may become HIGH_RISK_PROTECTED if promoted to validator or /aos/ semantics change."
risk_profile_assigned_by_human: null
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
scope_type: planning_or_code_candidate
ready_for_execution: false
allowed_files_proposed_for_future_task:
  - reports/problem-intake-to-ta-traceability-draft.md
  - templates/spec-to-execution-traceability-matrix-template.md
actual_files_changed_in_this_cycle:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
  - reports/aos-farm-505-draft-task-candidates.md
  - reports/aos-farm-506-draft-task-traceability-validation-report.md
  - reports/aos-farm-507-planning-cycle-final-review-package.md
forbidden_files:
  - /aos/**
  - aos/scripts/**
  - aos/templates/**
  - aos/schemas/**
  - .github/workflows/**
  - tasks/**
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
```

- Problem found: the path from interview output to Technical Assignment can lose assumptions, UNKNOWNs, and source anchors.
- Why it matters: unsupported technical scope can create false confidence before task decomposition.
- Source refs: `AOS-FARM.502 / Six-Stage Workflow Audit`, `AOS-FARM.504 / Include In Third Pass`.
- Proposed fix: create a traceability matrix from Problem Intake fields to Technical Assignment sections.
- Code translation candidate: yes later, as a read-only helper or validator.
- Proposed files if later promoted: report/template/helper paths chosen by a real task brief.
- Required validation: every Technical Assignment claim maps to intake source or explicit human decision.
- Evidence requirements: traceability matrix, unresolved UNKNOWN list, human decision list.
- Human checkpoint needed: yes before using the output for task execution.
- Reason it remains DRAFT_CANDIDATE: no task file, no approval, no assigned Risk Profile.

## Candidate 0003 - DRAFT Candidate Traceability Validator

```yaml
task_candidate_id: AOS-FARM-DRAFT-CANDIDATE-0003
status: DRAFT_CANDIDATE
source_cycle: AOS-FARM-CYCLE-0001
source_reports:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
requires_human_review: true
risk_profile_proposed: HIGH_RISK_PROTECTED
risk_profile_proposal_reason: "Validator work can affect lifecycle/approval semantics and must preserve fail-closed behavior."
risk_profile_assigned_by_human: null
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
scope_type: planning_or_code_candidate
ready_for_execution: false
allowed_files_proposed_for_future_task:
  - reports/draft-candidate-validator-design.md
  - tests/fixtures/draft_candidate_validation/**
actual_files_changed_in_this_cycle:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
  - reports/aos-farm-505-draft-task-candidates.md
  - reports/aos-farm-506-draft-task-traceability-validation-report.md
  - reports/aos-farm-507-planning-cycle-final-review-package.md
forbidden_files:
  - /aos/**
  - aos/scripts/**
  - aos/templates/**
  - aos/schemas/**
  - .github/workflows/**
  - tasks/**
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
```

- Problem found: DRAFT candidates rely on manual review to ensure no executable-task semantics leak in.
- Why it matters: validator gaps can allow `READY_FOR_EXECUTION`, assigned risk, or authorization fields to appear unnoticed.
- Source refs: `AOS-FARM.504 / Requires Validator`, `AOS-FARM.506 validation requirements`.
- Proposed fix: design and later implement a read-only validator for DRAFT candidate reports.
- Code translation candidate: yes, but only after a separate human checkpoint.
- Proposed files if later promoted: design report, fixtures, and a future script path chosen by human-approved scope.
- Required validation: negative cases for approval claims, execution authorization, missing source refs, and protected file proposals.
- Evidence requirements: py_compile, unit tests, negative fixture results, path-scoped diff.
- Human checkpoint needed: yes, HIGH_RISK_PROTECTED proposed.
- Reason it remains DRAFT_CANDIDATE: validator implementation is not authorized in this planning cycle.

## Candidate 0004 - Candidate Promotion Human Checkpoint

```yaml
task_candidate_id: AOS-FARM-DRAFT-CANDIDATE-0004
status: DRAFT_CANDIDATE
source_cycle: AOS-FARM-CYCLE-0001
source_reports:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
requires_human_review: true
risk_profile_proposed: HIGH_RISK_PROTECTED
risk_profile_proposal_reason: "Promotion boundary touches lifecycle and execution-readiness semantics."
risk_profile_assigned_by_human: null
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
scope_type: planning_or_code_candidate
ready_for_execution: false
allowed_files_proposed_for_future_task:
  - reports/candidate-promotion-checkpoint-draft.md
actual_files_changed_in_this_cycle:
  - reports/aos-farm-502-user-workflow-stage-gap-audit.md
  - reports/aos-farm-503-external-best-practices-reference.md
  - reports/aos-farm-504-third-pass-planning-synthesis-report.md
  - reports/aos-farm-505-draft-task-candidates.md
  - reports/aos-farm-506-draft-task-traceability-validation-report.md
  - reports/aos-farm-507-planning-cycle-final-review-package.md
forbidden_files:
  - /aos/**
  - aos/scripts/**
  - aos/templates/**
  - aos/schemas/**
  - .github/workflows/**
  - tasks/**
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
```

- Problem found: the transition from DRAFT candidate to real task needs an explicit checkpoint.
- Why it matters: candidate review can be mistaken for approval or execution readiness.
- Source refs: `AOS-FARM.502 / Gaps`, `AOS-FARM.504 / Requires Human Checkpoint`.
- Proposed fix: draft a human checkpoint format for candidate promotion.
- Code translation candidate: no initially; checkpoint/report only.
- Proposed files if later promoted: report/checkpoint draft path chosen by human-approved task.
- Required validation: no approval status unless human explicitly fills it; no execution authorization in draft.
- Evidence requirements: checkpoint diff, source candidate reference, human decision fields.
- Human checkpoint needed: yes.
- Reason it remains DRAFT_CANDIDATE: promotion itself is a human decision and is not available here.
