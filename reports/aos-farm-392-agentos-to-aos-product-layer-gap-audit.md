# AOS-FARM-392 AgentOS to AOS Product Layer Gap Audit

## Preflight Results
- **Branch**: dev
- **HEAD Commit**: `f2467be` (Matches origin/dev)
- **Staged Changes**: None.
- **Required Sources**: Verified `00/01/02` exist and were read.
- **Directories**: `agentos/` and `aos/` verified to exist.

## Required Sources Read Confirmation
- [x] `00_AOS_Core_Control.md`
- [x] `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- [x] `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## Overview
The `aos/` directory correctly houses the Markdown-first consumer methodology (governance, workflow, basic task briefs, safety checkpoints). However, the initial migration explicitly focused on execution control. "Top-of-funnel" activities like scoping, problem interviewing, and technical assignment formulation remain stranded in the old `agentos/` layer, often coupled with Python scripts.

---

## Table 1 — AgentOS Inventory Summary

| Area | File Count | Representative Paths | Likely Classification | Notes |
|---|---|---|---|---|
| **Problem Intake & Elicitation** | ~12 | `agentos/docs/methodology/technical-assignment/*` | NOT_MIGRATED_PRODUCT_GAP | Valuable conceptual workflow for defining requirements before execution. |
| **Python Scripts & Validators** | 4 | `agentos/scripts/*.py` | DEFER_RUNTIME | Conflicts with `aos/` no-runner-by-default rule. |
| **Prompts** | 1 | `agentos/docs/prompts/problem-intake-agent.md` | NOT_MIGRATED_PRODUCT_GAP | Needs adaptation for consumer use without Python dependencies. |
| **Pipelines & Runtime Contracts** | ~5 | `agentos/pipelines/*`, `agentos/docs/*pipeline*` | DEFER_RUNTIME | Too complex/executable for the baseline Markdown product. |
| **Historical Build Reports** | ~30+ | `agentos/reports/build-step-*` | INTERNAL_ONLY | AOS-FARM development history. |
| **Old Templates** | 6 | `agentos/templates/*` | MIGRATED | Replaced by `aos/templates/`. |
| **Legacy Governance Docs** | 2 | `agentos/docs/governance-control-module*.md` | LEGACY_REFERENCE_ONLY | Superseded by root `02_AOS_...`. |

---

## Table 2 — AOS Consumer Kit Coverage

| Product Capability | Old Source Path(s) | Current AOS Equivalent | Migration Status | Recommendation |
|---|---|---|---|---|
| **Controlled Task Execution** | `agentos/templates/task-brief.md` | `aos/templates/task-briefs/controlled-task-brief-template.md` | MIGRATED | - |
| **Safety & Governance** | `agentos/docs/governance-control-module-v1.md` | `aos/docs/governance/*` | MIGRATED | - |
| **Checkpoints & Authorization** | `agentos/templates/human-review.md` | `aos/templates/checkpoints/*` | MIGRATED | - |
| **Problem Intake / Elicitation** | `agentos/docs/methodology/technical-assignment/*` | None | NOT_MIGRATED_PRODUCT_GAP | Migrate as Markdown addendum. |
| **Automated Output Validation** | `agentos/scripts/thin_validator.py` | None | DEFER_RUNTIME | Keep Python out of default kit. |

---

## Table 3 — Product Gaps

| Gap ID | Capability | Source Path(s) | Recommended AOS Target Path(s) | Suggested Migration Type | Priority | Risk | Rationale |
|---|---|---|---|---|---|---|---|
| **GAP-01** | Problem Intake & Tech Assignment | `agentos/docs/methodology/technical-assignment/*`<br>`agentos/docs/prompts/problem-intake-agent.md` | `aos/docs/workflow/problem-intake-workflow.md`<br>`aos/templates/task-briefs/technical-assignment-template.md`<br>`aos/prompts/problem-intake.md` | Markdown Rewrite | HIGH | LOW | Fills the missing "Top-of-Funnel" gap. Users need to know *how* to write good briefs before executing them. |

---

## Table 4 — Runtime / Runner Deferred Items

| Item | Source Path | Why Deferred | Possible Future Form | Blocker Status |
|---|---|---|---|---|
| **Intake Runner** | `agentos/scripts/problem_intake_runner.py` | Active Python script violates the Markdown-first consumer model rule. | Optional CLI addon (`aos/extensions/`) | Blocked |
| **Thin Validator** | `agentos/scripts/thin_validator.py` | Requires active execution environment. | Optional test framework | Blocked |
| **Document Pipeline** | `agentos/pipelines/document_pipeline.py` | Custom AST/Markdown parser not required for base methodology. | Optional workflow tool | Blocked |

---

## Table 5 — Internal-only / Legacy-only Items

| Item | Source Path | Classification | Reason |
|---|---|---|---|
| **Build Reports** | `agentos/reports/build-step-*` | INTERNAL_ONLY | Internal dogfooding and evidence loops specific to the AOS-FARM repo lifecycle. |
| **Legacy Governance** | `agentos/docs/governance-control-module-v1.md` | LEGACY_REFERENCE_ONLY | Fully replaced by `02_AOS_Governance_Control_Module_and_Safety_Rules.md`. |

---

## Mandatory Findings: Problem Intake & Technical Assignment
**Was it migrated?**
No. The Problem Intake and Technical Assignment pipelines have not been migrated.

**Where does it currently exist?**
It exists in the old `agentos/docs/methodology/technical-assignment/` directory and as a prompt in `agentos/docs/prompts/problem-intake-agent.md`.

**Should it be migrated?**
Yes. It provides crucial methodology for extracting requirements from users (Problem Intake) and translating them into actionable plans (Technical Assignment). Without it, the Consumer Kit explains *how to safely execute* tasks, but doesn't explain *how to properly define them*.

**Why must Python runners be deferred?**
The core Consumer Kit (`aos/`) must remain universally accessible via purely text-based prompting. Introducing `problem_intake_runner.py` directly into the core violates the "No runner required" safety invariant and creates a deployment barrier.

## Recommended Next Task
**AOS-FARM.393 — Problem Intake and Technical Assignment Consumer Kit Addendum Authorization Preparation**

## Final Status
**AOS_FARM_392_AGENTOS_TO_AOS_PRODUCT_LAYER_GAP_AUDIT_COMPLETE**
