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
