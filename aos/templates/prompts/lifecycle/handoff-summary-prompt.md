# Handoff Summary Prompt

## Purpose
To generate a comprehensive summary of the current state of a task before handing it off or ending a session.

## When to use
Use this prompt when you need to transition work between sessions, hand off execution to another agent, or simply record the current progress context without making execution decisions.

## Commands or helper entrypoint
```bash
python3 aos/scripts/aos_handoff_summary.py
```

## Required safety notes
- Handoff is not Source of Truth.
- Generated handoff summary is not approval.
- Next safe step is not execution authorization.
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Remote closure verification is not release authorization.
- Commit authorization is not push authorization.
- Push authorization is not release authorization.
- Merge authorization is not dev push authorization.
- Dev push requires separate exact phrase: AOS PUSH DEV OK AOS-FARM.<ID>.
- Feature branch push authorization is not dev push authorization.
- Combined local integration + remote write command is forbidden.
- Post-merge local verification required before dev push.
- Accepted violation state is not authorization precedent.
- Merge type must be explicit or default --ff-only.
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Skeleton ≠ implementation.
- Scope must not expand without explicit human permission.
- Protected/canonical changes require human checkpoint.
- Destructive operations are forbidden by default.

## What this template does not authorize
This template does not authorize any mutations, commits, pushes, approvals, merges, releases, Risk Profile assignments, or lifecycle changes.

## Expected final status
`HANDOFF SUMMARY STATUS: GENERATED` (or equivalent read-only status indicating generation success)
