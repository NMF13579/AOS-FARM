# Technical Assignment Workflow

The Technical Assignment (TA) workflow bridges the gap between raw problem definition (Intake) and controlled execution (Task Briefs).

## Purpose
- Convert structured Problem Intake data into a controlled, actionable technical assignment.
- Explicitly define the Scope, Non-Goals, Acceptance Criteria, and required files.
- Establish strict boundaries for the AI agent to prevent scope creep.

## How it works
1. **Initialize the Agent**: Use the `aos/prompts/technical-assignment-builder.md` prompt, providing the completed Problem Intake document as context.
2. **Refine and Bound**: The agent translates business goals into strict technical boundaries, identifying exactly what files need to change and what actions are strictly forbidden. It will ask questions to resolve any remaining contradictions or `UNKNOWN`s.
3. **Capture Output**: The outcome is a structured document based on `aos/templates/task-briefs/technical-assignment-template.md`.

## Handoff & Saving Output
- **Consuming Intake:** The TA prompt requires the saved Problem Intake output as direct input context.
- **Where to save TA output:** `aos/reports/technical-assignments/<project-or-feature-name>.md`
- **Required fields:** Scope, Non-Goals, target files, Acceptance Criteria, dependencies.
- **When to prepare Task Brief:** A controlled task brief may be prepared only *after* the TA output is finalized and saved.

## Bridge to Controlled Task
The Technical Assignment provides the foundational constraints for creating a specific **Controlled Task Brief** (`aos/templates/task-briefs/controlled-task-brief-template.md`). 

`Idea → Problem Intake → Technical Assignment → Controlled Task Brief → Execution → Verification → Human Checkpoint`

## Methodology Integration
This workflow is governed by `aos/docs/methodology/technical-assignment-methodology.md`. It relies purely on Markdown and prompt engineering, with no legacy Python validators required.

## Safety Semantics
- A Technical Assignment is a planning document. **Skeleton ≠ implementation**.
- Generating a TA does not grant the agent permission to write code or modify files. 
- Commit, push, release, or destructive operations always require explicit human authorization.
- Technical Assignment is readiness/planning evidence, not approval.
