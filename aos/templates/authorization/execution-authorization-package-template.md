# Execution Authorization Package

## User Review Before Authorization
- Review the exact `Controlled Task Brief`.
- Review the exact allowed scope and forbidden scope.
- Review the human-assigned Risk Profile.
- Review the validation plan, expected execution output, and Evidence requirements.
- If anything is ambiguous, missing, `UNKNOWN`, or would require scope expansion, stop with `BLOCKED`.

## Controlled Task Brief
State the exact brief path or ID this package refers to.

## Human Risk Profile
State the human-assigned Risk Profile.

## Authorized Inputs
- `Controlled Task Brief`: [Path or ID]
- Human Execution Authorization checkpoint: [Path or ID]
- Any exact file paths, validation commands, or Evidence requirements referenced by the brief: [List]

## Authorized Execution Scope
- Exact target files or directories the agent may change: [List]
- Scope the agent must not expand beyond: [List]

## Expected Execution Output
- One `Execution Report`
- Evidence summary
- Validation results separated into `PASS`, `NOT_RUN`, and `UNKNOWN`
- Any blockers or unresolved questions

## Required Evidence
- changed file list
- diff summary
- validation output or explicit `NOT_RUN`
- any remaining `UNKNOWN`
- confirmation that forbidden actions were not taken

## BLOCKED Conditions
- required control sources are missing or unreadable
- Human Execution Authorization is missing for this exact brief
- human-assigned Risk Profile is missing
- allowed or forbidden scope is ambiguous
- execution requires extra files or scope expansion
- `UNKNOWN` remains in a blocking way
- `NOT_RUN` is being treated as `PASS`

## Boundary Reminder
- `UNKNOWN` is not OK.
- `NOT_RUN` is not `PASS`.
- `PASS` is not approval.
- Evidence is not approval.
- Execution authorization does not authorize scope expansion.
- Execution authorization does not authorize commit.
- Execution authorization does not authorize push.
- Execution authorization does not authorize release.

## Lifecycle Status
State explicitly that commit is deferred and push is deferred until separate human authorization.
