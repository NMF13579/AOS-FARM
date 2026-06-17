# AOS-FARM.TA-12 — Minimal Problem Intake Runner MVP Design

## 1. Current Baseline

Following the TA-11 gap classification and recovery planning, the current state of the Problem Intake package is defined as follows:

*   **methodology_status**: `ACTIVE_OPERATIONAL_METHOD`
*   **prompt_status**: `DRAFT_OPERATIONAL`
*   **runner_status**: `NOT_IMPLEMENTED`
*   **evidence_run_status**: `NOT_RUN`
*   **validation_status**: `FAIL` (due to keyword conflicts and missing environment dependencies)
*   **approval_status**: `NOT_APPROVED`
*   **automation_status**: `NOT_PROVEN`

---

## 2. MVP Boundary

The Minimal Problem Intake Runner MVP is designed as a **minimal local CLI script only**. 

The recommended future path for this script is:
`agentos/scripts/problem_intake_runner.py`

**Explicit Exclusions:**
To adhere to AOS safety invariants, the MVP is explicitly **not**:
*   a service;
*   a daemon;
*   a web application;
*   a state-machine engine;
*   a database-backed runtime;
*   an autonomous agent;
*   a production workflow;
*   a human approval substitute.

---

## 3. Proposed CLI Interface

The runner must expose a minimal command-line interface to prevent scope expansion and unintended automation loops. 

The proposed shape is:

```bash
python3 agentos/scripts/problem_intake_runner.py \
  --input <path-to-intake-input.md> \
  --run-id <run-id>
```

**Interface Constraints:**
*   No extraneous flags or configuration parameters should be introduced at the MVP stage. The system must operate only on the provided input and uniquely identifiable run ID.

---

## 4. Input Contract

The runner expects a Markdown file representing the raw intake notes, brief, or specification. 

**Required Sections:**
The input file must contain at least the following sections:
1.  problem statement
2.  target user
3.  current workflow
4.  desired outcome
5.  constraints
6.  known risks
7.  open questions

**Failure Semantics:**
Missing required fields **must not be treated as PASS**.
If required fields are missing, the runner must produce the following status in its output artifacts:
*   `draft_status`: `INCOMPLETE`
*   `validation_status`: `NEEDS_HUMAN_REVIEW`

---

## 5. Output Directory Contract

To maintain traceability and evidence isolation, each run gets its own dedicated directory.

**Directory Shape:**
```text
agentos/reports/problem-intake/<run_id>/
```

---

## 6. Required Output Artifacts

The runner must generate a minimum set of output artifacts representing the parsed and structured intake.

### 6.1. PROJECT_SPEC.draft.md
*   **Purpose**: To structure the raw intake into a baseline project specification draft.
*   **Required Sections**: User vision, target users, desired outcome, constraints, risks.
*   **Allowed Status Values**: `DRAFT_ONLY`, `INCOMPLETE`.
*   **Must Not Claim**: Implementation authorization, architectural finality, or PASS.

### 6.2. REQUIREMENTS.draft.md
*   **Purpose**: To list the extracted functional and non-functional requirements.
*   **Required Sections**: Core requirements, negative constraints.
*   **Allowed Status Values**: `DRAFT_ONLY`, `INCOMPLETE`.
*   **Must Not Claim**: Approval, completeness, or execution readiness.

### 6.3. problem-interview-report.md
*   **Purpose**: To document the extracted context and problem evidence.
*   **Required Sections**: Current workflow, problem statement, known risks, open questions.
*   **Allowed Status Values**: `DRAFT_ONLY`, `INCOMPLETE`.
*   **Must Not Claim**: Semantic validation of the problem or approval.

### 6.4. requirements-checklist-draft.md
*   **Purpose**: To provide a checklist for human review and gap analysis.
*   **Required Sections**: Verification items based on extracted constraints and requirements.
*   **Allowed Status Values**: `DRAFT_ONLY`, `INCOMPLETE`.
*   **Must Not Claim**: Checklist completion or human checkoff simulation.

### 6.5. problem-intake-run-report.md
*   **Purpose**: To provide an execution record for the CLI runner itself.
*   **Required Sections**: Run ID, input file used, generated files, missing fields (if any).
*   **Allowed Status Values**: `DRAFT_CREATED`, `INCOMPLETE`, `FAILED`.
*   **Must Not Claim**: Successful end-to-end TA creation, PASS, or approval.

---

## 7. Required Status Semantics

To prevent false confidence and align with AOS invariants, the following status semantics must be strictly enforced in all generated artifacts:

*   **run_status**: `DRAFT_CREATED` | `INCOMPLETE` | `FAILED`
*   **draft_status**: `DRAFT_ONLY` | `INCOMPLETE`
*   **validation_status**: `NOT_VALIDATED` | `BASIC_STRUCTURE_CHECKED` | `NEEDS_HUMAN_REVIEW`
*   **approval_status**: `NOT_APPROVED`
*   **automation_status**: `MVP_RUNNER_ONLY`
*   **production_status**: `NOT_PRODUCTION`

**Explicit Clarifications:**
*   `DRAFT_CREATED` is not `PASS`.
*   `BASIC_STRUCTURE_CHECKED` is not approval.
*   `NOT_RUN` is not `PASS`.
*   `NOT_APPROVED` cannot be changed by the runner.

---

## 8. Safety Rules

The MVP implementation must enforce the following safety rules:
*   no human approval simulation;
*   no `PASS` claim in generated artifacts;
*   no commit / push operations;
*   no modification of source methodology or prompt files;
*   no overwrite of previous run directories unless explicitly forced by a future separately authorized design;
*   fail closed on missing required input fields (generating incomplete statuses);
*   output artifacts must be explicitly marked as draft;
*   all generated files must contain `approval_status: NOT_APPROVED`.

---

## 9. Minimal Validation Design

The MVP handles basic structural verification, intentionally stopping before semantic evaluation.

**Allowed MVP validation:**
*   input file exists;
*   required sections detected in the input file;
*   output directory created successfully;
*   required artifacts created successfully;
*   required status fields present in generated artifacts;
*   no approval claim present in the generated output.

**Forbidden for MVP:**
*   semantic quality `PASS`;
*   production readiness `PASS`;
*   human approval inference;
*   roadmap mutation;
*   automatic implementation authorization.

---

## 10. Future Implementation Task Proposal

The recommended next step is to implement the runner strictly according to this design:

**AOS-FARM.TA-13 — Controlled Minimal Problem Intake Runner MVP Implementation**

*Note: TA-13 may implement only the design detailed in TA-12 after explicit human authorization.*

---

## 11. Non-Goals

This design document explicitly states that TA-12 does **not**:
*   implement the runner;
*   run the runner;
*   generate draft TA artifacts;
*   validate automation end-to-end;
*   approve production use;
*   commit or push anything.
