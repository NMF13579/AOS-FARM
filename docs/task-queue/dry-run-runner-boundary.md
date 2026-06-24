# Dry-Run Runner Boundary

## Purpose
This document strictly defines what a "runner" or "helper" is allowed to do in AOS-FARM. The current implementation is a dry-run helper.

## Allowed Helper Actions
- Read Markdown files.
- Parse key-value pairs and checkboxes.
- Detect missing approvals (`execution_authorized: false`).
- Detect forbidden status transitions (e.g., `READY_FOR_EXECUTION` -> `IN_PROGRESS` without human checkpoint).
- Generate draft templates for the next step.

## Forbidden Helper Actions
- Executing code.
- Mutating the task queue files automatically.
- Approving tasks.
- Running Git commands (`add`, `commit`, `push`).

## Approval Boundary
The helper cannot simulate human approval. It can only report `HELPER_BLOCKED_MISSING_APPROVAL`.

## Lifecycle Boundary
The helper must not transition states. It must not write `Current Status: IN_PROGRESS` to any file.

## Source of Truth Boundary
The Markdown files are the Source of Truth. The helper has no internal database or SQLite registry. If the Markdown file says `execution_authorized: false`, the helper must trust it.

## UNKNOWN / NOT_RUN Boundary
The helper must explicitly detect `UNKNOWN` and `NOT_RUN` and flag them. It cannot convert them to `OK` or `PASS`.

## Failure Modes
If the helper encounters an ambiguous state, it fails closed with `HELPER_UNKNOWN_BLOCKED`.

## Future Expansion Conditions
Before this helper can ever execute code (AOS-FARM.251+), it must be dogfooded extensively in its current dry-run state. Even then, execution will require strict sandboxing and human checkpoints.
