# AOS-FARM.TA-11 — Problem Intake Automation Gap Classification & Recovery Plan

## 1. Current Status

Based on a thorough read-only audit of the repository, the active Git branch (`dev`), and execution checks of existing validator files, the status of the Problem Intake and Technical Assignment automation package is classified as follows:

| Semantics Field | Value | Rationale |
| :--- | :--- | :--- |
| **methodology_status** | `ACTIVE_OPERATIONAL_METHOD` | The methodology files in `agentos/docs/methodology/technical-assignment/` are labeled as active operational methods or components, but their instruction scope is limited to manual/human-guided intake and draft creation. |
| **prompt_status** | `DRAFT_OPERATIONAL` | The main prompt at [problem-intake-agent.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/prompts/problem-intake-agent.md) is marked as a draft operational prompt and is explicitly unauthorized for implementation, execution, or commits. |
| **executable_automation_status** | `UNAUTHORIZED` / `NOT_FOUND` | No executable runner script, CLI utility, state machine, or agent service is implemented to run the intake loop. |
| **evidence_run_status** | `NOT_RUN` | No evidence run or interview transcript exists showing a successful transition from interview to draft TA. |
| **validation_status** | `FAIL` | The existing validator [thin_validator.py](file:///Users/muhammed/Documents/GitHub/AOS-FARM/tools/validators/thin_validator.py) fails when checking the prompt file due to literal syntax matches (detecting UNKNOWN/OK and NOT_RUN/PASS rules as conflicts), and the other script [thin_validator.py](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/scripts/thin_validator.py) fails outright due to a missing `yaml` environment dependency. |
| **approval_status** | `UNAUTHORIZED` | Human approval for execution or automation runtime implementation has not been granted. |
| **final_status** | `TA_INTAKE_AUTOMATION_RECOVERY_PLAN_READY` | The audit is complete, and the recovery plan is ready for review. |

---

## 2. Existing Artifact Inventory

The existing package artifacts are classified into the following inventory categories:

*   **docs (Methodology & Architecture)**:
    *   [00-overview-and-routing.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/00-overview-and-routing.md)
    *   [01-human-methodology.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/01-human-methodology.md)
    *   [02-agent-contract.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/02-agent-contract.md)
    *   [03-data-discovery-and-access.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/03-data-discovery-and-access.md)
    *   [04-draft-artifact-templates.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/04-draft-artifact-templates.md)
    *   [05-safety-gates-and-statuses.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/05-safety-gates-and-statuses.md)
    *   [06-domain-extension-interface.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/06-domain-extension-interface.md)
    *   [07-consistency-checklist.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/07-consistency-checklist.md)
    *   [08-interview-depth-loop-and-entity-process-traversal.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/08-interview-depth-loop-and-entity-process-traversal.md)
    *   [09-adaptive-elicitation-method-selector.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/09-adaptive-elicitation-method-selector.md)
    *   [README.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/methodology/technical-assignment/README.md)
    *   `extensions/` (Otracle extensions for medical, construction, education, etc.)
    *   `runbooks/` (Modular elicitation methods: JTBD, Five Whys, Kano, etc.)
*   **prompts**:
    *   [problem-intake-agent.md](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/docs/prompts/problem-intake-agent.md)
*   **reports**:
    *   *None* relating to Problem Intake execution. (Other build step reports are present in `/reports` but none represent intake evidence runs).
*   **validators**:
    *   [tools/validators/thin_validator.py](file:///Users/muhammed/Documents/GitHub/AOS-FARM/tools/validators/thin_validator.py) (fails check on the prompt file due to literal keyword triggers).
    *   [agentos/scripts/thin_validator.py](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/scripts/thin_validator.py) (fails due to missing dependency).
*   **scripts**:
    *   [agentos/scripts/thin_validator.py](file:///Users/muhammed/Documents/GitHub/AOS-FARM/agentos/scripts/thin_validator.py)
    *   [scripts/validate-spec.sh](file:///Users/muhammed/Documents/GitHub/AOS-FARM/scripts/validate-spec.sh) (validates spec folder preconditions/frontmatter only).
*   **missing expected outputs**:
    *   `PROJECT_SPEC.draft.md` (unbuilt)
    *   `REQUIREMENTS.draft.md` (unbuilt)
    *   `problem-interview-report.md` (unbuilt)
    *   `requirements-checklist-draft.md` (unbuilt)
    *   `agentos/reports/problem-intake/` (directory does not exist)

---

## 3. Gap Register

| Gap ID | Description | Impact |
| :--- | :--- | :--- |
| **GAP-01** | **No executable runner / CLI / service / state machine** | There is no python/bash runner that executes the prompt or parses an interview conversation to output drafts. |
| **GAP-02** | **Prompt not active as operational loop** | The prompt remains an offline markdown instruction document only, with no runtime binding. |
| **GAP-03** | **No evidence run** | The repository lacks execution output or transcripts proving that a problem interview -> draft TA flow has been completed. |
| **GAP-04** | **Missing standard output artifacts** | `PROJECT_SPEC.draft.md`, `REQUIREMENTS.draft.md`, `problem-interview-report.md`, and `requirements-checklist-draft.md` are absent. |
| **GAP-05** | **Missing problem-intake reports directory** | The destination output directory `agentos/reports/problem-intake/` is missing. |
| **GAP-06** | **Contract file extension mismatch** | The package README and overview files refer to `02-agent-contract.yaml`, but only `02-agent-contract.md` (containing YAML blocks) exists. |
| **GAP-07** | **No end-to-end TA intake validator** | The validator scripts check frontmatter formatting or basic keyword flags, but do not validate whether the generated draft spec conforms to the agent contract structure. |
| **GAP-08** | **Validator dependency issue** | `agentos/scripts/thin_validator.py` crashes due to a missing `yaml` library dependency in the environment. |

---

## 4. Risk Assessment

*   **automation_claim_risk**: High. The README claims that the system is an "active/automated TA workflow," which can mislead auditors and users into thinking executable mechanisms are ready.
*   **false_pass_risk**: Medium. Validators might be bypassed or incorrectly report `PASS` on formatting while the actual operational pipeline is unverified.
*   **evidence_gap_risk**: High. Without a recorded evidence run of the interview and generated drafts, the system's correctness and practical safety constraints remain entirely unproven.
*   **parser_contract_risk**: Low-Medium. System integrations searching for `02-agent-contract.yaml` will crash because the file exists as `02-agent-contract.md`.
*   **validator_coverage_risk**: High. The validators fail to verify structural safety rules (e.g. ensuring `ready_for_execution: false` is preserved in drafts and that no stack selection is made).

---

## 5. Recovery Options

### Option A — Documentation-only honesty correction
*   **Purpose**: Update status labels and documentation to align with the current manual state.
*   **Scope**:
    *   Change README and overview wording to explicitly define the problem intake package as a **manual methodology** (using markdown prompts via human copy-paste).
    *   Fix the `02-agent-contract.yaml` vs `02-agent-contract.md` reference mismatch in documentation.
    *   Keep the system strictly manual. No executable code or CLI runtime loop will be written.

### Option B — Minimal executable intake runner MVP
*   **Purpose**: Implement a minimal, safe python execution CLI to run the intake loop and generate the required draft output artifacts.
*   **Scope**:
    *   Implement a minimal CLI script `agentos/scripts/problem_intake_runner.py` that takes a text-based interview transcript or conducts a mock CLI question-and-answer session.
    *   Generate mock/dry-run outputs: `PROJECT_SPEC.draft.md`, `REQUIREMENTS.draft.md`, `problem-interview-report.md`, and `requirements-checklist-draft.md`.
    *   Save outputs to `agentos/reports/problem-intake/`.
    *   Maintain strict boundaries: the runner only aggregates requirements into draft schemas; it does not approve execution, write code, or alter production state.

---

## 6. Recommended Path

We recommend **Option B (Minimal executable intake runner MVP)** combined with minor alignment updates from Option A (correcting file extension references in documents).

**Rationale**:
*   Without an executable runner and a corresponding evidence run, the system cannot prove automation readiness.
*   Implementing a minimal CLI-based Python runner remains within bounded, non-destructive limits. It does not select stacks, select database schemas, or override human check-gates, keeping it compliant with the core `AOS Core Control` invariants.
*   It directly resolves the missing directories, missing draft outputs, and validation gaps.

---

## 7. Proposed Next Tasks

1.  **TA-12: Minimal Problem Intake Runner MVP Design**
    *   Define the CLI interface, mock transcript input format, and parsing logic.
2.  **TA-13: Controlled Runner Implementation**
    *   Create `agentos/scripts/problem_intake_runner.py` without external complex dependencies (using standard Python libraries where possible).
3.  **TA-14: Example Intake Run Evidence**
    *   Execute the runner using a sample interview transcript to produce the four draft markdown artifacts. Save logs and outputs in `agentos/reports/problem-intake/`.
4.  **TA-15: End-to-End Intake Validator**
    *   Update `thin_validator.py` to check the generated draft specs against the contract rules (specifically ensuring safety fields are set to `false`).
5.  **TA-16: Document Honesty Alignment**
    *   Correct `02-agent-contract.yaml` references to `02-agent-contract.md` across the methodology files.

---

## 8. Non-Goals

*   This recovery plan does **not** implement the Python runner script.
*   It does **not** run any automated loops or validate runtime correctness in this turn.
*   It does **not** modify any prompts or existing validator files.
*   It does **not** approve any production deployments or stack selections.
