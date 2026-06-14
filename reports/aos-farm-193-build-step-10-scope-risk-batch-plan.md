# AOS-FARM.193: Build Step 10 Scope / Risk / Batch Plan

## 1. Goal
Prepare a bounded Batch 1 for the Thin Validator Implementation (Build Step 10). This step defines the scope and risk profile but does not perform any execution or create validator code yet.

## 2. Batch 1 Candidate Scope
The following exact files are proposed for creation in Batch 1 (AOS-FARM.195):
- `tools/validators/thin_validator.py`
- `tests/fixtures/thin-validator/pass/minimal-valid-report.md`
- `tests/fixtures/thin-validator/fail/fake-approval-claim.md`
- `tests/fixtures/thin-validator/fail/unknown-ok-conflict.md`
- `tests/fixtures/thin-validator/fail/not-run-pass-conflict.md`
- `tests/fixtures/thin-validator/fail/missing-required-field.md`
- `reports/aos-farm-195-thin-validator-implementation-execution-report.md`
- `reports/aos-farm-195-thin-validator-smoke-test-output.md`

## 3. Proposed Risk Profile
**Proposed Risk Profile:** `HIGH_RISK_PROTECTED`

**Reasoning:**
Step 10 creates the first validator behavior. Validator behavior is inextricably linked to PASS semantics, Evidence semantics, approval boundaries, and false PASS prevention. It must be highly protected.
*Note: The agent can only propose a Risk Profile. The Human must assign the Risk Profile in the checkpoint.*

## 4. Execution Restrictions for Step 10
- One thin validator only (no broad script suite).
- Python stdlib only.
- Read-only input validation (no auto-fix, no repo mutation).
- No git commands or network calls.
- Deterministic exit codes (0 = PASS, 1 = FAIL/BLOCKED, 2 = Error).
- No runtime enforcement or CI workflow changes.
- No branch protection changes or auto-approval.
- No auto-commit or auto-push without explicit checkpoint.
- No Spec Kit commands or destructive operations.
