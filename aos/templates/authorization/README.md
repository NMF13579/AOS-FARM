# AOS Consumer Kit

AOS is a self-contained consumer kit. `aos/` is the installable and removable unit.
The root `AGENTS.md` is the primary required root entrypoint. Optional marker blocks may be placed in the project root `README.md` and `.gitignore`.

## Authorization Templates
- Execution authorization must point to one exact Controlled Task Brief and one exact Controlled Execution Package.
- The package should be copied from `aos/templates/execution-packages/controlled-execution-package-template.yaml` and filled before guard `precheck`.
- Commit authorization and push authorization remain separate from execution authorization and Evidence Review.

**AOS Core Rules & Boundaries:**
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
