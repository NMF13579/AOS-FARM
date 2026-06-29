# AOS Package Manifest

## Product Package Purpose
AOS is a self-contained consumer kit designed to provide agentic governance, safety bounds, and planning templates to any target repository.

## Top-Level Files/Folders
- `aos/`: Required consumer package directory.
- `aos/START_HERE.md`: Required entry point for consumer onboarding.
- `aos/AGENT_CONTEXT.md`: Required context definition for agents.
- `aos/prompts/`: Required consumer-facing prompts.
- `aos/schemas/`: Required JSON schemas for task definitions.
- `aos/tools/`: Optional helper tooling.
- `aos/examples/`: Optional examples and templates.

## Required vs Optional
- Core docs (`START_HERE.md`, `AGENT_CONTEXT.md`), prompts, and schemas are REQUIRED.
- `aos/tools/` and `aos/examples/` are OPTIONAL helpers and examples.

## Source of Truth Boundaries
- What is NOT Source of Truth: Generated artifacts, `aos/tools/optional/` scratch outputs (e.g. `.aos-tmp/`), and `aos/examples/` fixtures.
- What is Excluded from Consumer Runtime Prerequisites: Internal `agentos/` directories and AOS-FARM root control sources (`00_AOS...`, `01_AOS...`, `02_AOS...`).
