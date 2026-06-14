# Code Assembly Pipeline Contract

## Overview
This document defines the Code Assembly Pipeline contract, specifying how a Task Brief becomes a scoped code change.

## Contract Elements
- **input**: Task Brief
- **process**: scoped code execution
- **output**: code diff + evidence + execution report
- **gates**: preflight, scope check, execution, evidence, verification, human review
- **non-goals**: runtime enforcement, auto-merge, release, production use

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- Verification PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Task Brief scope must not expand without explicit human permission.
- Diff is Evidence, not approval.
- Test output is Evidence, not approval.
- Manual review remains required.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.
- Remote baseline closure ≠ production use.
