# Problem Interview Report

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

## Interview Route

`EXISTING_SPEC_REVIEW` only. No interview automation was performed.

## Problem

The source brief asks for a technical assignment to automate an intake flow, but also says automation must not start until the scope is clarified.

## Target User

Controller reviewing contradictory user instructions.

## Current Workflow

The user provides mixed instructions in one brief, and the agent must preserve the contradiction instead of smoothing it away.

## Target Outcome

Generate candidate drafts that expose the contradiction and require human review.

## Risks

- The agent might treat contradictory instructions as permission to continue.
- The agent might hide a skip/blocker condition.

## UNKNOWN / Open Questions

- UNKNOWN: Should automation continue, pause, or be split into a new task?
- UNKNOWN: Which instruction has priority?
- UNKNOWN: What exact scope is authorized?

## Final Status

final_status: NEEDS_HUMAN_REVIEW
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
