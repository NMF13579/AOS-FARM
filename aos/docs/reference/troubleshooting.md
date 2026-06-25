# Troubleshooting

## Agent Stuck in a Loop
If the agent repeatedly tries to fix a failing test without success:
1. Stop the agent.
2. Review the execution report.
3. Re-evaluate the task brief and provide a smaller, more guided step.

## Unintended File Modifications
If the agent modifies files outside the authorized scope:
1. Use `git restore <file>` or `git clean` to revert the unauthorized changes.
2. Ensure the preflight check enforces a clean baseline before the next execution.
3. Update the task constraints to be more explicit.
