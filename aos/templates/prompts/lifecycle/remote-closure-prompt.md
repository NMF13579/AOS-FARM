# Remote Closure Verification Prompt

## Purpose
To verify the synchronization state between the local branch and the target remote branch, ensuring no undetected drift or missed upstream commits exist before proceeding with handoffs or reviews.

## When to use
Use this prompt as a safety verification step prior to submitting review packages or generating final lifecycle status reports.

## Commands or helper entrypoint
```bash
python3 aos/scripts/aos_remote_closure_check.py --target dev
```

## Required safety notes
- Remote closure verification is Evidence, not approval.
- Remote closure verification is not release authorization.
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Commit authorization is not push authorization.
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

## What this template does not authorize
This template does not authorize git fetches, pulls, merges, rebases, commits, pushes, or releases.

## Expected final status
`REMOTE CLOSURE STATUS: REMOTE_CLOSURE_VERIFIED` (if cleanly synchronized)
