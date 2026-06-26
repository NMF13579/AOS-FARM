# AOS Consumer Kit

AOS is a self-contained consumer kit. `aos/` is the installable and removable unit.
The root `AGENTS.md` is the primary required root entrypoint. Optional marker blocks may be placed in the project root `README.md` and `.gitignore`.

## Report Templates
- `execution-report-template.md` records what the agent changed, what commands ran, and Controlled Execution Guard `precheck`, `scopecheck`, and `postcheck` results.
- `controlled-execution-evidence-report-template.md` records Evidence, NOT_RUN, UNKNOWN, BLOCKED, and approval boundaries for controlled execution.
- `evidence-review-template.md` helps a human review Evidence after the report is complete. It does not authorize commit or push.

**AOS Core Rules & Boundaries:**
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
