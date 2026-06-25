# Example: From Problem Intake to Controlled Task

This example demonstrates the complete "Top-of-Funnel" workflow in AOS, utilizing the full methodology depth.

## Step 1: Problem Intake
The user initializes an AI agent using `aos/prompts/problem-intake.md`.
- **Mode Selection**: The user selects `FULL` mode because this affects user data.
- **Adaptive Interview**: The agent uses the *Five Whys* and *Scenario Walkthrough* framework.
  - User: "I want an export button."
  - Agent: "Why do you need to export?" -> Discovers the real job (JTBD) is generating monthly reports for the finance team.
- **Output**: A filled `problem-intake-template.md` that captures the true root cause, stakeholders, and risks (e.g., PII data).

## Step 2: Technical Assignment
The user initializes an agent with `aos/prompts/technical-assignment-builder.md` and provides the intake document.
- **Grey-Zone Discovery**: The agent notices the intake says "finance needs access" but doesn't define authentication. It asks the user to clarify this assumption.
- **Bounding Scope**: The agent defines:
  - **In-Scope**: A `.github/workflows/report.yml` automated script.
  - **Out-of-Scope**: A full UI dashboard.
- **Output**: A filled `technical-assignment-template.md`.

## Step 3: Controlled Task Execution
The user creates a `controlled-task-brief-template.md` targeting exactly the files defined in the TA. The executing agent runs the task, verified by strict safety boundaries.

## Step 4: Human Checkpoint
The user reviews the evidence. `PASS ≠ approval`, so the user explicitly approves the commit and push in a Human Checkpoint.
