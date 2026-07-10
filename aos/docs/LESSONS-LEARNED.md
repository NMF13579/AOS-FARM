# Lessons Learned and Incident Memory

> **GUIDANCE BOUNDARY:**
> This document is guidance only.
> Lessons are not Source of Truth.
> Lessons are not approval.
> Lessons do not mutate lifecycle state.
> Lessons do not assign Risk Profile.
> Lessons do not grant validator authority.
> Lessons do not replace Evidence.
> Lessons do not replace human checkpoints.
> Lessons do not replace root 00/01/02 control sources.

---

## Initial Lessons

1. **PASS / Evidence / CI PASS are never approval.**
   - No matter how exhaustive a test suite or verification script is, a successful run (`PASS`) does not grant approval or authorization to execute, commit, or push.

2. **Queue NEXT is not execution authorization.**
   - Selecting the next task candidate from the queue does not implicitly authorize an agent to begin writing code or changing files.

3. **Helper scripts must be read-only unless explicitly authorized.**
   - Scripts that are run by agents (e.g., validators, dashboards, packages) must not mutate state, write Evidence, or claim approval.

4. **Internal function return contracts must be inspected before wrapper use.**
   - Ensure the internal functions (e.g., `subprocess` calls, parsing logic) properly fail closed on unexpected output instead of silently proceeding.

5. **Prompt packs must remain thin guidance, not Source of Truth.**
   - Prompts provide behavioral guidance, but they must never override the repository's canonical governance rules (`00`, `01`, `02`).

6. **Python Environment and Workspace Hygiene**
   - **Incident:** `aos_doctor.py` implicitly relied on `python3` from the system PATH, leading to PATH drift and unreproducible behavior. 
   - **PATH Drift:** Relying on `"python3"` literals causes child processes to escape the active `.venv` if the PATH is modified.
   - **Proper Execution:** Always use `sys.executable` for Python-to-Python subprocess invocations to ensure inheritance of the active interpreter.
   - **Dependencies:** `requirements-dev.txt` is the authoritative contract for development tools. The working `.venv` uses these, while the system Python lacks them.
   - **Safe Duplicate Handling:** `* 2` files (like `* 2.py`) are untracked duplicates. Never perform destructive workspace cleanup without human authorization.
   - **Diagnostics Checklist:**
     | Missing Dependency | Expected Behavior |
     | :--- | :--- |
     | `pytest` | Dependent checks skipped (`NOT_RUN`), independent checks continue, aggregate is fail-closed. |
   - **Pre-Commit Checklist:**
     - [ ] Verify branch and HEAD against baseline.
     - [ ] Verify `sys.executable` instead of `"python3"`.
     - [ ] Verify installation from `requirements-dev.txt`.
     - [ ] Confirm non-zero number of executed tests.
     - [ ] Ensure fail-closed status does not rely on substring matching in `stderr` (e.g. `BLOCKED`).
     - [ ] Provide full untracked inventory.
     - [ ] Ensure `/.aos-tmp/` is absent from Git status (requires ignore).
     - [ ] Verify `* 2` files (duplicates) are untouched.
     - [ ] Obtain explicit separate commit and push authorization.
   - **Canonical Boundaries:**
     - lesson ≠ policy authority
     - PASS ≠ approval
     - Evidence ≠ approval
     - NOT_RUN ≠ PASS
     - UNKNOWN ≠ OK
   - **References:** See canonical control sources (`00`, `01`, `02`) for core rules.
