# AOS-FARM.267 — Deep Logical and Structural Audit Report

## 1. Executive Summary
This report presents the findings of a deep logical and structural audit conducted across the AOS-FARM core documentation, templates, user guides, and task queue boundaries. The project maintains a strong safety posture and adheres strictly to the Governance Control Module. However, several structural anomalies and legacy remnants have been identified that contradict the current single Source of Truth rules and repository layout.

## 2. Identified Contradictions and Anomalies

### A. Structural Duplication in Templates
**Finding:** The `templates/` directory contains exact duplicates of almost every template file (e.g., `feature-spec-template.md` and `feature-spec-template 2.md`).
**Violation:** This violates the **Source of Truth** rule defined in `00_AOS_Core_Control.md`, which requires unambiguous canonical Markdown files. Duplication creates ambiguity regarding which template is the active, canonical version.
**Risk Level:** Medium (Can lead to disjointed task execution and conflicting evidence artifacts).

### B. Legacy Drift in `00_AOS_Core_Control.md` Active Areas
**Finding:** In `00_AOS_Core_Control.md` under the **Active-now Areas** section, the document lists:
```text
agentos/architecture/
agentos/governance/
agentos/templates/
agentos/schemas/
agentos/pipelines/
agentos/state/
agentos/reports/
agentos/approvals/
agentos/scripts/
```
**Violation:** The actual, audited Core Working Version layout uses root-level directories like `docs/`, `reports/`, and `templates/`, with `agentos/` only containing `scripts/`. `00` contradicts the active architecture and implies a legacy directory structure.
**Risk Level:** Medium (Causes confusion for autonomous agents reading `00` to find canonical directories).

### C. Overlap in User Guide Roles
**Finding:** `docs/user-guide/agent-tutor-mode.md` and `docs/user-guide/bootstrap-agent-workflow.md` both independently define the roles and boundaries of the Agent Tutor. 
**Violation:** While not a strict safety violation, the overlap creates redundant definitions of the Agent Tutor, which contradicts the design goal of having clear, unambiguous onboarding for non-programmers. 
**Risk Level:** Low (Usability issue).

## 3. Governance and Safety Posture
- **Minimal Safety Floor:** Fully intact. No definitions in `01` or `02` contradict the core safety floor.
- **Approval Boundaries:** The rules surrounding `UNKNOWN`, `NOT_RUN`, `PASS`, and `Evidence` are consistently defined and do not logically contradict each other across the 3 core files.
- **Task Queue Helper:** `task_queue_helper.py` aligns with the documented dry-run constraints and does not possess runtime authority.

## 4. Next Safe Steps (Recommendations)
To resolve these findings without violating governance boundaries, the following tasks should be added to the queue (e.g., `AOS-FARM.268+`):
1. **Deduplicate Templates:** Plan a destructive/canonical task (requires `DESTRUCTIVE_OR_CANONICAL` risk profile) to remove all `* 2.md` files from the `templates/` directory.
2. **Update Core Document:** Plan a `HIGH_RISK_PROTECTED` task to update the `Active-now Areas` in `00_AOS_Core_Control.md` to reflect the current `docs/`, `reports/`, and `templates/` root structure.
3. **Consolidate User Guides:** Plan a `MEDIUM_RISK_GUIDED` task to merge the Agent Tutor guidelines into a single canonical document.
