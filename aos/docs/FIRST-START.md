# AOS First Start Guide

**Purpose**: This is the first run and orientation page when AOS is present in a target project.

## Pointers
- **Primary workflow entrypoint**: [../START_HERE.md](../START_HERE.md)
- **Install/transfer authority**: [./INSTALL-AND-TRANSFER.md](./INSTALL-AND-TRANSFER.md)

## Minimal Verification Commands
Run these read-only checks to understand the current state:
```bash
python3 aos/scripts/aos_install.py --dry-run
python3 aos/scripts/aos_consumer_self_test.py
python3 aos/scripts/aos_doctor.py --json
```

## Safety Invariants
- PASS ≠ approval
- Evidence ≠ approval
- UNKNOWN ≠ OK
- NOT_RUN ≠ PASS
- HUMAN_REVIEW_REQUIRED means stop for human review
