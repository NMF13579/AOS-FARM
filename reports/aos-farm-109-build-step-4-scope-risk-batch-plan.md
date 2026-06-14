# AOS-FARM.109 — Build Step 4 Scope, Risk, and Batch Plan

## 1. Step 4 Name
Build Step 4 — Code Assembly Pipeline Contract

## 2. Goal
Define how a Task Brief becomes a scoped code change by creating the documentation/templates contract for future code assembly work. Does not implement runtime enforcement, validators, CI workflows, automatic merge, release, or production use.

## 3. Fast-Safe Execution Strategy
A single, large docs/templates/reports batch.

## 4. Corrected Task Chain
- **AOS-FARM.109** — Step 4 Scope, Risk, Batch Plan, and Execution Auth Preparation
- **AOS-FARM.110** — Human Execution Authorization
- **AOS-FARM.111** — Controlled Execution: Step 4 Code Assembly Pipeline Contract
- **AOS-FARM.112** — Step 4 Batch Verification + Final Step 4 Verification
- **AOS-FARM.113** — Final Step 4 Commit Authorization Preparation
- **AOS-FARM.114** — Human Commit Authorization
- **AOS-FARM.115** — Controlled Final Step 4 Commit Execution + Push Authorization Preparation
- **AOS-FARM.116** — Human Push Authorization
- **AOS-FARM.117** — Controlled Step 4 Push Execution + Remote Baseline Closure

## 5. Merged Safety Boundaries
- Verification Merge: Batch verification + final step verification merged (AOS-FARM.112).
- Commit Execution + Push Auth Prep Merge: AOS-FARM.115.
- Push Execution + Closure Merge: AOS-FARM.117.

## 6. Forbidden Merges
PASS ≠ approval. Evidence ≠ approval. Commit authorization ≠ push authorization. Human approval cannot be simulated. Human approval boundaries remain distinct and unmerged.

## 7. Step 4 Batch 1 Scope
Proposed files:
1. `docs/assembly/code-assembly-pipeline-contract.md`
2. `docs/assembly/task-brief-to-scoped-code-change.md`
3. `docs/assembly/code-diff-evidence-expectations.md`
4. `templates/code-execution-package-template.md`
5. `templates/code-change-scope-template.md`
6. `templates/allowed-forbidden-code-change-template.md`
7. `templates/code-diff-evidence-template.md`
8. `templates/manual-code-review-checkpoint-template.md`
9. `templates/code-assembly-verification-report-template.md`
10. `templates/code-assembly-traceability-matrix-template.md`
11. `reports/aos-farm-code-assembly-pipeline-contract-report.md`

## 8. Expected Step 4 Candidate Set
Total Step 4 expected commit candidate count: 17.

## 9. Risk Profile
- **Agent Proposed Risk Profile:** MEDIUM_RISK_GUIDED
- **Human Assigned Risk Profile:** PENDING_HUMAN_ASSIGNMENT

## 10. Explicitly Unauthorized Actions
Commit, push, release, production use, Spec Kit commands, CI workflow creation, validator implementation, runtime enforcement implementation, and modification of protected/canonical files are explicitly unauthorized.

## 11. Final Status
```yaml
FINAL_STATUS: AOS_FARM_109_BUILD_STEP_4_AUTHORIZATION_PREPARATION_COMPLETE
```
