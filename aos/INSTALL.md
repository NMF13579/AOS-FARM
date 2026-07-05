# AOS Consumer Kit Installation

AOS is a self-contained consumer kit. The `aos/` directory is the installable and removable unit.

## Quick Pointers
- **Quick install pointer:** [docs/INSTALL-AND-TRANSFER.md](docs/INSTALL-AND-TRANSFER.md)
- **Quick first-start pointer:** [START_HERE.md](START_HERE.md)

## Useful Commands
- `python3 aos/scripts/aos_install.py --dry-run`
- `python3 aos/scripts/aos_consumer_self_test.py`

## Uninstallation
1. **Remove AOS Folder:** Delete the entire `aos/` folder from your project root.
2. **Remove AGENTS.md:** Delete `AGENTS.md` and `llms.txt` from your project root.
3. **Remove Markers:** Remove any AOS marker blocks from your `README.md` and `.gitignore`.

## AOS Core Rules & Boundaries
- PASS ≠ approval
- Evidence ≠ approval
- CI PASS ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- Human approval cannot be simulated
- Commit, push, merge, release, and destructive operations require explicit human authorization.
