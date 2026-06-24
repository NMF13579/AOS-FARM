# AOS-FARM Core Loop Ready

## What This Means
The AOS-FARM repository has reached a **Core Loop Ready** state. It can now be used as a minimal public template for a first real consumer workflow. 
The governance control loop is active, meaning you can assign tasks, verify evidence, and safely execute changes under strict boundary conditions.

## What is NOT Authorized
- **Production Use:** Core Loop Ready does not mean production-ready.
- **Autonomous Runner:** The agent cannot execute without a human-in-the-loop. Runner autonomy is strictly disabled.
- **Self-Approval:** The agent cannot self-approve scope expansions, protected changes, commits, or pushes.
- **Destructive Operations:** Data deletion, tag moving, or force-pushing are strictly forbidden unless explicitly authorized by a separate human checkpoint.

## How to Start a New Controlled Task
1. Copy the `templates/first-controlled-task-brief-template.md` to define your task.
2. Provide the task brief to the agent.
3. Review the agent's plan and assign a Risk Profile in the template.
4. Authorize execution.

## Safety Invariants Reminder
- **PASS/Evidence/checks ≠ approval.** Just because tests pass or evidence is gathered does not grant approval to commit or push.
- **Commit/Push require Human Authorization.** Even for perfectly executed tasks, you must explicitly authorize the commit and push steps via human checkpoints.
