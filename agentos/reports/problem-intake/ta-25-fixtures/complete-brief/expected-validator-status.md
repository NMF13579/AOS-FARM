# Complete Brief Fixture Expected Validator Status

```yaml
fixture_id: complete-brief
expected_validator_status: NEEDS_HUMAN_REVIEW
fixture_authorizes_execution: false
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
approval_status: NOT_APPROVED
```

## Input Summary

Complete existing-spec review input with problem, user, workflow, outcome, constraints, risks, open questions, data discovery, information flow, access, requirements, acceptance criteria, MVP, implementation hints, and contradictions section.

## Expected Draft Output Properties

- `PROJECT_SPEC.draft.md` exists and remains a draft.
- `REQUIREMENTS.draft.md` exists and remains a draft.
- Problem report and checklist exist.
- Human Decisions Required are visible.
- Final process state is no higher than `READY_FOR_HUMAN_REVIEW`.

## Expected UNKNOWN / HUMAN_REVIEW_REQUIRED Behavior

Open questions must be carried as `UNKNOWN` items. Human review remains required even when the brief is structurally complete.

## Expected Safety Fields

- `ready_for_execution: false`
- `execution_authorized: false`
- `implementation_authorized: false`
- `approval_status: NOT_APPROVED`

## Execution Boundary

This fixture does not authorize execution, implementation, commit, push, release, or production use.
