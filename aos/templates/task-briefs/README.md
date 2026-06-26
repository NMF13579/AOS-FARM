# AOS Consumer Kit

AOS is a self-contained consumer kit. `aos/` is the installable and removable unit.
The root `AGENTS.md` is the primary required root entrypoint. Optional marker blocks may be placed in the project root `README.md` and `.gitignore`.

## Controlled Task Brief Templates
- Use `controlled-task-brief-template.md` to define one exact execution task.
- The brief should name the expected execution package path, usually copied from `aos/templates/execution-packages/controlled-execution-package-template.yaml`.
- The brief is not execution approval. Pair it with a real Human Execution Authorization before running guard `precheck`.

**AOS Core Rules & Boundaries:**
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
