# AOS-FARM.415 — Consumer-to-Runtime Handoff Contract Remediation Authorization Package

## 1. Task Metadata
- **Task ID:** AOS-FARM.415
- **Mode:** Authorization-preparation only
- **Target Component:** Consumer-to-Runtime Handoff Contract

## 2. Preflight Results
- **Branch:** dev
- **HEAD:** 3203fece89720ee68960b41e88bd4d343051b9f7
- **Origin Sync Status:** HEAD == origin/dev
- **Ahead/Behind:** 0 0
- **Status:** Required sources present. Several untracked and unstaged deleted files from previous test runs were observed and remain untouched.

## 3. Required Sources Read Confirmation
The following primary control sources have been read and their precedence rules are acknowledged:
1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## 4. Files Inspected
- `README.md`, `README.ru.md`, `AGENTS.md`
- `aos/README.md`, `aos/START_HERE.md`
- `aos/docs/workflow/first-session-guide.md`
- `aos/docs/workflow/problem-intake-workflow.md`, `aos/docs/workflow/technical-assignment-workflow.md`
- `aos/prompts/problem-intake.md`, `aos/prompts/technical-assignment-builder.md`
- `aos/templates/task-briefs/problem-intake-template.md`, `aos/templates/task-briefs/technical-assignment-template.md`
- `aos/examples/problem-intake-to-controlled-task/README.md`, `aos/tools/optional/problem-intake-runner/README.md`
- `agentos/pipelines/document_pipeline.py`, `agentos/pipelines/__init__.py`
- `tests/test_document_pipeline.py`
- `.github/` directory contents

## 5. Summary of Confirmed Bridge Gap
The consumer-facing Markdown workflow (`aos/`) and the runtime/code layer (`agentos/` and `tests/`) currently operate as disconnected environments. Specifically:
- It is unclear where Problem Intake output should be saved and how it feeds into Technical Assignment input.
- File naming conventions and locations for Technical Assignment outputs are undefined.
- The boundary of when a controlled task brief begins is not clearly documented.
- The role of `agentos/pipelines/document_pipeline.py` lacks clear definition as an optional local ingestion tool, confusing users on whether it is a mandatory part of the workflow.
- It is not explicitly stated what remains manual, optional, and what does not constitute execution or lifecycle approval.

## 6. Proposed Future Remediation Goal
Prepare an authorization package and human checkpoint for a future controlled remediation task that creates a clear Consumer-to-Runtime Handoff Contract. This will involve creating one new bridge document and making targeted updates to a small set of existing workflow docs without altering runtime code.

## 7. Proposed Exact Candidate Files
**Target Remediation Files:**
- `aos/docs/workflow/consumer-runtime-handoff.md` (New)
- `aos/docs/workflow/problem-intake-workflow.md`
- `aos/docs/workflow/technical-assignment-workflow.md`
- `aos/docs/workflow/first-session-guide.md`
- `aos/README.md`
- `aos/START_HERE.md`

**Optional Target:**
- `aos/tools/optional/problem-intake-runner/README.md` (Only if clearly necessary)

## 8. Proposed Bridge Contract Outline
**Layer Boundary:**
- `aos/` is the user-facing kit and the default starting path.
- `agentos/` contains implementation/runtime-side code slices and is not the first-start path.
- `agentos/pipelines/document_pipeline.py` is an optional local ingestion tool; it is **not** lifecycle or approval authority.

**Suggested Artifact Locations:**
- `aos/reports/problem-intake/<project-or-feature-name>.md`
- `aos/reports/technical-assignments/<project-or-feature-name>.md`
- `aos/reports/task-briefs/<project-or-feature-name>.md`

**Prompt-to-Prompt Handoff:**
Define exactly what the user should copy from Problem Intake into Technical Assignment. Minimum required fields:
- problem statement, target user, desired outcome, scope, non-goals, constraints, UNKNOWN items, risks, assumptions, success criteria, pending human decisions.

**Technical Assignment Output Boundary:**
Clarify that Technical Assignment output is a readiness/planning artifact. It is **not** approval, execution authorization, commit/push authorization, release authorization, or production use authorization.

## 9. Proposed Manual Happy Path
The expected manual file flow is:
1. Idea
2. Problem Intake prompt
3. Saved Problem Intake markdown output
4. Technical Assignment prompt
5. Saved Technical Assignment markdown output
6. Controlled task brief / execution package
7. Human review / approval checkpoint

## 10. Proposed Optional Runtime/Document-Pipeline Boundary
- `agentos/pipelines/document_pipeline.py` is an **optional local document ingestion helper** for Markdown/text/PDF/DOCX artifacts.
- It is **not**: a required runner, a required approval gate, a required lifecycle engine, production RAG, CI/CD authority, or an automatic execution mechanism.

## 11. Proposed Optional Runner Boundary
The optional runner:
- Is not required for normal user workflow.
- Does not approve anything, commit, push, or create release authority.
- Does not replace human review.
- Must preserve the invariant: `PASS ≠ approval`.

## 12. Proposed Safety Invariant Requirements
The bridge contract will explicitly preserve the following Always-On AOS invariants:
- `PASS ≠ approval`
- `Evidence ≠ approval`
- `CI PASS ≠ approval`
- `UNKNOWN ≠ OK`
- `NOT_RUN ≠ PASS`
- Human approval cannot be simulated.
- Scope must not expand without explicit human permission.
- Runner PASS ≠ approval.
- Validator PASS ≠ approval.
- Document ingestion success ≠ approval.
- Document parsed ≠ accepted.
- `ready_for_local_index` ≠ `ready_for_execution`.

## 13. Proposed Risk Profile
**MEDIUM_RISK_GUIDED**

## 14. Forbidden Operations
During the future remediation execution, the agent must **not**:
- Edit `README.md`, `README.ru.md`, `aos/prompts/*`, `aos/templates/*`.
- Edit `agentos/`, `tests/`.
- Edit or create `.github/workflows/*`.
- Edit protected/canonical sources (`00`, `01`, `02`).
- Activate runtime or CI, or create runner integrations.
- Run the implementation pipeline.
- Stage, commit, push, merge, tag, or release.
- Perform any destructive operations.

## 15. Expected Future Execution Report
The future execution task should generate a comprehensive report outlining the exact changes made to the candidate files, the validation of safety invariants within those changes, and confirmation that no forbidden files or processes were touched.

## 16. Next Task Recommendation
AOS-FARM.416 — Consumer-to-Runtime Handoff Contract Remediation Execution

## 17. Final Status
**AOS_FARM_415_CONSUMER_RUNTIME_HANDOFF_REMEDIATION_AUTHORIZATION_PREPARED**
