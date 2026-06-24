# Agent Controller Workflow

AOS-FARM heavily relies on AI agents, but it strictly separates their roles to prevent runaway, unsafe behavior.

## The Roles

1. **The Controller / Architect (e.g., GPT-4o)**: Plans tasks, suggests next steps, and reviews architecture.
2. **The Executor (e.g., Codex / Antigravity / IDE Agent)**: Writes the actual code, runs terminal commands, and generates files.
3. **The Tutor**: A specific mode where the agent acts as an explanatory interface (see [Agent Tutor Mode](agent-tutor-mode.md)).
4. **The Approver (You, the Human)**: The sole authority. Only you can authorize changes to canonical rules, commits, pushes, or releases.

## The Separation of Powers
- **The Controller suggests.** It creates task briefs and plans.
- **The Executor implements.** It writes code strictly within the boundaries set by the Controller and authorized by you.
- **The Verifier checks.** The agent runs self-checks to ensure it didn't break rules.
- **The Human approves.** The system halts until you provide explicit authorization.

## Critical Rule
**An agent can NEVER replace Human approval.**
Even if you use an advanced model like GPT-4o to review the code of a smaller executor model, the "GPT Review" is NOT Human approval. Only explicit authorization provided by you counts.
