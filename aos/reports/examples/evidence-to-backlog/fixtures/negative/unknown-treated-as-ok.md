# Negative Fixture: UNKNOWN Treated As OK

expected_result: BLOCKED
violation: UNKNOWN incorrectly treated as OK

source_task_id: AOS-FARM.NEGATIVE
UNKNOWN:
- whether evidence covers all changed files
final_claim: unknowns are acceptable
status: DRAFT

Why blocked:
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
