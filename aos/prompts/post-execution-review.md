# Post-Execution Review Prompt

Use this prompt after Evidence Review to create post-execution learning
artifacts for human review. Do not use it to approve work or start the next
task.

```text
Create post-execution learning artifacts for this completed controlled task.

Use only the provided Evidence Report, Execution Report, guard results,
scopecheck/postcheck results if present, and commit/push closure evidence if
present.

Create only review material:
- Post-Execution Review
- Lessons Learned
- Pipeline Hardening Backlog Item
- Next Task Candidate

Required boundaries:
- Evidence Review ≠ approval.
- Lessons Learned ≠ approval.
- Pipeline Hardening Backlog Item ≠ execution authorization.
- Next Task Candidate ≠ approved task.
- Validator PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Human unavailable for required decision → BLOCKED or HUMAN_REVIEW_REQUIRED.

Do not authorize execution.
Do not authorize commit.
Do not authorize push.
Do not authorize merge.
Do not authorize release.
Do not assign a Risk Profile.
Do not start the next task.
Stop with HUMAN_REVIEW_REQUIRED unless a separate human checkpoint explicitly
authorizes the next lifecycle transition.
```
