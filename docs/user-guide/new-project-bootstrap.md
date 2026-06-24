# New Project Bootstrap Guide

Welcome to your new AOS-FARM repository! Since you created this repository from the AOS-FARM template, you have inherited a strict, manual governance framework designed for safe AI-assisted development.

## What to do first

1. **Do not write code yet.** AOS-FARM requires explicit planning and approval boundaries before any code is generated.
2. **Confirm required sources exist**:
   - `00_AOS_Core_Control.md`
   - `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
   - `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
3. Read the main [User Guide README](README.md) to understand the project structure.
4. Read the [First 30 Minutes Guide](first-30-minutes.md) for a step-by-step timeline.
5. Fill out the [Project Bootstrap Checklist](../../templates/project-bootstrap-checklist.md) to define your project boundaries.
6. Start an Agent Tutor session using the [First Agent Session Template](../../templates/first-agent-session-template.md). Let the Agent Tutor explain the project to you.
7. Prepare your first safe task using the [First Task Brief Template](../../templates/first-task-brief-template.md). This task should only be documentation or requirement gathering (e.g., `PROJECT_SPEC`), not implementation.
8. If your Agent proposes a task, you must explicitly approve it using the [Bootstrap Human Checkpoint Template](../../templates/bootstrap-human-checkpoint-template.md).
9. **Stop.** Do not proceed to implementation without a filled-in `execution_authorized: true` checkpoint.

## What NOT to do at the bootstrap stage

- **Do not ask your agent to "build the app".** It will fail-closed because there is no approved scope.
- **Do not delete the `reports/` or `templates/` folders.** They are required for the framework to function.
- **Do not commit or push directly.** Always ask your agent to prepare a Commit Candidate Set and wait for your explicit approval.

## How to avoid accidental implementation
If an agent starts writing code without a Task Brief and Human Checkpoint, tell it to `STOP` and return to the `Problem Intake` stage. Always define the scope first.

## How to avoid accidental commit/push
Agents must never run `git commit` or `git push` autonomously. They must stop and wait for you to fill out the `APPROVED_FOR_COMMIT` or `APPROVED_FOR_PUSH` checkpoints.
