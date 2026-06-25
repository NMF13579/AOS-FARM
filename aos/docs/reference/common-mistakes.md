# Common Mistakes & Failure Modes

## 1. Simulating Human Approval
**Mistake**: The agent fills out the `[x] APPROVED` checkbox itself to bypass a wait state.
**Correction**: The human must explicitly instruct the agent to stop, and the human must physically edit the file.

## 2. Unapproved Scope Creep
**Mistake**: While fixing a bug, the agent decides to refactor an unrelated file without authorization.
**Correction**: The agent must strictly adhere to the file constraints in the task brief.

## 3. Treating "No Errors" as Approval
**Mistake**: The agent runs a build script, sees no errors, and proceeds to commit.
**Correction**: Remember the rule: `PASS ≠ approval`. The agent must request a human checkpoint before committing.
