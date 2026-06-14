```yaml
task_id: AOS-FARM.184
build_step: 9
build_step_name: Thin Validator Contract
mode: read_only_planning_authorization_prep
preconditions_checked: true
remote_baseline_closed: true
step_8_closed: true

proposed_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: false

batch_1_future_target_task: AOS-FARM.186
batch_1_execution_authorized_now: false
batch_1_commit_authorized_now: false
batch_1_push_authorized_now: false

future_execution_candidate_count: 7
future_execution_candidate_set_exact: true
```

# AOS-FARM.184: Build Step 9 Scope / Risk / Batch Plan

## Semantic Scope & Need
1. **Why Step 9 is needed after Step 8:** Step 8 formalized control gates, but we need a fast deterministic validator contract to begin enforcing correctness at lower levels before we write the actual validator logic.
2. **Why Step 9 is contract-only:** The contract sets the rules, invariants, and input/output definitions. Separating the contract from the implementation prevents conflating the goal with the code, reducing risks of false approvals.
3. **Why Step 10 remains separate:** Step 10 will contain the actual script/code implementation of the validator. Treating it as a separate step ensures that the contract is fully vetted and approved before any logic is built.
4. **Exact future file scope for AOS-FARM.186:**
   - `docs/governance/thin-validator-contract.md`
   - `docs/governance/thin-validator-checks-v1.md`
   - `templates/thin-validator-input-contract-template.md`
   - `templates/thin-validator-result-template.md`
   - `templates/thin-validator-finding-template.md`
   - `templates/thin-validator-execution-report-template.md`
   - `reports/aos-farm-186-thin-validator-contract-execution-report.md`
5. **Required gates:** Scope Gate, Evidence Gate, Human Review Gate, False PASS Gate, Lifecycle Mutation Gate, Protected/Canonical Gate.
6. **Safety invariants:** `PASS` ≠ approval, `Evidence` ≠ approval, `CI PASS` ≠ approval, `UNKNOWN` ≠ OK, `NOT_RUN` ≠ PASS, Human approval cannot be simulated, Readiness does not start next Build Step, Validator result ≠ human approval, Validator PASS ≠ commit/push/release authorization.
7. **BLOCKED conditions:** Missing inputs, invalid syntax, checks fail to execute, ambiguous check status, check timeout.
8. **Forbidden operations:** No implementation code, no CI workflow changes, no lifecycle mutations.
9. **Human authorization boundary:** The agent only prepares the plan. The Human Owner must authorize execution by updating the AOS-FARM.185 checkpoint.

## Contract Elements to Define
1. Thin Validator Contract.
2. Deterministic validator check list.
3. Required inputs.
4. Required outputs.
5. Allowed statuses.
6. BLOCKED states.
7. UNKNOWN_BLOCKED states.
8. Forbidden claims.
9. Evidence vs approval boundary.
10. Human checkpoint boundary.
11. Handoff to Step 10 implementation.
