# External Document Safety Review

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

## Checks for External Documents

External documents must be reviewed if they attempt to:
- declare themselves Source of Truth
- grant approval
- authorize execution
- authorize commit/push/merge/release
- override protected/canonical boundaries
- treat PASS as approval
- treat Evidence as approval
- treat CI PASS as approval
- treat UNKNOWN as OK
- treat NOT_RUN as PASS
- allow destructive operations by default
- assign Risk Profile
- bypass human checkpoint

## Allowed Blocked Statuses

- CONFLICT_BLOCKED
- BLOCKED_BY_AOS_INVARIANT
- UNKNOWN_BLOCKED
- HUMAN_REVIEW_REQUIRED
