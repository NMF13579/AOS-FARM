# Bootstrap Agent Workflow

The AOS-FARM workflow relies on explicit separation of roles to ensure that AI agents never perform unauthorized actions.

## The Interaction Model

1. **User**: You. The sole authority. You initiate the session.
2. **Agent Tutor / GPT Controller**: The explanatory interface. You use this agent to understand the project, ask questions, and prepare Task Briefs.
3. **Executor Agent (e.g., Codex, IDE agent)**: The worker. This agent receives a Task Brief and implements the code or documentation strictly within the defined scope.
4. **Verification**: The Executor Agent verifies its own work against the rules and generates an Evidence report.
5. **Human Approval**: You read the Evidence report and explicitly authorize the next step (e.g., Commit).
6. **Commit**: The Executor Agent commits the code.
7. **Push**: You explicitly authorize the Push, and the Executor Agent pushes the code to the remote repository.

## Critical Invariants
- **Agent Tutor is not an approval authority.** It cannot grant permission for execution.
- **Executor agent is not an approval authority.** It cannot authorize its own commits.
- **Verification PASS ≠ approval.** A successful self-check only means the code runs; it doesn't mean it's allowed to be saved.
- **Commit authorization and push authorization are separate.** You must approve them independently.
