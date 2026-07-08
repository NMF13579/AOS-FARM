# Architecture Decision Layer

This document does not grant approval.
This document does not authorize execution.
This document does not authorize commit.
This document does not authorize push.
This document does not authorize release.
Human approval cannot be simulated.
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.

## Workflow Description

1. Technical Assignment
2. Architecture Input Intake
3. Architecture Decision Layer
4. Architecture Readiness Gate
5. Task Breakdown
6. Task Candidate Queue

## Decision Question

Every Architecture Decision Layer artifact must state the decision question it is answering. Example:

```text
Which architecture option should be carried forward as candidate evidence for human review, given the Technical Assignment constraints and unresolved UNKNOWNs?
```

The question frames review. It does not authorize implementation.

## Options

List all material options considered, including:
- candidate architecture patterns;
- candidate stack presets;
- no-architecture-input path, if applicable;
- defer / UNKNOWN_BLOCKED option;
- rejected options.

Each option must preserve traceability to source constraints, assumptions, risks, UNKNOWNs, and conflicts.

## Recommended Option

The agent may recommend a candidate option for human review.

Recommendation status must remain candidate-only until a human checkpoint records a decision.
Recommendation confidence is evidence only. It is not approval, Risk Profile assignment, or execution authorization.

## Rejected Options

Rejected options must record the reason for rejection, the evidence used, and any unresolved UNKNOWN.

Agent rejection is review evidence only. It does not create lifecycle authority unless a human checkpoint explicitly adopts the decision.

## Approval Boundary

The Architecture Decision Layer may produce architecture decision Evidence, but it must stop at human review. It must not convert readiness, recommendation, validator PASS, or Evidence into approval.

Use:
- `aos/docs/architecture/review/architecture-decision-evidence-packet.md`
- `aos/docs/architecture/review/human-architecture-checkpoint-template.md`

before architecture decisions affect task breakdown, stack selection, pattern promotion, or implementation planning.

## Safety Rules

- Architecture readiness is not approval.
- READY_FOR_TASK_BREAKDOWN ≠ READY_FOR_EXECUTION.
- Agent inference never has authority.
- Architecture Validator must be called before task breakdown is allowed to proceed to queue review.
- Validator NOT_RUN blocks progression.
- Validator PASS is required before queue review.
- Validator PASS ≠ approval.
- Validator PASS ≠ READY_FOR_EXECUTION.
- Validator PASS does not authorize execution, commit, push, or release.
- HUMAN_REVIEW_REQUIRED does not mean approval exists.

### Architecture-to-Task Export Safety Rules

- Architecture Decision Layer may produce architecture decision Evidence.
- Architecture decision Evidence is not approval.
- Architecture decision Evidence must list: selected option, rejected alternatives, unresolved UNKNOWN, downstream task impact, and required human checkpoint.
- Architecture Decision Layer must not authorize Task Brief creation by itself.
- Human checkpoint is required before downstream canonical/task conversion when protected/canonical scope is affected.

#### Required Statuses

**`architecture_decision_evidence_status`:**
- `DRAFT`
- `READY_FOR_HUMAN_REVIEW`
- `HUMAN_REVIEW_REQUIRED`
- `UNKNOWN_BLOCKED`
- `BLOCKED`

**`not_allowed_as_approval`:**
- `PASS`
- `Evidence`
- `READY_FOR_HUMAN_REVIEW`
- `validator PASS`
- `CI PASS`

## Architecture Validator (AOS-FARM.618 MVP)

AOS-FARM.618 adds an MVP validator for Architecture Brief, Mini ADR, Pattern Fit Matrix, architecture registries, and task breakdown traceability.

The validator is manually or agent-invoked by explicit command.
It is not a root canonical lifecycle gate.
It is not CI integration.
It is not release authorization.
It is not approval.

### CLI Commands

```bash
python3 aos/scripts/aos_architecture_document_check.py --help
python3 aos/scripts/aos_architecture_document_check.py brief --file <path>
python3 aos/scripts/aos_architecture_document_check.py adr --file <path>
python3 aos/scripts/aos_architecture_document_check.py matrix --file <path>
python3 aos/scripts/aos_architecture_document_check.py registry --validate
python3 aos/scripts/aos_architecture_document_check.py registry --file <path>
python3 aos/scripts/aos_architecture_document_check.py task-breakdown --file <path>
```

### Status Meanings

- PASS -> required validation result, but not approval
- BLOCKED -> progression blocked
- UNKNOWN_BLOCKED -> UNKNOWN not resolved or required UNKNOWN handling missing
- CONFLICT_BLOCKED -> conflict not resolved or required conflict handling missing
- VALIDATION_NOT_RUN_BLOCKED -> validator has not been run before queue review
- HUMAN_REVIEW_REQUIRED -> human review required; not approval
- CLI_USAGE_ERROR -> command usage error

### Exit Code Semantics

- 0 = PASS
- 1 = BLOCKED / UNKNOWN_BLOCKED / CONFLICT_BLOCKED / VALIDATION_NOT_RUN_BLOCKED / HUMAN_REVIEW_REQUIRED
- 2 = CLI_USAGE_ERROR

## Stack Choice Map reference
When stack questions arise during Architecture Fixed Interview or architecture decision review, use:
- `aos/docs/architecture/stack-choice-map.md`
This reference explains stack elements in plain language.
Stack Choice Map is not approval.
Stack Choice Map does not select a default stack.
Stack Choice Map does not authorize implementation.
Human review is required before any stack preset becomes ACTIVE or default.
