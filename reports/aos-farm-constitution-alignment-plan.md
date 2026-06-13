# AOS-FARM Constitution Alignment Plan

## 9.1 Executive Summary

1. **Task ID:** AOS-FARM.13
2. **Repository:** NMF13579/AOS-FARM
3. **Branch:** dev
4. **Mode:** Planning-only / alignment-plan-only / report-only
5. **Source mapping dependency status:** Verified (AOS-FARM.12 complete).
6. **Constitution files inspected:** `.specify/memory/constitution.md`, `constitution.md`
7. **Final alignment planning status:** AOS_FARM_13_CONSTITUTION_ALIGNMENT_PLAN_COMPLETE
8. **Constitution files modified:** false
9. **Implementation authorized:** false
10. **`/speckit.implement` authorized or run:** false
11. **`/specify` authorized or run:** false
12. **`/plan` authorized or run:** false
13. **Commit or push occurred:** false
14. **Human approval simulated:** false

## 9.2 AOS-FARM.12 Intake

1. **AOS-FARM.12 final status:** `AOS_FARM_12_SOURCE_MAPPING_COMPLETE`
2. **Mapping report exists:** true (`reports/aos-farm-source-pack-mapping.md`)
3. **Setup report exists:** true (`reports/aos-farm-setup-report.md`)
4. **Prior gaps carried into AOS-FARM.13:**
   - Spec Kit defaults treat PASS as approval.
   - Missing protected/canonical file mapping.
   - Agent default behavior attempts implementation automatically.
5. **AOS-FARM.12 commit/push occurred:** Yes (`c9b181c` on `dev`).
6. **Prior commit/push authorization limit:** Confirmed. The prior commit/push only recorded the mapping report and does not authorize implementation, execution, or further push operations.

## 9.3 Required Source Verification

1. `00_AOS_Core_Control.md`: Checked. Exists. Readable. Role: Root Control. Relevant rule: Canonical authority over Spec Kit. Blocking: false.
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Checked. Exists. Readable. Role: Roadmap. Relevant rule: Execution gates. Blocking: false.
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Checked. Exists. Readable. Role: Safety constraints. Relevant rule: Invariants (PASS ≠ approval). Blocking: false.

## 9.4 Constitution File Inventory

1. `.specify/memory/constitution.md`
   - Exists: true
   - Readable: true
   - Current role: Active Spec Kit constraints memory.
   - Canonical or derived: Derived
   - Protected status: Protected
   - Modification allowed in AOS-FARM.13: false
   - Human checkpoint required before modification: true
   - Notes: Found 131 lines. Contains some basic safety rules but lacks comprehensive command constraints.

2. `constitution.md`
   - Exists: true
   - Readable: true
   - Current role: Root mirror of active memory.
   - Canonical or derived: Derived
   - Protected status: Protected
   - Modification allowed in AOS-FARM.13: false
   - Human checkpoint required before modification: true
   - Notes: Identical to `.specify/memory/constitution.md`.

## 9.5 AOS Invariant Coverage Matrix

| ID | AOS-required statement | Authority | In `.specify/memory/constitution.md` | In `constitution.md` | Alignment Status | Required Action | Checkpoint Required |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | PASS ≠ approval. | 02 | yes | yes | ALIGNED | None | N/A |
| 2 | Evidence ≠ approval. | 02 | yes | yes | ALIGNED | None | N/A |
| 3 | CI PASS ≠ approval. | 02 | yes | yes | ALIGNED | None | N/A |
| 4 | UNKNOWN ≠ OK. | 02 | yes | yes | ALIGNED | None | N/A |
| 5 | NOT_RUN ≠ PASS. | 02 | yes | yes | ALIGNED | None | N/A |
| 6 | Human approval cannot be simulated. | 02 | yes | yes | ALIGNED | None | N/A |
| 7 | Skeleton ≠ implementation. | 02 | yes | yes | ALIGNED | None | N/A |
| 8 | Scope must not expand without explicit human permission. | 02 | yes | yes | ALIGNED | None | N/A |
| 9 | Protected/canonical changes require human checkpoint. | 00, 02 | partial | partial | PARTIAL | Add specific files list. | Yes |
| 10 | Destructive operations are forbidden by default. | 02 | yes | yes | ALIGNED | None | N/A |
| 11 | Minimal Safety Floor is always-on from day one. | 02 | yes | yes | ALIGNED | None | N/A |
| 12 | Human unavailable -> BLOCKED / HUMAN_REVIEW_REQUIRED. | 02 | no | no | MISSING | Inject rule. | Yes |
| 13 | Agent may propose Risk Profile but cannot assign LOW_RISK_FAST. | 02 | no | no | MISSING | Inject rule. | Yes |
| 14 | AOS overrides Spec Kit defaults on governance/control. | 00 | partial | partial | PARTIAL | Clarify override. | Yes |
| 15 | Spec Kit is scaffold/substrate, not final authority. | 00 | partial | partial | PARTIAL | Clarify override. | Yes |
| 16 | `/speckit.implement` requires explicit authorization. | 01, 02 | partial | partial | PARTIAL | Make universal constraint. | Yes |
| 17 | `/specify` requires explicit authorization. | 01, 02 | no | no | MISSING | Inject rule. | Yes |
| 18 | `/plan` requires explicit authorization. | 01, 02 | no | no | MISSING | Inject rule. | Yes |
| 19 | Release requires explicit human authorization. | 01, 02 | partial | partial | PARTIAL | Make universal constraint. | Yes |
| 20 | Production use requires explicit human authorization. | 01, 02 | partial | partial | PARTIAL | Make universal constraint. | Yes |

## 9.6 Constitution Gap Register

1. **gap_id:** `GAP-CONST-001`
   - **source_invariant:** 12. Human unavailable -> BLOCKED.
   - **affected_file:** `.specify/memory/constitution.md`, `constitution.md`
   - **gap_type:** `missing`
   - **current_text_summary:** Rule does not exist.
   - **required_aos_semantics:** Must block execution if human review is required but unavailable.
   - **risk:** `HIGH`
   - **blocks_future_implementation_readiness:** `true`
   - **blocks_future_speckit_implement_readiness:** `true`
   - **requires_human_checkpoint:** `true`
   - **agent_may_fix_now:** `false`
   - **recommended_future_change:** Add explicit rule blocking operations when human is unavailable.

2. **gap_id:** `GAP-CONST-002`
   - **source_invariant:** 13. Risk Profile assignment limits.
   - **affected_file:** `.specify/memory/constitution.md`, `constitution.md`
   - **gap_type:** `missing`
   - **current_text_summary:** Rule does not exist.
   - **required_aos_semantics:** Agent cannot assign LOW_RISK_FAST; risk assignment requires human.
   - **risk:** `MEDIUM`
   - **blocks_future_implementation_readiness:** `true`
   - **blocks_future_speckit_implement_readiness:** `true`
   - **requires_human_checkpoint:** `true`
   - **agent_may_fix_now:** `false`
   - **recommended_future_change:** Add Risk Profile rule explicitly forbidding LOW_RISK_FAST assignment by agents.

3. **gap_id:** `GAP-CONST-003`
   - **source_invariant:** 16, 17, 18. Universal command constraints.
   - **affected_file:** `.specify/memory/constitution.md`, `constitution.md`
   - **gap_type:** `missing` / `partial`
   - **current_text_summary:** Only blocks `/speckit.implement` in the context of the current activation approval, but lacks universal rules for `/specify` and `/plan`.
   - **required_aos_semantics:** `/speckit.implement`, `/specify`, and `/plan` must be globally blocked by default unless explicitly authorized.
   - **risk:** `HIGH`
   - **blocks_future_implementation_readiness:** `true`
   - **blocks_future_speckit_implement_readiness:** `true`
   - **requires_human_checkpoint:** `true`
   - **agent_may_fix_now:** `false`
   - **recommended_future_change:** Add dedicated section for Spec Kit Command Limits.

4. **gap_id:** `GAP-CONST-004`
   - **source_invariant:** 9. Protected/canonical changes require human checkpoint.
   - **affected_file:** `.specify/memory/constitution.md`, `constitution.md`
   - **gap_type:** `partial`
   - **current_text_summary:** "This constitution does not authorize protected/canonical changes." (Line 64).
   - **required_aos_semantics:** Must explicitly list canonical files (00_, 01_, 02_) and require checkpoint for changes.
   - **risk:** `MEDIUM`
   - **blocks_future_implementation_readiness:** `true`
   - **blocks_future_speckit_implement_readiness:** `false`
   - **requires_human_checkpoint:** `true`
   - **agent_may_fix_now:** `false`
   - **recommended_future_change:** Clarify Section 11 with explicit protected file paths.

## 9.7 Proposed Alignment Change Set

```yaml
proposed_changes_applied: false
```

**Change 1: Command Limits**
- **change_id:** `CHG-CONST-001`
- **Target file:** Both constitution files.
- **Target section:** New section "Spec Kit Command Limits"
- **Change type:** `add`
- **Current problem:** `/specify`, `/plan`, and `/speckit.implement` lack universal blocks.
- **Proposed wording summary:** "All Spec Kit commands (`/specify`, `/plan`, `/speckit.implement`) are strictly blocked and require explicit human authorization in a Task Brief before use."
- **AOS source authority:** `01`, `02`
- **Risk level candidate:** `MEDIUM_RISK_CONTROLLED`
- **Human checkpoint required:** `true`
- **Validation required after change:** Verify `grep` for command block rules.
- **Rollback requirement:** Revert to prior git commit if validation fails.

**Change 2: Human Availability Rule**
- **change_id:** `CHG-CONST-002`
- **Target file:** Both constitution files.
- **Target section:** Add to Section 23 "Human Review Rule"
- **Change type:** `clarify`
- **Current problem:** Missing block on unavailable humans.
- **Proposed wording summary:** "If human review, approval, or Risk Profile assignment is required but the human is unavailable, the agent must immediately halt and report BLOCKED."
- **AOS source authority:** `02`
- **Risk level candidate:** `MEDIUM_RISK_CONTROLLED`
- **Human checkpoint required:** `true`
- **Validation required after change:** Verify rule existence.
- **Rollback requirement:** Revert to prior commit.

**Change 3: Risk Profile Constraint**
- **change_id:** `CHG-CONST-003`
- **Target file:** Both constitution files.
- **Target section:** Section 17 "Risk Profile Rules"
- **Change type:** `clarify`
- **Current problem:** Missing constraint against agent assigning LOW_RISK_FAST.
- **Proposed wording summary:** "Agents may propose a Risk Profile but cannot assign LOW_RISK_FAST. Only humans may authorize LOW_RISK_FAST execution."
- **AOS source authority:** `02`
- **Risk level candidate:** `MEDIUM_RISK_CONTROLLED`
- **Human checkpoint required:** `true`
- **Validation required after change:** Verify rule existence.
- **Rollback requirement:** Revert to prior commit.

## 9.8 Human Checkpoint Requirements

```yaml
human_checkpoint_required_before_constitution_edit: true
human_checkpoint_exists_for_constitution_edit: false
agent_may_create_human_approval: false
agent_may_simulate_human_approval: false
```

Required Package Contents:
1. Human reviewer identity.
2. Explicit authorization to edit `.specify/memory/constitution.md` and `constitution.md`.
3. Exact allowed files.
4. Exact forbidden files.
5. Exact allowed semantic changes (the CHG-CONST set).
6. Confirmation that PASS remains not approval.
7. Confirmation that Evidence remains not approval.
8. Confirmation that CI PASS remains not approval.
9. Confirmation that Risk Profile assignment remains human-controlled.
10. Confirmation that implementation remains unauthorized.
11. Confirmation that `/speckit.implement` remains unauthorized.
12. Confirmation that release and production use remain unauthorized.

## 9.9 Risk Profile Candidate

```yaml
agent_proposed_risk_profile: MEDIUM_RISK_CONTROLLED
risk_profile_assigned_by_agent: false
human_risk_profile_assignment_required: true
low_risk_fast_assigned_by_agent: false
```

## 9.10 Future Task Recommendation

Recommended next task: `AOS-FARM.14 — Human Checkpoint for Constitution Alignment`

This recommendation is not approval.
This recommendation does not start AOS-FARM.14.
This recommendation does not authorize constitution edits.
This recommendation does not authorize implementation.
This recommendation does not authorize `/speckit.implement`.
This recommendation does not authorize release.
This recommendation does not authorize production use.

```yaml
final_status: AOS_FARM_13_CONSTITUTION_ALIGNMENT_PLAN_COMPLETE
constitution_files_modified: false
proposed_changes_applied: false
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
commit_created: false
push_performed: false
ready_for_implementation: false
ready_for_speckit_implement: false
ready_for_release: false
may_prepare_aos_farm_14: true
```
