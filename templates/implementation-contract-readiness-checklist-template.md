# Implementation Contract Readiness Checklist Template

```yaml
artifact_type: implementation_contract_readiness_checklist
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
- Checklist `PASS` is not approval.
- Evidence is not approval.
- Human approval cannot be simulated.

## Instructions

For each checklist item, record:

- status: `PASS`, `FAIL`, `UNKNOWN`, `NOT_RUN`, or `N/A_WITH_REASON`;
- evidence link or reason;
- blocker impact;
- required human decision, if any.

Do not mark an item `PASS` unless the supporting input is present and specific enough for Task Brief preparation.

## Checklist

| Item | Status | Evidence / Reason | Blocker? | Required Human Decision |
|---|---|---|---|---|
| Problem / goal clarity | NOT_RUN |  |  |  |
| MVP scope boundary | NOT_RUN |  |  |  |
| Non-goals | NOT_RUN |  |  |  |
| Actors / roles | NOT_RUN |  |  |  |
| Data model | NOT_RUN |  |  |  |
| State machine or lifecycle | NOT_RUN |  |  |  |
| RBAC / permissions | NOT_RUN |  |  |  |
| Core user flows | NOT_RUN |  |  |  |
| Integration points | NOT_RUN |  |  |  |
| Error handling | NOT_RUN |  |  |  |
| Nonfunctional constraints | NOT_RUN |  |  |  |
| Assumptions | NOT_RUN |  |  |  |
| Unresolved UNKNOWN | NOT_RUN |  |  |  |
| Explicit implementation blockers | NOT_RUN |  |  |  |
| Evidence links | NOT_RUN |  |  |  |

## Summary

```yaml
total_pass: 0
total_fail: 0
total_unknown: 0
total_not_run: 0
total_na_with_reason: 0
implementation_blockers_present: UNKNOWN
recommended_readiness_result: UNKNOWN_BLOCKED
```

Allowed recommended readiness results:

- `READY_FOR_TASK_BRIEF`
- `NOT_READY_FOR_TASK_BRIEF`
- `UNKNOWN_BLOCKED`
- `HUMAN_REVIEW_REQUIRED`
