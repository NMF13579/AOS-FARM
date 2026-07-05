# Prompt Pack: chatgpt

This prompt pack is a thin adapter for chatgpt.

## Routing
Before proceeding with any task, you MUST read and follow the instructions in:

**For Consumer Target Repositories:**
- `/AGENTS.md` (deployed root file)
- `/llms.txt` (deployed root file)
- `aos/START_HERE.md`
- `aos/docs/INSTALL-AND-TRANSFER.md`
- `aos/docs/ROUTES.md`
- `aos/docs/STORAGE.md`
- `aos/docs/AUTHORIZATION-COMMANDS.md`
- `aos/docs/FIRST-SAFE-COMMANDS.md`
- `aos/docs/WORKSPACE-BOUNDARY.md`

*Note: Consumer target repos do NOT require `00`, `01`, `02` root files. Do not point to `/aos/root/AGENTS.md` as the active runtime file.*

**For AOS-FARM Development Repository ONLY:**
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

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
