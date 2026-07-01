# Planning Cycle Template Package Draft

```yaml
artifact_id: planning-cycle-template-package-draft
artifact_type: draft_planning_cycle_package_format
source_task: tasks/AOS-FARM-TASK-0516.md
source_candidate: AOS-FARM-DRAFT-CANDIDATE-0001
status: DRAFT
source_of_truth: false
canonical: false
approval_granted: false
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
requires_human_review: true
```

## 7.1. Purpose

This planning-cycle package format exists to make planning cycles repeatable, reviewable, and bounded.

It explicitly prevents these false transitions:
- planning-cycle package draft → Source of Truth
- planning-cycle package draft → approval
- template draft → canonical template
- template draft → validator enforcement
- report package PASS → approval
- Evidence package → approval
- external reference → Source of Truth
- DRAFT candidate → executable task
- real task draft → READY_FOR_EXECUTION
- commit authorization → push authorization
- push authorization → release authorization

## 7.2. Planning-cycle lifecycle boundary

planning cycle start
→ source collection
→ canonical source review
→ audit / gap analysis
→ external reference if provided
→ synthesis
→ DRAFT task candidates
→ candidate traceability validation
→ final review package
→ human review
→ candidate promotion checkpoint
→ real task draft
→ human Risk Profile assignment
→ human execution authorization
→ READY_FOR_EXECUTION
→ execution
→ Evidence / validation
→ human review
→ commit authorization
→ commit
→ push authorization
→ push
→ merge/release authorization if applicable

The following invariants apply:
- planning-cycle package ≠ approval
- planning-cycle PASS ≠ approval
- Evidence ≠ approval
- external reference ≠ Source of Truth
- DRAFT candidate ≠ real task
- real task draft ≠ READY_FOR_EXECUTION
- Risk Profile proposal ≠ Risk Profile assignment
- execution authorization ≠ commit authorization
- commit authorization ≠ push authorization
- push authorization ≠ release authorization
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- UNKNOWN_BLOCKED cannot be treated as OK

## 7.3. Planning-cycle package schema

```yaml
planning_cycle_package:
  cycle_id: null
  cycle_status: DRAFT
  source_reports: []
  canonical_sources_reviewed:
    required:
      - 00_AOS_Core_Control.md
      - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
      - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
    optional_reference:
      - 03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
      - 04_AOS_Model_Routing_and_Task_Decomposition_Research.md
    availability:
      all_required_available: false
      missing_required_sources: []
  external_references:
    provided: false
    source_of_truth: false
    not_run_reason: null
    notes: []
  audit_findings: []
  synthesis:
    summary: null
    assumptions: []
    unknowns: []
    not_run: []
    blocked: []
    unknown_blocked: []
  draft_candidates:
    candidates: []
    required_fields:
      - candidate_id
      - title
      - status
      - source_reports
      - risk_profile_proposed
      - risk_profile_assigned_by_human
      - execution_authorized
      - approval_granted
  candidate_promotion_checkpoints: []
  traceability_records: []
  human_decisions:
    required: true
    decisions: []
  risk_management:
    proposed_risk_profiles: []
    assigned_risk_profiles_by_human: []
    escalation_required_if: []
  validation:
    validators_run: []
    validators_not_run: []
    pass_is_approval: false
    evidence_is_approval: false
    unknown_is_ok: false
    not_run_is_pass: false
  blocked_items:
    blocked: []
    unknown_blocked: []
    not_run: []
  authority:
    approval_granted: false
    execution_authorized: false
    commit_authorized: false
    push_authorized: false
    merge_authorized: false
    release_authorized: false
```

## 7.4. Required planning-cycle sections

For future planning-cycle packages:
1. Cycle identity
2. Source inventory
3. Canonical sources reviewed
4. External references
5. Audit findings
6. Synthesis
7. DRAFT task candidates
8. Candidate traceability validation
9. Candidate promotion checkpoint status
10. Problem Intake to Technical Assignment traceability status
11. Human decisions
12. Risk Profile proposals and assignments
13. Validation results
14. BLOCKED / UNKNOWN_BLOCKED / NOT_RUN
15. Authority boundaries
16. Final review package
17. Human decision options

## 7.5. Required planning-cycle rules

- every planning cycle must list source reports;
- every planning cycle must state which required canonical sources were reviewed;
- missing required canonical sources must block architecture/roadmap/governance decisions;
- every external reference must be marked source_of_truth: false unless explicitly promoted by human decision;
- every draft candidate must have source reports;
- every draft candidate must have lifecycle status;
- every draft candidate must distinguish proposed Risk Profile from human-assigned Risk Profile;
- every draft candidate must state whether execution is authorized;
- planning-cycle PASS is not approval;
- report package Evidence is not approval;
- UNKNOWN and NOT_RUN must remain visible;
- UNKNOWN_BLOCKED cannot be treated as OK;
- DRAFT candidate cannot become real task without human checkpoint;
- real task draft cannot become READY_FOR_EXECUTION without human Risk Profile assignment and execution authorization;
- commit/push/merge/release must remain separate authorities;
- protected/canonical changes require checkpoint;
- template promotion requires separate Risk Profile assignment and human authorization.

## 7.6. Human decision requirements

Explicit human decision is required for:
- accepting a planning-cycle package as report-only
- requesting fixes
- rejecting a planning-cycle package
- promoting a DRAFT candidate to real task draft
- assigning Risk Profile
- authorizing execution
- authorizing commit
- authorizing push
- authorizing merge
- authorizing release
- promoting report-only draft to template
- promoting report-only draft to /aos/ consumer material
- promoting report-only draft to canonical governance documentation
- promoting report-only draft to validator requirements

```yaml
human_decision_record:
  decision_id: null
  reviewer: null
  decision_timestamp: null
  decision_type: null
  allowed_decision_types:
    - ACCEPT_REPORT_ONLY
    - REQUEST_FIX
    - REJECT
    - CANDIDATE_PROMOTION
    - RISK_PROFILE_ASSIGNMENT
    - EXECUTION_AUTHORIZATION
    - COMMIT_AUTHORIZATION
    - PUSH_AUTHORIZATION
    - MERGE_AUTHORIZATION
    - RELEASE_AUTHORIZATION
    - ARTIFACT_PROMOTION
  decision_text: null
  affected_artifacts: []
  authority_granted:
    approval_granted: false
    execution_authorized: false
    commit_authorized: false
    push_authorized: false
    merge_authorized: false
    release_authorized: false
```

## 7.7. Validation checklist

```yaml
planning_cycle_validation_checklist:
  cycle_id_present: false
  source_reports_present: false
  required_canonical_sources_reviewed: false
  missing_required_sources_blocked: false
  external_refs_marked_non_source_of_truth: false
  audit_findings_present: false
  synthesis_present: false
  draft_candidates_present: false
  every_candidate_has_source_reports: false
  every_candidate_has_lifecycle_status: false
  risk_profile_proposal_assignment_separated: false
  candidate_promotion_checkpoints_present: false
  traceability_records_present: false
  unknowns_preserved: false
  not_run_preserved: false
  unknown_blocked_explicit: false
  pass_not_approval_statement_present: false
  evidence_not_approval_statement_present: false
  execution_not_commit_statement_present: false
  commit_not_push_statement_present: false
  push_not_release_statement_present: false
```

## 7.8. Blocked conditions

```yaml
blocked_if:
  - required_canonical_source_missing
  - source_reports_missing
  - candidate_source_refs_missing
  - candidate_lifecycle_status_missing
  - risk_profile_assignment_simulated_by_agent
  - execution_authorization_missing
  - approval_inferred_from_pass
  - approval_inferred_from_evidence
  - unknown_dropped
  - not_run_treated_as_pass
  - unknown_blocked_treated_as_ok
  - external_reference_treated_as_source_of_truth
  - draft_candidate_auto_promoted
  - ready_for_execution_without_human_risk_profile_assignment
  - commit_authorized_without_human_decision
  - push_authorized_without_human_decision
  - protected_canonical_change_needed
  - scope_unclear
```

## 7.9. Non-goals

- this draft does not update /aos/;
- this draft does not update canonical governance sources;
- this draft does not implement validator code;
- this draft does not create task files;
- this draft does not create helper code;
- this draft does not create actual templates;
- this draft does not authorize execution by itself;
- this draft does not authorize commit/push/merge/release;
- this draft does not promote itself to template;
- this draft does not become Source of Truth unless separately promoted by human decision.

## 7.10. Future promotion path

If this draft is accepted, a later human checkpoint may decide whether to:
- keep as report-only reference
- revise
- promote to template
- promote to /aos/ consumer material
- promote to validator requirements
- promote to canonical governance documentation

Each promotion path requires its own Risk Profile and explicit human authorization.
If promotion touches protected/canonical files, `/aos/`, validators, lifecycle semantics, approval semantics, Evidence semantics, workflow enforcement, or CI/workflow behavior, Risk Profile must be `HIGH_RISK_PROTECTED`.
