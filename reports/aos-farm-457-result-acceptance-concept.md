# AOS-FARM.457 — Result Acceptance Concept Report

## Task identity

```yaml
task_id: AOS-FARM.457
title: Task Execution Result Acceptance Gate
risk_profile: HIGH_RISK_PROTECTED
created_at: "2026-06-28"
```

## Purpose

AOS-FARM.457 adds the **Result Acceptance Gate** — the structural layer that
closes the gap between task execution and Human Review.

After a task is executed, an agent must assemble a **Result Acceptance Package**
that collects:

```text
what was tasked         → task_id, task_brief reference
what was changed        → changed_files (with scope_status per file)
what validation ran     → validation_results (with explicit status per check)
what evidence exists    → evidence_items
what is NOT_RUN         → not_run_items (explicit array, may be empty)
what is UNKNOWN         → unknown_items (explicit array, may be empty)
what forbidden behaviors were checked → related_forbidden_behavior_mapping
what the human must decide → Human Review trigger
what the acceptance status is → final_status (never APPROVED by agent)
```

## Scope

This gate adds:

| File | Role |
|---|---|
| `aos/schemas/task-execution-result-acceptance.schema.json` | Structural schema for result packages |
| `aos/templates/task-execution-result-acceptance.md` | Human-readable template for result packages |
| `aos/scripts/aos_task_quality_check.py` | `check_result_acceptance()` + `validate-result-acceptance` CLI action |
| `tests/test_task_execution_result_acceptance.py` | Unittest suite |
| `tests/fixtures/task_execution_result_acceptance/` | 6 fixtures (1 positive, 5 negative) |
| `reports/aos-farm-457-*.md` | Reports |

## Validator Limits (Non-Negotiable)

The validator checks **only structural and binary facts**:

```text
result file exists
result file parses as valid JSON
all required fields present
changed_files is an array of objects with required keys
validation_results is an array of objects with required keys
evidence_items, not_run_items, unknown_items are explicit arrays
approval_boundary has all required flags set to true
result_acceptance_boundary has all required flags set to true
final_status is not APPROVED
final_status is in the allowed enum
UNKNOWN validation result without human_review_required=true → UNKNOWN_BLOCKED
NOT_RUN validation result without human_review_required=true → BLOCKED
OUT_OF_SCOPE changed file without human_review_required=true → BLOCKED
approval_granted / commit_authorized / push_authorized / merge_authorized / release_authorized must not be true
```

The validator does **NOT** check:

```text
quality or correctness of the implementation
whether Evidence is sufficient for approval
whether the task goal was actually achieved
semantic meaning of implementation_summary
whether tests cover all edge cases
```

## Schema Boundary

The schema requires:

- `changed_files`: array of objects, each with `path`, `change_type`, `scope_status`, `human_review_required`
- `validation_results`: array of objects, each with `name`, `command_or_check`, `status`, `evidence`, `human_review_required`
- `evidence_items`: explicit array (may be empty)
- `not_run_items`: explicit array (may be empty) — empty ≠ missing
- `unknown_items`: explicit array (may be empty) — empty ≠ missing
- `approval_boundary`: object with all required `const: true` flags
- `result_acceptance_boundary`: object with `validator_checks_structure_only`, `validator_does_not_check_semantic_correctness`, `human_decision_required_for_acceptance` — all `const: true`
- `final_status`: enum — never `APPROVED`

## Approval Boundary

```yaml
pass_is_not_approval: true
evidence_is_not_approval: true
ci_pass_is_not_approval: true
result_acceptance_is_not_approval: true
human_review_required: true
validator_does_not_grant_approval: true
validator_does_not_grant_commit_authorization: true
validator_does_not_grant_push_authorization: true
validator_does_not_grant_merge_authorization: true
validator_does_not_grant_release_authorization: true
```

## NOT_RUN Handling

- `not_run_items` must be an explicit array. Missing is invalid.
- `validation_results` items with `status: NOT_RUN` must have `human_review_required: true`, otherwise the validator returns `RESULT_ACCEPTANCE_BLOCKED`.
- Rationale: NOT_RUN ≠ PASS. An unrun check cannot be treated as passing.

## UNKNOWN Handling

- `unknown_items` must be an explicit array. Missing is invalid.
- `validation_results` items with `status: UNKNOWN` must have `human_review_required: true`, otherwise the validator returns `RESULT_ACCEPTANCE_UNKNOWN_BLOCKED`.
- `unknown_items` entries must have `human_review_required: true`.
- Rationale: UNKNOWN ≠ OK. Unknown state must escalate to Human Review.

## Forbidden Behavior Mapping Relationship

AOS-FARM.456 produced the layer:
```
forbidden_behavior → evidence_item → verification_method → status → Human Review note
```

AOS-FARM.457 references the 456 mapping via `related_forbidden_behavior_mapping`
(optional string field). The result acceptance package does not duplicate the
mapping — it only points to it.

## Human Review Boundary

The validator marks valid packages as:

```text
RESULT_ACCEPTANCE_READY_FOR_HUMAN_REVIEW
```

This status means: the package is structurally valid and can be presented to
a human for review. It does **not** mean the work is approved, correct, or
ready for commit.

The human makes the only acceptance decision.

## CLI

```bash
python3 aos/scripts/aos_task_quality_check.py validate-result-acceptance --result <path>
```

Exit codes:
- `0` = structurally valid, Human Review required
- `1` = blocked, invalid, or UNKNOWN

Output always includes:
```json
{
  "approval_granted": false,
  "commit_authorized": false,
  "push_authorized": false,
  "merge_authorized": false,
  "release_authorized": false,
  "human_review_required": true
}
```

## Final Status

```yaml
final_status: HUMAN_REVIEW_REQUIRED
created_at: "2026-06-28"
implementation_started: true
implementation_completed: true
commit_authorized: false
push_authorized: false
```
