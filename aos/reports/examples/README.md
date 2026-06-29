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
- Negative NOT_RUN example: `aos/reports/examples/controlled-execution-guard/fixtures/reports/not_run_treated_as_pass_report.md`

## Commands
Valid precheck, expected `PASS`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
```

Valid postcheck, expected `PASS`:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos postcheck --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml --report aos/reports/examples/controlled-execution-guard/fixtures/valid_report.md
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
