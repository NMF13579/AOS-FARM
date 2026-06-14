# AOS-FARM.175: Build Step 8 Scope / Risk / Batch Plan

## 1. Goal
Prepare a bounded Batch 1 for Governance / Control Module v1. This step defines the scope and risk profile but does not perform any execution.

## 2. Batch 1 Candidate Scope
The following exact files are proposed for creation/modification in Batch 1:
- `docs/governance/control-module-v1.md`
- `docs/governance/control-gates-v1.md`
- `templates/control-module-v1-checklist-template.md`
- `templates/control-gate-result-template.md`
- `templates/control-module-v1-execution-report-template.md`
- `templates/control-module-v1-human-review-template.md`
- `reports/aos-farm-177-control-module-v1-execution-report.md`

## 3. Proposed Risk Profile
**Proposed Risk Profile:** `HIGH_RISK_PROTECTED`

**Reasoning:**
Step 8 touches upon the Governance / Control Module authority, PASS/Evidence/approval semantics, human review gate, protected/canonical gate, and lifecycle mutation gate. Due to the foundational safety impact of these definitions, a high-risk protected profile is required.
Important: The agent can only propose a Risk Profile. The Human must assign the Risk Profile in the checkpoint.

## 4. Execution Restrictions for Step 8
- No runtime enforcement
- No validator implementation
- No CI workflow creation
- No Spec Kit command definitions
- No branch protection changes
- No release or production use
- No auto-approval or simulated human approval
- No protected/canonical source changes without explicit checkpoint
- No destructive operations
