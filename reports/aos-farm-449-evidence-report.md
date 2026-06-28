# AOS-FARM.449 Evidence Report

## Validation Outputs

### Unit Test Execution
```bash
python3 -m unittest tests/test_aos_task_queue_helper.py
........
----------------------------------------------------------------------
Ran 8 tests in 0.142s
OK
```

```bash
python3 -m unittest discover -s tests
.................
----------------------------------------------------------------------
Ran 17 tests in 0.146s
OK
```

### Validator Results (Fixture tests)
- `tests/fixtures/task_queue_valid.yaml` -> PASS (Exit 0)
- `tests/fixtures/task_queue_invalid_candidate_as_approved.yaml` -> BLOCKED (Exit 1)
- `tests/fixtures/task_queue_invalid_transition.yaml` -> BLOCKED (Exit 1)
- `tests/fixtures/task_queue_missing_human_authorization.yaml` -> BLOCKED (Exit 1)

### Explicit CLI Warnings Shown
The helper script `aos/scripts/aos_task_queue_helper.py` explicitly prints to stderr on every run:
```text
WARNING: PASS ≠ approval.
WARNING: Evidence ≠ approval.
WARNING: Queue position ≠ approval.
WARNING: Next Task Candidate ≠ approved task.
WARNING: UNKNOWN is treated as BLOCKED.
WARNING: NOT_RUN is not PASS.
WARNING: Risk Profile must not be self-assigned by the agent.
WARNING: This helper is read-only. It does not authorize execution, approve tasks, assign Risk Profiles, or start tasks.
```

## Disclosures
- **UNKNOWN:** None
- **NOT_RUN:** None. The entire test suite was run (`unittest discover -s tests`).
- **Pre-existing Untracked Files:** Numerous files with suffix `" 2.md"`, `" 2.py"`, and `" 2.json"` were ignored as they are pre-existing and out of scope.
