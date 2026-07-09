# Push Authorization Package Prompt

## Purpose
To assemble a review package tailored for requesting human push authorization, detailing the commits and state ready to be pushed to the remote repository.

## When to use
Use this prompt after commits are successfully completed and verified, and you need explicit human authorization before executing a push to the remote branch.

## Commands or helper entrypoint
```bash
python3 aos/scripts/aos_review_package.py --mode push-authorization --task-id <TASK_ID> --files <LIST_OF_FILES> --target-branch <TARGET_BRANCH> --format markdown
```

## Required safety notes
- Push authorization package is not push authorization.
- Human must explicitly authorize push separately.
- Push authorization is not release authorization.
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Remote closure verification is not release authorization.
- Commit authorization is not push authorization.
- Merge authorization is not dev push authorization.
- Dev push requires separate exact phrase: AOS PUSH DEV OK AOS-FARM.<ID>.
- Feature branch push authorization is not dev push authorization.
- Combined local integration + remote write command is forbidden.
- Post-merge local verification required before dev push.
- Accepted violation state is not authorization precedent.
- Merge type must be explicit or default --ff-only.
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
This template does not authorize pushes, merges, commits, or the creation of releases.

## Expected final status
`PUSH AUTHORIZATION PACKAGE STATUS: READY_FOR_HUMAN_DECISION`
