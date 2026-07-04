# Commit Authorization Package Prompt

## Purpose
To assemble a review package specifically tailored for requesting human commit authorization, ensuring all files in scope are verified against the declared task boundaries.

## When to use
Use this prompt after a successful human review, when you need to formally present the final diff summary and file list to secure explicit commit authorization from a human owner.

## Commands or helper entrypoint
```bash
python3 aos/scripts/aos_review_package.py --mode commit-authorization --task-id <TASK_ID> --files <LIST_OF_FILES> --target-branch <TARGET_BRANCH> --format markdown
```

## Required safety notes
- Commit authorization package is not commit authorization.
- Human must explicitly authorize commit separately.
- Commit authorization is not push authorization.
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Remote closure verification is not release authorization.
- Push authorization is not release authorization.
- PASS ≠ approval.
- Evidence ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Skeleton ≠ implementation.
- Scope must not expand without explicit human permission.
- Protected/canonical changes require human checkpoint.
- Destructive operations are forbidden by default.
- Human decision required.

## What this template does not authorize
This template does not authorize commits, pushes, merges, or the execution of staging commands.

## Expected final status
`COMMIT AUTHORIZATION PACKAGE STATUS: READY_FOR_HUMAN_DECISION`
