# Bootstrap Agent Workflow

The AOS-FARM workflow relies on explicit separation of roles to ensure that AI agents never perform unauthorized actions.

## The Interaction Model

1. **User (You)**: The sole authority. You initiate the session and approve all critical actions.
2. **Agent Tutor**: The explanatory interface. You use this agent to understand the project, ask questions, and prepare Task Briefs (see [Agent Tutor Mode](agent-tutor-mode.md)).
3. **Thin Task Queue Helper**: A lightweight script or process that performs a dry-run check on your planned task. It verifies structure and detects missing approvals before you pass the task to an executor.
4. **Executor Agent (e.g., Codex, IDE agent)**: The worker. This agent receives a validated Task Brief and implements the code or documentation strictly within the defined scope.
5. **Verification**: The Executor Agent verifies its own work against the rules and generates an Evidence report.
6. **Human Commit Approval**: You read the Evidence report and explicitly authorize the Commit via a Human Checkpoint.
7. **Human Push Approval**: You explicitly authorize the Push in a separate step, allowing the Executor to push the code to the remote repository.

## The First-User Journey (How it fits together)
When you are ready to build a new feature or stage, follow this cycle:
1. Start a conversation with the **Agent Tutor** to plan your task.
2. Have the Tutor draft the task and place it in the **Manual Task Queue**.
3. Use the **Thin Helper** to dry-run the task.
4. Once safe, hand off the task to the **Executor Agent**.
5. Wait for the Executor to finish and produce the Verification Report.
6. Explicitly grant **Commit Authorization** and **Push Authorization**.

*(For a high-level overview, return to the [User Guide README](README.md))*

## Critical Invariants
- **Agent Tutor is not an approval authority.** It cannot grant permission for execution.
- **Thin Helper is not a runner.** It only performs read-only validations; it cannot execute tasks autonomously.
- **Executor agent is not an approval authority.** It cannot authorize its own commits.
- **Verification PASS ≠ approval.** A successful self-check only means the code runs; it doesn't mean it's allowed to be saved.
- **Commit authorization and push authorization are separate.** You must approve them independently.
