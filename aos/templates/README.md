# AOS Consumer Kit

AOS is a self-contained consumer kit. `aos/` is the installable and removable unit.
The root `AGENTS.md` is the primary required root entrypoint. Optional marker blocks may be placed in the project root `README.md` and `.gitignore`.

## Template Index
- `task-briefs/controlled-task-brief-template.md` defines the task scope before execution.
- `checkpoints/human-execution-authorization-template.md` records the human execution decision for one exact task.
- `execution-packages/controlled-execution-package-template.yaml` is the Controlled Execution Guard package template for `precheck`, `scopecheck`, and `postcheck`.
- `reports/execution-report-template.md` records execution claims and guard results.
- `reports/controlled-execution-evidence-report-template.md` records Evidence, NOT_RUN, UNKNOWN, BLOCKED, and approval-boundary fields.
- `reports/evidence-review-template.md` supports human review after Evidence is collected.
- `reviews/post-execution-review-template.md` records lessons, gaps, backlog items, and next-task candidates after Evidence Review.
- `reviews/lessons-learned-template.md` records one lesson from completed evidence.
- `backlog/pipeline-hardening-backlog-item-template.md` records one possible hardening item without authorizing execution.
- `task-briefs/next-task-candidate-template.md` frames a possible follow-up task for human review only.

**AOS Core Rules & Boundaries:**
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Lessons Learned ≠ approval.
- Pipeline Hardening Backlog Item ≠ execution authorization.
- Next Task Candidate ≠ approved task.
- Validator PASS ≠ approval.
- Exclusions: No runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
