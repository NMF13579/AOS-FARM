# Candidate Promotion Human Checkpoint Draft

```yaml
artifact_id: candidate-promotion-checkpoint-draft
artifact_type: draft_checkpoint_format
source_task: tasks/AOS-FARM-TASK-0509.md
source_candidate: AOS-FARM-DRAFT-CANDIDATE-0004
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

## 6.1. Purpose

This checkpoint format exists to explicitly prevent confusing different states of readiness, specifically:
- DRAFT_CANDIDATE
- real task draft
- READY_FOR_EXECUTION
- approval
- execution authorization
- commit authorization
- push authorization
- merge/release authorization

## 6.2. Promotion boundary

The lifecycle sequence is strictly defined as follows:

DRAFT_CANDIDATE
→ human review
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

It is explicitly stated that:
- DRAFT_CANDIDATE ≠ real task
- real task draft ≠ READY_FOR_EXECUTION
- Risk Profile proposal ≠ Risk Profile assignment
- human review ≠ approval
- approval ≠ execution authorization unless explicitly stated
- execution authorization ≠ commit authorization
- commit authorization ≠ push authorization
- push authorization ≠ release authorization

## 6.3. Checkpoint record schema

```yaml
checkpoint_id: null
checkpoint_type: candidate_promotion_human_checkpoint
status: PENDING
candidate:
  candidate_id: null
  source_cycle: null
  source_reports: []
  candidate_status: DRAFT_CANDIDATE
promotion_decision:
  status: PENDING
  allowed_options:
    - REJECT
    - REQUEST_FIX
    - ACCEPT_AS_REPORT_ONLY
    - PROMOTE_TO_REAL_TASK_DRAFT
  selected_option: null
risk_profile:
  proposed_by_agent: null
  assigned_by_human: null
  assignment_required_before_ready_for_execution: true
execution:
  ready_for_execution: false
  execution_authorized: false
  authorization_required_before_execution: true
git_authority:
  commit_authorized: false
  push_authorized: false
release_authority:
  merge_authorized: false
  release_authorized: false
human_statement:
  required: true
  reviewer: null
  decision_timestamp: null
  decision_text: null
blocked_if:
  - source_refs_missing
  - candidate_status_not_draft_candidate
  - risk_profile_missing
  - human_decision_missing
  - execution_authorization_ambiguous
  - protected_canonical_change_needed
  - scope_unclear
```

## 6.4. Allowed human decisions

Allowed decisions for candidate promotion are:
- REJECT
- REQUEST_FIX
- ACCEPT_AS_REPORT_ONLY
- PROMOTE_TO_REAL_TASK_DRAFT

The following automated actions are explicitly forbidden:
- AUTO_PROMOTE
- AUTO_APPROVE
- AUTO_READY_FOR_EXECUTION
- AUTO_ASSIGN_RISK_PROFILE
- AUTO_COMMIT
- AUTO_PUSH

## 6.5. Required human statement

A human-authored statement is required for promotion. Minimum fields include:

```yaml
human_decision_statement:
  reviewer: null
  decision: null
  risk_profile_assigned_by_human: null
  execution_authorized: false
  commit_authorized: false
  push_authorized: false
  rationale: null
```

## 6.6. Validation rules

- candidate must have source reports;
- candidate must have source refs;
- candidate must remain DRAFT_CANDIDATE until promotion;
- promotion cannot assign Risk Profile unless human supplies it;
- READY_FOR_EXECUTION cannot be set without human Risk Profile assignment and execution authorization;
- reports cannot grant approval;
- Evidence cannot grant approval;
- PASS cannot grant approval;
- commit/push/release authority must remain separate;
- protected/canonical changes require checkpoint;
- UNKNOWN and NOT_RUN must remain visible and cannot be treated as PASS.

## 6.7. Non-goals

- this draft does not update `/aos/`;
- this draft does not update canonical governance sources;
- this draft does not implement validator code;
- this draft does not create task files;
- this draft does not authorize execution by itself;
- this draft does not authorize commit/push/merge/release.

## 6.8. Future promotion path

If this draft is accepted, a later human checkpoint may decide whether to:
- keep as report-only reference
- revise
- promote to template
- promote to `/aos/` consumer material
- promote to validator requirements

Each promotion path requires its own Risk Profile and human authorization.
