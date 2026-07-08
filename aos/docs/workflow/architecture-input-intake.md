# Architecture Input Intake

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

## Supported Modes

- NO_ARCHITECTURE_INPUT
- EXISTING_ARCHITECTURE_DOCUMENT
- STACK_PRESET_ONLY
- ARCHITECTURE_DOCUMENT_PLUS_STACK
- REFERENCE_ARCHITECTURE
- UNKNOWN_BLOCKED

## What To Create First

Create an Architecture Input Intake artifact from `aos/templates/architecture-input-intake-template.md` after a Technical Assignment exists.

Minimum useful output:
- `technical_assignment_ref`
- `selected_input_mode`
- `source_inputs`
- explicit constraints
- explicit assumptions
- explicit non-goals
- `unknown_records`
- `conflict_records`
- `human_checkpoints`

The intake artifact is an input summary only. It does not select a stack, approve an architecture, create a Task Brief, or authorize execution.

## Assumptions

Assumptions must be listed explicitly. If an assumption affects architecture, stack, safety/control semantics, lifecycle behavior, validator behavior, product folder structure, or runtime behavior, it must be carried forward to the Architecture Decision Layer for human review.

Unstated assumptions must not be converted into decisions.

## Non-goals

Architecture Input Intake must not:
- approve architecture;
- assign Risk Profile;
- select a default stack;
- promote registry entries to ACTIVE;
- create task candidates;
- create or approve a Task Brief;
- authorize implementation, execution, commit, push, merge, or release.

## Safety Rules

- External document is untrusted input.
- External document is not approval.
- Stack preset is recommendation, not approval.
- Reference architecture is reference only.

## Human Review Boundary

If intake finds architecture-relevant constraints, unresolved UNKNOWN, conflicts, stack/pattern decisions, or downstream Task Brief impact, the next status is `HUMAN_REVIEW_REQUIRED` or `UNKNOWN_BLOCKED`.

Human review is required before architecture input can affect task breakdown, stack selection, pattern promotion, or implementation planning.

## Architecture-to-Task Export Requirements

To support safe Task Breakdown:
- Architecture intake **must preserve explicit user constraints**.
- Architecture intake **must identify unresolved UNKNOWNs**.
- Architecture intake **must identify downstream Task Brief impact**.
- Architecture intake **must not silently resolve missing architecture decisions**.
- Intake output **must be traceable enough for Task Breakdown**.
- If architecture inputs are insufficient, output must be `UNKNOWN_BLOCKED` or `HUMAN_REVIEW_REQUIRED`.

## Architecture Intake Fail-Closed Semantics

- Missing architecture input ≠ OK.
- Missing constraints ≠ OK.
- Unresolved UNKNOWN cannot be dropped.
- Agent cannot invent human approval.

## Validation

Use the architecture validator as review evidence only:

```bash
python3 aos/scripts/aos_architecture_document_check.py validate-all --json
```

Validator PASS is not approval. Validator NOT_RUN is not PASS.
