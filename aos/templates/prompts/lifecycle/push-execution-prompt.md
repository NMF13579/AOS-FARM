# Push Execution Prompt

## Purpose
To execute a git push operation to upload local commits to the designated remote repository.

## When to use
Use only after explicit human push authorization.

## Commands or helper entrypoint
```bash
git push origin HEAD
```
*(No helper script exists for mutation; use native git commands under strict explicit authorization.)*

## Required safety notes
- Use only after explicit human push authorization.
- Do not merge.
- Do not release.
- Push Evidence is not approval.
- Push authorization is not release authorization.
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Remote closure verification is not release authorization.
- Commit authorization is not push authorization.
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
This template does not authorize merges into trunk, the creation or publishing of release artifacts, or further execution beyond the push itself.

## Expected final status
`PUSH STATUS: PUSHED`
