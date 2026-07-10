# AOS-FARM.674 Evidence Report
**Goal**: Python Environment Reproducibility, Doctor Interpreter Integrity, Workspace Duplicate Audit and Preventive Lesson

## 1. Baseline Verification
- **Branch**: `build/aos-farm-674-python-environment-doctor-hygiene`
- **HEAD Baseline**: `6415578` (matches exact state of AOS-FARM.673 remote feature branch).
- **Relation to AOS-FARM.673 & origin/dev**: Safely branched off the unmerged `AOS-FARM.673` without integration into `origin/dev`.

## 2. Environment Details
- **Python Version**: `3.9.6`
- **pytest Version**: `8.4.2`
- **Dependency Declaration**: Created `requirements-dev.txt` with constraint `pytest>=8.4.2,<9`.

## 3. Interpreter Integrity (aos_doctor.py)
**Before:** Hardcoded `"python3"` literals, susceptible to PATH drift.
**After:** Uses `sys.executable` for all Python-to-Python subprocesses. Tested and proven via `tests/test_aos_doctor.py`.

## 4. Test Results & Dependency Diagnostics
### Working Environment (Positive)
- `compileall aos/scripts tests`: PASS
- `pytest`: 504 passed in ~67s (Exit Code 0)
- `aos_doctor.py`: PASS (overall status PASS)
- `aos_validate.py --json`: Exit Code 1. Overall status `HUMAN_REVIEW_REQUIRED`. Child technical checks are `PASS` (confirmed by `"structural_status": "PASS"` in JSON).

### Clean Environment
- `venv` creation and `pip install -r requirements-dev.txt`: SUCCESS
- `pytest`: PASS (504 tests executed successfully)
- `aos_doctor.py`: PASS
- `aos_validate.py --json`: Exit Code 1. Overall status `HUMAN_REVIEW_REQUIRED`. Child technical checks are `PASS` (confirmed by JSON payload).

### Negative Dependency Test
In an isolated environment without `pytest`:
- **Dependency check** `import pytest`: FAILED with diagnostic message containing missing dependency, correct `sys.executable`, authoritative `requirements-dev.txt`, and installation command.
- **Pytest-dependent test discovery**: NOT_RUN (skipped).
- **Independent checks**: Continued execution normally.
- **Aggregate Status**: FAILED_OR_BLOCKED (fail-closed, not PASS).
- **No mutations**: Doctor did not execute `pip` or modify the environment.

## 5. Duplicate Audit Summary
- **175** EXACT_DUPLICATE
- **7** CONTENT_DIVERGED
- **0** deleted files (read-only audit).
- **Divergent Files:**
  1. `aos/scripts/aos_architecture_document_check 2.py`
  2. `aos/scripts/aos_lifecycle_state 2.py`
  3. `aos/templates/architecture-brief-template 2.md`
  4. `aos/templates/architecture-input-intake-template 2.md`
  5. `aos/templates/compact/compact-safe-path-template 2.md`
  6. `aos/templates/task-breakdown-from-architecture-template 2.md`
  7. `tests/test_aos_architecture_document_check 2.py`

## 6. Changed-File Inventory
- `requirements-dev.txt` (NEW)
- `aos/scripts/aos_doctor.py` (MODIFIED)
- `tests/test_aos_doctor.py` (MODIFIED)
- `aos/docs/LESSONS-LEARNED.md` (MODIFIED)
- `reports/aos-farm-674-evidence-report.md` (NEW)

## 7. Protected Boundary Confirmations
- **CONTENT_DIVERGED Files**: UNCHANGED (not touched, deleted, merged, or read as canonical).
- `pytest.ini`: UNCHANGED
- `aos/scripts/aos_validate.py`: UNCHANGED
- `00_AOS_Core_Control.md`: UNCHANGED
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: UNCHANGED
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: UNCHANGED

## 8. Commit and Push Status
- **Commit Status**: NOT_COMMITTED
- **Push Status**: NOT_PUSHED
