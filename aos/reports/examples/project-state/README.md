# Project State Scanner Example

This example shows the compact machine-readable output shape produced by the
read-only project state scanner.

The scanner does not approve, authorize, execute, commit, push, merge,
release, or start the next task. It reports deterministic local state only.

## Example File

- `status-example.json`

## Safety Notes

- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Human approval cannot be simulated.
