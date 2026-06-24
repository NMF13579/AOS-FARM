# AOS-FARM.283 — README Onboarding Gap Execution Authorization Package

## Final Status
DRAFT_FOR_HUMAN_REVIEW

## Target Execution Task
target_task: AOS-FARM.284

## Authorized Target File
- `README.md`

## Authorized Scope
- Remove/replace the stale `python3 agentos/agentos.py start` command.
- Add pointers/links to:
  - `docs/user-guide/README.md`
  - `docs/user-guide/bootstrap-agent-workflow.md`
  - `docs/user-guide/agent-tutor-mode.md`
- Clarify that PASS, Evidence, and Metrics do not equal production or release approval.

## Forbidden Actions
- No runner creation.
- No restoration of `agentos/agentos.py`.
- No edits to canonical files `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- No edits to `docs/user-guide/*` files.
- No template cleanup (Batch 3 deferred).
- No `git add`, `git commit`, `git push` in AOS-FARM.284.
- No release/tag creation.
- No production use claims.

## Execution Boundary
execution_authorized_now: false
human_checkpoint_required: true

## Commit / Push Boundary
commit_authorized_now: false
push_authorized_now: false

## Final Recommendation
Approve execution of AOS-FARM.284 to eliminate the blocker for vibe-coders and provide a clean entry point.
