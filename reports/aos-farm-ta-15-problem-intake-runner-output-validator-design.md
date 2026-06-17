# AOS-FARM.TA-15 — Problem Intake Runner Output Validator Design

## 1. Current Evidence Baseline

Following the TA-14 example run, the current state of the Problem Intake automation is defined as:

*   **runner_status**: `IMPLEMENTED`
*   **example_run_status**: `EXECUTED`
*   **draft_artifacts_status**: `CREATED`
*   **validation_status**: `MANUAL_BASIC_STRUCTURE_CHECKED`
*   **approval_status**: `NOT_APPROVED`
*   **automation_status**: `MVP_RUNNER_EVIDENCE_CREATED`
*   **production_status**: `NOT_PRODUCTION`

**Explicit Clarification**: Automated output validation does not exist yet. The TA-14 verification was performed via manual CLI commands.

---

## 2. Validator Boundary

The output validator is designed as a **local CLI script only**. 

The recommended future script path is:
`agentos/scripts/problem_intake_output_validator.py`

**Explicit Exclusions:**
To adhere to AOS safety invariants, the validator must **not** be:
*   a service;
*   a daemon;
*   a web app;
*   a production approval engine;
*   a semantic quality judge;
*   a human approval substitute;
*   a roadmap mutation tool;
*   a commit / push gate by itself.

---

## 3. Proposed CLI Interface

The validator must expose a minimal command-line interface to prevent scope expansion.

**Proposed Shape:**
```bash
python3 agentos/scripts/problem_intake_output_validator.py \
  --run-dir agentos/reports/problem-intake/<run_id>
```

**Optional Allowed Flag:**
*   `--report reports/<validator-report-name>.md`

No additional flags are permitted unless strictly justified by safety constraints.

---

## 4. Required File Checks

The validator must verify the structural integrity of the runner's output.

**Required Files:**
The run directory must contain exactly these files:
*   `PROJECT_SPEC.draft.md`
*   `REQUIREMENTS.draft.md`
*   `problem-interview-report.md`
*   `requirements-checklist-draft.md`
*   `problem-intake-run-report.md`

**Failure Conditions:**
The validator must fail if:
*   any required file is missing;
*   any unexpected generated file exists in the run directory;
*   the run directory does not exist;
*   the run directory is not a directory.

---

## 5. Required Status Field Checks

The validator must verify that safe status invariants are present in all output artifacts.

**Generated Artifacts:**
Each generated artifact must contain exactly these values:
*   `artifact_status: DRAFT`
*   `approval_status: NOT_APPROVED`
*   `automation_status: MVP_RUNNER_ONLY`
*   `production_status: NOT_PRODUCTION`

**Run Report Artifact:**
The `problem-intake-run-report.md` must also contain valid permutations for run lifecycle states:
*   `run_status`: `DRAFT_CREATED` | `INCOMPLETE` | `FAILED`
*   `draft_status`: `DRAFT_ONLY` | `INCOMPLETE`
*   `validation_status`: `BASIC_STRUCTURE_CHECKED` | `NEEDS_HUMAN_REVIEW` | `NOT_VALIDATED`
*   `approval_status`: `NOT_APPROVED`

---

## 6. False Claim Detection

The validator must fail closed if generated output contains unsafe positive claims that simulate human authorization or completion.

**Unsafe Positive Claims (Must trigger validation failure):**
*   `PASS`
*   `APPROVED`
*   `PRODUCTION_READY`
*   `IMPLEMENTATION_AUTHORIZED`
*   `EXECUTION_AUTHORIZED`
*   `HUMAN_APPROVED`
*   `READY_FOR_RELEASE`

**Safe Negative Forms (Must be allowed):**
The validator must use word-boundary or exact-match parsing so that the following safe negative fields are not falsely flagged as unsafe:
*   `NOT_APPROVED`
*   `NOT_PRODUCTION`
*   `NOT_VALIDATED`
*   `NOT_RUN`

---

## 7. Validation Result Semantics

The validator must output explicit, scoped statuses that do not over-claim safety or approval.

**Allowed Validator Statuses:**
*   **validator_status**: `VALIDATION_COMPLETE` | `VALIDATION_FAILED` | `VALIDATION_ERROR`
*   **structure_status**: `STRUCTURE_CHECKED` | `STRUCTURE_INVALID`
*   **status_field_status**: `STATUS_FIELDS_CHECKED` | `STATUS_FIELDS_INVALID`
*   **false_claim_status**: `NO_UNSAFE_CLAIMS_FOUND` | `UNSAFE_CLAIMS_FOUND`
*   **approval_status**: `NOT_APPROVED`
*   **production_status**: `NOT_PRODUCTION`

**Explicit Boundaries:**
*   `VALIDATION_COMPLETE` is not human approval.
*   `STRUCTURE_CHECKED` is not semantic correctness.
*   `NO_UNSAFE_CLAIMS_FOUND` is not production readiness.
*   Validator success does not authorize commit, push, release, or implementation expansion.

---

## 8. Exit Code Design

The script must operate predictably in Unix environments with deterministic exit codes:
*   `0` = validation completed with no structural/status/false-claim failures
*   `1` = validation failed due to missing files, unexpected files, missing fields, or unsafe claims
*   `2` = validator usage/configuration error

---

## 9. Expected Validation Report Format

When executed (especially with the `--report` flag), the validator must generate a standardized report containing:

1.  **task metadata**: Run ID, timestamps, target directory.
2.  **run directory**: Target path analyzed.
3.  **required file inventory**: Verification checklist of expected files.
4.  **unexpected file inventory**: List of any extraneous files (should be empty).
5.  **status field check results**: Pass/fail table for required field presence.
6.  **false claim scan results**: Pass/fail summary of unsafe keyword detection.
7.  **final validator status**: The aggregate status code and explicit failure context if applicable.
8.  **limitations**: Standard disclaimer of validation boundaries.
9.  **recommended next task**: Clear recommendation for the next human or agent action.

---

## 10. Limitations

This design explicitly states that the validator **will not** verify:
*   semantic quality of the generated project spec;
*   business correctness;
*   product-market fit;
*   human approval;
*   production readiness;
*   completeness of real user requirements;
*   implementation readiness.

---

## 11. Proposed Next Task

The recommended next safe step is:

**AOS-FARM.TA-16 — Controlled Problem Intake Output Validator Implementation**

*Note: TA-16 may implement only the validator design from TA-15 after explicit authorization.*
