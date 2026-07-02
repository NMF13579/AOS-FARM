# AOS-FARM.585 — Consumer First-Start Dogfood Report

## 1. Stage Info
**Stage Title:** AOS-FARM.585 — Consumer First-Start Dogfood
**Branch:** dev
**Local HEAD:** 3ffc23bbf6bf080d95d74b97572386ec4b68d840
**Origin/dev HEAD:** 3ffc23bbf6bf080d95d74b97572386ec4b68d840
**Branch Alignment Result:** Aligned (`0 0` left-right difference). Working tree is clean of unrelated tracked changes.

## 2. Files Inspected
- `aos/root/AGENTS.md`
- `aos/root/llms.txt`
- `aos/docs/ROUTES.md`
- `aos/docs/FIRST-START.md`
- `aos/docs/WORKSPACE-BOUNDARY.md`
- `aos/docs/AUTHORIZATION-COMMANDS.md`
- `aos/docs/INSTALL.md`
- `aos/docs/SELF-TEST.md`

## 3. Commands Run
```bash
git branch --show-current
git fetch origin
git rev-parse HEAD
git rev-parse origin/dev
git rev-list --left-right --count origin/dev...HEAD
git status -sb
git log --oneline -5
python3 aos/scripts/aos_install.py --dry-run
python3 aos/scripts/aos_consumer_self_test.py
python3 tests/test_aos_consumer_self_test.py (Fallback since pytest was unavailable)
git diff --stat
git diff --name-status
find aos/docs -maxdepth 2 -type d | sort
```

## 4. Command Results
- **Git Alignment:** Verified correct.
- **Dry-run (`aos_install.py --dry-run`):** Executed safely as read-only. Yielded `HUMAN_REVIEW_REQUIRED` due to existing target files (e.g., `llms.txt`, `AGENTS.md`). Emitted safety invariants (dry-run PASS is not approval).
- **Self-Test (`aos_consumer_self_test.py`):** Package Integrity `PASS`, Target Install State `PASS` (deployed). Emitted safety invariants. Overall final status `PASS`.
- **Pytest Fallback:** `test_aos_consumer_self_test.py` completed successfully (`Ran 6 tests in 0.004s, OK`).
- **Diff:** Empty diff, confirming zero product docs or code were mutated.
- **Find Duplicate Folders:** Detected duplicate `* 2` folders in `aos/docs` (e.g., `aos/docs/assembly 2`, `aos/docs/governance 2`, etc.).

## 5. First-Start Route Result
- The route successfully mapped `AGENTS.md` -> `llms.txt` -> `ROUTES.md` -> `FIRST-START.md`.
- `FIRST-START.md` clearly instructs a non-programmer on the safe initial commands to run (`--dry-run` and `self-test`), and sets expectations about conflicts and workspace boundaries.

## 6. Target Checks
- **Dry-Run Result:** Correct behavior observed. Read-only validation; apply explicitly NOT_IMPLEMENTED.
- **Self-Test Result:** Correct behavior observed. `PASS` achieved without approval assumption.
- **Workspace Boundary Result:** `WORKSPACE-BOUNDARY.md` correctly models `/aos/`, `/aos/root/`, `/project/`, `/aos-modules/`, and `/.aos-tmp/`. It mandates `/.aos-tmp/` is never a Source of Truth.
- **Authorization Command Result:** `AUTHORIZATION-COMMANDS.md` successfully defines strict exact commands (`AOS COMMIT OK`, `AOS PUSH OK`, `AOS MICRO COMMIT+PUSH OK`) and downgrades plain language to intent only.
- **PASS/Evidence/Approval Safety Result:** Checked extensively across `FIRST-START.md`, `INSTALL.md`, and `SELF-TEST.md`. Dry-run PASS, self-test PASS, CI PASS, and Evidence are explicitly marked as NOT approval. Commit authorization ≠ push authorization. Human approval cannot be simulated.

## 7. Warnings and Defects
- **Duplicate Folder Warning:** Detected duplicated directory trees in `/aos/docs/` (e.g. `assembly 2`, `lifecycle 2`, etc.). These folders were intentionally untouched as cleanup was forbidden in this stage.
- **Defects Found:** No blocking documentation defects found.
- **Fixes Needed:** No fixes needed for the documentation workflow itself. (Duplicate folders should be cleaned up in a separate hygiene stage if necessary).

## 8. Safety & Compliance Statements
- **Explicit Statement:** No commit was made.
- **Explicit Statement:** No push was made.

## 9. Final Verdict
**Final Dogfood Verdict:** PASS_WITH_WARNINGS (due to duplicate docs folders).

## 10. Next Recommended Stage
**Next recommended stage:** AOS-FARM.586 — Consumer Corridor Final Closure Review
