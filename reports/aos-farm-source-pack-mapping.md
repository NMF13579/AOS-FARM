# AOS-FARM Source Pack Mapping Into Spec Kit Structure

## 9.1 Executive Summary

1. **Task ID:** AOS-FARM.12
2. **Repository:** NMF13579/AOS-FARM
3. **Branch:** dev
4. **Mode:** Planning-only / mapping-only / report-only
5. **Final mapping status:** AOS_FARM_12_SOURCE_MAPPING_COMPLETE
6. **Implementation authorized:** false
7. **`/speckit.implement` authorized:** false
8. **Release authorized:** false
9. **Protected/canonical files changed:** false
10. **Human approval simulated:** false

## 9.2 Required Source Inventory

| Source | Path Checked | Exists | Readable | Role | Authority Level | Blocking Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `00_AOS_Core_Control.md` | `00_AOS_Core_Control.md` | `true` | `true` | Root Core Control | 1 (Highest) | Not Blocking | Found and readable. |
| `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` | `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` | `true` | `true` | Pipeline Roadmap | 2 | Not Blocking | Found and readable. |
| `02_AOS_Governance_Control_Module_and_Safety_Rules.md` | `02_AOS_Governance_Control_Module_and_Safety_Rules.md` | `true` | `true` | Governance & Safety Rules | 3 | Not Blocking | Found and readable. |

## 9.3 Optional Source Inventory

1. **Exists:** `true` (`03_AOS_Future_and_Legacy_Reference_OPTIONAL.md`)
2. **Readable:** `true`
3. **Used as optional reference only:** Confirmed.
4. **Confirmation that it did not override required sources:** Confirmed. Did not override any required safety/control semantics.

## 9.4 Spec Kit Structure Inventory

| Location | Exists | Current Apparent Role | Status | Overridden by AOS | Human Checkpoint Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `.specify/` | `true` | Spec Kit engine root | Scaffold | Yes (overall safety logic) | Yes |
| `.specify/memory/` | `true` | Internal context/memory | Scaffold | Yes | Yes |
| `.specify/memory/constitution.md` | `true` | Active constitution | Derived | Yes | Yes |
| `constitution.md` | `true` | Root constitution reference | Derived / Mirror | Yes | Yes |
| `specs/` | `true` | Specifications directory | Scaffold | No | No (for specs) |
| `templates/` | `true` (in `.specify/`) | Template repository | Scaffold | No | No (unless protected template) |
| `scripts/` | `true` | Script utilities | Scaffold | Yes | Yes |
| `reports/` | `true` | Evidence / Reports | Canonical (for Checkpoints) | No (AOS mandates it) | Yes (for Checkpoints) |
| `docs/` | `true` | Documentation / Manuals | Scaffold | No | No |
| `.github/` | `true` | GitHub Actions / Configs | Scaffold | Yes (workflow creation blocked) | Yes |

## 9.5 Source-to-Spec-Kit Mapping Matrix

| AOS Concept | AOS Source Authority | Spec Kit Location | Mapping Status | Notes | Protected | Checkpoint | Risk Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Source of Truth hierarchy | `00` | `.specify/memory/constitution.md` | `PARTIAL` | Spec Kit defaults to itself; AOS overrides. | Yes | Yes | `UNKNOWN_BLOCKED` |
| Human approval boundary | `02` | `reports/human-checkpoints/` | `MAPPED` | Strictly enforced by AOS rules. | Yes | Yes | Checked |
| Evidence discipline | `02` | `reports/` | `MAPPED` | Used actively for trace logs. | No | No | Checked |
| PASS boundary | `02` | N/A | `CONFLICT` | Spec Kit assumes PASS is OK. AOS rejects this. | N/A | N/A | `UNKNOWN_BLOCKED` |
| UNKNOWN / NOT_RUN semantics | `02` | N/A | `CONFLICT` | LLM implicitly assumes OK; AOS rejects. | N/A | N/A | `UNKNOWN_BLOCKED` |
| Minimal Safety Floor | `02` | `.specify/memory/constitution.md` | `PARTIAL` | Needs explicit instructions injected into memory. | Yes | Yes | `UNKNOWN_BLOCKED` |
| Risk Profile handling | `02` | N/A | `MISSING` | Spec Kit lacks Risk Profile assignments. | N/A | N/A | `UNKNOWN_BLOCKED` |
| Protected/canonical rules | `00`, `02` | `.specify/memory/constitution.md` | `MISSING` | Needs injection into Constitution limits. | Yes | Yes | `UNKNOWN_BLOCKED` |
| Doc Assembly Pipeline | `01` | `.specify/scripts/` | `MISSING` | Pipeline logic is undefined in Spec Kit. | No | Yes | `UNKNOWN_BLOCKED` |
| Code Assembly Pipeline | `01` | `.specify/scripts/` | `MISSING` | Code logic is undefined. | No | Yes | `UNKNOWN_BLOCKED` |
| Assembly Core | `01` | `src/` (not created) | `MISSING` | Core not mapped yet. | No | Yes | `UNKNOWN_BLOCKED` |
| Governance/Control Module | `02` | `.specify/memory/constitution.md` | `PARTIAL` | Control limits are implicit, not fully encoded. | Yes | Yes | `UNKNOWN_BLOCKED` |
| Build Step roadmap | `01` | `specs/` | `PARTIAL` | Spec Kit can handle it, but specs are missing. | No | No | Checked |
| Task brief lifecycle | `00` | `specs/`, `reports/` | `MAPPED` | Currently functioning well. | No | No | Checked |
| Report artifacts | `00` | `reports/` | `MAPPED` | Currently functioning well. | No | No | Checked |
| Human checkpoints | `02` | `reports/human-checkpoints/` | `MAPPED` | Used actively for authorizations. | Yes | Yes | Checked |
| Spec Kit constitution | Spec Kit | `.specify/memory/constitution.md` | `MAPPED` | Integrated. | Yes | Yes | Checked |
| Spec Kit templates | Spec Kit | `.specify/templates/` | `MAPPED` | Available. | No | No | Checked |
| Spec Kit scripts | Spec Kit | `.specify/scripts/` | `MAPPED` | Available. | No | No | Checked |
| Future readiness gate | `01`, `02` | N/A | `CONFLICT` | Spec Kit defaults to immediate implementation. AOS blocks it. | Yes | Yes | `UNKNOWN_BLOCKED` |

## 9.6 Conflict and Gap Register

1. **gap_id:** `GAP-001`
   - **type:** `source_conflict`
   - **affected_source:** `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
   - **affected_spec_kit_location:** `.specify/memory/constitution.md`
   - **description:** Spec Kit implicitly treats PASS/CI PASS as sufficient for execution; AOS forbids this.
   - **risk:** `HIGH`
   - **blocks_implementation_readiness:** `true`
   - **requires_human_review:** `true`
   - **agent_resolution_allowed:** `false`
   - **recommended_next_report_only_action:** Align Spec Kit Constitution with AOS safety boundaries.

2. **gap_id:** `GAP-002`
   - **type:** `missing_mapping`
   - **affected_source:** `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
   - **affected_spec_kit_location:** `.specify/memory/constitution.md`
   - **description:** Missing explicit protection lists and canonical file mapping within Spec Kit memory.
   - **risk:** `MEDIUM`
   - **blocks_implementation_readiness:** `true`
   - **requires_human_review:** `true`
   - **agent_resolution_allowed:** `false`
   - **recommended_next_report_only_action:** Inject protected rules into Constitution.

3. **gap_id:** `GAP-003`
   - **type:** `source_conflict`
   - **affected_source:** `00_AOS_Core_Control.md`
   - **affected_spec_kit_location:** Agent Default Behavior
   - **description:** Default agent behavior attempts implementation automatically if requested.
   - **risk:** `HIGH`
   - **blocks_implementation_readiness:** `true`
   - **requires_human_review:** `true`
   - **agent_resolution_allowed:** `false`
   - **recommended_next_report_only_action:** Establish Minimal Governance/Control Module.

## 9.7 Protected / Canonical Boundary Review

| Path | Protected | Canonical | Current Modification Allowed | Checkpoint Required | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `00_AOS_Core_Control.md` | `true` | `true` | `false` | `true` | Highest authority source. |
| `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` | `true` | `true` | `false` | `true` | Roadmap canonical source. |
| `02_AOS_Governance_Control_Module_and_Safety_Rules.md` | `true` | `true` | `false` | `true` | Safety canonical source. |
| `.specify/memory/constitution.md` | `true` | `false` | `false` | `true` | Derived, but limits agent execution. |
| `constitution.md` | `true` | `false` | `false` | `true` | Root mirror of memory. |
| `reports/human-checkpoints/` | `true` | `true` | `false` | `true` | Directory of explicit authorizations. |
| `.github/workflows/` | `true` | `false` | `false` | `true` | Infrastructure protection. |

## 9.8 AOS over Spec Kit Control Summary

Spec Kit is actively serving as the scaffold and memory substrate for AOS-FARM, providing organized paths for reports, specs, and basic memory (`constitution.md`). However, AOS remains the absolute Source of Truth for governance and control. Spec Kit defaults do not override AOS safety rules. Constitution alignment to properly reflect AOS control is strictly allowed only through explicitly controlled human-authorized tasks. Consequently, all implementation actions remain entirely blocked until explicit human authorization is granted to lift the boundary.

## 9.9 Risk Profile Candidate

```yaml
agent_proposed_risk_profile: MEDIUM_RISK_CONTROLLED
risk_profile_assigned_by_agent: false
human_risk_profile_assignment_required: true
```

## 9.10 Next-Step Recommendation

Recommended next planning target: `AOS-FARM.13 — Spec Kit Constitution Alignment Plan`

This recommendation is not approval.
This recommendation does not start the next task.
This recommendation does not authorize implementation.
This recommendation does not authorize `/speckit.implement`.
This recommendation does not authorize release.

```yaml
final_status: AOS_FARM_12_SOURCE_MAPPING_COMPLETE
implementation_authorized: false
speckit_implement_authorized: false
release_authorized: false
production_use_authorized: false
workflow_created: false
ci_activated: false
branch_protection_changed: false
protected_canonical_files_changed: false
human_approval_simulated: false
risk_profile_assigned_by_agent: false
ready_for_implementation: false
ready_for_speckit_implement: false
ready_for_release: false
```
