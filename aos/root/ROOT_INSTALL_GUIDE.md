# AOS Root Install Guide

This guide explains the manual transfer process for deploying AOS into your target repository.

## Manual Transfer Steps
1. Copy `/aos/` into target repo root.
2. Copy `aos/root/AGENTS.md` to `/AGENTS.md`.
3. Copy `aos/root/llms.txt` to `/llms.txt`.
4. If no `/.gitignore` exists, copy `.gitignore.template` as `/.gitignore`.
5. If `/.gitignore` exists, merge `gitignore.snippet` manually.
6. Optional: copy `README_AOS_SECTION.md` content into target `README.md`.
7. Optional: copy advisory workflow only after review.
8. Run dry-run: `python3 aos/scripts/aos_install.py --dry-run`
9. Run self-test: `python3 aos/scripts/aos_consumer_self_test.py`
10. Run doctor: `python3 aos/scripts/aos_doctor.py`
11. Read `aos/START_HERE.md`.

*Note: Installer `--apply` is NOT_IMPLEMENTED.*
