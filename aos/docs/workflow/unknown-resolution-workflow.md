# UNKNOWN Resolution Workflow

This document does not grant approval.
This document does not authorize execution.
This document does not authorize commit.
This document does not authorize push.
This document does not authorize release.
Human approval cannot be simulated.
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.

## Flow

1. UNKNOWN Register
2. UNKNOWN Resolution Proposal
3. Human Answer / Evidence
4. Resolution Record
5. Re-run Gate

## Allowed Statuses

- UNKNOWN_OPEN
- UNKNOWN_NEEDS_HUMAN
- UNKNOWN_NEEDS_EVIDENCE
- UNKNOWN_RESOLVED_BY_HUMAN
- UNKNOWN_RESOLVED_BY_SOURCE
- UNKNOWN_DEFERRED_WITH_SCOPE_LIMIT
- UNKNOWN_BLOCKED

## Safety Rules

- UNKNOWN cannot be deleted silently.
- UNKNOWN cannot be treated as PASS.
- UNKNOWN cannot be treated as OK.
