# Agentic Operating System (AOS)

**The secure framework for AI-driven software development.**

AOS is a pure-methodology, markdown-first framework designed to safely manage autonomous AI agents. Instead of relying on active Python runners, CI hooks, or databases, AOS enforces a fail-closed structural boundary through deterministic file management and explicit human checkpoints.

## What is AOS?
AOS is distributed as a self-contained consumer kit. The complete **Product folder AOS** is located strictly in the `/aos/` directory. It provides:
- **Strict Methodology**: Rules that AI agents must obey (e.g. `PASS ≠ approval`).
- **Templates**: Checkpoints, task briefs, and execution reports.
- **Prompts**: Standardized agent entrypoints.
- **Governance**: Clear boundaries defining what an agent can and cannot do autonomously.

## Core Philosophy
1. **Fail-Closed by Default**: If a state is unknown, the agent must stop and ask.
2. **PASS ≠ Approval**: A passing test or successful script execution does not authorize a commit or a deployment.
3. **No Simulated Approval**: Agents are strictly forbidden from writing "Approved by Human" without genuine human intervention.
4. **Deferred Commits**: Agents perform work locally and wait for explicit batch-commit authorization.

## Quick Start
To adopt AOS in your project:
1. Copy the `/aos/` folder into your project root.
2. Copy the template `/aos/root/AGENTS.md` to your project root as `AGENTS.md`.
3. The consumer user and their agent must start at `/aos/START_HERE.md`.

## No Magic Allowed
AOS requires **no mandatory active Python runners**, continuous integration scripts, databases, or RAG components to function. It relies entirely on the AI agent's adherence to clear, markdown-defined systemic rules.

While the `/aos/` folder includes optional validators and local artifact generators (e.g., in `/aos/scripts/`), these helpers have no approval, commit, push, merge, or release authority. They may generate local drafts or validation signals, but they cannot execute tasks or approve operations.

## Documentation
- **[Installation Guide](aos/INSTALL.md)**
- **[Consumer Start Here](aos/START_HERE.md)**
- **[Agent Context](aos/AGENT_CONTEXT.md)**
- **[Adoption Guide](aos/ADOPTION.md)**

---
*Note: The root of this specific repository is the development environment for the AOS-FARM framework itself. If you are a consumer, refer only to the `/aos/` directory.*
