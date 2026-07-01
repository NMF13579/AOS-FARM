# AOS-FARM.504 Third Pass Planning Synthesis Report

```yaml
report_id: AOS-FARM.504
cycle: AOS-FARM-CYCLE-0001
report_type: planning_synthesis
status: READY_FOR_HUMAN_REVIEW
approval_granted: false
execution_authorized: false
```

## Inputs

- Codex audit findings: `reports/aos-farm-502-user-workflow-stage-gap-audit.md`
- External best-practice reference: `reports/aos-farm-503-external-best-practices-reference.md`
- External output status: `NOT_RUN_EXTERNAL_REFERENCE`
- Canonical constraints: `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## Current Third Pass Direction

Third Pass should strengthen the planning path from user workflow discovery to reviewable DRAFT task candidates, without crossing into executable tasks. The priority is to make traceability, human checkpoints, and non-approval semantics visible and machine-checkable enough for later helpers.

## Include In Third Pass

- Planning-cycle package structure for audit, external reference, synthesis, DRAFT candidates, traceability validation, and final review.
- Problem Intake to Technical Assignment traceability.
- Technical Assignment to DRAFT task candidate traceability.
- Manual queue acceptance and candidate promotion boundary.
- Report-only validation checklist for planning-cycle artifacts.
- Clear `DRAFT_CANDIDATE` status and `ready_for_execution: false` fields.

## Defer

- Runtime enforcement.
- CI required checks and branch protection.
- Release workflow.
- Cross-repo automation.
- Database, RAG, vector search, or SaaS behavior.
- Broad cleanup of copied or duplicate files.

## Forbidden To Automate

- Human approval.
- Risk Profile assignment.
- Candidate promotion into a real task.
- Execution authorization.
- Commit, push, merge, release, production use.
- Protected/canonical file changes.
- Destructive operations.
- Treating PASS, Evidence, CI PASS, validator PASS, report readiness, or external reference output as approval.

## Requires Human Checkpoint

- Promoting any DRAFT candidate into a real task file.
- Assigning a Risk Profile.
- Authorizing execution.
- Touching `/aos/`, `aos/scripts/`, `aos/templates/`, `aos/schemas/`, `.github/workflows/`, `tasks/`, or canonical root sources.
- Enabling or weakening validators or CI gates.
- Cleanup, delete, move, rename, archive, merge, release, or push.

## Requires Code Helper

- Later planning-cycle package generator that creates reports with fixed fields.
- Later traceability checker from source report sections to candidate fields.
- Later read-only status summarizer that is safe around noisy worktrees.

## Requires Template / Report

- Planning-cycle audit report template.
- External-reference placeholder report template.
- Synthesis report template.
- DRAFT task candidate report template.
- Candidate promotion human checkpoint template.
- Final planning-cycle review package template.

## Requires Validator

- Candidate field validator.
- Forbidden status validator: no `READY_FOR_EXECUTION`, no `execution_authorized: true`, no approval wording.
- Source reference validator.
- External-reference boundary validator.
- UNKNOWN / NOT_RUN visibility validator.
- Raw `.aos-tmp` non-evidence validator.

## Requires Later Runtime Enforcement

- Command/write allowlists.
- Protected path guard.
- Git operation guard.
- Audit log.
- Sandbox policy.

## Planning / Execution Boundary

This synthesis stops at DRAFT task candidates. It does not create files in `tasks/`, does not set `READY_FOR_EXECUTION`, does not assign Risk Profile, and does not authorize implementation, commit, push, merge, release, or production use.
