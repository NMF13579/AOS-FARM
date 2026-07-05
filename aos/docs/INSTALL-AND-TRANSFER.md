# AOS Installation and Transfer Guide

## 1. What this guide is
This is the primary guide for installing and transferring AOS into your target project. It explains how to deploy AOS safely, what files to copy, and how to verify the installation using read-only commands.

## 2. What /aos/ is
The `/aos/` directory is the core installable consumer kit. It contains the control scripts, templates, prompt packs, and core documentation necessary for AOS to function.

## 3. What /aos/root/ is
The `/aos/root/` directory contains templates for files that must live in the root of your target project. These files bridge your project with the AOS control system.

## 4. What gets copied
- The entire `/aos/` folder into your project root.
- Required root files from `/aos/root/` to your project root.

## 5. What must not be copied
- Do not copy internal AOS-FARM development files (`00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`).
- Do not copy `/agentos/` or historical reports.

## 6. Required root files
- `/AGENTS.md` - Primary entrypoint for AI agents.
- `/llms.txt` - Secondary entrypoint pointing to AOS documentation.

## 7. Optional root files
- `/.gitignore` updates (using `gitignore.snippet`).
- `/README.md` updates (using `README_AOS_SECTION.md`).
- `/.github/workflows/aos-advisory.yml` (advisory CI workflow).

## 8. Manual transfer map
- `/aos/`                              → `/aos/`
- `/aos/root/AGENTS.md`                → `/AGENTS.md`
- `/aos/root/llms.txt`                 → `/llms.txt`
- `/aos/root/.gitignore.template`      → `/.gitignore` (only if no `.gitignore` exists)
- `/aos/root/gitignore.snippet`        → manually merge into existing `/.gitignore`
- `/aos/root/README_AOS_SECTION.md`    → optional README block
- `/aos/root/.github/workflows/aos-advisory.yml` → optional advisory workflow

*Rules:*
- Manual install remains fully supported.
- No silent overwrite in any mode.
- Existing `.gitignore` receives only controlled AOS block append in safe mode.
- No automatic `AGENTS.md` or `llms.txt` merge or append; these are never modified automatically.
- No automatic `README.md` or workflow mutation.

## 9. Dry-run command
To verify what needs to be installed or transferred without changing files, run:
```bash
python3 aos/scripts/aos_install.py --dry-run
```
Dry-run validates and reports; it does not deploy.

## 10. After dry-run PASS
After a successful dry-run without conflicts, you can either perform manual transfer or use the safe apply mode.

To safely apply:
*(Note: Safe apply is for first deployment from an AOS package into a target repo where `/aos/` does not already exist. If `/aos/` already exists, safe apply is expected to stop rather than merge or overwrite. Use self-test, Doctor, and manual root template review instead. Manual copy ≠ safe apply, dry-run PASS ≠ installed, safe apply conflict ≠ failure to approve, existing `/aos/` → HUMAN_REVIEW_REQUIRED.)*
```bash
python3 aos/scripts/aos_install.py --apply --safe-create-and-gitignore-append --confirm "AOS INSTALL SAFE CREATE OK" --tutor
```
**Safe apply is strictly limited.** It requires exact Human confirmation.
Apply DONE is not approval, and READY_FOR_FIRST_START is not execution authorization.
Tutor mode provides explanation only and does not claim approval.

## 11. Conflict handling
If target files like `README.md` or `AGENTS.md` already exist, do not overwrite them. Manually merge the required content.

## 12. .gitignore handling
If you have an existing `.gitignore`, manually append the contents of `aos/root/gitignore.snippet` to it. If you do not have one, copy `aos/root/.gitignore.template` to `/.gitignore`.

## 13. Self-test command
To check the integrity of the installed package and verify the target state, run:
```bash
python3 aos/scripts/aos_consumer_self_test.py
```

## 14. Doctor command
To get a read-only validation summary of your AOS installation, run:
```bash
python3 aos/scripts/aos_doctor.py
```

## 15. Queue dashboard command
To view the current task queue status, run:
```bash
python3 aos/scripts/aos_queue_dashboard.py
```

## 16. Status meanings
- `PASS`: The check succeeded.
- `PASS_WITH_WARNINGS`: The check succeeded but has advisory warnings.
- `HUMAN_REVIEW_REQUIRED`: A manual decision or intervention is needed.
- `UNKNOWN_BLOCKED`: The state is unclear and execution cannot proceed.
- `BLOCKED`: The operation is explicitly forbidden or blocked.

## 17. Expected deployed state
After installation, your project root should contain:
- `/aos/`
- `/AGENTS.md`
- `/llms.txt`
- `/.aos-tmp/` (ignored by git)

## 18. Troubleshooting
- If commands fail with import errors, ensure you are running them from the project root.
- If conflicts are reported during dry-run, manually resolve them by merging the templates into your existing files.

## 19. Next safe action
Read `aos/START_HERE.md` to begin the AOS workflow.

## 20. Non-goals
- No autonomous execution setup.
- No CI enforcement setup by default.
- No production database provisioning.

---

**AOS Core Rules & Boundaries:**
- PASS ≠ approval
- Evidence ≠ approval
- CI PASS ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- Human approval cannot be simulated
- Dry-run PASS ≠ approval
- Self-test PASS ≠ approval
- Doctor PASS ≠ approval
- Queue NEXT ≠ execution authorization
- Apply DONE ≠ approval
- READY_FOR_FIRST_START ≠ execution authorization
- Tutor output ≠ approval

Manual transfer remains a supported path.
Safe apply requires exact confirmation and is limited to non-destructive creation and controlled `.gitignore` appending.
Dry-run validates and reports; it remains the default.
