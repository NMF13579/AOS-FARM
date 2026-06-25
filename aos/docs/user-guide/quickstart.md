# AOS Quickstart

Welcome to AOS, the Agentic Operating System consumer kit.

## Adopting AOS
To use AOS in your project, ensure the `aos/` directory is copied into your project root.
You must also include the primary root entrypoint `AGENTS.md` (or the AOS marker block) in your project's root folder to guide your AI assistants.

## Basic Workflow
1. **Define the Task**: Create a clear task brief.
2. **Authorize Execution**: Use a human checkpoint to assign a Risk Profile and authorize execution.
3. **Execute**: The agent executes the task strictly within boundaries.
4. **Verify**: Perform post-execution verification before committing.

*AOS requires explicit human authorization for all commits, pushes, and destructive operations.*
