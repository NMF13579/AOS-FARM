# AOS-FARM.447 Execution Report

* **stage:** AOS-FARM.447 — Canonical Project Documentation Alignment
* **branch:** build/canonical-project-docs-alignment
* **Risk Profile:** HIGH_RISK_PROTECTED (Assigned by human)
* **files modified:**
  * `00_AOS_Core_Control.md`
  * `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
  * `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## Summary of Changes

### Repository Naming Alignment Summary
Updated the active repository references from `NMF13579/AOS-1` to `NMF13579/AOS-FARM` in `00_AOS_Core_Control.md`. Added explicit clarifications in `00_AOS_Core_Control.md` that legacy naming (AOS-1, AgentOS, AgentOS Next) is historical/reference naming only, and legacy AgentOS must not be imported into AOS-FARM.

### Branch Model Alignment Summary
Updated `00_AOS_Core_Control.md` to establish `dev` as the "active controlled integration baseline" (removing "frozen skeleton") and `build/` as the recommended branch pattern (removing "build/assembly-first").

### Product Folder Boundary Preservation Summary
Confirmed and maintained the Product folder boundaries (`/aos/`, `/aos/root/AGENTS.md`) across all three canonical sources. Added explicit notation that legacy AgentOS is for reference only and must not be imported into AOS-FARM.

### Local Temporary Workspace Boundary Summary
Injected the "Local Temporary Workspace Boundary" definition into `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and `02_AOS_Governance_Control_Module_and_Safety_Rules.md`. This standardizes the use of `/.aos-tmp/` for local-only, ignored, and disposable outputs while strictly forbidding Evidence, checkpoints, and approvals in this directory.

### Safety/Control Clarification Summary for 02
Added a strict clarification to `02_AOS_Governance_Control_Module_and_Safety_Rules.md` that if an agent finds protected items (Evidence, approvals, lifecycle decisions, etc.) in `/.aos-tmp/`, the safe state transitions to `HUMAN_REVIEW_REQUIRED` or `UNKNOWN_BLOCKED`.

## Exact sections changed
* `00_AOS_Core_Control.md`:
  * `## Статус`
  * `## Назначение`
  * `## Repository Baseline`
  * `## Strategy Lock`
  * `## Product Identity`
  * `## Product Folder Boundaries`
  * `## Local Temporary Workspace Boundary` (New section)
  * `## Legacy Boundary`
  * `## Medical Boundary`
* `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`:
  * `## Статус`
  * `## Product Folder Boundaries`
  * `## Local Temporary Workspace Boundary` (New section)
* `02_AOS_Governance_Control_Module_and_Safety_Rules.md`:
  * `## Статус`
  * `## Product Folder Boundaries`
  * `## Local Temporary Workspace Boundary` (New section, including safety/control escalation triggers)

## Verification Command Outputs

```text
git status --short
 M 00_AOS_Core_Control.md
 M 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
 M 02_AOS_Governance_Control_Module_and_Safety_Rules.md

git status -sb
## build/canonical-project-docs-alignment

git diff --check
(No output, clean)

git diff --name-status
M	00_AOS_Core_Control.md
M	01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
M	02_AOS_Governance_Control_Module_and_Safety_Rules.md

git diff --stat
 00_AOS_Core_Control.md                             | 41 +++++++++++++++-------
 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md     | 21 +++++++++--
 ...S_Governance_Control_Module_and_Safety_Rules.md | 33 +++++++++++++++--
 3 files changed, 79 insertions(+), 16 deletions(-)
```

### Grep outputs (Summary):
- Matches for `NMF13579/AOS-FARM` successfully replaced old references.
- `active controlled integration baseline` verified in `00_AOS_Core_Control.md`.
- `Local Temporary Workspace` and `.aos-tmp` strings verified in 00, 01, and 02.
- `frozen skeleton/reference baseline` and `build/assembly-first` were successfully removed from `00_AOS_Core_Control.md`.

## Confirmations
* **Confirmation that no files outside 00/01/02 were modified except the execution report:** Verified.
* **Confirmation that no commit/push/merge/release was performed:** Verified.

* **final_status:** HUMAN_REVIEW_REQUIRED
