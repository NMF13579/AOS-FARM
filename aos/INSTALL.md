# AOS Consumer Kit Installation

AOS is a self-contained consumer kit. The `aos/` directory is the installable and removable unit.

## Installation
1. **Copy AOS Folder:** Copy the entire `aos/` folder into your target project root.
2. **Copy AGENTS.md Template:** Copy the template file `/aos/root/AGENTS.md` into your project root as `AGENTS.md`. This is the primary required root entrypoint for AI agents.
3. (Optional) Add marker blocks in your project root `README.md` to point users and agents to `/aos/START_HERE.md`.
4. (Optional) Update your `.gitignore` to ignore active reports if desired.

## Uninstallation
1. **Remove AOS Folder:** Delete the entire `aos/` folder from your project root.
2. **Remove AGENTS.md:** Delete `AGENTS.md` from your project root.
3. **Remove Markers:** Remove any AOS marker blocks from your `README.md` and `.gitignore`.

**AOS Core Rules & Boundaries:**
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No active runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
