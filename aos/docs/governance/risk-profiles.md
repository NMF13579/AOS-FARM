# Risk Profiles

Every AOS task requires a human-assigned Risk Profile to dictate the level of autonomy and constraint applied to the agent.

## Common Profiles
- **LOW_RISK_FAST**: Minor local changes, documentation updates, or isolated code edits. The agent has more leeway in execution but still cannot commit without approval.
- **MEDIUM_RISK_GUIDED**: Feature development or structural changes. The agent must strictly follow the implementation plan and verify extensively.
- **HIGH_RISK_PROTECTED**: Changes to root configuration, governance rules, or canonical architecture. The agent must operate under extreme constraints and fail closed on any ambiguity.
- **DESTRUCTIVE_OR_CANONICAL**: Commits, pushes, or deletions. Requires the highest level of scrutiny and explicit authorization.
