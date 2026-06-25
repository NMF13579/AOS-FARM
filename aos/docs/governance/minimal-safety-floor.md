# Minimal Safety Floor

AOS operates on a strict set of safety invariant rules that cannot be overridden by AI agents.

## Core Rules
- **PASS ≠ approval**: A successful test or validation does not equal human authorization.
- **Evidence ≠ approval**: Generating an evidence report does not authorize moving forward.
- **CI PASS ≠ approval**: Continuous integration checks passing does not replace explicit human checkpoints.
- **UNKNOWN ≠ OK**: If a state cannot be determined, the agent must fail closed.
- **NOT_RUN ≠ PASS**: A skipped check is considered a failure, not a success.
- **No Simulated Approval**: Agents are strictly forbidden from writing "Approved by Human" without a genuine human action.
- **Explicit Authorization Required**: Commit, push, merge, release, and destructive operations require an explicit human checkpoint.
