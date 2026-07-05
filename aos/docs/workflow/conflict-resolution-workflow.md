# Conflict Resolution Workflow

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

## Source Priority

1. AOS Core / Governance invariants
2. explicit human decision in current project context
3. accepted Architecture Brief / ADR
4. current Technical Assignment
5. existing user architecture document
6. stack preset
7. reference architecture
8. agent inference/default

## Safety Rules

- Agent inference never has authority.
- External document is input, not approval.
- Stack preset is recommendation, not approval.
- Reference architecture is reference only.

## Allowed Statuses

- CONFLICT_OPEN
- CONFLICT_BLOCKED
- CONFLICT_NEEDS_HUMAN
- CONFLICT_RESOLVED_BY_HUMAN
- CONFLICT_RESOLVED_BY_SOURCE
- CONFLICT_DEFERRED_WITH_SCOPE_LIMIT
