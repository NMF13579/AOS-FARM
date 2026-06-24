# AOS-FARM Manual Task Queue

Welcome to the manual task queue system. This system relies on explicitly written Markdown files to coordinate between humans, the Agent Tutor, and executor agents.

## What is the Manual Task Queue?
It is a collection of Markdown files located in the project tree that document the exact state, scope, and progress of every task.

## Why it exists
AOS-FARM avoids hidden databases, SQLite files, or closed-source tracking tools. A manual queue ensures:
- Full transparency (all states are readable by standard text editors and git).
- Total human control.
- Prevention of rogue automation.

## Who uses it
- **You (the Human)**: To explicitly approve states and review verification reports.
- **Agent Tutor**: To read the queue and help you understand what is happening and what to do next.
- **Executor Agents**: To receive highly constrained handoff packages and report back the results.

## How it relates to Execution
The task queue **records** workflow state, but it **does not approve** execution. Changing a status to `READY_FOR_EXECUTION` does not authorize an agent to start coding. Explicit Human Checkpoints are required for execution, commit, and push.

## What this system does NOT automate
This system will **not**:
- Automatically assign tasks to agents.
- Automatically run your code.
- Automatically update statuses based on tests.
- Automatically verify outcomes.
- Automatically commit or push.
