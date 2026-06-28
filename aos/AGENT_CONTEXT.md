# AOS Agent Context & Operating Rules

This file is designed for AI agents operating within a consumer project that has adopted the AOS framework.

## Agent Operating Rules
When operating within a project containing the `/aos/` product folder, you **MUST** adhere to the following rules:
1. **No Magic Allowed:** There are no active Python runners, CI hooks, or databases governing your behavior automatically. You are bound by the markdown methodology.
2. **Fail-Closed by Default:** If the state of a task, execution, or artifact is `UNKNOWN`, you must stop and ask the human user.
3. **No Simulated Approval:** You are strictly forbidden from writing "Approved by Human" or assigning Risk Profiles without genuine human instruction.
4. **Separation of Concerns:** You must not invent or authorize tasks. You may only execute tasks that are explicitly authorized in a `Controlled Task Brief`.
5. **Execution Boundaries:** You must stop and request explicit human authorization before committing code, pushing to a remote repository, merging, releasing, or performing destructive operations.

**AOS Core Invariants:**
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No active runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
