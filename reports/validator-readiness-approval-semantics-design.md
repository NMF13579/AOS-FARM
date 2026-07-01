---
artifact_id: validator-readiness-approval-semantics-design
artifact_type: report_only_design
source_task: tasks/AOS-FARM-TASK-0524.md
source_reports:
  - reports/aos-farm-523-readiness-vs-approval-validator-semantics-conflict-review.md
  - reports/aos-farm-524-validator-readiness-approval-semantics-design-task-draft-report.md
  - reports/aos-farm-525-task-0524-risk-profile-execution-gate-report.md
status: DRAFT
source_of_truth: false
canonical: false
implementation_authorized: false
validator_change_authorized: false
task_migration_authorized: false
approval_granted: false
execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
requires_human_review: true
---

# Validator Readiness/Approval Semantics Design

## Purpose
This design exists to safely separate:
- readiness
- execution authorization
- approval
- validator PASS
- Evidence
- commit/push/release authority

It must explicitly state:
- READY_FOR_EXECUTION is not approval.
- execution_authorized is not approval.
- validator PASS is not approval.
- Evidence is not approval.
- approval_status: APPROVED must never be inferred.
- Human approval cannot be simulated.

## Current conflict
`aos_task_document_check.py` currently blocks `status: READY_FOR_EXECUTION` without `approval_status: APPROVED`.

This is unsafe because it forces task authors either to add fake approval or to avoid `READY_FOR_EXECUTION` even when execution authorization was explicitly granted. This strictly contradicts the core safety rule that human approval cannot be simulated.

## Current validator behavior
Based on read-only inspection of `aos/scripts/aos_task_document_check.py`:
- **Logic Area**: The conflict resides in the `validate_task_document` readiness check, specifically around lines 606-608 where it asserts: `if yaml_data.get("status") == "READY_FOR_EXECUTION": if yaml_data.get("approval_status") != "APPROVED": reasons_blocked.append("status READY_FOR_EXECUTION without explicit APPROVED approval_status")`.
- **Required Fields**: The validator mandates `approval_status`, `status`, `execution_authorized`, `commit_authorized`, `push_authorized`, `release_authorized`, etc.
- **Required Sections**: The validator requires sections like `## Задача`, `## Done когда`, `## История`, `## Evidence`, `## ⛔ Решение`.
- **How approval_status is currently interpreted**: It is incorrectly treated as a blanket prerequisite for execution readiness, committing, pushing, and releasing. 
- **How READY_FOR_EXECUTION is currently interpreted**: It is tightly coupled to explicit task approval (`APPROVED`).
- **Why 0509/0513/0516/0524 remain BLOCKED**: These tasks are authorized for execution (readiness) without full approval. Because the script demands `APPROVED` for readiness, they are indefinitely blocked from passing validation.

## Target authority model
```yaml
target_task_authority_model:
  readiness_status:
    allowed_values:
      - DRAFT
      - READY_FOR_EXECUTION
      - BLOCKED
      - REJECTED
    meaning: "Task is structurally ready and execution has been separately authorized."
    approval_implication: false
  approval_status:
    allowed_values:
      - NOT_REQUESTED
      - HUMAN_REVIEW_REQUIRED
      - APPROVED
      - REJECTED
    meaning: "Explicit human approval state."
    approval_implication:
      NOT_REQUESTED: false
      HUMAN_REVIEW_REQUIRED: false
      APPROVED: true
      REJECTED: false
  execution_authorized:
    allowed_values:
      - true
      - false
    meaning: "Human authorized execution of the task scope."
    approval_implication: false
  approval_granted:
    allowed_values:
      - true
      - false
    meaning: "Explicit human approval granted."
    must_not_be_inferred_from:
      - validator PASS
      - Evidence
      - READY_FOR_EXECUTION
      - execution_authorized
      - Risk Profile assignment
      - commit authorization
      - push authorization
```

## Target validator readiness behavior
```yaml
validator_readiness_should_require:
  - required_yaml_fields_present
  - required_sections_present
  - status_is_READY_FOR_EXECUTION
  - risk_profile_assigned_by_human_not_null
  - execution_authorized_true
  - approval_granted_false_or_true_but_not_required
  - approval_status_present
  - approval_status_not_REJECTED
  - no_blocked_status
  - no_unknown_blocked
  - no_required_review_missing

validator_readiness_should_not_require:
  - approval_status_APPROVED
  - approval_granted_true
  - commit_authorized_true
  - push_authorized_true
  - release_authorized_true
```

## Approval validation behavior
```yaml
validator_approval_checks_should_require:
  approval_status_APPROVED:
    requires_explicit_human_decision: true
    cannot_be_inferred_from:
      - PASS
      - Evidence
      - READY_FOR_EXECUTION
      - execution_authorized
      - validator_status
      - CI
  approval_granted_true:
    requires_explicit_human_decision: true
    cannot_be_inferred_from:
      - PASS
      - Evidence
      - READY_FOR_EXECUTION
      - execution_authorized
      - validator_status
      - CI
```

## Proposed schema fields
```yaml
recommended_task_fields:
  status:
    purpose: lifecycle/readiness state
    examples:
      - DRAFT
      - READY_FOR_EXECUTION
      - BLOCKED
      - REJECTED
  approval_status:
    purpose: explicit human approval state
    examples:
      - NOT_REQUESTED
      - HUMAN_REVIEW_REQUIRED
      - APPROVED
      - REJECTED
  risk_profile_assigned_by_human:
    purpose: human-assigned Risk Profile
    required_for_readiness: true
  execution_authorized:
    purpose: human execution authorization
    required_for_readiness: true
  approval_granted:
    purpose: explicit approval flag
    required_for_readiness: false
  validator_status:
    purpose: latest validator result
    approval_implication: false
  evidence_status:
    purpose: Evidence collection state
    approval_implication: false
```

## Migration strategy
No task may receive `approval_status: APPROVED` unless explicit human approval exists.

```yaml
migration_recommendation_for_current_tasks:
  status: READY_FOR_EXECUTION
  approval_status: NOT_REQUESTED
  approval_granted: false
  execution_authorized: true
  risk_profile_assigned_by_human: keep_existing_value
```
These values preserve:
- `READY_FOR_EXECUTION ≠ approval`
- `execution_authorized ≠ approval`

## Validator update strategy
1. Add tests/fixtures for `READY_FOR_EXECUTION` + `approval_status: NOT_REQUESTED` + `execution_authorized: true`.
2. Update readiness check to stop requiring `APPROVED`.
3. Add separate approval check for `APPROVED`.
4. Update task schema completion expectations.
5. Re-run task readiness for 0509/0513/0516/0524.
6. Run validate-all.
7. Produce migration report.

Future implementation likely requires:
`HIGH_RISK_PROTECTED`
because it touches validator behavior and lifecycle / approval semantics.

## Test fixture strategy
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

## Non-goals
* this design does not modify validator;
* this design does not migrate task files;
* this design does not change canonical sources;
* this design does not grant approval;
* this design does not authorize commit/push/merge/release;
* this design does not promote itself to Source of Truth;
* this design does not remove human checkpoints.

## Future decision options
```yaml
future_human_decision_options:
  - ACCEPT_REPORT_ONLY
  - REQUEST_FIX
  - REJECT
  - PROMOTE_TO_VALIDATOR_IMPLEMENTATION_TASK_DRAFT
  - PROMOTE_TO_SCHEMA_MIGRATION_TASK_DRAFT
  - PROMOTE_TO_CANONICAL_SOURCE_UPDATE_TASK_DRAFT
```

## Recommended next stage
**AOS-FARM.527 — Validator Readiness/Approval Semantics Design Review**
This should be a review-only stage of the design report.
