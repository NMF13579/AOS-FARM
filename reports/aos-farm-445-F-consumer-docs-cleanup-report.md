# AOS-FARM.445.F Consumer Docs Cleanup Report

## Task Context
AOS-FARM.445.F — Consumer Docs / Product Folder Cleanup
Authorized Risk Profile: HIGH_RISK_PROTECTED

## Objective
Clarify the consumer-facing documentation by strictly separating the `/aos/` product folder from the internal `agentos/` reference layer, clearly labeling the `AGENTS.md` template, explicitly denying mandatory runners, and asserting fail-closed human checkpoint boundaries.

## File Updates

### `README.md` & `START_HERE.md` (Project Root)
- `README.md`: Clarified that `aos/` is the complete product folder, the user must start at `aos/START_HERE.md`, there is no mandatory active runner, and any python tools included are strictly read-only checkers.
- `START_HERE.md`: Explicitly added a `WARNING` indicating the repository root is the AOS-FARM development workspace and points the consumer user to `/aos/START_HERE.md` as the actual start point.

### `aos/START_HERE.md`
- Added explicit boundary definitions: the product folder is `/aos/`, `aos/root/AGENTS.md` is a template, and `agentos/` is an internal reference layer that should not be used as the primary start path.

### `aos/INSTALL.md` & `aos/ADOPTION.md`
- `aos/INSTALL.md`: Added clear installation and uninstallation flows involving copying the `/aos/` folder and copying the `/aos/root/AGENTS.md` template to the project root.
- `aos/ADOPTION.md`: Added adoption flow for existing projects and mapped out the "First Session Flow" explicitly (Intake -> Assignment -> Task Queue).

### `aos/AGENT_CONTEXT.md` & `aos/root/AGENTS.md`
- `aos/AGENT_CONTEXT.md`: Added "Agent Operating Rules" explaining boundaries within consumer projects (no magic allowed, fail-closed by default, separation of concerns).
- `aos/root/AGENTS.md`: Added a `> TEMPLATE NOTE:` block clarifying that this file is a template to be copied to the target project root and renamed to `AGENTS.md`. 

### `aos/docs/workflow/first-session-guide.md` & `aos/docs/workflow/consumer-runtime-handoff.md`
- `aos/docs/workflow/first-session-guide.md`: Re-emphasized starting at `aos/START_HERE.md`, explicitly removed mention of a required python runner, and clarified the step-by-step human checkpoint boundaries (e.g. Task Quality PASS ≠ Result Acceptance ≠ Commit Auth ≠ Push Auth).
- `aos/docs/workflow/consumer-runtime-handoff.md`: Updated layer boundaries to explicitly label `/aos/` as the product folder and `agentos/` as internal/reference.

### `aos/prompts/problem-intake.md`
- Reworded active path recommendations away from `agentos/` to `aos/`.
- Updated default report save locations to point to `aos/reports/problem-intake/`.
- Clarified that `agentos/docs/...` are internal reference methodology sources rather than active consumer workflow endpoints.

## Execution Constraints Verification
- [x] Canonical files were not modified.
- [x] Task Quality files were not modified.
- [x] Human Result Acceptance files were not modified.
- [x] Queue model files were not modified.
- [x] No runner, auto-execution, auto-approval, SQLite, or RAG-light introduced.
- [x] No destructive cleanup was performed.
- [x] No commit, push, merge, or release was executed.
- [x] 445.G was not started.

## Status
Current Status: `HUMAN_REVIEW_REQUIRED`
