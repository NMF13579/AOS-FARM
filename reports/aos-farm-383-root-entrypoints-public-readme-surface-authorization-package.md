# AOS-FARM-383 Root Entrypoints & Public README Surface Authorization Package

## Target Task
AOS-FARM.384 — Controlled Root Entrypoints and Public README Surface Update

## Migration Scope
Update the top-level repository entrypoints to present AOS-FARM as the public open-source home of the Agentic Operating System.

**Rules:**
- Do not modify `00/01/02/03`.
- Do not modify old `docs/`, `templates/`, `agentos/`.
- Do not create `llms.txt`.
- Do not stage, commit, or push.

## Proposed Target File List

| Target File | Decision | Required Consumer Content | Forbidden Internal Content |
|-------------|----------|---------------------------|----------------------------|
| `README.md` | REWRITE | What AOS is, how to install (`aos/`), basic workflow, strict safety rules (PASS ≠ approval), where to start (`aos/START_HERE.md`). | Internal development history, roadmap steps, runner documentation. |
| `README.ru.md` | REWRITE | Accurate translation of the new `README.md`. | Same as above. |
| `AGENTS.md` | MODIFY | Add pointers directing agents to the `aos/` consumer kit for product rules. Re-affirm that `00/01/02/03` remain internal to AOS-FARM. | Do NOT remove existing safety instructions for modifying AOS-FARM. |

## Proposed README Content Sections
1. **Title & Tagline**: Agentic Operating System (AOS) - The secure framework for AI-driven software development.
2. **What is AOS?**: Self-contained markdown kit inside `aos/`.
3. **Core Philosophy**: Fail-closed, PASS ≠ approval, strict human checkpoints.
4. **Who is it for?**: Developers managing autonomous AI agents.
5. **Quick Start**: Copy `aos/` to your project, add `AGENTS.md`, write a task brief.
6. **No Magic Allowed**: Clarify that there are no active Python runners, CI, DB, or RAG components required. It is pure methodology.

## Proposed AGENTS.md Update Decision
- **Keep** all existing repository-level instructions (`00`, `01`, `02`, `03` read order, invariant rules, fail-closed rule).
- **Append** a new section: `## AOS Consumer Kit Reference`. This section will instruct agents that if they are asked about "How AOS works for consumers", they should refer to `aos/AGENT_CONTEXT.md` and `aos/START_HERE.md`.

## llms.txt Decision
**DEFER**. The `aos/AGENT_CONTEXT.md` provides sufficient standard context for now. An `llms.txt` file at the repository root will be evaluated during final release polishing.

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**
*Reasoning: Modifying the repository's root `AGENTS.md` and public `README.md` directly impacts the canonical face of the project and agent behavior.*

## Status
- **Authorization**: PENDING
- **Final Status**: **AOS_FARM_383_ROOT_ENTRYPOINTS_PUBLIC_README_SURFACE_AUTHORIZATION_PREPARED**
