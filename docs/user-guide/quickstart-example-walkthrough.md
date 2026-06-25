# First Public Example Task Walkthrough

## Short Purpose
This walkthrough demonstrates exactly how a non-programmer user can complete their first safe, controlled task using the AOS-FARM system. It takes you from a simple idea through the strict human authorization boundaries required to finalize the work.

## Prerequisites
- You must have read the `README.md` and `docs/user-guide/quickstart.md`.
- You must have read the three canonical sources: `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.

## Example Task Idea
**Goal**: Add one small documentation note to a user guide.
This is a small, bounded task that does not affect code, infrastructure, or CI pipelines.

## Example Task Brief Summary
To start, the user creates a "Task Brief" (a strict instruction document). A copyable example is provided in `templates/example-first-controlled-task-brief.md`. The Brief specifies the exact boundaries: only modifying one specific documentation file and creating the necessary reports, with no push or autonomous execution allowed.

## Controlled Execution Flow
1. **Initiation**: The user provides the Task Brief to the agent.
2. **Pre-flight**: The agent reads the canonical sources and verifies the Git baseline (e.g., `git rev-parse HEAD`).
3. **Implementation**: The agent safely makes the requested documentation change.
4. **Validation**: The agent runs read-only commands (like `git diff` and `git status`) to ensure no forbidden files were touched.
5. **Reporting**: The agent generates an Evidence report.

## Evidence Step
The agent produces Evidence (such as validation command outputs and checkmarks) that the task was completed.
*CRITICAL REMINDER: Evidence ≠ approval. PASS ≠ approval. CI PASS ≠ approval.*
The agent cannot self-approve its work.

## Verification Step
The user (human) manually reviews the generated reports and `git diff` to verify the agent stayed within scope. The user ensures no runner, autonomous logic, or protected files were modified.

## Human Commit Authorization Boundary
Before any commit happens, the agent stops and prepares a DRAFT Human Checkpoint and a Commit Authorization Package. 
**The agent cannot commit on its own.** The user must explicitly change the DRAFT status to `APPROVED_FOR_COMMIT`.

## Commit Step Boundary
Only after explicit Human Commit Authorization, the agent (in a subsequent task) is allowed to run `git commit` for exactly the authorized files. It still cannot push.

## Human Push Authorization Boundary
After the commit is created, the agent must prepare another DRAFT Human Checkpoint for push authorization. The human reviews the commit SHA and explicitly grants `APPROVED_FOR_PUSH`.

## Push Step Boundary
Only after explicit Human Push Authorization, the agent runs `git push`. The task is then closed.

## Common Mistakes
- Confusing Evidence with Approval: An agent saying "Task complete" or generating a "PASS" report does not mean the work is approved. The human must explicitly authorize it.
- Skipping Boundaries: Requesting the agent to "just fix and push it" violates the fundamental safety invariants.

## Stop Conditions
The agent must stop and fail-closed if:
- Required canonical sources are missing.
- The Git baseline differs from expectations.
- Forbidden files (like `00_AOS_Core_Control.md`) are modified.

## Forbidden Actions
The agent is explicitly forbidden from:
- Approving its own work.
- Performing autonomous `git commit` or `git push` without explicit checkpoints.
- Creating GitHub releases, altering tags, or claiming production readiness.
- Merging branches or simulating human approval.
