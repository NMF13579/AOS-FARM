# The First 30 Minutes

This timeline is designed for a non-programmer starting a new project from the AOS-FARM template.

## 0–5 Minutes: Verification
- Create your new repository from the AOS-FARM GitHub template and open it in your IDE.
- Open the `docs/user-guide/new-project-bootstrap.md` file and read it.
- **Goal**: Confirm to yourself that this is a *governed* framework, not an autonomous coding system. The AI will not write code until you tell it to and approve its plan.

## 5–10 Minutes: Definition
- Open `templates/project-bootstrap-checklist.md`.
- Fill in the blanks: Project Name, Problem Statement, Target User.
- Define your **MVP Boundary** (what you want to build) and **Explicit Non-Goals** (what you absolutely do not want the AI to build).
- **Goal**: Establish the constraints for the AI agent.

## 10–15 Minutes: Agent Introduction
- Open a new chat session with your AI agent (e.g., ChatGPT or Antigravity).
- Paste the contents of `templates/first-agent-session-template.md`.
- Tell the agent to act as your "Agent Tutor". 
- Ask it: *"What is the safest next step for this project?"*
- **Goal**: Ensure the agent reads the rules and understands its role as a tutor, not a rogue executor. **Do not request implementation yet.**

## 15–25 Minutes: Task Preparation
- Use the agent's advice and the `templates/first-task-brief-template.md` to prepare your first real task.
- This task should be something safe, like "Draft the PROJECT_SPEC" or "Write the Requirements Document".
- Identify where human approval is required.
- Identify the forbidden scope (e.g., "Do not write code, do not edit canonical files").
- **Goal**: Create a constrained, safe boundary for the agent's first actual work.

## 25–30 Minutes: Authorization Decision
- Review the Task Brief and the prepared Human Checkpoint (`templates/bootstrap-human-checkpoint-template.md`).
- Decide if you want to authorize execution.
- If you are not ready, leave the status as `PENDING` or `HUMAN_REVIEW_REQUIRED`. The agent will wait patiently.
- If you are ready, change the status to `APPROVED_FOR_EXECUTION` and tell the agent to begin.
- **Goal**: Exercise your authority as the Human Approver for the first time.
