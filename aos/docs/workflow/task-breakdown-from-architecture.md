# Task Breakdown From Architecture

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

## Traceability Requirements

- origin_technical_assignment
- origin_architecture_brief
- origin_adr
- origin_pattern
- origin_stack_preset
- origin_unknown_resolution
- origin_conflict_resolution

## Safety Rules

- Without traceability, a task may be TASK_CANDIDATE_DRAFT.
- Without traceability, a task must not become APPROVED.
- This rule does not grant approval authority.
- Task breakdown may not proceed to queue review unless Architecture Validator has been run successfully against required architecture inputs and task breakdown traceability.
- Architecture Validator must be called before task breakdown is allowed to proceed to queue review.
- Validator NOT_RUN blocks progression.
- Validator PASS is required before queue review.
- Validator PASS ≠ approval.
- Validator PASS ≠ READY_FOR_EXECUTION.
- Validator PASS does not authorize execution, commit, push, or release.
- HUMAN_REVIEW_REQUIRED does not mean approval exists.

## Validation Status Checks

- Validator NOT_RUN -> VALIDATION_NOT_RUN_BLOCKED
- Validator PASS -> may proceed to human queue review, but does not create approval
- Validator HUMAN_REVIEW_REQUIRED -> blocks progression until human review
- Validator BLOCKED / UNKNOWN_BLOCKED / CONFLICT_BLOCKED -> blocks progression

## Architecture-to-Task Export Requirements

### Input and Traceability Requirements
- Task Breakdown **must reference architecture decision Evidence**.
- Task Breakdown **must reference human architecture checkpoint status**.
- Task Breakdown **must carry forward unresolved UNKNOWN**.

### Task Output Requirements
- Task Breakdown **must produce task candidates, not execution authorization**.
- Task Breakdown **must distinguish** between task types:
    - documentation task;
    - template task;
    - validator/script task;
    - implementation task;
    - dogfood task.
- Task Breakdown **may suggest Risk Profile but cannot assign it**.
- Task Breakdown **must not infer LOW_RISK_FAST**.
- Task Breakdown **must not create Task Brief if required architecture checkpoint is missing**.

### Fail-Closed Rules
- Missing architecture decision reference → `UNKNOWN_BLOCKED` or `HUMAN_REVIEW_REQUIRED`.
- Missing human checkpoint → `HUMAN_REVIEW_REQUIRED`.
- Unresolved UNKNOWN dropped → `UNKNOWN_BLOCKED`.
- Risk Profile needed but not assigned by human → `HUMAN_REVIEW_REQUIRED`.
- Protected/canonical change needed → `HUMAN_REVIEW_REQUIRED`.

### Required Output Boundary
- Task candidates ≠ Task Brief approval.
- Task Breakdown ≠ Build Step execution.
- Task Breakdown PASS ≠ human approval.
