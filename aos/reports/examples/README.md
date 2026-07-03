---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# AOS Report Examples

Use these examples to copy a working shape before creating your own controlled execution package or evidence report.

## Controlled Execution Guard Examples
- Valid package example: `aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml`
- Valid report example: `aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md`
- Valid sessioncheck example: `aos/reports/examples/controlled-execution-guard/fixtures/session/valid/`
- Valid resultcheck example: `aos/reports/examples/controlled-execution-guard/fixtures/result/valid/`
- Negative NOT_RUN example: `aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md`
- Negative sessioncheck examples: `task-id-mismatch`, `request-id-mismatch`, `approval-claimed`, and `missing-handoff` under `aos/reports/examples/controlled-execution-guard/fixtures/session/`
- Negative resultcheck examples: `task-id-mismatch`, `approval-status-approved`, `blockers-present`, and `known-unknowns-present` under `aos/reports/examples/controlled-execution-guard/fixtures/result/`

## Commands
Valid precheck, expected `PASS`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
```

Valid postcheck, expected `PASS`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
```

Valid sessioncheck, expected `SESSION_CONSISTENCY_PASS`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos sessioncheck --request aos/reports/examples/controlled-execution-guard/fixtures/session/valid/request.json --preconditions aos/reports/examples/controlled-execution-guard/fixtures/session/valid/preconditions.json --boundary aos/reports/examples/controlled-execution-guard/fixtures/session/valid/boundary.json --record aos/reports/examples/controlled-execution-guard/fixtures/session/valid/record.json
```

Sessioncheck missing handoff, expected `SESSION_CONSISTENCY_NOT_READY`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos sessioncheck --request aos/reports/examples/controlled-execution-guard/fixtures/session/missing-handoff/request.json --preconditions aos/reports/examples/controlled-execution-guard/fixtures/session/missing-handoff/preconditions.json --boundary aos/reports/examples/controlled-execution-guard/fixtures/session/missing-handoff/boundary.json --record aos/reports/examples/controlled-execution-guard/fixtures/session/missing-handoff/record.json
```

Valid resultcheck, expected `RESULT_VERIFICATION_READY_FOR_HUMAN_REVIEW`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos resultcheck --session-record aos/reports/examples/controlled-execution-guard/fixtures/result/valid/session-record.json --result-package aos/reports/examples/controlled-execution-guard/fixtures/result/valid/result-package.json
```

Resultcheck with NOT_RUN disclosed, expected `RESULT_VERIFICATION_READY_WITH_LIMITATIONS`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos resultcheck --session-record aos/reports/examples/controlled-execution-guard/fixtures/result/not-run/session-record.json --result-package aos/reports/examples/controlled-execution-guard/fixtures/result/not-run/result-package.json
```

Resultcheck known unknowns present, expected `RESULT_VERIFICATION_NOT_READY`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos resultcheck --session-record aos/reports/examples/controlled-execution-guard/fixtures/result/known-unknowns-present/session-record.json --result-package aos/reports/examples/controlled-execution-guard/fixtures/result/known-unknowns-present/result-package.json
```

Resultcheck approval status approved, expected `RESULT_VERIFICATION_BLOCKED`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos resultcheck --session-record aos/reports/examples/controlled-execution-guard/fixtures/result/approval-status-approved/session-record.json --result-package aos/reports/examples/controlled-execution-guard/fixtures/result/approval-status-approved/result-package.json
```

Negative NOT_RUN example, expected `BLOCKED`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md
```

## Safety Notes
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Commit and push require separate human authorization.
- `SESSION_CONSISTENCY_PASS` is not approval.
- `RESULT_VERIFICATION_READY_FOR_HUMAN_REVIEW` is not approval.
- `RESULT_VERIFICATION_READY_WITH_LIMITATIONS` is not approval.
- postcheck PASS is not approval.
