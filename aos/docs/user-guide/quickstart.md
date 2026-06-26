# AOS Quickstart

Welcome to AOS, the Agentic Operating System consumer kit.

## Adopting AOS
To use AOS in your project, ensure the `aos/` directory is copied into your project root.
You must also include the primary root entrypoint `AGENTS.md` (or the AOS marker block) in your project's root folder to guide your AI assistants.

## Basic Workflow
1. **Define the Problem**: Start with Problem Intake, then create a Technical Assignment.
2. **Break Work Down**: Build a Task Breakdown and Task Queue before selecting one task.
3. **Create A Controlled Task Brief**: Convert one reviewed queue item into an exact execution brief.
4. **Authorize Execution**: Use a human checkpoint to assign the Risk Profile and authorize that exact brief.
5. **Run Guarded Execution**: Run Controlled Execution Guard `precheck`, execute inside scope, then run `scopecheck` and `postcheck`.
6. **Verify Before Git Gates**: Review Evidence before any separate commit authorization or push authorization.

*PASS is not approval. Evidence is not approval. AOS requires explicit human authorization for all commits, pushes, and destructive operations.*
