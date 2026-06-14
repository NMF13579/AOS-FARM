# Thin Validator Checks v1

## Deterministic Check List

1. **Check 01: Scope Alignment**
   - Verifies that the files being modified exactly match the authorized scope list.
2. **Check 02: Checkpoint Presence**
   - Verifies that the required Human Authorization Checkpoint exists for the current task.
3. **Check 03: Checkpoint Signature**
   - Verifies that the `checkpoint_status` is explicitly set to an approved state (e.g., `APPROVED_FOR_EXECUTION`) by the Human Owner.
4. **Check 04: Protected/Canonical Invariants**
   - Verifies that no canonical files (e.g., `00_AOS_Core_Control.md`) are modified unless explicitly authorized by a separate, specific checkpoint.
5. **Check 05: Evidence Completeness**
   - Verifies that all required evidence documents (plans, reports) are generated and formatted correctly.
6. **Check 06: Forbidden Operations Scanning**
   - Scans proposed operations to ensure no destructive actions (e.g., `git push --force`) are being executed.

*Note: This is the specification. The actual code to execute these checks will be developed in Build Step 10.*
