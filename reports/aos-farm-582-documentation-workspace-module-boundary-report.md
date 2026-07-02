# AOS-FARM.582 — Documentation Workspace and Module Boundary Report

## State
- **Branch:** `dev`
- **HEAD:** `f9b0d1cb3640a829a582e499905b4e217c8061e6`
- **origin/dev HEAD:** `f9b0d1cb3640a829a582e499905b4e217c8061e6`
- **Branch Alignment Result:** Aligned (0 0 difference)

## Files Changed
- `[NEW]` `aos/docs/WORKSPACE-BOUNDARY.md`
- `[MODIFIED]` `aos/docs/ROUTES.md`
- `[MODIFIED]` `aos/docs/START-RU.md`
- `[MODIFIED]` `aos/docs/INSTALL.md`
- `[MODIFIED]` `aos/scripts/aos_consumer_self_test.py`
- `[MODIFIED]` `tests/test_aos_consumer_self_test.py`
- `[NEW]` `reports/aos-farm-582-documentation-workspace-module-boundary-report.md`

## Documentation Summary
Created `WORKSPACE-BOUNDARY.md` to define the exact purpose of `/aos/`, `/aos/root/`, `/project/`, `/aos-modules/`, and `/.aos-tmp/`. Updated `START-RU.md` and `INSTALL.md` to point users to this boundary model before they execute any install changes. Added the boundary documentation to `ROUTES.md`.

## Workspace Boundary Summary
- **`/aos/`**: AOS core package (docs, scripts, templates). Not target product code. Source of Truth for AOS package.
- **`/aos/root/`**: Root templates. Not active target runtime state. Source of Truth as templates.
- **`/project/`**: Project documentation workspace. Not default source code root. Source of Truth for project docs.
- **`/aos-modules/`**: Module container. Not core package files. Source of Truth depends on the module.
- **`/.aos-tmp/`**: Temporary scratch space. Disposable. Never Source of Truth. Evidence and reports are forbidden here.

## Self-Test Relation
Updated `aos_consumer_self_test.py` to add `aos/docs/WORKSPACE-BOUNDARY.md` to package integrity checks. Added a specific check (`check_aos_tmp_boundary`) that flags a `HUMAN_REVIEW_REQUIRED` warning if any Evidence, report, or canonical files are found inside `/.aos-tmp/`. Tests were updated accordingly. No installer functionality or update functionality was implemented.

## Validation Commands Run
```bash
python3 aos/scripts/aos_consumer_self_test.py
python3 aos/scripts/aos_install.py --dry-run
python3 -m py_compile aos/scripts/aos_consumer_self_test.py
python3 -m pytest tests/test_aos_consumer_self_test.py
git status -sb
git diff --stat
git diff --name-status
find aos/docs -maxdepth 2 -type d | sort
```

## Validation Results
- Python compilation passed cleanly.
- `pytest` executed successfully (6 passing unit tests, including the new `/.aos-tmp/` boundary test).
- `aos_consumer_self_test.py` executed cleanly as a standalone script.
- Installer dry-run successfully captured as Evidence without modifying any files.
- `git status` confirmed only authorized scope files were modified.

## Duplicate Folder Warning
> [!WARNING]
> Duplicate documentation folders were detected under `aos/docs` (e.g., `assembly 2/`, `governance 2/`, `lifecycle 2/`, `operations 2/`, `reference 2/`, `user-guide 2/`, `workflow 2/`). As per strict stage requirements, they were **not** deleted, merged, or renamed. They are merely logged as a known warning.

## Safety Checks
- [x] No modifications to `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- [x] Installer apply was not implemented.
- [x] Update check/apply was not implemented.
- [x] Autonomous executor, release automation, or additional agent adapters were not implemented.
- [x] Workspace folders were not restructured or deleted.

## Explicit Statements
- **Commit:** No commit was made.
- **Push:** No push was made.
- **Approval:** Documentation updates, Evidence generation, or self-test `PASS` do **NOT** equal approval.

## Known Limitations
- Duplicate `* 2` documentation folders remain in the repository. They will require a separate cleanup stage.

## Next Recommended Stage
`AOS-FARM.583 — Target Project First-Start Guide`
*(or `AOS-FARM.580B — Additional Agent Entrypoint Adapters` if additional environment entrypoints are required).*

---

### AOS-FARM.582 STATUS: READY_FOR_REVIEW
