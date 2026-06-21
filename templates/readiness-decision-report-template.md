# Readiness Decision Report Template

```yaml
artifact_type: readiness_decision_report
status: TEMPLATE
allowed_readiness_results:
  - READY_FOR_TASK_BRIEF
  - NOT_READY_FOR_TASK_BRIEF
  - UNKNOWN_BLOCKED
  - HUMAN_REVIEW_REQUIRED
```

## Input Artifact List

| Artifact | Path / Link | Present? | Notes |
|---|---|---|---|
| Implementation Contract |  | UNKNOWN |  |
| MVP Slice Plan |  | UNKNOWN |  |
| UNKNOWN Resolution Addendum, if present |  | UNKNOWN |  |
| Prior Engineering Clarification output, if present |  | UNKNOWN |  |

## Checklist Summaries

### Implementation Contract Checklist

```yaml
pass: 0
fail: 0
unknown: 0
not_run: 0
na_with_reason: 0
```

### MVP Slice Checklist

```yaml
pass: 0
fail: 0
unknown: 0
not_run: 0
na_with_reason: 0
```

## Unresolved UNKNOWN List

| UNKNOWN | Source | Blocks Task Brief? | Required Resolver |
|---|---|---|---|
|  |  | UNKNOWN |  |

## NOT_RUN Item List

| Item | Source Checklist | Why NOT_RUN | Required Next Step |
|---|---|---|---|
|  |  |  |  |

## Blockers

| Blocker | Source | Impact | Required Decision / Evidence |
|---|---|---|---|
|  |  |  |  |

## Warnings

| Warning | Source | Follow-up |
|---|---|---|
|  |  |  |

## Readiness Result

```yaml
readiness_result: UNKNOWN_BLOCKED
```

Allowed readiness results only:

- `READY_FOR_TASK_BRIEF`
- `NOT_READY_FOR_TASK_BRIEF`
- `UNKNOWN_BLOCKED`
- `HUMAN_REVIEW_REQUIRED`

## Evidence Links

| Evidence | Path / Link | Notes |
|---|---|---|
|  |  |  |

## Explicit Approval Boundary

- Readiness result is not approval.
- Task Brief generation is not started by this template.
- Human approval cannot be simulated.
- Evidence is not approval.
- Checklist `PASS` is not approval.
- `READY_FOR_TASK_BRIEF` is not execution permission.
- Readiness result is not lifecycle mutation.

## Required Human Decision

```yaml
human_decision_required: UNKNOWN
decision_needed: ""
decision_owner: human
```
