# AOS Self Test Checklist

## Purpose
Manual verification of the AOS package integrity and runtime safety inside a consumer repository.

## Preconditions
- The `/aos/` directory is present.
- `llms.txt` and `AGENTS.md` are correctly installed at the repository root.

## Manual Self-Test Checklist
- [ ] Verify `aos/START_HERE.md` is accessible.
- [ ] Check that `llms.txt` points correctly to the `/aos/` boundary.
- [ ] Verify no unexpected modifications to root `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.

## Expected Results
- All checklist items pass.
- AOS commands execute without error.

## Meanings
- **PASS**: The self-test checklist items have been successfully verified. PASS ≠ approval for implementation or execution.
- **FAIL**: One or more checks failed. AOS usage is blocked until resolved.
- **NOT_RUN**: The self-test has not been executed. NOT_RUN ≠ PASS.
- **Evidence ≠ approval**.
- **No destructive operations** are authorized as part of this self-test.
