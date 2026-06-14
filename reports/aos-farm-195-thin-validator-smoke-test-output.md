# Thin Validator Smoke Test Output
## Testing tests/fixtures/thin-validator/pass/minimal-valid-report.md
```text
--- Thin Validator Execution Report ---
Input: tests/fixtures/thin-validator/pass/minimal-valid-report.md
Status: PASS
Exit code: 0
```
## Testing tests/fixtures/thin-validator/fail/fake-approval-claim.md
```text
--- Thin Validator Execution Report ---
Input: tests/fixtures/thin-validator/fail/fake-approval-claim.md
Status: FAIL
- [fake_approval_claim] Found potential fake approval phrase outside human checkpoint context: 'approved: true'
Exit code: 1
```
## Testing tests/fixtures/thin-validator/fail/missing-required-field.md
```text
--- Thin Validator Execution Report ---
Input: tests/fixtures/thin-validator/fail/missing-required-field.md
Status: FAIL
- [missing_required_field] Missing required field: task_id or final_status/checkpoint_status
Exit code: 1
```
## Testing tests/fixtures/thin-validator/fail/not-run-pass-conflict.md
```text
--- Thin Validator Execution Report ---
Input: tests/fixtures/thin-validator/fail/not-run-pass-conflict.md
Status: FAIL
- [not_run_pass_conflict] Found NOT_RUN claim mixed with PASS claim
Exit code: 1
```
## Testing tests/fixtures/thin-validator/fail/unknown-ok-conflict.md
```text
--- Thin Validator Execution Report ---
Input: tests/fixtures/thin-validator/fail/unknown-ok-conflict.md
Status: FAIL
- [unknown_ok_conflict] Found UNKNOWN state mixed with OK/PASS/clean/no blockers claims
Exit code: 1
```
