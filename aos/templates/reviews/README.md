# Review Templates

Use review templates after controlled execution evidence exists and before any
follow-up work is authorized.

- `post-execution-review-template.md` records whether evidence is sufficient,
  what was learned, and whether lessons, backlog items, or task candidates were
  created for human review.
- `lessons-learned-template.md` records one lesson from completed evidence.

## Safety Boundary
- Evidence Review ≠ approval.
- Lessons Learned ≠ approval.
- Pipeline Hardening Backlog Item ≠ execution authorization.
- Next Task Candidate ≠ approved task.
- Validator PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Human unavailable for required decision → BLOCKED or HUMAN_REVIEW_REQUIRED.

These templates do not authorize execution, commit, push, merge, release, Risk
Profile assignment, or the next task.
