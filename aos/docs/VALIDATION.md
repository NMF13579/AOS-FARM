# Unified Validation

> **GUIDANCE BOUNDARY:**
> This document is guidance only.
> It does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

## Purpose

AOS-FARM provides a unified validation script to aggregate multiple read-only checks into a single report. 
This script is `aos/scripts/aos_validate.py`.

It orchestrates existing validation tools and checks.
It does not:
- create tasks
- mutate the task queue
- write Evidence
- claim approval
- commit, push, release, or merge
- change lifecycle state
- assign Risk Profile

## Commands

Run all validation checks:
```bash
python3 aos/scripts/aos_validate.py all
```

Output as JSON (useful for agents):
```bash
python3 aos/scripts/aos_validate.py all --json
```

## Mandatory Boundary Statement

```text
These commands produce validation signals and Evidence.
They do not approve execution, commit, push, merge, release,
or lifecycle transition.

PASS output from any command is not approval.
Evidence produced by any command is not approval.
CI PASS is not approval.
NOT_RUN is not PASS.
UNKNOWN is not OK.
```
