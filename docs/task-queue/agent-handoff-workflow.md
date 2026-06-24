# Agent Handoff Workflow

## Handoff Purpose
This defines how a task moves from the Human (or Agent Tutor) to an Executor Agent.

## Pre-handoff Checks
Before an agent begins work, it must verify:
- The required canonical sources exist.
- A task brief exists.
- An explicit Human Execution Authorization checkpoint is filled with `execution_authorized: true`.

## Required Human Execution Authorization
Agent handoff is **not** approval. An executor receiving a task is **not** authorization to execute. If the Human Execution Authorization checkpoint is absent or `false`, the executor must stop immediately with `HUMAN_REVIEW_REQUIRED`.

## Handoff Package Fields
The executor is handed a package based on `templates/agent-handoff-package-template.md`. It contains:
- Target task and Scope.
- Allowed Files.
- Forbidden Files.
- Expected Final Report format.

## Allowed and Forbidden Scope
The executor may only act inside the authorized scope. Any attempt to modify forbidden files, especially canonical sources or CI/CD pipelines, will trigger a fail-closed response.

## Expected Executor Behavior
1. Read the handoff package.
2. Re-verify the authorization checkpoint.
3. Perform the work strictly within the scope.
4. Stop immediately if it hits a blocker or forbidden boundary.
5. Generate the Final Report.
6. Stop and await verification.

## Stop Conditions
The agent must stop if:
- Scope needs to expand.
- A forbidden file needs modification.
- Ambiguity is high (`UNKNOWN_BLOCKED`).
- It has completed the work and generated the report.

## Post-handoff Review
After the executor stops, the workflow moves to the Execution Result Verification Loop.
