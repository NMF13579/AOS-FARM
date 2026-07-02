# Review and Handoff Package

> **GUIDANCE BOUNDARY:**
> This document is guidance only.
> It does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

## Purpose
The Review & Handoff Package Generator compiles a summary of the current branch state relative to a given baseline (e.g., `origin/dev`). It helps human reviewers understand what has changed before they provide explicit authorization for commits or pushes.

The package status is strictly derived from the git state and optional validation checks. 

**Allowed package statuses are:**
- `READY_FOR_HUMAN_REVIEW`
- `CHANGES_REQUIRED`
- `BLOCKED`
- `UNKNOWN_BLOCKED`
- `HUMAN_REVIEW_REQUIRED`

**The package generator will NEVER output `APPROVED`.**

## Commands

Default inspection (read-only git check, NO validation):
```bash
python3 aos/scripts/aos_review_package.py --since origin/dev
```

Default inspection with JSON output:
```bash
python3 aos/scripts/aos_review_package.py --since origin/dev --json
```

Include validation checks (runs AOS Validate):
```bash
python3 aos/scripts/aos_review_package.py --since origin/dev --include-validation
```

Include validation checks with JSON output:
```bash
python3 aos/scripts/aos_review_package.py --since origin/dev --include-validation --json
```

## Mandatory Boundary Statement

```text
This tool produces a review package.
It does not approve execution, commit, push, merge, release,
or lifecycle transition.

The tool output is not approval.
validation_status: NOT_RUN is not PASS.
```
