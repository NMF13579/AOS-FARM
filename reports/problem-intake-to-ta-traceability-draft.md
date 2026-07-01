# Problem Intake To Technical Assignment Traceability Draft

```yaml
artifact_id: problem-intake-to-ta-traceability-draft
artifact_type: draft_traceability_format
source_task: tasks/AOS-FARM-TASK-0513.md
source_candidate: AOS-FARM-DRAFT-CANDIDATE-0002
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

This traceability format exists to preserve links between:
- Problem Intake
- Problem Brief / ТЗ
- Technical Assignment
- Implementation Plan
- DRAFT task candidates

It explicitly prevents the following false transitions:
- Problem Intake output → automatic Technical Assignment
- Technical Assignment → implementation approval
- Traceability PASS → approval
- External reference → Source of Truth
- UNKNOWN omitted → OK
- NOT_RUN omitted → PASS
- DRAFT candidate → executable task

## 7.2. Lifecycle boundary

The traceability sequence is strictly defined as:

Problem Intake
→ Problem Brief / ТЗ
→ Technical Assignment
→ Implementation Plan
→ DRAFT task candidates
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

It is explicitly stated that:
- Problem Intake ≠ Technical Assignment
- Problem Brief ≠ implementation approval
- Technical Assignment ≠ execution authorization
- Implementation Plan ≠ approval
- DRAFT task candidate ≠ real task
- real task draft ≠ READY_FOR_EXECUTION
- Risk Profile proposal ≠ Risk Profile assignment
- PASS ≠ approval
- Evidence ≠ approval
- NOT_RUN ≠ PASS
- UNKNOWN ≠ OK
- commit authorization ≠ push authorization
- push authorization ≠ release authorization

## 7.3. Traceability record schema

```yaml
traceability_record_id: null
record_type: problem_intake_to_technical_assignment_traceability
status: DRAFT
source_problem_intake:
  source_file: null
  source_sections: []
  intake_status: null
  assumptions: []
  unknowns: []
  user_constraints: []
  safety_notes: []
problem_brief:
  source_file: null
  source_sections: []
  claims: []
  assumptions: []
  unknowns: []
  non_goals: []
technical_assignment:
  source_file: null
  source_sections: []
  claims: []
  implementation_scope: []
  non_goals: []
  explicit_human_decisions: []
implementation_plan:
  source_file: null
  source_sections: []
  planned_steps: []
  non_goals: []
  blockers: []
draft_task_candidates:
  source_file: null
  candidates: []
mapping:
  intake_to_brief: []
  brief_to_ta: []
  ta_to_implementation_plan: []
  implementation_plan_to_draft_candidates: []
human_decisions:
  required: true
  decisions: []
risk_and_safety:
  proposed_risk_profile: null
  assigned_risk_profile_by_human: null
  risk_profile_assignment_required_before_ready_for_execution: true
  blockers: []
  unknown_blocked: []
  not_run: []
validation:
  every_ta_claim_has_source: false
  every_scope_item_has_source: false
  non_goals_preserved: false
  unknowns_preserved: false
  not_run_preserved: false
  human_decisions_explicit: false
  external_refs_marked_non_source_of_truth: false
  ready_for_execution: false
authority:
  approval_granted: false
  execution_authorized: false
  commit_authorized: false
  push_authorized: false
  merge_authorized: false
  release_authorized: false
```

## 7.4. Required mapping rules

- every Technical Assignment claim must map to a Problem Intake source, Problem Brief source, or explicit human decision;
- every implementation scope item must have a source reference;
- every planned implementation step must map back to a Technical Assignment claim or explicit human decision;
- every DRAFT task candidate must map back to a Technical Assignment claim, implementation plan step, or explicit human decision;
- every non-goal must remain visible through the chain;
- every UNKNOWN must remain visible until resolved by human decision or documented Evidence;
- every NOT_RUN must remain visible and cannot be treated as PASS;
- unsupported scope must be marked UNKNOWN_BLOCKED;
- external references must be marked `source_of_truth: false`;
- traceability PASS is not approval;
- traceability report is not execution authorization;
- Risk Profile proposal is not Risk Profile assignment;
- human review is not approval unless explicit approval field exists and is human-provided.

## 7.5. Human decision requirements

An explicit human decision is strictly required for:
- scope expansion
- UNKNOWN resolution
- Risk Profile assignment
- execution authorization
- commit authorization
- push authorization
- merge authorization
- release authorization
- promotion from DRAFT candidate to real task draft
- promotion from report-only draft to template/canonical/product artifact

```yaml
human_decision_record:
  decision_id: null
  reviewer: null
  decision_timestamp: null
  decision_type: null
  allowed_decision_types:
    - SCOPE_CONFIRMATION
    - UNKNOWN_RESOLUTION
    - RISK_PROFILE_ASSIGNMENT
    - EXECUTION_AUTHORIZATION
    - COMMIT_AUTHORIZATION
    - PUSH_AUTHORIZATION
    - MERGE_AUTHORIZATION
    - RELEASE_AUTHORIZATION
    - CANDIDATE_PROMOTION
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

## 7.6. Validation checklist

```yaml
traceability_validation_checklist:
  source_problem_intake_present: false
  problem_brief_present: false
  technical_assignment_present: false
  implementation_plan_present: false
  draft_candidates_present: false
  every_ta_claim_has_source: false
  every_scope_item_has_source: false
  every_draft_candidate_has_source: false
  non_goals_preserved: false
  unknowns_preserved: false
  not_run_preserved: false
  unknown_blocked_explicit: false
  external_refs_marked_non_source_of_truth: false
  human_decisions_explicit: false
  pass_not_approval_statement_present: false
  evidence_not_approval_statement_present: false
  execution_not_commit_statement_present: false
  commit_not_push_statement_present: false
  push_not_release_statement_present: false
```

## 7.7. Blocked conditions

```yaml
blocked_if:
  - source_problem_intake_missing
  - problem_brief_missing
  - technical_assignment_missing
  - implementation_scope_without_source
  - ta_claim_without_source
  - draft_candidate_without_source
  - unknown_dropped
  - not_run_treated_as_pass
  - external_reference_treated_as_source_of_truth
  - risk_profile_assigned_by_agent
  - ready_for_execution_without_human_risk_profile_assignment
  - execution_authorized_without_human_decision
  - commit_authorized_without_human_decision
  - push_authorized_without_human_decision
  - protected_canonical_change_needed
  - scope_unclear
```

## 7.8. Non-goals

This draft explicitly states:
- this draft does not update `/aos/`;
- this draft does not update canonical governance sources;
- this draft does not implement validator code;
- this draft does not create task files;
- this draft does not create helper code;
- this draft does not authorize execution by itself;
- this draft does not authorize commit/push/merge/release;
- this draft does not promote itself to template;
- this draft does not become Source of Truth unless separately promoted by human decision.

## 7.9. Future promotion path

If this draft is accepted, a later human checkpoint may decide whether to:
- keep as report-only reference
- revise
- promote to template
- promote to `/aos/` consumer material
- promote to validator requirements
- promote to canonical governance documentation

Each promotion path requires its own Risk Profile and explicit human authorization.
If promotion touches protected/canonical files, `/aos/`, validators, lifecycle semantics, approval semantics, Evidence semantics, or workflow enforcement, Risk Profile must be `HIGH_RISK_PROTECTED`.
