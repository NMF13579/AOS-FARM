# AOS-FARM.361 Spec Kit and Recurring Warnings Inventory Audit

## Preflight Results
- **Branch**: dev
- **HEAD**: `d33b1a6d93f0075bfe716a1ec6488caf92bafaef`
- **origin/dev**: `d33b1a6d93f0075bfe716a1ec6488caf92bafaef`
- **Ahead/Behind**: 0 0
- **Required Sources Read Confirmation**: Confirmed. `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and `02_AOS_Governance_Control_Module_and_Safety_Rules.md` were successfully read.

## Inventory Analysis

### 1. Spec Kit Inventory
The following files and paths related to Spec Kit were identified in the repository:
- **Core Engine (Tracked)**:
  - `.specify/` (workflows, extensions, templates, memory, constitution)
  - `scripts/validate-spec.sh`
- **Agent Prompts & Profiles (Tracked)**:
  - `.github/agents/speckit.*.agent.md`
  - `.github/prompts/speckit.*.prompt.md`
- **Root Configurations (Tracked)**:
  - `constitution.md`
- **Specs / Example Features (Tracked)**:
  - `specs/` (example-feature)
- **Documentation & References (Tracked)**:
  - `docs/references/spec-kit-reference.md`
  - `docs/boundaries/spec-kit-implement-boundary.md`
- **AOS-FARM Core Spec Docs (Tracked - likely safe/needed)**:
  - `templates/feature-spec-template.md`
  - `templates/spec-to-execution-traceability-matrix-template.md`
  - `docs/assembly/aos-native-spec-to-execution-pattern-pack-mvp.md`
- **Reports (Tracked & Untracked)**:
  - Multiple reports referencing constitution alignment and spec-to-execution patterns.

### 2. Recurring Warning Inventory
The following recurring warnings and untracked files were found:
- **Duplicate Docs (Untracked)**:
  - Multiple `* 2.md` files in `docs/assembly/`, `docs/governance/`, `docs/operations/`, `docs/validation/`.
- **Local-Only Evidence-Tail / Closure Reports (Untracked)**:
  - e.g., `reports/aos-farm-351-remediation-commit-push-authorization-package.md`, `reports/aos-farm-353-remediation-push-and-remote-closure.md`, `reports/aos-farm-364-readme-landing-page-push-and-remote-closure.md`, etc.
- **Problem Intake / Dogfood Fixtures (Untracked)**:
  - `agentos/reports/problem-intake/` and all its subdirectories containing draft specs, inputs, and validation reports.

---

## Classification

### Proposed DELETE_CANDIDATE
These files are safe to completely remove to clean up the consumer installation path.
- **Spec Kit Code/Configs (Tracked)**:
  - `.specify/`
  - `.github/agents/speckit.*`
  - `.github/prompts/speckit.*`
  - `scripts/validate-spec.sh`
  - `specs/` (example feature)
  - `constitution.md`
- **Recurring Warnings (Untracked)**:
  - All `* 2.md` duplicate documents.
  - All untracked closure, remediation, and push authorization packages in `reports/` and `reports/human-checkpoints/`.
  - The entire `agentos/reports/problem-intake/` directory.

### Proposed MOVE_TO_INTERNAL_OR_LEGACY
These files should be retained for internal project history but removed from the main surface.
- **Spec Kit Documentation**:
  - `docs/references/spec-kit-reference.md`
  - `docs/boundaries/spec-kit-implement-boundary.md`

### Proposed KEEP_AS_REFERENCE
These files are historical tracked reports that document past AOS-FARM milestones and should remain in the repository.
- Tracked reports mentioning constitution alignment, spec-to-execution, release preparations, and historical execution authorizations.

### Proposed KEEP_AS_LOCAL_ONLY
- None currently required. The untracked local-only files are all stale remnants of closed loops and can be deleted.

### Proposed KEEP_AS_ACTIVE
- `templates/feature-spec-template.md`
- `templates/spec-to-execution-traceability-matrix-template.md`
- `docs/assembly/aos-native-spec-to-execution-pattern-pack-mvp.md`
*(These are native AOS-FARM artifacts for the Assembly Pipeline, despite containing the word "spec").*

### Proposed BLOCKED_UNKNOWN
- None.

---

## Impact Assessment

### Does Spec Kit appear active in the public first-run path?
**No.** The public README, Installation Guide, and Quickstart point the user toward standard Markdown templates and AI Tutor mode. The Spec Kit automated commands (`/specify`, `/plan`) are not part of the documented first-run flow and act as unnecessary bloat for standard consumers.

### Is Spec Kit safe to remove later?
**Yes.** AOS-FARM relies on the `00`, `01`, `02` governance controls and standard Markdown templates, not on Spec Kit's execution engine or `.specify` configurations. Removing it will significantly clean up the repository root and `.github` directory without breaking the AOS-FARM workflow. Explicit human authorization will be required to execute the deletion of tracked files.

### Can recurring warnings be removed later?
**Yes.** The untracked `* 2.md` files, stale closure reports, and `problem-intake` dogfood fixtures are local clutter. Deleting them requires human authorization since it constitutes a destructive operation, but it is entirely safe and will not affect the Git baseline.

## Exact Next Recommended Task
Create a new Task Brief for **AOS-FARM.365 — Clean Consumer Install Remediation** with Risk Profile `DESTRUCTIVE_OR_CANONICAL`. The task should request explicit human authorization to delete the proposed `DELETE_CANDIDATE` and `MOVE_TO_INTERNAL_OR_LEGACY` files.

## Blocking Issues
None for this audit.

## Warnings
The repository contains significant untracked state (over 50 files) and legacy tracked Spec Kit code. No actions were taken to remediate these warnings during this read-only audit.

## Final Status
**AOS_FARM_361_SPEC_KIT_AND_WARNINGS_INVENTORY_COMPLETE**
