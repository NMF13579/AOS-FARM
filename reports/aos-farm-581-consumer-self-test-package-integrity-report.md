# AOS-FARM.581 — Consumer Self-Test / Package Integrity

## State
- **Branch:** `dev`
- **HEAD:** `513e5192c06d91137d1969ea7f8558ed8e0651a7`
- **origin/dev HEAD:** `513e5192c06d91137d1969ea7f8558ed8e0651a7`
- **Branch Alignment Result:** Aligned (0 0 difference)

## Files Changed
- `[NEW]` `aos/scripts/aos_consumer_self_test.py`
- `[NEW]` `aos/docs/SELF-TEST.md`
- `[NEW]` `tests/test_aos_consumer_self_test.py`
- `[MODIFIED]` `aos/docs/ROUTES.md`
- `[NEW]` `reports/aos-farm-581-consumer-self-test-package-integrity-report.md`

## Self-Test Behavior Summary
Implemented a new python script `aos/scripts/aos_consumer_self_test.py` that verifies:
1. **Package Integrity**: All required AOS core files and scripts exist in the repository.
2. **Target Install State**: Inspects if `llms.txt`, `AGENTS.md`, and `.github/workflows/aos-advisory.yml` are deployed, missing, or pending from templates. Verifies no default product code folders exist in the `/project/` workspace.
3. **Safety Boundaries**: Explicitly lists immutable safety invariants.

The script outputs a human-readable summary followed by a machine-readable JSON block. It is strictly read-only and does not mutate any files or simulate human approval.

## Self-Test Output Summary
- When executed, `python3 aos/scripts/aos_consumer_self_test.py` successfully completed all checks.
- Output included states: `PASS` for package integrity and safety boundaries, and accurately reflected the environment's `target_install_state`.
- All safety statements (e.g. `PASS ≠ approval`) were explicitly printed.
- Returned proper exit code (0 for PASS/PASS_WITH_WARNINGS, 1 for BLOCKED).

## Installer Dry-Run Relation
- The self-test leverages `subprocess.run` to safely execute `python3 aos/scripts/aos_install.py --dry-run` and captures its output as Evidence only.
- It explicitly logs that dry-run PASS/HUMAN_REVIEW_REQUIRED is Evidence only and not approval.
- It **never** invokes `--apply`.

## Validation Commands Run
```bash
python3 -m py_compile aos/scripts/aos_consumer_self_test.py
python3 -m pytest tests/test_aos_consumer_self_test.py
python3 aos/scripts/aos_consumer_self_test.py
python3 aos/scripts/aos_install.py --dry-run
find aos/docs -maxdepth 2 -type d | sort
git status -sb
git diff --stat
git diff --name-status
```

## Validation Results
- Python compilation passed cleanly.
- `pytest` executed successfully (5 passing unit tests), verifying package integrity checks, state representations, safety statements, and immutability.
- `aos_consumer_self_test.py` executed cleanly as a standalone script.
- Dry-run successfully captured as Evidence.
- `git status` confirmed only authorized scope files were added/modified. No product code was generated or altered.

## Duplicate Folder Warning
> [!WARNING]
> Duplicate documentation folders were detected under `aos/docs` (e.g., `assembly 2/`, `governance 2/`, `lifecycle 2/`, `operations 2/`, `reference 2/`, `user-guide 2/`, `workflow 2/`). No cleanup was performed as deduplication is out of scope. These are merely logged as a known warning.

## Safety Checks
- [x] No modifications to `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- [x] Self-test logic does not execute `installer apply`.
- [x] Self-test does not perform `git commit` or `git push`.
- [x] Self-test logic does not simulate approval.

## Explicit Statements
- **Commit:** No commit was made.
- **Push:** No push was made.
- **Approval:** self-test PASS or Evidence generation does **NOT** equal approval.

## Known Limitations
- The script uses `subprocess.run` to invoke the dry run which adds minor execution overhead, but ensures strict sandbox encapsulation of the installer's stdout logic.

## Next Recommended Stage
`AOS-FARM.582 — Documentation Workspace and Module Boundary`
*(or `AOS-FARM.580B — Additional Agent Entrypoint Adapters` if additional environment entrypoints are required).*

---

### AOS-FARM.581 STATUS: READY_FOR_REVIEW
