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

## Controlled Execution Guard Flow
- Follow `aos/docs/workflow/first-controlled-execution.md` for controlled execution.
- Use `precheck`, `scopecheck`, `sessioncheck`, `resultcheck`, and `postcheck` when the task requires the controlled execution guard.
- Human Review Package is not approval.
- `RESULT_VERIFICATION_READY_FOR_HUMAN_REVIEW` is not approval.
- Commit authorization and push authorization remain separate human checkpoints.
- This prompt pack remains guidance only and is not Source of Truth.

This prompt pack does NOT grant lifecycle mutation authority, execution authority, commit/push authority, nor does it define new approval semantics.
