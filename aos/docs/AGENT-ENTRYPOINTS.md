# Agent Entrypoints

This document explains the entrypoint strategy for AI agents interacting with an AOS-enabled repository.

## The Thin Adapter Model
Agent-specific start files (like `AGENTS.md`, `.cursor/rules/aos.mdc`) are designed to be thin adapters. 
They do not duplicate the full governance logic, Control Module rules, or safety invariants. 

### Why?
Duplicating large rule sets across multiple environment-specific start files leads to desynchronization and a fragile "Source of Truth". A thin adapter ensures that every agent environment correctly routes to a single, unified entrypoint.

## The Common Route: `llms.txt`
`llms.txt` serves as the common route entrypoint for all agents. The thin adapters explicitly instruct agents to read `llms.txt` before doing any work. `llms.txt` itself provides the initial navigation instructions, pointing the agent to detailed documentation within `/aos/docs/`.

### How AGENTS.md Points to `llms.txt`
`AGENTS.md` is the starting file for Codex/OpenAI-style environments. Its only responsibility is to inform the agent that the repository uses AOS and to direct it to `llms.txt` to follow the established route.

## Detailed Instructions Live in `/aos/docs/`
`llms.txt` directs agents to `/aos/docs/ROUTES.md`, `/aos/docs/STORAGE.md`, `/aos/docs/AUTHORIZATION-COMMANDS.md`, etc. 
This structure ensures that detailed instructions, governance, workflow, and safety definitions live strictly in their designated documentation files, avoiding bloat in the root entrypoint files.

## Prompt Packs
Agents may also be provided with specific [Prompt Packs](../prompt-packs/README.md) that contain tailored contexts and commands. These packs also strictly adhere to the rule of pointing to the core governance documents rather than duplicating them.

## Future Planned Adapters
In future stages, additional adapters will be implemented following this same model (pointing to `llms.txt`):
- `CLAUDE.md`
- `GEMINI.md`
- `.cursor/rules/aos.mdc`
- `.windsurf/rules/aos.md`
- `.github/copilot-instructions.md`

All future adapters must remain thin and point to `llms.txt`. They must not include redundant copies of the AOS control framework.
