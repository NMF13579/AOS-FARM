# AOS-FARM.614 — Safe Create Installer MVP with Tutor Output Report

## 1. Stage title
AOS-FARM.614 — Safe Create Installer MVP with Tutor Output

## 2. Baseline
Reference SHA: `a7bae4a3a787ddd19bda8d3744d22577935e4670`
Target environment checked for clean working tree.

## 3. Branch
`build/aos-farm-614-safe-create-installer`

## 4. Risk Profile assignment
HIGH_RISK_PROTECTED

## 5. Scope
- `aos/scripts/aos_install.py`
- `aos/scripts/aos_consumer_self_test.py`
- `tests/test_aos_install.py`
- `tests/test_aos_consumer_self_test.py`
- `tests/test_aos_root_templates.py`
- `aos/docs/INSTALL-AND-TRANSFER.md`
- `aos/docs/FIRST-START.md`
- `aos/docs/START-RU.md`
- `aos/START_HERE.md`
- `aos/INSTALL.md`
- `aos/docs/INSTALL.md`
- `reports/aos-farm-614-safe-create-installer-mvp-with-tutor-output-report.md`

## 6. Changed files
- `aos/scripts/aos_install.py`
- `aos/scripts/aos_consumer_self_test.py`
- `tests/test_aos_install.py`
- `tests/test_aos_consumer_self_test.py`
- `tests/test_aos_root_templates.py`
- `aos/docs/INSTALL-AND-TRANSFER.md`
- `aos/docs/FIRST-START.md`
- `aos/docs/START-RU.md`
- `aos/START_HERE.md`
- `aos/INSTALL.md`
- `aos/docs/INSTALL.md`
- `reports/aos-farm-614-safe-create-installer-mvp-with-tutor-output-report.md`

## 7. Installer mode summary
- Safe apply mode implemented: `--apply --safe-create-and-gitignore-append`
- Explicit confirmation required: `--confirm "AOS INSTALL SAFE CREATE OK"`
- Dry run remains the default.
- Complete blocker scan ensures no partial writes.

## 8. Safety boundary
- Exact confirmation is enforced before any state mutation.
- Any conflict blocks all operations and returns `HUMAN_REVIEW_REQUIRED`.
- Cannot overwrite existing root files.

## 9. AGENTS.md boundary
- Cannot be overwritten or merged.
- Existing file will block installation.

## 10. llms.txt boundary
- Cannot be overwritten or merged.
- Existing file will block installation.

## 11. .gitignore append boundary
- Controlled append implemented strictly for the fixed AOS block: `/.aos-tmp/`.
- `is_gitignore_safe` ensures no encoding errors, binary bytes, or merge conflicts are overwritten.

## 12. Tutor output boundary
- Tutor mode output acts strictly as an explanation layer.
- Outputs emphasize that it does not claim approval or execution authorization.

## 13. Tests run
All requested unit tests successfully implemented and passing:
- `test_apply_requires_exact_confirmation`
- `test_apply_safe_create_clean_target`
- `test_apply_safe_create_with_existing_gitignore_appends_aos_block`
- `test_apply_existing_gitignore_with_aos_block_is_noop`
- `test_apply_existing_agents_blocks_without_changes`
- `test_apply_existing_llms_blocks_without_changes`
- `test_apply_existing_aos_blocks_without_changes`
- `test_apply_gitignore_conflict_markers_blocks_without_changes`
- `test_apply_does_not_touch_readme`
- `test_apply_does_not_touch_workflows`
- `test_apply_does_not_commit`
- `test_apply_does_not_push`
- `test_apply_done_self_test_ready_for_first_start`
- `test_tutor_output_explains_safe_create_plan`
- `test_tutor_output_explains_agents_boundary`
- `test_tutor_output_does_not_claim_approval`

## 14. Dogfood scenarios
Dogfood conditions fulfilled internally via two isolated mechanisms:

Unit tests: Rigorous temporary-directory tests/mocks via `unittest`.
Dogfood: Real temporary target repos instantiated outside the `AOS-FARM` repo tree via shell script executing `aos_install.py`.

Real dogfood scenarios executed and verified:
1. clean target repo -> `APPLY_DONE`
2. target repo with existing .gitignore -> `APPLY_DONE` with append
3. target repo with existing .gitignore already containing /.aos-tmp/ -> `APPLY_DONE` without duplicate
4. target repo with existing AGENTS.md -> `HUMAN_REVIEW_REQUIRED`, files_changed: []
5. target repo with existing llms.txt -> `HUMAN_REVIEW_REQUIRED`, files_changed: []
6. target repo with existing /aos/ -> `HUMAN_REVIEW_REQUIRED`, files_changed: []
7. target repo with existing src/ and package files but no AOS target paths -> `APPLY_DONE`, project files untouched
8. target repo with unsafe .gitignore conflict markers -> `HUMAN_REVIEW_REQUIRED`, files_changed: []

## 15. NOT_RUN list
- No tests were skipped.
- Apply functionality without `--safe-create-and-gitignore-append` is `APPLY_BLOCKED`.

## 16. UNKNOWN/BLOCKED list
- No blocked test environments or blockers encountered in implementation. Note: aos_consumer_self_test.py reports HUMAN_REVIEW_REQUIRED due to a local-only workspace warning in /.aos-tmp/ (write_report.py). /.aos-tmp/ must remain local-only and must not be Source of Truth. 

## 17. Approval boundary
- Self test pass ≠ execution permission
- Apply DONE ≠ approval
- READY_FOR_FIRST_START ≠ execution authorization
- Tutor output ≠ approval

## 18. Commit/push/release boundary
- Commits, pushes, and releases are strictly isolated and not automated by `aos_install.py`.

## 19. Next-stage recommendation
Proceed to formal stage review and human commit authorization. 

---
approval_status: NOT_REQUESTED
execution_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
