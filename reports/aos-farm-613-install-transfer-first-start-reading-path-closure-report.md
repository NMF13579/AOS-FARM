# AOS-FARM.613 — Installation, Transfer, and First-Start Reading Path Closure Report

## 1. Stage title
Installation, Transfer, and First-Start Reading Path Closure

## 2. Baseline
- origin/dev: `47a6e46b99c384c14f988837273b39acf855537b`
- Tracked worktree: clean (prior to branch checkout)
- Known untracked: `.venv/`

## 3. Branch
- `build/aos-farm-613-install-transfer-first-start`

## 4. Risk Profile assignment
- Assigned by Human: `MEDIUM_RISK_GUIDED`

## 5. Scope
- Repair root templates (placeholders -> actual files)
- Align docs for single reading path
- Align prompt-pack boundaries
- Add tests for dry-run install and templates
- Clarify install transfer instructions without implementing `--apply`

## 6. Changed files
- `aos/docs/INSTALL-AND-TRANSFER.md` (Created)
- `aos/root/ROOT_INSTALL_GUIDE.md`
- `aos/root/ROOT_FILES_MANIFEST.md`
- `aos/root/README_AOS_SECTION.md`
- `aos/root/gitignore.snippet`
- `aos/README.md`
- `aos/INSTALL.md`
- `aos/docs/INSTALL.md`
- `aos/docs/FIRST-START.md`
- `aos/docs/START-RU.md`
- `aos/prompt-packs/codex.md`
- `aos/prompt-packs/cursor.md`
- `aos/prompt-packs/gemini.md`
- `aos/prompt-packs/chatgpt.md`
- `tests/test_aos_install.py` (Created)
- `tests/test_aos_root_templates.py` (Created)

## 7. Install contract summary
- Installer `--apply` remains explicitly `NOT_IMPLEMENTED`.
- The supported path is manual transfer as detailed in `aos/docs/INSTALL-AND-TRANSFER.md`.
- Dry-run successfully validates target file system and displays what is missing, but does not deploy files.
- The corrected dry-run contract ensures:
  - `.gitignore.template` is mapped to `/.gitignore` only when no target `.gitignore` exists.
  - `gitignore.snippet` is manual merge input only; it is not deployed as `/gitignore.snippet`.
  - `ROOT_INSTALL_GUIDE.md` and `ROOT_FILES_MANIFEST.md` remain `/aos/root/` reference templates; they are not required target root runtime files.

## 8. Root template repair summary
- Repaired all root templates in `aos/root/` that were formerly identical placeholders.
- `ROOT_INSTALL_GUIDE.md` details the manual transfer steps.
- `ROOT_FILES_MANIFEST.md` lists files to be transferred to the target repo.
- `README_AOS_SECTION.md` contains an advisory marker block.
- `gitignore.snippet` strictly contains `/.aos-tmp/`.

## 9. Docs alignment summary
- Created `INSTALL-AND-TRANSFER.md` as the single authoritative guide for deployment.
- Reduced `aos/README.md` to thin navigation.
- Pointed Russian docs (`START-RU.md`, `INSTALL.md`) to the main transfer guide.
- Removed duplicated steps and clarified safe first commands in `FIRST-START.md`.

## 10. Prompt-pack boundary summary
- Delineated reading paths for target repos vs the `AOS-FARM` repo.
- Instructed agents in target repos NOT to use root sources (`00`, `01`, `02`) from the target repo.
- Explicitly stated that `/AGENTS.md` and `/llms.txt` deployed to root are the runtime entrypoints for consumer target repos.

## 11. Tests run
- `python3 -m unittest discover -s tests -p 'test*.py'`
- Included new coverage for install dry run combinations and template validation.
- All 150 tests PASS.

## 12. Clean target dogfood
- Created a clean repo at `/private/tmp/aos-farm-613-clean-target/`.
- Copied `aos/` kit and ran `aos_install.py --dry-run` and `aos_consumer_self_test.py`.
- Verified status correctly identifies pending templates:
  - `package_integrity_status: PASS`
  - `target_install_state: HUMAN_REVIEW_REQUIRED`
  - `installation_readiness: MANUAL_TRANSFER_REQUIRED`
  - `reason: required root runtime entrypoints are pending_from_template`
  - `next_safe_action: manually deploy /AGENTS.md and /llms.txt, handle .gitignore, then rerun self-test`

## 13. Full snapshot dogfood
- Full snapshot dogfood inside `AOS-FARM` returned `HUMAN_REVIEW_REQUIRED` correctly because target files like `AGENTS.md` and `llms.txt` already exist in the repository root (expected conflict handling).

## 14. Known local blockers
- The script `write_report.py` was found in `/.aos-tmp/`, which triggers a `HUMAN_REVIEW_REQUIRED` warning in `aos_consumer_self_test.py` as a Source of Truth artifact found in the temporary workspace. Cleanup was NOT performed as it lacks human authorization.

## 15. NOT_RUN list
- Implementation of installer `--apply` was explicitly not run as it is forbidden.
- `aos/scripts/aos_task_document_check.py task --validate-all` ran, but we did not implement missing features in the installer script itself.
- Local temp workspace cleanup was not run.

## 16. UNKNOWN/BLOCKED list
- No critical UNKNOWNs remain for this task.
- `aos_install.py --apply` remains explicitly `BLOCKED`.

## 17. Approval boundary
- Approval is requested for these scoped changes.

## 18. Commit/push boundary
- `AOS COMMIT OK` and `AOS PUSH OK` are required from human for final check-in.

## 19. Next-stage recommendation
- Proceed with onboarding and Documentation Assembly Pipeline steps as planned in the roadmap.

---

```yaml
approval_status: NOT_REQUESTED
execution_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
```
