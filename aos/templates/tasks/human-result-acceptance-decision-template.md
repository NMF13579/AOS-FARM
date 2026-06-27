# Human Result Acceptance Decision

**Task ID**: <TASK_ID>
**Task Title**: <TASK_TITLE>

## Quality and Evidence
- **Task Quality Status**: <STATUS>
- **Task Quality Package**: [Package Path]
- **Task Quality Result**: [Result Path]
- **Acceptance Summary**: [Summary Path]

## Known Limits
- <KNOWN_LIMIT_1>
- <KNOWN_LIMIT_2>

## Human Decision
Please explicitly set the decision below. 
Must be one of: `ACCEPT_RESULT`, `NEEDS_CHANGES`, `REJECT_RESULT`.

**Decision**: `<DECISION>`
**Reason**: `<REASON>`

**Result Accepted By Human**: `<true/false>`
**Human Acknowledges Known Limits**: `<true/false>`

### If NEEDS_CHANGES
**Requires Follow-Up Task**: `<true/false>`
**Follow-Up Task Candidate**: `<path_to_candidate>`

### If REJECT_RESULT
**Rejection Reason**: `<REASON>`

## Verification (Forbidden Boundaries)
These MUST be false in this context:
- `commit_authorized`: false
- `push_authorized`: false
- `merge_authorized`: false
- `release_authorized`: false
- `next_task_started`: false
- `lifecycle_mutation_authorized`: false
