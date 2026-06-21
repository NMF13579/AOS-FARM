# MVP Slice Readiness Checklist Template

```yaml
artifact_type: mvp_slice_readiness_checklist
status: TEMPLATE
allowed_item_statuses:
  - PASS
  - FAIL
  - UNKNOWN
  - NOT_RUN
  - N/A_WITH_REASON
```

## Safety Semantics

- `NOT_RUN` is not `PASS`.
- `UNKNOWN` is not OK.
- `PASS` does not authorize implementation.
- Checklist completion does not authorize Task Brief generation.
- Readiness result is not lifecycle mutation.
- Human approval cannot be simulated.

## Instructions

For each item, record:

- status: `PASS`, `FAIL`, `UNKNOWN`, `NOT_RUN`, or `N/A_WITH_REASON`;
- evidence link or reason;
- whether the item blocks Task Brief preparation;
- required human review point, if any.

## Checklist

| Item | Status | Evidence / Reason | Blocks Task Brief? | Human Review Point |
|---|---|---|---|---|
| Selected MVP slice | NOT_RUN |  |  |  |
| Excluded scope | NOT_RUN |  |  |  |
| First implementation path | NOT_RUN |  |  |  |
| File/module boundary if known | NOT_RUN |  |  |  |
| Dependencies | NOT_RUN |  |  |  |
| Required test/evidence expectations | NOT_RUN |  |  |  |
| Rollback/recovery notes, if applicable | NOT_RUN |  |  |  |
| Remaining UNKNOWN | NOT_RUN |  |  |  |
| Human review points | NOT_RUN |  |  |  |

## Summary

```yaml
total_pass: 0
total_fail: 0
total_unknown: 0
total_not_run: 0
total_na_with_reason: 0
remaining_unknown_blocks_task_brief: UNKNOWN
recommended_readiness_result: UNKNOWN_BLOCKED
```

Allowed recommended readiness results:

- `READY_FOR_TASK_BRIEF`
- `NOT_READY_FOR_TASK_BRIEF`
- `UNKNOWN_BLOCKED`
- `HUMAN_REVIEW_REQUIRED`
