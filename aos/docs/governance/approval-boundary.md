# Human Approval Boundary

AI agents operating under AOS do not have the authority to self-approve critical lifecycle events.

## When is Human Approval Required?
- Starting a new task execution.
- Changing a Risk Profile.
- Expanding the scope of an approved task.
- Modifying protected configuration files.
- Staging, committing, or pushing code.

## The Checkpoint Process
1. The agent prepares a Human Checkpoint artifact (`reports/human-checkpoints/...`).
2. The agent stops and waits.
3. The human reviews the checkpoint, marks it as `[x] APPROVED`, and saves the file.
4. The human instructs the agent to continue based on the approval.
