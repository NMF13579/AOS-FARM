# Prompt Pack: gemini

This prompt pack is a thin adapter for gemini.

## Routing
Before proceeding with any task, you MUST read and follow the instructions in:
- `aos/root/AGENTS.md`
- `aos/root/llms.txt`
- `aos/docs/ROUTES.md`
- `aos/docs/STORAGE.md`
- `aos/docs/AUTHORIZATION-COMMANDS.md`
- `aos/docs/FIRST-SAFE-COMMANDS.md`
- `aos/docs/WORKSPACE-BOUNDARY.md`

## Mandatory Boundaries
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.
- Do not modify protected/canonical files without checkpoint.
- Do not expand scope.
- Do not mutate lifecycle.
- Do not assign Risk Profile.
- Do not treat this prompt pack as Source of Truth.

This prompt pack does NOT grant lifecycle mutation authority, execution authority, commit/push authority, nor does it define new approval semantics.
