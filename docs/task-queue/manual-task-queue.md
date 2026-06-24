# Manual Task Queue Contract

## Purpose
This document defines how tasks are tracked, what statuses are valid, and how they progress.

## Queue Item Anatomy
A task is represented by a Markdown file generated from `templates/task-queue-item-template.md`. It contains the ID, goal, scope, dependencies, and strict safety boundaries.

## Allowed Task Types
- `DOCUMENTATION`
- `PLANNING`
- `CODE_IMPLEMENTATION`
- `VERIFICATION`
- `REFACTORING`

## Allowed Statuses
- `DRAFT`
- `READY_FOR_REVIEW`
- `READY_FOR_EXECUTION`
- `HUMAN_REVIEW_REQUIRED`
- `EXECUTION_AUTHORIZED`
- `IN_PROGRESS`
- `RESULT_REPORTED`
- `VERIFICATION_PENDING`
- `VERIFIED`
- `BLOCKED`
- `UNKNOWN_BLOCKED`
- `COMMIT_AUTHORIZATION_PENDING`
- `COMMITTED`
- `PUSH_AUTHORIZATION_PENDING`
- `PUSHED`
- `CLOSED`
- `SUPERSEDED`

## Status Owner Rules
- **Agents** may transition states up to `HUMAN_REVIEW_REQUIRED`, `RESULT_REPORTED`, or `VERIFICATION_PENDING`.
- **Humans** own `EXECUTION_AUTHORIZED`, `COMMIT_AUTHORIZATION_PENDING` -> `COMMITTED`, and `PUSH_AUTHORIZATION_PENDING` -> `PUSHED`.
- `CLOSED` is assigned only after verified remote closure.

## Human Approval Requirements
- **READY_FOR_EXECUTION ≠ execution approval.** It means the plan is ready for a human to read.
- **VERIFIED ≠ approval.** It means a post-execution check passed, but the human still needs to authorize the commit.
- **COMMITTED ≠ pushed.** Push requires independent approval.
- **PUSHED ≠ release.** Release requires independent approval.

## Blocked, UNKNOWN, NOT_RUN Handling
- If a required source is missing or an invariant is broken, task state becomes `UNKNOWN_BLOCKED`.
- `UNKNOWN` is never treated as `OK`.
- `NOT_RUN` is never treated as `PASS`.

## Adding and Updating Tasks
Tasks are added manually using the provided templates. Any status change must use the `templates/task-queue-status-update-template.md` to prevent silent lifecycle mutation.

## Preventing Approval Simulation
Agents are strictly forbidden from modifying fields named `execution_authorized`, `commit_authorized`, or `push_authorized` unless explicitly copying a verified Human Checkpoint.
