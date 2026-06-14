# UNKNOWN / NOT_RUN / PASS Semantics Template

## 1. Task Identity
- Task ID: 

## 2. Status Definitions
UNKNOWN → BLOCKED or HUMAN_REVIEW_REQUIRED unless explicitly resolved.
NOT_RUN → not PASS.
BLOCKED → not PASS.
PASS → validation result only, not approval.
PASS_WITH_WARNINGS → validation result with non-blocking warnings, not approval.

## 3. Status Evidence Requirements
- Evidence required for each status.

## 4. Forbidden Status Conversions
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.

## 5. Fail-Closed Requirements
- Fail-closed required.

## 6. Final Status Semantics
- Applied semantics for this task.
