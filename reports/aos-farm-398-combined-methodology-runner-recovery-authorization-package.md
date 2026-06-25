# AOS-FARM-398 Combined Methodology and Runner Recovery Authorization Package

## Target Tasks
- **AOS-FARM.399** — Human Combined Methodology + Runner Execution Authorization
- **AOS-FARM.400** — Controlled Full Runbook-Level Methodology Recovery
- **AOS-FARM.401** — Controlled Optional Full Problem Intake Runner Recovery
- **AOS-FARM.402** — Combined Methodology + Runner Verification
- **AOS-FARM.403** — Combined Commit Authorization Preparation

## Context
AOS-FARM.397 attempted to recover the Problem Intake methodology but compressed the deep state-machine logic (Runbooks) into a highly simplified prompt. The user clarified that the full interview methodology (with step-by-step algorithms) is the core product value. Furthermore, the Python runner itself is valuable, provided it is deployed strictly as **optional tooling** that depends on the Markdown methodology, without gaining lifecycle/approval authority.

This package authorizes a combined recovery line. Commit and push are strictly blocked until the entire combined sequence (Methodology + Optional Runner) is implemented and verified.

## Mandatory Methodology + Runner Parity Matrix

| Old Source File | Old Mechanism | Old Operational Role | Target AOS File | Target Representation | Migration Decision | Rationale |
|---|---|---|---|---|---|---|
| `agentos/docs/methodology/.../00-overview-and-routing.md` | EXPRESS/FULL Routing | State switching | `aos/docs/methodology/problem-intake-methodology.md` | PRESERVE_FULL_TEXT_AS_MARKDOWN | PRESERVE_FULL_TEXT_AS_MARKDOWN | Core conceptual workflow. |
| `agentos/prompts/problem-intake-agent.md` | Strict interview state machine | LLM Agent constraints | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_PROTOCOL | PRESERVE_AS_PROMPT_PROTOCOL | Core conversational invariant. |
| `agentos/docs/methodology/.../runbooks/five-whys-runbook.md` | Iterative root-cause | Framework execution | `aos/docs/methodology/problem-intake/runbooks/five-whys-runbook.md` | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | Deep algorithmic product value. |
| `agentos/docs/methodology/.../runbooks/jtbd-runbook.md` | Job to be done extraction | Framework execution | `aos/docs/methodology/problem-intake/runbooks/jtbd-runbook.md` | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | Deep algorithmic product value. |
| `agentos/docs/methodology/.../runbooks/scenario-walkthrough-runbook.md` | Edge case discovery | Framework execution | `aos/docs/methodology/problem-intake/runbooks/scenario-walkthrough-runbook.md` | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | Deep algorithmic product value. |
| `agentos/docs/methodology/.../runbooks/entity-process-traversal-runbook.md` | Data/State flow mapping | Framework execution | `aos/docs/methodology/problem-intake/runbooks/entity-process-traversal-runbook.md` | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | PRESERVE_FULL_ALGORITHM_AS_RUNBOOK | Deep algorithmic product value. |
| `agentos/templates/project-brief.md` | Output capture | Data schema | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_CONTRACT | PRESERVE_AS_TEMPLATE_CONTRACT | Required structural output. |
| `agentos/scripts/problem_intake_runner.py` | Python state enforcement | LLM Orchestrator | `aos/tools/optional/problem-intake-runner/problem_intake_runner.py` | PRESERVE_AS_OPTIONAL_RUNNER_LOGIC | PRESERVE_AS_OPTIONAL_RUNNER_LOGIC | Optional helper. Must rely on Markdown runbooks. |
| `agentos/scripts/problem_intake_output_validator.py` | Output schema check | Validation | `aos/tools/optional/problem-intake-runner/problem_intake_validator.py` | PRESERVE_AS_OPTIONAL_VALIDATOR_CHECK | PRESERVE_AS_OPTIONAL_VALIDATOR_CHECK | Optional helper. |
| `agentos/reports/problem-intake/ta-25-fixtures/` | Test edge cases | TDD Fixtures | `aos/tools/optional/problem-intake-runner/fixtures/` | PRESERVE_AS_RUNNER_FIXTURE | PRESERVE_AS_RUNNER_FIXTURE | Ensures runner robustness. |

## Methodology / Runner Loss and Deferral Register
*(No product-relevant interview or technical assignment mechanism is scheduled for loss or deferral. All features will be mapped to either Markdown runbooks, the optional runner, or both.)*
- **REJECT_LEGACY_ONLY**: Historical execution logs (`agentos/reports/build-step-*`) are excluded.

## Exact Methodology Target File List (AOS-FARM.400)
- `aos/docs/methodology/problem-intake-methodology.md`
- `aos/docs/methodology/technical-assignment-methodology.md`
- `aos/docs/methodology/problem-intake/runbooks/express-mode-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/full-mode-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/entity-process-traversal-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/five-whys-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/jtbd-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/scenario-walkthrough-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/skip-handling-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/grey-zone-discovery-runbook.md`
- `aos/docs/methodology/problem-intake/runbooks/unknown-handling-runbook.md`
- `aos/docs/methodology/technical-assignment/runbooks/technical-assignment-routing-runbook.md`
- `aos/docs/methodology/technical-assignment/runbooks/scope-and-nongoals-runbook.md`
- `aos/docs/methodology/technical-assignment/runbooks/acceptance-criteria-runbook.md`
- `aos/docs/methodology/technical-assignment/runbooks/controlled-task-brief-handoff-runbook.md`
- `aos/prompts/problem-intake.md`
- `aos/prompts/technical-assignment-builder.md`
- `aos/templates/task-briefs/problem-intake-template.md`
- `aos/templates/task-briefs/technical-assignment-template.md`
- `aos/examples/problem-intake-to-controlled-task/README.md`

## Exact Optional Runner Target File List (AOS-FARM.401)
- `aos/tools/optional/problem-intake-runner/README.md`
- `aos/tools/optional/problem-intake-runner/problem_intake_runner.py`
- `aos/tools/optional/problem-intake-runner/problem_intake_validator.py`
- `aos/tools/optional/problem-intake-runner/runbooks-map.yaml`
- `aos/tools/optional/problem-intake-runner/fixtures/`

## Combined Execution Sequence
1. **AOS-FARM.399**: Human Checkpoint Authorization.
2. **AOS-FARM.400**: Reconstruct the deep Markdown-only methodology and runbooks.
3. **AOS-FARM.401**: Reconstruct the optional Python runner, wiring it to read from the Markdown runbooks.
4. **AOS-FARM.402**: Verify parity and safety. No push yet.
5. **AOS-FARM.403**: Generate commit/push authorization package for the entire feature set.

## Combined Verification Requirements (AOS-FARM.402)
- Must verify that Markdown runbooks match old logic.
- Must verify the Python runner is optional and requires no DB/RAG/vector.
- Must verify the runner has no git push/commit/lifecycle authority.
- Must verify the runner respects `PASS ≠ approval`.

## Commit/Push Boundary
**DO NOT COMMIT OR PUSH** until AOS-FARM.403 explicitly prepares and authorizes the combined commit package.

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**

## Status
- **Authorization**: PENDING
- **Final Status**: **AOS_FARM_398_COMBINED_METHODOLOGY_RUNNER_RECOVERY_AUTHORIZATION_PREPARED**
