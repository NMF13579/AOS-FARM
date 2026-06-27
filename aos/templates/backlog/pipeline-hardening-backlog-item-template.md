# Pipeline Hardening Backlog Item Template

Use this template to record one possible hardening item discovered from
post-execution evidence. A backlog item is not execution authorization.

## Status
gap_id:
source_evidence:
problem:
impact:
affected_surface:
risk:
candidate_fix:
protected_or_canonical_impact:
requires_human_review:
recommended_next_step:
execution_authorized: false
commit_authorized: false
push_authorized: false
status: DRAFT

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

## Next Safe Step
If the item should become work, draft a separate Next Task Candidate for human
review. Do not start implementation from this backlog item.
