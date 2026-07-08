# AOS-FARM.637 - Architecture Creation Process Deep Audit Report

## Verdict

AUDIT_FINDINGS_FIXES_APPLIED_REVIEW_REQUIRED

This audit report is not approval.
This audit report does not authorize execution, commit, push, merge, release, or Risk Profile assignment.
PASS is not approval. Evidence is not approval. Architecture validation PASS is not architecture approval.

## Scope

Checked the architecture creation path from Technical Assignment through Architecture Input Intake, Architecture Decision Layer, Architecture Validator, Evidence packet, Human Architecture Checkpoint, Task Breakdown from Architecture, and downstream Task Brief drafting boundary.

Checked:
- root required sources: `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- consumer entrypoints and routes: `aos/START_HERE.md`, `aos/AGENT_CONTEXT.md`, `aos/root/AGENTS.md`, `aos/docs/ROUTES.md`
- workflow docs: `aos/docs/workflow/architecture-input-intake.md`, `aos/docs/workflow/architecture-decision-layer.md`, `aos/docs/workflow/task-breakdown-from-architecture.md`, `aos/docs/workflow/technical-assignment-workflow.md`, `aos/docs/workflow/technical-assignment-to-task-brief.md`, `aos/docs/workflow/first-session-guide.md`
- architecture review docs and registries under `aos/docs/architecture/`
- architecture templates and prompts under `aos/templates/` and `aos/prompts/`
- architecture validator and tests: `aos/scripts/aos_architecture_document_check.py`, `aos/scripts/aos_validate.py`, `tests/test_aos_architecture_document_check.py`, `tests/fixtures/architecture/`
- recent architecture reports in `aos/reports/architecture/`

Untracked duplicate files and `.venv/` were observed but not modified.

## Sources Used

| Source | Status | Notes |
|---|---|---|
| `00_AOS_Core_Control.md` | READ | Highest project control source. |
| `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` | READ | Assembly pipeline and roadmap authority. |
| `02_AOS_Governance_Control_Module_and_Safety_Rules.md` | READ | Safety, approval, Risk Profile, gate, lifecycle authority. |
| Attached AOS-FARM.637 request | READ | Task scope, branch, audit axes, allowed changes, validation, commit boundary. |
| Project architecture docs/templates/scripts/tests listed above | READ | Audited surfaces. |

## Baseline Validation Snapshot

| Command | Result | Notes |
|---|---|---|
| `PYTHONPYCACHEPREFIX=/private/tmp/aos-farm-637-pycache python3 aos/scripts/aos_architecture_document_check.py validate-all --json` | PASS_WITH_WARNINGS_AND_NOT_RUN | Exit code 0. JSON status `PASS`; summary: 38 passed, 24 warnings, 0 failed, 0 blocked, 1 not_run. NOT_RUN is not PASS. |

## Findings Matrix

| ID | Severity | Area | Finding | Evidence | Risk | Proposed Fix | Applied |
|---|---|---|---|---|---|---|---|
| F-637-01 | MEDIUM | route_clarity | `technical-assignment-workflow.md` still describes a direct Technical Assignment to Controlled Task Brief path and does not insert the architecture need check before task breakdown. | The file states `Idea -> Problem Intake -> Technical Assignment -> Controlled Task Brief -> Execution -> Verification -> Human Checkpoint`. | Users or agents may skip architecture intake when architecture, stack, integration, validator, lifecycle, or safety-control questions are present. | Update the TA workflow bridge to insert Architecture Need Check, Architecture Input Intake/Decision Layer when required, Human Architecture Checkpoint, then Task Breakdown/Task Brief drafting. | APPLIED |
| F-637-02 | MEDIUM | validator_coverage | Architecture `validate-all` reports task-breakdown as `NOT_RUN` even though a standalone task-breakdown checker and canonical fixture exist. | Baseline JSON includes `{ "checker": "task-breakdown", "result": "NOT_RUN", "reason": "checker_not_implemented" }`. | Aggregate evidence suggests a gap and forces humans to separate expected NOT_RUN from real coverage, reducing smoothness. | Add a narrow aggregate task-breakdown fixture check and update tests to assert it runs. | APPLIED |
| F-637-03 | LOW | docs_consistency | `aos/docs/ROUTES.md` has the architecture route, but validator cross-reference checks miss exact markers `architecture route` and `no automatic execution authority`. | Baseline warnings `ARCH-REF-ROUTES` for both exact cross-references. | Route is semantically present but machine-readable evidence is noisy. | Add exact route marker wording without changing route authority. | APPLIED |
| F-637-04 | LOW | route_clarity | `architecture-decision-layer.md` lacks explicit cross-reference strings to the evidence packet and human checkpoint template, and lacks recommended section markers for decision question, options, recommended option, rejected options, and approval boundary. | Baseline warnings `ARCH-REF-DECISION-TO-EVIDENCE`, `ARCH-REF-EVIDENCE-TO-HUMAN-CHECKPOINT`, and `ARCH-MARKER-REC`. | Humans can find the route through surrounding docs, but the local decision-layer page is less self-contained. | Add concise route sections and exact cross-references. | APPLIED |
| F-637-05 | LOW | artifact_contract | `architecture-input-intake.md` is safe but thin: it lacks explicit assumptions, non-goals, and human review/checkpoint markers. | Baseline warnings for missing `assumptions`, `non-goals`, and `human review or checkpoint`. | Non-programmer users may not know what to capture or when to stop. | Add assumptions, non-goals, output and stop-boundary guidance. | APPLIED |
| F-637-06 | LOW | evidence_boundary | `architecture-decision-evidence-packet.md` validates as PASS but structural marker warnings show missing explicit evidence summary, inspected files, validation results, assumptions, UNKNOWNs, rejected options, human questions, and approval-not-claimed text. | Baseline `ARCH-MARKER-HARD` and `ARCH-MARKER-REC` warnings on the evidence packet. | Evidence remains non-approval, but the review packet is less scannable. | Add explicit sections/markers while preserving candidate-only and non-approval semantics. | APPLIED |
| F-637-07 | LOW | user_smoothness | Architecture templates provide metadata and safety boundaries but little step-by-step user guidance, required/prohibited field explanation, or validation commands. | `aos/templates/architecture-brief-template.md`, `aos/templates/architecture-input-intake-template.md`, and `aos/templates/task-breakdown-from-architecture-template.md` are compact field stubs. | Users can fill fields incorrectly or miss validation/human review boundaries. | Add concise usage notes, required fields, prohibited claims, validation command, and human review boundaries. | APPLIED |
| F-637-08 | LOW | architecture_to_task_boundary | `task-brief-builder.md` says Architecture Brief is input "if applicable" but does not make the architecture checkpoint/validator condition explicit when architecture is required. | Task Brief Builder prompt step 1 only verifies the TA; input note says Architecture Brief if applicable elsewhere. | Task drafting can appear to proceed from TA alone when architecture is required. | Add a preflight architecture gate to the prompt. | APPLIED |

## Canonical Change Candidates

No root `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md` changes are required by this audit.

No release, merge-to-main, runtime enforcement, DB/RAG/vector store, broad refactor, or destructive operation is required.

## Unknowns / Not Run

| Item | Status | Notes |
|---|---|---|
| Human approval of architecture | HUMAN_REVIEW_REQUIRED | Not requested and not simulated. |
| Risk Profile assignment | HUMAN_REVIEW_REQUIRED | Agent did not assign Risk Profile. |
| Commit | NOT_RUN | Commit requires explicit `AOS COMMIT OK AOS-FARM.637`. |
| Push | NOT_RUN | Push requires separate explicit `AOS PUSH OK AOS-FARM.637`. |
| Release / merge to main | NOT_RUN | Out of scope and not authorized. |

## Recommended Fix Set

### Safe fixes applied in this stage

- Tighten TA-to-architecture-to-task route docs.
- Clarify architecture intake/decision/evidence docs.
- Clarify architecture templates and task-brief-builder preflight.
- Run task-breakdown fixture in architecture `validate-all`.
- Update validator tests for the new aggregate coverage.

### Fixes requiring human checkpoint

- Any root `00/01/02` change.
- Any branch model, release, merge, runtime enforcement, required CI, or Source of Truth model change.

### Deferred fixes / out of scope

- Full schema parser replacement for marker-based checks.
- Full Problem Intake -> TA -> Architecture -> Task Queue dogfood.
- Creation of a full architecture runner or runtime enforcement layer.
- Cleanup or deletion of untracked duplicate files.
