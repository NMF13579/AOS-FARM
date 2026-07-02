# AOS First Start Guide

This guide explains what to do when AOS is present in a target project for the first time.

## 1. What is the first file an agent should read?
- Read `AGENTS.md` if present.
- `AGENTS.md` points to `llms.txt`.
- `llms.txt` points to AOS docs and safety rules.
- If `AGENTS.md` is absent but `llms.txt` exists, read `llms.txt`.
- If both are absent, run the installer dry-run from the AOS package if available.

## 2. First safe commands
To understand the current state safely, run:
```bash
python3 aos/scripts/aos_install.py --dry-run
python3 aos/scripts/aos_consumer_self_test.py
```
- **dry-run** shows what would be installed;
- **self-test** checks package integrity and target state;
- both are Evidence only;
- neither grants approval.

## 3. Expected files
- `/llms.txt`
- `/AGENTS.md`
- `/aos/`
- `/project/`
- `/aos-modules/`
- `/.aos-tmp/`

Note that some root files (like `AGENTS.md` or `llms.txt`) may be pending from `/aos/root/`.

## 4. Conflict handling
If dry-run reports existing root files in the target project:
- do not overwrite silently;
- do not apply automatically;
- stop with `HUMAN_REVIEW_REQUIRED`;
- the user must decide.

## 5. Folder placement summary
For a detailed explanation of where to put files, see the [Workspace Boundary](WORKSPACE-BOUNDARY.md) documentation.

## 6. Authorization summary
For full details, see the [Authorization Commands](AUTHORIZATION-COMMANDS.md) document.

Exact authorization commands are:
- `AOS COMMIT OK`
- `AOS PUSH OK`
- `AOS MICRO COMMIT+PUSH OK`

Plain-language commands such as `commit`, `комит`, `push`, `пуш`, `залей`, `отправь` are intent only. Exact authorization is required.

## 7. Safety invariants
- PASS ≠ approval
- Evidence ≠ approval
- CI PASS ≠ approval
- self-test PASS ≠ approval
- dry-run PASS ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- Human approval cannot be simulated
- Commit authorization ≠ push authorization
- Push authorization ≠ release authorization

## 8. What not to do
- do not run apply;
- do not overwrite root files;
- do not cleanup duplicate folders;
- do not move project code;
- do not store Evidence/reports/approvals/checkpoints in `/.aos-tmp/`;
- do not treat `/project/` as default product source root.
