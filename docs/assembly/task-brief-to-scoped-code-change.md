# Task Brief to Scoped Code Change

## Definition
This document defines how a Task Brief is converted into a strictly scoped code change.

## Elements
- **authorized files**: The explicit set of files permitted to be created, read, updated, or deleted.
- **allowed changes**: Explicitly listed permitted actions.
- **forbidden changes**: Explicitly listed prohibited actions.
- **scope expansion rule**: Task Brief scope must not expand without explicit human permission.
- **protected/canonical boundary**: Protected and canonical files cannot be modified without specific elevated human authorization.
- **human checkpoint requirement for expansion**: Any deviation or expansion from the Task Brief requires a new or updated human checkpoint.

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- Verification PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
