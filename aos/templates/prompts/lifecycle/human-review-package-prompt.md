# Human Review Package Prompt

## Purpose
To generate a read-only review package containing all necessary context and diffs for a human to review a specific implementation.

## When to use
Use this prompt when an implementation sub-step is complete, and you need to present the files in scope to a human for formal safety and functional review.

## Commands or helper entrypoint
```bash
python3 aos/scripts/aos_review_package.py --mode human-review --task-id <TASK_ID> --files <LIST_OF_FILES> --target-branch <TARGET_BRANCH> --format markdown
```

## Required safety notes
- Review package is not approval.
- Evidence is not approval.
- Human decision required.
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Remote closure verification is not release authorization.
- Commit authorization is not push authorization.
- Push authorization is not release authorization.
- PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Skeleton ≠ implementation.
- Scope must not expand without explicit human permission.
- Protected/canonical changes require human checkpoint.
- Destructive operations are forbidden by default.

## What this template does not authorize
This template does not authorize any git mutations (commits, pushes, staging), execution approvals, or assignments of Risk Profiles.

## Expected final status
`REVIEW PACKAGE STATUS: READY_FOR_HUMAN_DECISION`
