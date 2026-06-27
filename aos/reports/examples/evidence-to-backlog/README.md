# Evidence-to-Backlog Examples

These examples show safe post-execution learning artifacts and intentionally
invalid fixtures for future validator/helper work.

## Safe Examples
- `post-execution-review-example.md`
- `lessons-learned-example.md`
- `pipeline-hardening-backlog-item-example.md`
- `next-task-candidate-example.md`

## Valid Fixtures
- `fixtures/valid/post-execution-review.md`
- `fixtures/valid/lessons-learned.md`
- `fixtures/valid/backlog-item.md`
- `fixtures/valid/next-task-candidate.md`

## Negative Fixtures
- `fixtures/negative/not-run-treated-as-pass.md` expects `BLOCKED`.
- `fixtures/negative/unknown-treated-as-ok.md` expects `BLOCKED`.
- `fixtures/negative/candidate-claims-approval.md` expects `BLOCKED`.
- `fixtures/negative/risk-profile-self-assigned.md` expects `HUMAN_REVIEW_REQUIRED`.
- `fixtures/negative/execution-authorized-inside-candidate.md` expects `BLOCKED`.

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

These examples do not authorize execution, commit, push, merge, release, Risk
Profile assignment, or the next task.
