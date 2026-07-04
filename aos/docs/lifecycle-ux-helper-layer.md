# Lifecycle UX Helper Layer

## What is the Lifecycle UX Helper Layer?
The Lifecycle UX Helper Layer is a set of Python scripts and markdown templates designed to provide structured visibility into the current state of the AOS-FARM system. It helps answer questions like "where are we?", "what is the current status?", and "what files have changed?" without modifying the codebase itself.

## Why it exists
This layer exists to enforce the safety invariants of the AOS-FARM governance model. AI agents and human operators need reliable ways to inspect the environment, verify readiness for handoffs, and assemble review packages. By making these helpers strictly read-only, we eliminate the risk of accidental auto-commits, auto-pushes, or unauthorized scope expansions.

## What each helper does
- **`aos_baseline_summary.py`**: Gathers environment state (branch, HEAD, remote parity, working tree cleanliness) to establish a trusted starting point.
- **`aos_lifecycle_status.py`**: Reports the current execution phase, validating if the agent is ready for the next allowed action.
- **`aos_handoff_summary.py`**: Produces a comprehensive summary combining the baseline and lifecycle state, intended to be passed to the next session.
- **`aos_remote_closure_check.py`**: Verifies that the local branch HEAD precisely matches the intended remote tracking branch, preventing drift.
- **`aos_review_package.py`**: Compares the current uncommitted working tree against an explicitly declared list of files, identifying scoped changes versus unauthorized drift.

## What each helper does not do
- They do **not** run `git commit`, `git push`, `git add`, or any other mutating operations.
- They do **not** write to the canonical Source of Truth.
- They do **not** simulate human approval.
- They do **not** perform Risk Profile assignment.

## How to ask "на чём мы остановились?" ("where did we stop?")
To find out the current progress context without altering state, simply run the handoff summary helper:
```bash
python3 aos/scripts/aos_handoff_summary.py
```

## How to generate a handoff summary
Execute the handoff summary script:
```bash
python3 aos/scripts/aos_handoff_summary.py
```

## How to check baseline
Execute the baseline script (outputs in Markdown by default):
```bash
python3 aos/scripts/aos_baseline_summary.py --markdown
```

## How to check lifecycle status
Check the current state:
```bash
python3 aos/scripts/aos_lifecycle_status.py --markdown
```
Check what the allowed next steps are:
```bash
python3 aos/scripts/aos_lifecycle_status.py --next --markdown
```

## How to check remote closure
Verify synchronization with the remote `dev` branch:
```bash
python3 aos/scripts/aos_remote_closure_check.py --target dev
```

## How to assemble a review package
Assemble a review package by explicitly declaring the task ID and the files in scope:
```bash
python3 aos/scripts/aos_review_package.py --mode human-review --task-id AOS-FARM.610 --files aos/docs/lifecycle-ux-helper-layer.md --target-branch dev --format markdown
```

## How to use prompt templates
Prompt templates (located in `aos/templates/prompts/lifecycle/`) provide standard language for transitioning between stages. Copy the contents of the relevant prompt template and submit it to the agent when directing it to perform a specific action (e.g., executing a commit, generating a review package).

## Why helper output is not approval
AOS-FARM operates under a strict "Fail-Closed" governance model. **PASS ≠ approval**. A helper script verifying that a diff is clean or a test suite passes is merely generating **Evidence**. Only a human owner can interpret that Evidence and grant explicit approval to proceed with execution, commits, pushes, or releases. 

## What actions still require human decision
- Moving from implementation to staging/committing.
- Moving from committing to pushing.
- Merging to `main`.
- Releasing artifacts.
- Modifying canonical sources (00, 01, 02).
- Expanding the scope of an assigned task.

## Why commit and push remain separate checkpoints
- **Commit authorization is not push authorization.** Committing locks the state locally so it can be reviewed as an immutable SHA. Pushing alters the shared remote state, potentially triggering CI/CD pipelines or affecting other developers. These are fundamentally different Risk Profiles requiring distinct human authorizations.

## Why push and release remain separate checkpoints
- **Push authorization is not release authorization.** A pushed branch might just be a backup or a review artifact. A release modifies the production or consumer-facing state. Pushing does not imply readiness for release.

## Why generated summaries are not Source of Truth
Generated files (such as review packages or handoff summaries) are point-in-time snapshots. The repository file tree, git history, and canonical Markdown documents (`00_AOS_Core_Control.md`, `tasks/`, `queue/`) are the actual Source of Truth. Generated reports are disposable and must never be treated as authoritative data.

## Temporary local helper logs
Temporary helper logs, if later implemented, must live under `/.aos-tmp/logs/`.
They are local-only, ignored, disposable, and not Source of Truth.
They must not store approvals, Evidence, checkpoints, or canonical files.
Reports must not be auto-deleted.
Canonical files must not be auto-deleted.
Automatic pruning is allowed only for temporary local traces under `/.aos-tmp/logs/` if separately scoped and authorized.

## Safety Reminders
- Generated lifecycle status is not Source of Truth.
- Generated handoff summary is not Source of Truth.
- Generated review package is not Source of Truth.
- Helper outputs are not approval.
- Allowed next action is not authorization.
- Remote closure verification is not release authorization.
- Commit authorization is not push authorization.
- Push authorization is not release authorization.
- PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
