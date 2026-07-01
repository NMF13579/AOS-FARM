# Weak Brief Fixture Expected Validator Status

```yaml
fixture_id: weak-brief
expected_validator_status: NEEDS_HUMAN_REVIEW
fixture_authorizes_execution: false
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
approval_status: NOT_APPROVED
```

## Input Summary

Weak existing-spec review input with only a short problem, target user, target outcome, and open questions.

## Expected Draft Output Properties

- Required draft files are generated.
- Missing current workflow, constraints, risks, data discovery, information flow, access, acceptance criteria, and MVP are marked `NEEDS_HUMAN_REVIEW`.
- Human Decisions Required remain visible.

## Expected UNKNOWN / HUMAN_REVIEW_REQUIRED Behavior

Missing sections become `UNKNOWN` / `NEEDS_HUMAN_REVIEW`. The validator should accept the structural contract while preserving review blockers.

## Expected Safety Fields

- `ready_for_execution: false`
- `execution_authorized: false`
- `implementation_authorized: false`
- `approval_status: NOT_APPROVED`

## Execution Boundary

This fixture does not authorize execution, implementation, commit, push, release, or production use.
