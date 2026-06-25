# AOS-FARM-396 Full Problem Intake and Technical Assignment Methodology Recovery Authorization Package

## Target Task
AOS-FARM.397 — Controlled Full Problem Intake and Technical Assignment Methodology Recovery Rewrite

## Context
AOS-FARM.395 introduced a shallow, highly simplified version of the Problem Intake and Technical Assignment workflow into the Consumer Kit. However, the original methodology in `agentos/` contained significant product value (EXPRESS/FULL modes, adaptive depth, specific elicitation frameworks like Five Whys/JTBD) that must be preserved. The goal is to fully recover this methodology in a Markdown-only, consumer-facing format without reintroducing the legacy Python runners.

## Mandatory Methodology Coverage Matrix

| Old Methodology Feature | Old Source Path | Product Value | Target AOS File | Migration Decision | Rationale |
|---|---|---|---|---|---|
| EXPRESS mode | `agentos/docs/methodology/...` | Lean scoping for simple tasks | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_BEHAVIOR | Must be handled natively by the prompt logic. |
| FULL mode | `agentos/docs/methodology/...` | Deep scoping for sensitive/complex tasks | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_BEHAVIOR | Must be handled natively by the prompt logic. |
| Mode selection | `agentos/docs/methodology/...` | Routes user appropriately | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_BEHAVIOR | Agent must ask user at session start. |
| Escalation from EXPRESS to FULL | `agentos/docs/methodology/...` | Safety net for unexpected complexity | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_BEHAVIOR | Agent must suggest escalation if risks appear. |
| One-question-at-a-time | `agentos/prompts/problem-intake-agent.md` | Prevents user overwhelm | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_BEHAVIOR | Core conversational invariant. |
| Adaptive follow-up | `agentos/prompts/problem-intake-agent.md` | Dynamic context extraction | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_BEHAVIOR | Requires LLM to probe short answers. |
| Entity Process Traversal | `agentos/docs/methodology/.../runbooks/` | System mapping | `aos/docs/methodology/problem-intake-methodology.md` | PRESERVE_IN_MARKDOWN | Complex framework best documented as reference. |
| JTBD | `agentos/docs/methodology/.../runbooks/` | Value mapping | `aos/docs/methodology/problem-intake-methodology.md` | PRESERVE_IN_MARKDOWN | Complex framework best documented as reference. |
| Five Whys | `agentos/docs/methodology/.../runbooks/` | Root cause discovery | `aos/docs/methodology/problem-intake-methodology.md` | PRESERVE_IN_MARKDOWN | Complex framework best documented as reference. |
| Scenario Walkthrough | `agentos/docs/methodology/.../runbooks/` | Edge case discovery | `aos/docs/methodology/problem-intake-methodology.md` | PRESERVE_IN_MARKDOWN | Complex framework best documented as reference. |
| Skip handling | `agentos/prompts/problem-intake-agent.md` | Non-blocking flow | `aos/prompts/problem-intake.md` | PRESERVE_AS_PROMPT_BEHAVIOR | User can skip, but gaps are marked as warnings. |
| Grey-zone discovery | `agentos/docs/methodology/...` | Risk mitigation | `aos/docs/methodology/technical-assignment-methodology.md` | PRESERVE_IN_MARKDOWN | Core part of TA formulation. |
| Contradiction capture | `agentos/prompts/problem-intake-agent.md` | Resolves conflicting reqs | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Assumptions capture | `agentos/prompts/problem-intake-agent.md` | Highlights unverified facts | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| UNKNOWN capture | `agentos/prompts/problem-intake-agent.md` | Safety boundary | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Risk capture | `agentos/docs/methodology/...` | Safety boundary | `aos/templates/task-briefs/technical-assignment-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Non-goals capture | `agentos/docs/methodology/...` | Scope limitation | `aos/templates/task-briefs/technical-assignment-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Success criteria capture | `agentos/docs/methodology/...` | Definition of Done | `aos/templates/task-briefs/technical-assignment-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Current workflow mapping | `agentos/docs/methodology/...` | Baseline context | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Intended users / actors | `agentos/docs/methodology/...` | Role mapping | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Stakeholder mapping | `agentos/docs/methodology/...` | Impact mapping | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Constraints | `agentos/docs/methodology/...` | Hard bounds | `aos/templates/task-briefs/problem-intake-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Evidence | `agentos/docs/methodology/...` | Verifiability | `aos/templates/task-briefs/technical-assignment-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| Open decisions | `agentos/docs/methodology/...` | Defers design | `aos/templates/task-briefs/technical-assignment-template.md` | PRESERVE_AS_TEMPLATE_FIELD | Explicit artifact field. |
| TA routing | `agentos/docs/methodology/...` | Transition logic | `aos/docs/methodology/technical-assignment-methodology.md` | PRESERVE_IN_MARKDOWN | Logic for builder. |
| TA readiness vs approval | `agentos/docs/methodology/...` | Safety invariant | `aos/docs/workflow/technical-assignment-workflow.md` | PRESERVE_IN_MARKDOWN | Explicit boundary note. |

## Methodology Loss / Deferral Register
- `agentos/scripts/problem_intake_runner.py` -> **DEFER_RUNTIME**: Active execution conflicts with markdown-only consumer kit.
- `agentos/scripts/problem_intake_output_validator.py` -> **DEFER_RUNTIME**: Active execution conflicts with markdown-only consumer kit.

## Target File List for AOS-FARM.397
**Rewrite Existing Files (Deepen context):**
- `aos/docs/workflow/problem-intake-workflow.md`
- `aos/docs/workflow/technical-assignment-workflow.md`
- `aos/templates/task-briefs/problem-intake-template.md`
- `aos/templates/task-briefs/technical-assignment-template.md`
- `aos/prompts/problem-intake.md`
- `aos/prompts/technical-assignment-builder.md`
- `aos/examples/problem-intake-to-controlled-task/README.md`

**Create New Files (Methodology Reference):**
- `aos/docs/methodology/problem-intake-methodology.md`
- `aos/docs/methodology/technical-assignment-methodology.md`

## Safety Semantics and Constraints
The rewrite must explicitly preserve:
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Scope must not expand without explicit human permission.
- No Python runner or validator required by default.

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**

## Status
- **Authorization**: PENDING
- **Final Status**: **AOS_FARM_396_FULL_PROBLEM_INTAKE_TA_METHODOLOGY_RECOVERY_AUTHORIZATION_PREPARED**
