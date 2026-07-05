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
