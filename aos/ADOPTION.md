# AOS Adoption Guide

AOS is designed to be easily adopted into both greenfield and existing projects. The `aos/` directory is the installable and removable unit.

## Adopting in an Existing Project
To adopt AOS in an existing project:
1. Follow the [Installation Guide](INSTALL.md) to copy the `/aos/` folder and `/AGENTS.md` template into your project.
2. Direct your AI agent to read the `aos/START_HERE.md` entrypoint.
3. Treat your existing codebase as the environment. You do not need to rewrite your code; you only need to govern the *agent's actions* moving forward.
4. Ensure your project's root `.gitignore` ignores the `/.aos-tmp/` directory, which AI agents will use for temporary command outputs and logs.

## First Session Flow
When adopting AOS, your first interaction with an agent should follow the **First Session Flow**:
1. Open a new chat/agent session.
2. Ask the agent to read `aos/START_HERE.md`.
3. The agent will guide you through a **Problem Intake** interview to understand what you want to achieve.
4. Next, it will generate a **Technical Assignment** defining the scope of work.
5. Finally, it will propose a **Task Queue** for you to review.
6. Execution does not begin until you manually approve a task from the queue.

For detailed instructions, see the [First Session Guide](docs/workflow/first-session-guide.md).

**AOS Core Rules & Boundaries:**
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No active runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
