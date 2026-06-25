# Technical Assignment to Task Brief Assembly Workflow

Welcome to the Task Assembly Layer. This document explains the critical bridge between defining what you want to build (Technical Assignment) and actually building it (Execution).

## The Bridge (Workflow)
Problem Intake
→ Technical Assignment
→ Task Breakdown
→ Task Drafts
→ Traceability Check
→ Dependency Map
→ Priority Proposal
→ Batch Plan
→ Human Task Review
→ Task Queue
→ Controlled Task Brief
→ Execution Authorization

## When to use this step
Use this step **after** you have a completed Technical Assignment, but **before** you authorize an AI agent to write any code. A Technical Assignment is usually too broad for an AI to execute safely in one go.

## Required Input
- The completed `Technical Assignment` document.

## Expected Output
- A `Task Breakdown` (a detailed analysis of what needs to be done).
- A `Task Queue` (a manual list of tasks waiting for your review and authorization).

## What the Task Brief Builder Does
The Task Brief Builder is a prompt (`aos/prompts/task-brief-builder.md`) that you give to your AI agent.
- **Task Brief Builder does not write code.**
- **Task Brief Builder does not authorize execution.**
- **Task Brief Builder does not approve tasks.**
- **Task Brief Builder does not assign Risk Profile as human.**

### Extracting Task Drafts and Traceability
The agent reads your Technical Assignment (TA) and extracts smaller "Task Drafts". To prevent the agent from making up work, it must prove traceability: every single task must trace back directly to a specific section of the TA.

### Dependencies and Priorities
The agent maps out which tasks depend on others (Dependency Map) and proposes an order of execution (Priority Proposal).
- **Task draft ≠ approved task.** A draft is just a suggestion.
- **Priority ≠ approval.** Even if a task is "P0" (highest priority), it still needs your explicit approval.

### Batch Planning and Human Review
Some tasks are small and safe to group together into a "Batch Plan". Others must be done strictly alone. You (the human) will perform a Human Task Review of the Task Queue to decide what to authorize next.
- **Task queue position ≠ execution authorization.** Being next in line doesn't mean the agent can run it.
- **Readiness ≠ approval.** A task being completely planned does not mean it is approved to run.
- **Risk Profile proposal ≠ human-assigned Risk Profile.** The agent suggests how risky a task is, but only you assign the final Risk Profile.

### Handling UNKNOWN/BLOCKED
If a requirement is unclear, or a task cannot be traced to the TA, the agent marks it as `BLOCKED` or `UNKNOWN_BLOCKED`. The task cannot proceed until you resolve the ambiguity.

### Stale-Task Detection
If your Technical Assignment changes in the future, the task queue must be re-evaluated to detect "stale tasks" that no longer match the new requirements.

## Short Example for Non-Programmers

**Technical Assignment says:**
"Add a user settings page, do not change authentication, add tests."

**Task Brief Builder may produce:**
- `TASK-001`: Create settings page UI.
- `TASK-002`: Add settings form validation.
- `TASK-003`: Add tests for settings form.
- `BLOCKED`: Change authentication (Because TA forbids it).

You then review the manual task queue, pick `TASK-001`, convert it to a Controlled Task Brief, authorize execution, and only then does the agent write code!
