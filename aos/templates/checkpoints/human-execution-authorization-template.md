# Human Checkpoint: Execution Authorization

## Target Task
[Task Name]

## Controlled Task Brief
[Exact path or ID]

## Controlled Execution Package
[Exact package path copied from aos/templates/execution-packages/controlled-execution-package-template.yaml]

## Requested Authorization
Approval to execute this exact `Controlled Task Brief` and exact allowed scope only.

## Pre-Authorization Review
- [ ] I reviewed the full `Controlled Task Brief`.
- [ ] The exact allowed scope is explicit.
- [ ] The exact forbidden scope is explicit.
- [ ] The validation and Evidence expectations are explicit.
- [ ] I understand the expected execution output is an `Execution Report` with Evidence.

## Risk Profile Assignment
- Human must explicitly assign the Risk Profile.
- Agent may propose Risk Profile reasoning, but the agent cannot assign it.
- Missing human Risk Profile assignment means `BLOCKED` / `HUMAN_REVIEW_REQUIRED`.
- [ ] LOW_RISK_FAST
- [ ] MEDIUM_RISK_GUIDED
- [ ] HIGH_RISK_PROTECTED
- [ ] OTHER: _________

## Allowed Scope
[Exact files, directories, or components]

## Forbidden Scope
- commit
- push
- merge
- release
- production use
- destructive operations unless explicitly authorized
- protected/canonical changes unless explicitly authorized

## Agent Must Stop With BLOCKED If
- required control sources are missing or unreadable
- this authorization is missing
- this authorization does not match the exact `Controlled Task Brief`
- the allowed or forbidden scope is ambiguous
- `UNKNOWN` remains in a blocking way
- `NOT_RUN` is being treated as `PASS`
- execution would require scope expansion or extra files not authorized here

## Boundary Reminder
- `Controlled Task Brief` is not execution approval.
- readiness is not execution approval.
- Human Execution Authorization is required before execution.
- This approval applies only to this exact `Controlled Task Brief` and exact allowed scope.
- After this authorization is created, run Controlled Execution Guard `precheck` against the matching execution package before editing files.
- It does not authorize future tasks.
- `PASS` is not approval.
- Evidence is not approval.
- It does not authorize commit.
- It does not authorize push.
- It does not authorize release.

## Execution Boundary Reminder
- Agent must stop on missing required source.
- Agent must stop on missing authorization.
- Agent must stop on ambiguity.
- Agent must stop on `UNKNOWN`.
- Agent must stop on blocking `NOT_RUN`.
- Agent must not expand scope.
- Agent must not commit.
- Agent must not push.

## Human Decision
- [ ] APPROVED: Proceed with execution.
- [ ] REJECTED: Do not proceed.
- [ ] CHANGES REQUESTED: _________

**Authorized By:** 
**Date:** 
