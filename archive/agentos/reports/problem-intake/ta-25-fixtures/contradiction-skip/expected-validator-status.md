# Contradiction Skip Fixture Expected Validator Status

```yaml
fixture_id: contradiction-skip
expected_validator_status: NEEDS_HUMAN_REVIEW
fixture_authorizes_execution: false
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
approval_status: NOT_APPROVED
```

## Input Summary

Existing-spec review input with an explicit contradiction between automation request and scope-clarification blocker.

## Expected Draft Output Properties

- Required draft files are generated.
- Contradiction is visible in the candidate project spec.
- Human Decisions Required remain visible.

## Expected UNKNOWN / HUMAN_REVIEW_REQUIRED Behavior

Contradiction and scope ambiguity must remain human-review blockers. The fixture must not resolve them by assumption.

## Expected Safety Fields

- `ready_for_execution: false`
- `execution_authorized: false`
- `implementation_authorized: false`
- `approval_status: NOT_APPROVED`

## Execution Boundary

This fixture does not authorize execution, implementation, commit, push, release, or production use.
