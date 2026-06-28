# AOS-FARM.449 Lessons Learned

## What We Learned

1. **Explicit Invariants in CLI Tools Help Humans and Agents:** By printing explicit warnings to `stderr` (e.g., "Queue position ≠ approval"), the CLI helper immediately grounds the human and the agent reading the log, reducing the chance of falsely interpreting outputs.
2. **Without History, State Misalignment Checks Are Essential:** Because the registry represents the current state rather than a history of transitions, invalid transitions (e.g. CANDIDATE -> IN_PROGRESS) can only be caught if the metadata (`lifecycle_stage`, `registry_status`, `final_status`) are tightly bound and checked for contradictions.
3. **UNKNOWN Statuses Need Strict Enforcement:** If `UNKNOWN` can slip through as `PASS`, the pipeline can unknowingly accept missing data. Changing the validator to treat `UNKNOWN` as explicitly `BLOCKED/Not OK` forces the pipeline to halt and escalate.

## Pipeline Hardening Backlog Ideas (Not Authorized for Execution)

- **Backlog Item 1:** Integrate the new `aos_task_queue_helper.py` into the broader `aos_controlled_execution_guard.py` so that queue state validation happens automatically during precheck.
- **Backlog Item 2:** Implement a stricter state-machine transition logger if historical transitions need to be verified, beyond just current state misalignment.
