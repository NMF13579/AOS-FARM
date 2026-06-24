# Execution Result Verification Loop

## Execution Result Report
When an executor agent finishes a task, it generates a report summarizing its actions. However, the system does not automatically accept this report. It must be verified.

## Verification Inputs
Verification requires:
- The execution result report.
- The original Task Brief.
- The `00`, `01`, `02` canonical sources.

## Verification Checks
The verifier checks:
- **Scope Compliance**: Did the agent only touch allowed files?
- **Forbidden Operation Check**: Were any destructive operations performed? Were canonical files touched?
- **Evidence Check**: Did the agent provide evidence of its claims?
- **UNKNOWN / NOT_RUN Check**: Any remaining UNKNOWN or NOT_RUN statuses must be explicitly logged. They are NOT converted to PASS.

## Critical Verification Boundaries
- **Verification PASS does not authorize commit.** It only means the execution followed the rules.
- **Verification PASS does not authorize push.**
- **Evidence does not authorize commit or push.**

## Human Review Boundary
After verification, the human is presented with the `post-execution-verification-template.md` output. The human reads the warnings and blocking issues, and decides whether to authorize the Commit.
