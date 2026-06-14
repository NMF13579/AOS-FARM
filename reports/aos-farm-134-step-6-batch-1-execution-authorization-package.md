# AOS-FARM.134 — Build Step 6 Batch 1 Execution Authorization Package

## Execution Targets
- **task_id:** `AOS-FARM.134`
- **target_execution_task:** `AOS-FARM.135`
- **proposed Risk Profile:** `MEDIUM_RISK_GUIDED`
- **human approval required:** `true`

## Bounded Scope
- **exact Batch 1 scope:** Dogfood the multi-environment and controller templates by generating 4 report-only evidence artifacts. No runtime changes.
- **exact authorized output files:**
  1. `reports/aos-farm-135-build-step-6-dogfood-session-start.md`
  2. `reports/aos-farm-135-build-step-6-model-routing-decision.md`
  3. `reports/aos-farm-135-build-step-6-controller-review-report.md`
  4. `reports/aos-farm-135-build-step-6-dogfood-evidence-report.md`

## Forbidden Actions
- **exact forbidden actions:**
  - Do not stage, commit, push, release, or perform production use.
  - Do not modify protected/canonical files.
  - Do not implement validators, runtime enforcement, or CI workflows.
  - Do not execute Spec Kit commands.

## Expected Outcomes
- **required Evidence outputs:** The 4 newly created dogfood report markdown files.
- **required final status options:**
  - `AOS_FARM_135_BUILD_STEP_6_BATCH_1_DOGFOOD_EVIDENCE_CREATED`
  - `AOS_FARM_135_BUILD_STEP_6_BATCH_1_DOGFOOD_EVIDENCE_CREATED_WITH_WARNINGS`
  - `AOS_FARM_135_BLOCKED`
