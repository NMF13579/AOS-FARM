# First Agent Run

When invoking your AI agent for the first time in an AOS-enabled repository, provide it with the core context.

## Initializing the Agent
Prompt your agent with:
> "Please read `aos/START_HERE.md` and `AGENTS.md` to orient yourself to the repository rules, then wait for my first task."

## The First Task
For the first task, start small to verify the agent respects the boundaries:
- Task: "Review the current directory structure and list the root files."
- Expect the agent to read, report, and stop without modifying files or making unapproved commits.
