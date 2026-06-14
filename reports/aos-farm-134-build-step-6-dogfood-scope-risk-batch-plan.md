# AOS-FARM.134 — Build Step 6 Dogfood Scope, Risk, and Batch Plan

## Repository State
- **task_id:** `AOS-FARM.134`
- **current branch:** `dev`
- **HEAD:** `fff7bc9874aba5de96ea1562bb732bfa6d6cd93b`
- **origin/dev:** `fff7bc9874aba5de96ea1562bb732bfa6d6cd93b`
- **remote_baseline_closed:** `true`
- **required_sources_available:** `true`
- **multi_environment_controller_workflow_available:** `true`

## Dogfood Planning
- **build_step:** `6`
- **build_step_name:** `First Dogfood Trial`
- **proposed_risk_profile:** `MEDIUM_RISK_GUIDED`
- **human_risk_profile_assignment_required:** `true`
- **dogfood_objective:** Verify the new multi-environment controller and model routing workflow by generating evidence artifacts strictly governed by the newly created templates and agent rules.
- **dogfood_environment_plan:** Target environments include Antigravity or Codex CLI. The workflow will rely on `AGENTS.md` and the `docs/operations` boundary definitions.

## Batch 1 Execution Scope
- **exact_batch_1_scope:** Report-only dogfood trial. Generate session start, model routing, controller review, and final evidence reports to validate the agent's adherence to the new templates.
- **exact_batch_1_allowed_files:**
  1. `reports/aos-farm-135-build-step-6-dogfood-session-start.md`
  2. `reports/aos-farm-135-build-step-6-model-routing-decision.md`
  3. `reports/aos-farm-135-build-step-6-controller-review-report.md`
  4. `reports/aos-farm-135-build-step-6-dogfood-evidence-report.md`
- **exact_batch_1_forbidden_files_or_surfaces:** No modification to `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, `AGENTS.md`, or Step 5 MVP artifacts.

## Authorization Baseline
- **runtime_implementation_authorized_now:** `false`
- **validator_implementation_authorized_now:** `false`
- **ci_workflow_changes_authorized_now:** `false`
- **protected_canonical_changes_authorized_now:** `false`
- **spec_kit_commands_authorized_now:** `false`
- **execution_authorized_now:** `false`
- **commit_authorized_now:** `false`
- **push_authorized_now:** `false`
- **release_authorized_now:** `false`
- **production_use_authorized_now:** `false`

## Next Steps
- **recommended_next_task:** `AOS-FARM.135 — Controlled Execution: Build Step 6 Dogfood Batch 1`
