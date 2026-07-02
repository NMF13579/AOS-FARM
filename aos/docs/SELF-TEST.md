# Consumer Self-Test

This document explains the Consumer Self-Test command and what it checks within an AOS-enabled repository.

## How to Run

To execute the self-test, run the following read-only command:

```bash
python3 aos/scripts/aos_consumer_self_test.py
```

## What it Checks

The self-test evaluates the environment in three distinct groups:

### 1. Package Integrity (`package_integrity`)
Verifies that all required AOS core package files, documents, and scripts are present in the repository. If core files are missing, the test will return a `BLOCKED` status.

### 2. Target Install State (`target_install_state`)
Checks the deployment state of the root templates (e.g., `llms.txt`, `AGENTS.md`, and `.github/workflows/aos-advisory.yml`).
Files can be in the following states:
- **`deployed`**: The file exists in the repository root.
- **`pending_from_template`**: The file exists in `/aos/root/` but has not been deployed to the target root.
- **`missing_template`**: The file does not exist in the templates directory.

It also enforces the workspace boundary by checking `/project/` for unexpected product code folders (like `src/`, `tests/`), returning `HUMAN_REVIEW_REQUIRED` if any are found.

### 3. Safety Boundaries (`safety_boundaries`)
The script will explicitly print the immutable safety invariants of the AOS control framework.

## Status Meanings

- **`PASS`**: All required package files are present, and no target workspace violations exist.
- **`PASS_WITH_WARNINGS`**: The package is usable, but non-critical warnings exist (such as a missing optional advisory template).
- **`HUMAN_REVIEW_REQUIRED`**: Potential conflicts exist or unexpected product code folders are present. A human owner must review the state.
- **`BLOCKED`**: Required core package files are missing, rendering the environment unsafe to proceed.
- **`UNKNOWN_BLOCKED`**: The script encountered an ambiguous state and fails closed.
- **`NOT_RUN`**: A subsystem or sub-check failed to execute.

## Critical Safety Invariants

The self-test is strictly **read-only**. It may execute installer dry-run as read-only Evidence; it never executes installer apply. It will never mutate files or create folders.

Furthermore:
- Self-test `PASS` is **not** approval.
- Self-test `PASS` is **not** permission to apply the installer.
- Self-test `PASS` does **not** grant commit, push, or release permission.
- `UNKNOWN` conditions always fail closed.
- Human approval cannot be simulated.
