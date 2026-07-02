# FIRST-SAFE-COMMANDS

> **GUIDANCE BOUNDARY:**
> This document is guidance and navigation only.
> Canonical governance remains in `00_AOS_Core_Control.md`,
> `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and
> `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
> This document does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

## Purpose

This document lists commands that are safe to run for read-only inspection,
validation, and Evidence collection. It also lists commands that must **not**
be run automatically.

**These commands produce validation signals and Evidence.**
**They do not approve execution, commit, push, merge, release, or lifecycle transition.**

---

## Category 1 — Safe Read-Only Git Checks

These commands inspect repository state. They do not modify files.

```bash
# Show current branch
git branch --show-current

# Show HEAD commit
git rev-parse HEAD

# Show origin/dev commit
git rev-parse origin/dev

# Compare HEAD to origin/dev (ahead/behind)
git rev-list --left-right --count origin/dev...HEAD

# Show working tree status (short)
git status -sb

# Show all untracked files
git status --short --untracked-files=all

# Show diff stat (no output = no tracked changes)
git diff --stat

# Show changed file names and status
git diff --name-status

# Check protected/canonical files specifically
git status --short -- \
  00_AOS_Core_Control.md \
  01_AOS_Assembly_Pipelines_and_Build_Roadmap.md \
  02_AOS_Governance_Control_Module_and_Safety_Rules.md

# View last N commits
git log --oneline -10
```

---

## Category 2 — Validator / Compile Checks

These commands check Python syntax and run AOS validators. They do not commit
or push. Running them does not constitute approval of any kind.

```bash
# Syntax check: confirm script compiles without errors
python3 -m py_compile aos/scripts/aos_task_document_check.py

# Validate all task documents in scope
python3 aos/scripts/aos_task_document_check.py task --validate-all

# View task queue
python3 aos/scripts/aos_task_document_check.py queue --list

# View next task candidate
python3 aos/scripts/aos_task_document_check.py queue --next

# Run read-only validation aggregator (AOS Doctor)
python3 aos/scripts/aos_doctor.py

# View derived queue dashboard
python3 aos/scripts/aos_queue_dashboard.py
```

---

## Category 3 — Unit Test Discovery

```bash
# Discover and run unit tests (read-only validation)
python3 -m unittest discover
```

Running tests does not authorize any lifecycle transition.
`NOT_RUN` must be reported if tests are unavailable or skipped.
`NOT_RUN` is not `PASS`.

---

## Category 4 — Queue Visibility Checks

```bash
# List all tasks in queue
python3 aos/scripts/aos_task_document_check.py queue --list

# Show next candidate task
python3 aos/scripts/aos_task_document_check.py queue --next
```

Viewing the queue does not select, assign, or approve a task.
Human must explicitly authorize the next task.

---

## Category 5 — Consumer Advisory CI

Optional advisory CI for GitHub projects is available.

Template path: `/aos/root/.github/workflows/aos-advisory.yml`
Target copy path: `.github/workflows/aos-advisory.yml`

- Advisory CI is optional
- CI PASS is not approval
- It does not replace human review
- It does not authorize commit/push/merge/release
- It does not enable required checks by itself

---

## Mandatory Boundary Statement

```text
These commands produce validation signals and Evidence.
They do not approve execution, commit, push, merge, release,
or lifecycle transition.

PASS output from any command is not approval.
Evidence produced by any command is not approval.
CI PASS is not approval.
NOT_RUN is not PASS.
UNKNOWN is not OK.
```

---

## Commands That Must NOT Be Run Automatically

The following operations require explicit human authorization before execution.
An agent must **never** run these without a documented human checkpoint:

```text
git commit       — requires human commit authorization
git push         — requires human push authorization
git merge        — requires human merge authorization
git checkout -B  — allowed only during scoped branch setup with human direction
git rebase       — forbidden without explicit human authorization
git reset --hard — forbidden without explicit human authorization
git push --force — forbidden without explicit human authorization
git tag / release — requires human release authorization
```

Do not run destructive operations (delete, bulk rename, force-push,
archive, bulk rewrite) without explicit human authorization and a
documented rollback plan.

---

## Reporting NOT_RUN

If a validation command cannot be run (e.g., script missing, environment
unavailable, outside authorized scope), report:

```yaml
validation_status: NOT_RUN
command: <exact command that was not run>
reason: <brief explanation>
```

Do not report `PASS` for commands that were not run.

---

*This document is guidance only. It does not grant execution, commit, push,
merge, or release permission. Canonical governance in 00/01/02 always takes
precedence.*
