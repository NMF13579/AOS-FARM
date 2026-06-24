# First Consumer Workflow

This guide outlines a concrete, end-to-end workflow for executing your first task using AOS-FARM.

## The Workflow Steps

1. **Project Idea:** You have an idea for a feature or documentation update.
2. **Create Scoped Task Brief:** You fill out `templates/first-controlled-task-brief-template.md`, defining exactly what needs to be done and what is strictly forbidden.
3. **Agent Prepares Plan:** You hand the brief to the AI Agent. The agent reads the canonical rules and prepares a plan without making any changes.
4. **Human Assigns Risk Profile & Approval:** You review the plan. If acceptable, you assign a Risk Profile (e.g., `LOW_RISK_FAST` or `MEDIUM_RISK_GUIDED`) and explicitly authorize execution in the template.
5. **Agent Executes Bounded Work:** The agent performs the authorized work, remaining strictly within the allowed file scope.
6. **Verification Report Created:** The agent creates a verification report proving the task was completed safely and correctly.
7. **Human Authorizes Commit:** You review the evidence. If correct, you update a DRAFT Human Checkpoint to `APPROVED_FOR_COMMIT`.
8. **Agent Commits:** The agent stages and commits only the authorized files.
9. **Human Authorizes Push:** You update the next Human Checkpoint to `APPROVED_FOR_PUSH`.
10. **Agent Pushes:** The agent pushes the changes to the remote repository.

This human-in-the-loop mechanism guarantees safety and prevents unauthorized scope expansion.
