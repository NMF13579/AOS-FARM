# Task Candidate to Task Conversion Checklist

## Purpose

This checklist defines the boundary for moving a Task Candidate toward human review as a task draft. It does not authorize execution and does not approve the candidate.

## Source of Truth

Task files, registries, and canonical docs remain Source of Truth.

Candidate conversion notes, checklists, reports, and generated summaries are derived review aids only.

## Checklist

A Task Candidate may move to human review only if all required items are present or explicitly blocked:

1. task id follows accepted naming pattern.
2. task file path is valid.
3. title is present.
4. problem / goal is present.
5. scope is explicit.
6. non-goals / forbidden changes are explicit.
7. validation plan exists.
8. Evidence plan exists.
9. expected changed files or allowed file areas are explicit.
10. protected/canonical impact is declared.
11. Risk Profile is assigned by human or marked `HUMAN_REVIEW_REQUIRED`.
12. `execution_authorized` is false until human checkpoint.
13. approval/commit/push/merge/release flags are false by default.
14. UNKNOWN is not treated as OK.
15. NOT_RUN is not treated as PASS.

## Allowed Outputs

- `READY_FOR_HUMAN_REVIEW`
- `BLOCKED`
- `UNKNOWN_BLOCKED`

## Forbidden Outputs

- `READY_FOR_EXECUTION`
- `APPROVED`
- `LOW_RISK_FAST`
- `commit_authorized: true`
- `push_authorized: true`
- `release_authorized: true`

## Human Review Boundary

Human review may decide whether the candidate should become a real task draft. Human review is not automatic approval. Human review does not authorize execution unless the human checkpoint explicitly says so.

## Execution Boundary

Candidate conversion must preserve these defaults:

```yaml
execution_authorized: false
approval_granted: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```

Risk Profile must be assigned by a human or remain blocked for human review. The agent must not assign `LOW_RISK_FAST`.
