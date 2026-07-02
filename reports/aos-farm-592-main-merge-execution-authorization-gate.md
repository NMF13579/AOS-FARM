# AOS-FARM.592 — Main Merge Execution Authorization Gate

## 1. Stage Info
**Operational Mode:** REMOTE_SYNCED
**Branch:** dev
**Local HEAD:** 0ad214054a385eea70b52b24ad39686acf6b4df4
**Origin/dev HEAD:** 0ad214054a385eea70b52b24ad39686acf6b4df4
**Origin/main HEAD:** 5973aea797471d72c152ad44efd447a27fa11c35
**`origin/dev...HEAD` result:** 0 0
**`origin/main...origin/dev` result:** 0 11

## 2. Duplicate Folder Cleanup Verification
**Verified Clean.** No `aos/docs/* 2` duplicate folders were found. The local cleanup executed in the previous stage was fully successful.

## 3. Commit List (`origin/main..origin/dev`)
0ad2140 AOS-FARM.591: Empty Duplicate Docs Folder Cleanup Authorization Gate
1cb1c3a AOS-FARM.590: Duplicate Docs Folder Cleanup Audit
d4a748f AOS-FARM.589: Main Merge Human Review Gate
eb112a7 AOS-FARM.588: Main Merge Readiness Review
097e693 AOS-FARM.586: Consumer Corridor Final Closure Review
35db39e AOS-FARM.585: Consumer First-Start Dogfood
3ffc23b AOS-FARM.583: Target Project First-Start Guide
06b317c AOS-FARM.582: Documentation Workspace and Module Boundary
f9b0d1c AOS-FARM.581: Consumer Self-Test / Package Integrity
513e519 AOS-FARM.580: Installer Dry-Run MVP with Minimal Agent Entrypoints
e3106dd docs: implement AOS-FARM.579 consumer landing and authorization shortcuts

## 4. File Delta Summary
**28 files changed, 1845 insertions(+), 223 deletions(-)**

**Key Additions:**
- `aos/scripts/aos_install.py`
- `aos/scripts/aos_consumer_self_test.py`
- `tests/test_aos_consumer_self_test.py`
- `aos/templates/install-plan.md`
- `aos/docs/*` (Consumer Corridor docs: INSTALL, FIRST-START, STORAGE, ROUTES, SELF-TEST, etc.)
- `aos/root/llms.txt`
- `reports/*` (Audits and Gates 579 through 591)

**Key Modifications:**
- `README.md`
- `aos/root/AGENTS.md` (Massive reduction/cleanup)
- `aos/docs/ROUTES.md`, `aos/docs/TUTOR.md`

## 5. Protected/Canonical Delta Summary
- `00_AOS_Core_Control.md`: Unchanged.
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Unchanged.
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Unchanged.

## 6. Consumer Corridor Summary
The consumer corridor (`INSTALL.md`, `FIRST-START.md`, `SELF-TEST.md`, etc.), the installer (`aos_install.py`), and the self-test scripts are all included and structurally complete in the delta.

## 7. Cleanup Summary
The required cleanup documentation (`reports/aos-farm-590` and `reports/aos-farm-591`) is successfully included in the delta. The physical duplicate folders were successfully deleted locally and present no git delta.

## 8. Validation Results
- **Installer Dry-Run:** COMPLETED. (`HUMAN_REVIEW_REQUIRED` is properly logged as dry-run PASS is not approval).
- **Self-Test Validation:** PASS. (Package Integrity and Target Install State verified).
- **Pytest:** PASS (6 tests ran OK).

## 9. Blocker List
- **None.** All technical gates and validation steps have passed.

## 10. Exact Later Merge Command Proposal
*(This is a proposal only. Do not execute without explicit human authorization)*
```bash
git switch main
git fetch origin
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count origin/main...HEAD
git merge --ff-only origin/dev
```

## 11. Explicit Safety and Authorization Statements
1. **No merge was made** in this stage.
2. **No commit was made** in this stage.
3. **No push was made** in this stage.
4. **No release was made** in this stage.
5. **Merge readiness is NOT merge approval.**
6. **This stage is NOT approval.**
7. **This stage is NOT merge execution.**
8. **This stage is NOT push authorization.**
9. **This stage is NOT release authorization.**
10. **Separate human merge authorization is explicitly required.** The human must explicitly authorize the separate merge execution stage.
11. **Main push requires separate authorization.** Even after merge commit/fast-forward, push to `main` requires separate authorization.
12. PASS is not approval; Evidence is not approval; CI PASS is not approval; dry-run PASS is not approval; self-test PASS is not approval.

## 12. Final Gate Verdict
**READY_FOR_SEPARATE_MERGE_AUTHORIZATION**

## 13. Next Recommended Stage
**AOS-FARM.593 — Main Merge Execution**
