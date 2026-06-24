# AOS-FARM.296 — Minimal Public Release Preparation Scope/Risk Plan

## Current Baseline
- `branch`: dev
- `HEAD`: fd4cd2d3ec07ecbe290647c79b22b1b7ea2d1ab6
- `origin/dev`: fd4cd2d3ec07ecbe290647c79b22b1b7ea2d1ab6
- Duplicate templates count: 0

## Release Preparation Objective
The objective is to gather the necessary evidence, execute strict readiness checks, and prepare the authorization package for a Minimal Public Release. This prepares the system for transitioning the current stable, dogfood-verified state to a formally released, tagged baseline.

## Explicit Non-Goals
- Do **not** create a release.
- Do **not** create a tag.
- Do **not** declare production use.
- Do **not** modify canonical policy files (`00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`).
- Do **not** modify `README.md` or templates.

## Remaining Evidence-Tail
Local closure artifacts from AOS-FARM.294-296 remain untracked and must be authorized for commit and push prior to release finalization.

## Required Checks Before Actual Release
1. **README Entrypoint Check**: Validate that no legacy, broken commands (`agentos/agentos.py start`) exist in the first-user path.
2. **User Guide Check**: Ensure documentation aligns with the manual file-based workflow.
3. **Template Duplicate Check**: Validate 0 duplicates exist.
4. **Safety Invariant Check**: Confirm adherence to Minimal Safety Floor.
5. **Release Boundary Check**: Confirm no unauthorized changes occurred.
6. **Evidence-Tail Check**: Ensure all pre-release planning/verification artifacts are tracked.

## Proposed Minimal Release Candidate Content
The release candidate will encompass the current state at `fd4cd2d3ec07ecbe290647c79b22b1b7ea2d1ab6` plus the final evidence tail commits. It relies entirely on the tested file-based documentation-assembly process with no active scripts or runners.

## Files Likely Needing Review, But Not Edit Now
- `README.md` (Confirm usability)
- `docs/user-guide/README.md`
- `docs/user-guide/bootstrap-agent-workflow.md`
- `docs/user-guide/agent-tutor-mode.md`

## Risk Profile
`agent_proposed_risk_profile: HIGH_RISK_PROTECTED`
`human_assignment_required: true`

## Next Recommended Task
AOS-FARM.297 — Minimal Public Release Preparation Readiness Checklist Verification & Execution Authorization.
