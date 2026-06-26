# Agentic Operating System (AOS)

**The secure framework for AI-driven software development.**

AOS is a pure-methodology, markdown-first framework designed to safely manage autonomous AI agents. Instead of relying on active Python runners, CI hooks, or databases, AOS enforces a fail-closed structural boundary through deterministic file management and explicit human checkpoints.

## What is AOS?
AOS is distributed as a self-contained consumer kit located in the `aos/` directory. It provides:
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
1. Copy the `aos/` folder into your project root.
2. Copy `aos/root/AGENTS.md` to your project root.
3. Open `START_HERE.md` in the project root.
4. From there, follow `aos/START_HERE.md`. This is the user-facing starting point that guides you through Problem Intake, Technical Assignment, Task Breakdown, Controlled Task Brief, Human Execution Authorization, Controlled Execution Guard checks, and only then controlled execution.

## No Magic Allowed
AOS requires no active Python runners, continuous integration scripts, databases, or RAG components to function. It relies entirely on the AI agent's adherence to clear, markdown-defined systemic rules.

## Documentation
- **[Installation Guide](aos/INSTALL.md)**
- **[Root Start Here](START_HERE.md)**
- **[Start Here for Agents](aos/START_HERE.md)**
- **[Agent Context](aos/AGENT_CONTEXT.md)**
- **[Adoption Guide](aos/ADOPTION.md)**

---
*Note: The root of this specific repository is the development environment for the AOS framework itself. If you are a consumer, refer only to the `aos/` directory.*
