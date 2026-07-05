# AOS Consumer Kit Installation

AOS is a self-contained consumer kit. The `aos/` directory is the installable and removable unit.

For full installation and transfer instructions, please read [aos/docs/INSTALL-AND-TRANSFER.md](docs/INSTALL-AND-TRANSFER.md).

## Quick Reference
- Installer safe `--apply` is available but highly restricted.
- Manual transfer remains a supported path.
- Dry-run validates and reports; it remains the default.

## Uninstallation
1. **Remove AOS Folder:** Delete the entire `aos/` folder from your project root.
2. **Remove AGENTS.md:** Delete `AGENTS.md` and `llms.txt` from your project root.
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
