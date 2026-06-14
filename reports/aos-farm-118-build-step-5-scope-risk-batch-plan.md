# AOS-FARM.118 — Build Step 5 Scope, Risk, Batch Plan, and Execution Authorization Preparation

## 1. Scope Analysis

- **Does Step 5 create runtime files?** No.
- **Does Step 5 create scripts?** No.
- **Does Step 5 create validators?** No.
- **Does Step 5 modify protected/canonical files?** No.
- **Does Step 5 introduce CI workflow?** No.
- **Does Step 5 require Spec Kit commands?** No.
- **Does Step 5 only create docs/templates/reports?** Yes.

## 2. Risk Profile Assessment

- **minimum_expected_risk_profile:** MEDIUM_RISK_GUIDED
- **human_risk_profile_assignment_required:** true
- **agent_may_propose_risk_profile:** true
- **agent_must_not_assign_low_risk_fast:** true

**Agent Proposal:** `MEDIUM_RISK_GUIDED`. Since this step only creates markdown documentation and templates, there is no runtime enforcement, CI, or code modification. The risk remains at documentation level.

## 3. Fail-Closed Verification

The scope does not include validators, approval or PASS logic, runtime enforcement, CI required checks, or protected-canonical changes. Therefore, it does not require escalation to HIGH_RISK_PROTECTED or splitting into smaller batches. One single batch (Batch 1) is sufficient for the MVP.

## 4. Batch Plan (Batch 1)

**Task:** AOS-FARM.120 (Controlled Execution: Code Assembly Pipeline MVP Batch)

**Authorized Output Scope:**
1. `docs/assembly/code-assembly-pipeline-mvp.md`
2. `templates/code-assembly-mvp-input-template.md`
3. `templates/code-assembly-mvp-execution-report-template.md`
4. `templates/code-assembly-mvp-evidence-report-template.md`
5. `templates/code-assembly-mvp-human-review-template.md`
6. `reports/aos-farm-code-assembly-pipeline-mvp-report.md`

No execution, staging, commit, push, or release is authorized in this step. This is purely preparation.
