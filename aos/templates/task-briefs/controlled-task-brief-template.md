# Task Brief: [Task Name]

## Source Metadata
- **Source Technical Assignment:** [Link or SHA]
- **Source Task Breakdown:** [Link or SHA]
- **Source Task Queue Entry:** [Task ID / Link]

## Execution Context
- **Mode:** [e.g. code generation, audit, execution]
- **Repository:** [Repo Name]
- **Branch:** [Branch Name]
- **Risk Profile Assignment:** [e.g. MEDIUM_RISK_GUIDED - MUST be assigned by human, not proposed by agent]
- **Human Execution Authorization:** [Path / checkpoint / explicit decision record]

## Context & Goal
- **Context:** Provide background on why this task is being executed.
- **Goal:** Explicitly state the exact outcome required.

## Scope & Boundaries
- **Scope:** Broad definition of the task area.
- **Allowed Changes:** [Directories, files, or components allowed to change]
- **Forbidden Changes:** [Directories, files, or components NOT allowed to change]

## Implementation Details
- **Required Behavior / Content:** Detailed functional expectations.
- **Non-Goals:** What explicitly NOT to do.
- **UNKNOWN/BLOCKED Handling:** How the agent should respond if something is missing or unclear (default: STOP and ask human).

## Verification & Output
- **Validation:** Specific commands, tests, or checks to run to prove it works. (Validation plan ≠ validation PASS).
- **Evidence Requirements:** Artifacts, diffs, or logs to provide. (Evidence requirements ≠ collected Evidence).
- **Expected Final Report:** What the final agent response should contain.
- **Evidence Review Target:** [Where the human will review the execution result]

## Final Boundary Rule
- **Execution readiness ≠ execution authorization.**
- **proposed Risk Profile ≠ human-assigned Risk Profile.**
- **Human execution authorization is required before starting this task.**
- Required lifecycle limits (e.g. no commit/push, no destructive operations).
- Commit authorization remains separate.
- Push authorization remains separate.
