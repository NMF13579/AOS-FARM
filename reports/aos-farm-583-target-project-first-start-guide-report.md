# AOS-FARM.583 — Target Project First-Start Guide Report

## State
- **Branch:** `dev`
- **HEAD:** 06b317c686bf62d282059ef93e013df190cdab36
- **origin/dev HEAD:** f9b0d1cb3640a829a582e499905b4e217c8061e6
- **Operational mode:** LOCAL_STACK_UNPUSHED
- **Local stack summary:**
  - `06b317c` AOS-FARM.582: Documentation Workspace and Module Boundary

## Files Changed
- `[NEW]` `aos/docs/FIRST-START.md`
- `[MODIFIED]` `aos/docs/START-RU.md`
- `[MODIFIED]` `aos/docs/INSTALL.md`
- `[MODIFIED]` `aos/docs/ROUTES.md`
- `[NEW]` `reports/aos-farm-583-target-project-first-start-guide-report.md`

## Documentation Summary
Created `aos/docs/FIRST-START.md` as the authoritative first-start guide for non-programmers navigating AOS in a target project. Updated `START-RU.md` and `INSTALL.md` to point users to this guide. Added the route to `ROUTES.md`.

## First-Start Guide Summary
- **First Agent Route:** Explains the chain from `AGENTS.md` -> `llms.txt` -> AOS docs and rules.
- **First Safe Commands:** Directs the user to run `aos_install.py --dry-run` and `aos_consumer_self_test.py`, explicitly stating they only produce Evidence and do not grant approval.
- **Conflict Handling:** Instructs stopping and reporting `HUMAN_REVIEW_REQUIRED` if the dry-run reports existing files. No silent overrides.
- **Expected Files:** Defines the core elements (`/llms.txt`, `/AGENTS.md`, `/aos/`, `/project/`, `/aos-modules/`, `/.aos-tmp/`).
- **Authorization:** Directs the user to use exact authorization commands (`AOS COMMIT OK`, `AOS PUSH OK`, `AOS MICRO COMMIT+PUSH OK`) and clarifies that intent words (`commit`, `push`, `комит`) are not enough.
- **Safety Invariants:** Explicitly restates that `PASS ≠ approval`, `Evidence ≠ approval`, `self-test PASS ≠ approval`, and `dry-run PASS ≠ approval`.
- **What not to do:** Highlights the danger of running apply without approval or storing truth in `/.aos-tmp/`.

## Validation Commands Run
```bash
python3 aos/scripts/aos_consumer_self_test.py
python3 aos/scripts/aos_install.py --dry-run
python3 -m py_compile aos/scripts/aos_consumer_self_test.py
python3 -m pytest tests/test_aos_consumer_self_test.py
git status -sb
git diff --stat
git diff --name-status
git log --oneline origin/dev..HEAD
find aos/docs -maxdepth 2 -type d | sort
```

## Validation Results
- Python syntax compilation passed cleanly.
- `pytest` executed successfully (6 passing unit tests).
- `aos_consumer_self_test.py` ran standalone with no new warnings.
- `aos_install.py --dry-run` executed safely, recorded as Evidence only.
- `git diff` shows only the allowed documentation files.
- `git log` confirms the expected local stack.

## Duplicate Folder Warning
> [!WARNING]
> Duplicate documentation folders (e.g. `assembly 2/`, `governance 2/`, etc.) exist under `aos/docs`. As explicitly instructed, they were **not** deleted, merged, or renamed. They are logged here as a warning.

## Safety Checks
- [x] No modifications to `00_AOS_Core_Control.md`, `01`, `02`, `aos_install.py`, `aos_consumer_self_test.py`, tests, or templates.
- [x] Installer apply was not implemented.
- [x] Update check/apply was not implemented.
- [x] Autonomous executor, release automation, or additional agent adapters were not implemented.
- [x] Duplicate folders were not deduplicated.

## Explicit Statements
- **Commit:** No commit was made.
- **Push:** No push was made.
- **Approval:** Documentation updates, Evidence generation, self-test PASS, and dry-run PASS do **NOT** equal approval.

## Known Limitations
- Duplicate `* 2` documentation folders still remain.

## Next Recommended Stage
`AOS-FARM.584 — Final Local Stack Review and Accumulated Push Gate`
