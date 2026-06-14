# Governance Control Gates v1

## 1. Scope Gate
- **gate_id:** `GATE_01_SCOPE`
- **purpose:** Verify that the execution scope strictly matches the authorized scope.
- **required_inputs:** Execution plan, authorized file list.
- **checks:** Compare planned file modifications against the authorized file list.
- **pass_condition:** All modified files are in the authorized list.
- **blocked_condition:** Any file outside the authorized list is targeted for modification.
- **unknown_condition:** Authorized list is missing or unclear.
- **human_review_condition:** Scope expansion is requested.
- **forbidden_claims:** A `PASS` here is not an approval to execute.
- **evidence_required:** Diff comparison or explicit file list.

## 2. Evidence Gate
- **gate_id:** `GATE_02_EVIDENCE`
- **purpose:** Ensure that all required evidence of verification exists.
- **required_inputs:** Verification reports, logs.
- **checks:** Verify presence and non-emptiness of evidence artifacts.
- **pass_condition:** All required evidence artifacts exist.
- **blocked_condition:** Missing evidence artifacts.
- **unknown_condition:** Evidence format is unreadable.
- **human_review_condition:** Evidence evaluation requires human judgment.
- **forbidden_claims:** `Evidence` ≠ approval.
- **evidence_required:** Links to generated verification reports.

## 3. Human Review Gate
- **gate_id:** `GATE_03_HUMAN_REVIEW`
- **purpose:** Enforce the human checkpoint boundary.
- **required_inputs:** Human checkpoint file.
- **checks:** Verify the `checkpoint_status` and human-provided authorizations.
- **pass_condition:** `checkpoint_status` is explicitly set to an approved state by human.
- **blocked_condition:** `checkpoint_status` is `PENDING`, `BLOCKED`, or human authorization is missing.
- **unknown_condition:** Checkpoint file is unparseable or ambiguous.
- **human_review_condition:** Always requires human interaction.
- **forbidden_claims:** Human approval cannot be simulated.
- **evidence_required:** The human checkpoint file itself.

## 4. False PASS Gate
- **gate_id:** `GATE_04_FALSE_PASS`
- **purpose:** Detect and prevent agents from assuming `PASS` based on skipped checks or `UNKNOWN` states.
- **required_inputs:** Gate execution trace.
- **checks:** Ensure no `NOT_RUN` or `UNKNOWN` results were interpreted as `PASS`.
- **pass_condition:** All required checks have explicit `PASS` or `FAIL` results, and no forbidden interpretations are used.
- **blocked_condition:** `UNKNOWN` or `NOT_RUN` states are present.
- **unknown_condition:** Trace is incomplete.
- **human_review_condition:** Override requested for incomplete trace.
- **forbidden_claims:** `UNKNOWN` ≠ OK, `NOT_RUN` ≠ PASS.
- **evidence_required:** Gate execution trace log.

## 5. Lifecycle Mutation Gate
- **gate_id:** `GATE_05_LIFECYCLE_MUTATION`
- **purpose:** Control transitions between lifecycle phases (e.g., commit, push, release).
- **required_inputs:** Current state, proposed lifecycle mutation.
- **checks:** Verify explicit human authorization for the specific mutation type.
- **pass_condition:** Mutation is explicitly authorized (e.g., `commit_authorized: true`).
- **blocked_condition:** Mutation is proposed without authorization.
- **unknown_condition:** Target mutation state is undefined.
- **human_review_condition:** Authorization for mutation is required.
- **forbidden_claims:** Readiness does not start next Build Step.
- **evidence_required:** Lifecycle mutation authorization in checkpoint.

## 6. Protected/Canonical Gate
- **gate_id:** `GATE_06_PROTECTED_CANONICAL`
- **purpose:** Prevent unauthorized modifications to core protected rules and canonical sources.
- **required_inputs:** Target files, list of canonical sources.
- **checks:** Check if target files include any canonical sources.
- **pass_condition:** No canonical sources are targeted, or explicit human checkpoint for canonical modification exists.
- **blocked_condition:** Canonical sources targeted without explicit checkpoint.
- **unknown_condition:** Target file status is ambiguous.
- **human_review_condition:** Any change to canonical sources.
- **forbidden_claims:** Agent memory is NOT Source of Truth.
- **evidence_required:** Checkpoint explicitly authorizing canonical changes.
