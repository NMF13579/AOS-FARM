---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Negative Fixture: NOT_RUN Treated As PASS

expected_result: BLOCKED
violation: NOT_RUN incorrectly treated as PASS

source_task_id: GENERIC-TASK.NEGATIVE
validation_results:
  markdown_lint: NOT_RUN
final_claim: all validation PASS
status: DRAFT

Why blocked:
- NOT_RUN ≠ PASS.
- UNKNOWN ≠ OK.
- Validator PASS ≠ approval.
