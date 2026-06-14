# Code Diff Evidence Expectations

## Expectations
- **diff evidence**: All changed code must be represented in a clear diff. Diff is Evidence, not approval.
- **test output evidence**: Relevant test executions must be captured and logged. Test output is Evidence, not approval.
- **manual review evidence**: A recorded manual review checkpoint is required. Manual review remains required.
- **blocked evidence**: Any action blocked by the environment must be recorded as blocked evidence.
- **UNKNOWN evidence**: System states that cannot be determined must be explicitly logged. UNKNOWN ≠ OK.
- **NOT_RUN evidence**: Required actions that were bypassed or skipped must be logged. NOT_RUN ≠ PASS.

## Invariants
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- Verification PASS ≠ approval.
- Human approval cannot be simulated.
