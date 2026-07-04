# Commit Execution Prompt

## Purpose
To execute a git commit operation strictly on an authorized subset of files.

## When to use
Use only after explicit human commit authorization. Use this to stage and commit the declared scope of files.

## Commands or helper entrypoint
```bash
git add <AUTHORIZED_FILES>
git commit -m "<COMMIT_MESSAGE>"
```
*(No helper script exists for mutation; use native git commands under strict explicit authorization.)*

## Required safety notes
- Use only after explicit human commit authorization.
- Do not push.
- Commit Evidence is not approval.
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Remote closure verification is not release authorization.
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
This template does not authorize pushes, merges, release generation, or commits outside the explicitly authorized file scope. 

## Expected final status
`COMMIT STATUS: COMMITTED`
