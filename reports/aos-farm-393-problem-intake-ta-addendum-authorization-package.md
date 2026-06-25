# AOS-FARM-393 Problem Intake and Technical Assignment Consumer Kit Addendum Authorization Package

## Target Task
AOS-FARM.395 — Controlled Problem Intake and Technical Assignment Consumer Kit Addendum

## Old Source Analysis
AOS-FARM.392 identified that the top-of-funnel scoping workflow ("Problem Intake" and "Technical Assignment") was not migrated to the Consumer Kit (`aos/`). 
Currently, the old methodology relies on Python runners (`problem_intake_runner.py`) and specific internal prompts (`problem-intake-agent.md`) located in `agentos/`.
The old TA methodology (`agentos/docs/methodology/technical-assignment/`) is conceptually valuable but too deeply coupled with internal AOS-FARM development structures.

## Scope of Addendum
This addendum aims to introduce the Problem Intake and Technical Assignment workflows into the Consumer Kit using a strictly **Markdown-only approach** (no active Python scripts by default). It will cover:
1. **Problem Intake**: A workflow and prompt to extract user pain points, goals, constraints, and success criteria without jumping to implementation.
2. **Technical Assignment**: Translating the intake into a rigorous scope, non-goals, and acceptance criteria boundary.
3. **Bridge**: Explaining how these feed directly into the execution phase (Controlled Task Briefs).

## Out-of-Scope (Deferred)
The following old runtime/runner/validator files are strictly out-of-scope for the Consumer Kit default installation and must NOT be migrated or copied:
- `agentos/scripts/problem_intake_runner.py` -> **DEFER_RUNTIME**
- `agentos/scripts/problem_intake_output_validator.py` -> **DEFER_RUNTIME**

## Target Addendum File List & Classifications

| Target Path | Classification | Purpose |
|---|---|---|
| `aos/docs/workflow/problem-intake-workflow.md` | **NEW** | Documentation explaining how to perform Problem Intake. |
| `aos/docs/workflow/technical-assignment-workflow.md` | **NEW** | Documentation explaining how to build a Technical Assignment. |
| `aos/templates/task-briefs/problem-intake-template.md` | **NEW** | Template for structuring the output of a problem interview. |
| `aos/templates/task-briefs/technical-assignment-template.md` | **NEW** | Template for defining the strict technical bounds of the work. |
| `aos/prompts/problem-intake.md` | **REWRITE** | Consumer-facing prompt to initialize an agent for problem interviewing. |
| `aos/prompts/technical-assignment-builder.md` | **NEW** | Consumer-facing prompt to convert intake data into a technical assignment. |
| `aos/examples/problem-intake-to-controlled-task/README.md` | **NEW** | An end-to-end example showing the flow from raw idea to execution brief. |

*Note: All old `agentos/` files remain **DO_NOT_CHANGE**.*

## Safety Semantics and Constraints
The newly authored files must adhere to the Minimal Safety Floor:
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Scope must not expand without explicit human permission.
- Destructive operations require human authorization.

**Crucially, the addendum must NOT introduce or mandate any Python runner, validator, CLI, CI, DB, RAG, vector store, Spec Kit, or production runtime.**

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**
*(Reasoning: Introduces core methodology into the public Consumer Kit; requires precise adherence to no-runner constraints.)*

## Status
- **Authorization**: PENDING
- **Final Status**: **AOS_FARM_393_PROBLEM_INTAKE_TA_ADDENDUM_AUTHORIZATION_PREPARED**
