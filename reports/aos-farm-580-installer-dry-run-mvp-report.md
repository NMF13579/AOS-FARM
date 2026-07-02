# AOS-FARM.580 — Installer Dry-Run MVP with Minimal Agent Entrypoints

## State
- **Branch:** `dev`
- **HEAD:** `e3106ddf34d07636a8cf6b97cceca51ad9e7816a`
- **origin/dev HEAD:** `e3106ddf34d07636a8cf6b97cceca51ad9e7816a`
- **Branch Alignment Result:** Aligned

## Files Changed
- `[NEW]` `aos/scripts/aos_install.py`
- `[NEW]` `aos/templates/install-plan.md`
- `[NEW]` `aos/docs/AGENT-ENTRYPOINTS.md`
- `[NEW]` `aos/root/llms.txt`
- `[MODIFIED]` `aos/root/AGENTS.md` (Overwritten to be a thin adapter)
- `[MODIFIED]` `aos/docs/INSTALL.md`
- `[MODIFIED]` `aos/docs/ROUTES.md`
- `[NEW]` `reports/aos-farm-580-installer-dry-run-mvp-report.md`

## Root Templates Created
- `/aos/root/llms.txt` (Common route for AI agents)
- `/aos/root/AGENTS.md` (Thin adapter pointing to llms.txt)

## Installer Behavior Summary
- Developed `aos/scripts/aos_install.py` with `--dry-run` and `--apply` flags.
- **Dry-run**: Identifies the repo root and `/aos/root/`, builds an install map, checks for conflicts against the target root, enforces safety boundaries (like avoiding `.git/`, `/.aos-tmp/`, and source folders inside `/project/`), and generates an `install-plan` without mutating the filesystem.
- **Apply**: The `--apply` flag explicitly returns `NOT_IMPLEMENTED` and blocks execution, ensuring no files are written during this stage.

## Dry-run Output Summary
- When executed, `aos_install.py --dry-run` successfully produced the install plan output based on the `/aos/root/` mapping.
- Detected conflicts properly (e.g. `AGENTS.md` and `llms.txt` existing in root mapping if they do in target).
- Returned appropriate `install_status`.

## Apply Rejection Result
- `--apply` returned `install_status: BLOCKED`, `apply_status: NOT_IMPLEMENTED`, `approval_claimed: false`.

## Validation Commands Run
```bash
python3 -m py_compile aos/scripts/aos_install.py
python3 aos/scripts/aos_install.py --dry-run
python3 aos/scripts/aos_install.py --apply || true
find aos/root -type f | sort
find aos/docs -maxdepth 2 -type d | sort
git status -sb
git diff --stat
git diff --name-status
```

## Validation Results
- Python compilation passed cleanly.
- Dry-run executed and successfully formatted the `install-plan` output.
- Apply correctly blocked execution.
- `git status` confirmed only the allowed files were added/modified. No product source code or forbidden artifacts were generated.

## Duplicate Folder Warning
> [!WARNING]
> Duplicate documentation folders were detected under `aos/docs` (e.g. `assembly 2/`, `governance 2/`, `lifecycle 2/`, etc.). No cleanup was performed because deduplication is outside AOS-FARM.580 scope.

## Safety Checks
- [x] No modifications to `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- [x] No files written by installer during `--dry-run`.
- [x] No product code generated in `/project/`.

## Explicit Statements
- **Commit:** No commit was made.
- **Push:** No push was made.
- **Approval:** Dry-run PASS or Evidence generation does **NOT** equal approval.

## Known Limitations
- The `--apply` phase is intentionally not implemented.
- Agent entrypoints only include Codex/OpenAI thin adapter (`AGENTS.md`). Other environment adapters (Claude, Gemini, Cursor, etc.) are excluded.
- The installer relies on the assumption that it is run from within the repository tree to resolve the project root using `.git/`.

## Next Recommended Stage
`AOS-FARM.581 — Consumer Self-Test / Package Integrity`
*(or `AOS-FARM.580B — Additional Agent Entrypoint Adapters` if adapters need to be expanded first).*

---

### AOS-FARM.580 STATUS: READY_FOR_REVIEW
