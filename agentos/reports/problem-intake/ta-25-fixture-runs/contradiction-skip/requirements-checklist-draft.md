# Requirements Checklist Draft

```yaml
artifact_status: DRAFT
approval_status: NOT_APPROVED
automation_status: RUNNER_V2_EXISTING_SPEC_REVIEW_ONLY
production_status: NOT_PRODUCTION
intake_route: EXISTING_SPEC_REVIEW
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
final_status: NEEDS_HUMAN_REVIEW
```

## Field Coverage

| Field | Status |
|---|---|
| Problem | FOUND |
| Target User | FOUND |
| Current Workflow | FOUND |
| Target Outcome | FOUND |
| Constraints | FOUND |
| Known Risks | FOUND |
| Open Questions | FOUND |

## UNKNOWN / Open Questions

- UNKNOWN: Should automation continue, pause, or be split into a new task?
- UNKNOWN: Which instruction has priority?
- UNKNOWN: What exact scope is authorized?

## Human Decisions Required

- Assign Risk Profile before any execution.
- Confirm whether candidate requirements are in scope.
- Confirm exact allowed and forbidden changes before implementation.
- Confirm acceptance criteria before execution.
- Confirm execution authorization separately; this runner never authorizes execution.
- Resolve or explicitly accept listed UNKNOWN items before finalization.

## Final Status

final_status: NEEDS_HUMAN_REVIEW
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
