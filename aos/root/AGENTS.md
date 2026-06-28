# AGENTS

> **TEMPLATE NOTE:** This file (`/aos/root/AGENTS.md`) is a template. It should be copied to the root of your target project and renamed to `AGENTS.md`. It is not the product folder itself. The actual product folder remains `/aos/`.

When you copy this file to your project root, it serves as the primary root entrypoint for AI agents operating in your project, directing them to the strict AOS methodology.

## AOS Core Rules & Boundaries:
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Target projects must use a local-only `/.aos-tmp/` directory in their project root for temporary command outputs and logs. This directory must be ignored in git, and must never contain Evidence, reports, or approval checkpoints.
- Exclusions: No active runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.

**Agent Start Here:** Agents should always begin by reading `aos/START_HERE.md`.
