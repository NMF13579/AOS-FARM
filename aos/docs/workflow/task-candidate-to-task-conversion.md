# Task Candidate to Task Conversion Checklist

## Purpose

This checklist defines the boundary for moving a Task Candidate toward human review as a task draft. It does not authorize execution and does not approve the candidate.

## Source of Truth

Task files, registries, and canonical docs remain Source of Truth.

Candidate conversion notes, checklists, reports, and generated summaries are derived review aids only.

## Task Registry Draft Review Protocol

Task Registry Draft artifacts are review inputs, not lifecycle-active tasks.

Before a Task Candidate is converted into a task file, human review must confirm:

1. the candidate is still relevant to the current AOS-FARM state;
2. the candidate traces to a known source report, task, registry item, or human decision;
3. the proposed task objective is narrow enough for one controlled execution slice;
4. the proposed scope and non-goals are explicit;
5. the allowed file areas and forbidden file areas are explicit;
6. any protected/canonical impact is declared;
7. the validation and Evidence expectations are stated without treating either as approval;
8. the Risk Profile is assigned by human or the task remains `HUMAN_REVIEW_REQUIRED`;
9. execution, approval, commit, push, merge, and release flags remain false by default;
10. no derived rank, dashboard output, validator output, or Evidence claim is treated as approval.

Human review may accept a candidate for task drafting, request changes, defer it, or reject it. Acceptance for drafting does not authorize execution.

## Conversion Boundary

Converting a Task Candidate into a task file is a Source-of-Truth mutation and requires an explicit human checkpoint.

The conversion may create or update only the task file named by the checkpoint. It must not:

- silently create unrelated task files;
- mutate queue state outside the authorized task file;
- mark the task `READY_FOR_EXECUTION`;
- set approval, commit, push, merge, or release authorization to true;
- create Evidence;
- write reports, checkpoints, lifecycle decisions, or Evidence into `.aos-tmp`;
- edit protected/canonical sources unless a separate protected/canonical checkpoint explicitly authorizes that change.

If the candidate cannot satisfy the checklist below, the safe result is `BLOCKED` or `UNKNOWN_BLOCKED`.

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

After conversion, the resulting task remains non-executable until a separate execution authorization prompt grants execution. A later execution prompt must restate allowed files, forbidden files, validation commands, Evidence/report permissions, and commit/push boundaries.

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
