# AOS-FARM.675 Duplicate Prevention Validator Evidence

## Branch and HEAD
- Branch: build/aos-farm-675-duplicate-cleanup-prevention-gate
- HEAD: 4918b7263d6841ce9cf84a2009624d54b75ecf95

## Required Sources
- 00_AOS_Core_Control.md: Read
- 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md: Read
- 02_AOS_Governance_Control_Module_and_Safety_Rules.md: Read

## Cleanup Summary
- Exact duplicates deleted: 173
- Divergent duplicates deleted: 8
- Known cleanup Evidence limitations:
  - pre-cleanup exact manifest snapshot preserved: false
  - execution Evidence preserved: true
- **Important Restrictions**:
  - PASS ≠ approval
  - cleanup authorization ≠ commit authorization
  - commit authorization ≠ push authorization

## Validator Architecture
- **Patterns and Precedence**: 
  1. ` conflicted copy`
  2. ` copy`
  3. ` (1)`
  4. ` (2)`
  5. ` 2`
- **Path Safety**: Paths are resolved to their absolute paths and compared securely against the absolute `repository_root`. External symlinks or paths escaping the root raise `AMBIGUOUS`.
- **Classifications**: EXACT_DUPLICATE, CONTENT_DIVERGED, ORPHAN_NO_CANONICAL_PAIR, AMBIGUOUS.
- **Exit-Code Mapping**:
  - `0`: PASS
  - `1`: FAILED_OR_BLOCKED
  - `2`: HUMAN_REVIEW_REQUIRED
  - `3`: UNKNOWN_BLOCKED

## Integrations
- **Doctor Integration**: Implemented via sys.executable, safely parses JSON output of the checker, correctly applies strict precedence. `FAILED_OR_BLOCKED` and `HUMAN_REVIEW_REQUIRED` correctly block overall PASS.
- **Unified Validator Integration**: Implemented via explicit parse function. Strict status combining rules apply. No bare exceptions. Overall approval semantics untouched.

## Operational Rule
- Updated `aos/docs/LESSONS-LEARNED.md` to clarify patterns and temporary directories, avoiding naming it a safety authority.

## Verification
- **Scoped module tests**: 58 passed
- **Full test suite**: 518 passed
- **Dogfood**: Verified in active repository.
- **Clean Environment**: Executed securely in `/.aos-tmp/aos-farm-675-clean-venv/`.

## Final Workspace State
- **Checker JSON Summary**: PASS
- **Doctor Status**: PASS
- **Unified Validator Status**: PASS
- **Changed-File Inventory**: `aos/scripts/aos_duplicate_workspace_check.py`, `tests/test_aos_duplicate_workspace_check.py`, `aos/scripts/aos_doctor.py`, `tests/test_aos_doctor.py`, `aos/scripts/aos_validate.py`, `tests/test_aos_validate.py`, `aos/docs/LESSONS-LEARNED.md`, `reports/aos-farm-675-evidence-report.md`.
- **Unexpected-File Inventory**: 0 unexpected files remaining (eight temporary root scripts deleted by explicit human authorization).
- **Staging State**: 0 staged files.
- **Commit State**: No commits made.
- **Push State**: No pushes made.
