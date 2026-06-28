# AOS-FARM.449 — Controlled Task Brief

## Mode

MEDIUM_RISK_GUIDED

## Repository

NMF13579/AOS-FARM

## Branch

build/task-registry-queue-helper-hardening

## Risk Profile Assignment

```yaml
proposed_by_agent: MEDIUM_RISK_GUIDED
assigned_by_human: MEDIUM_RISK_GUIDED
assignment_evidence: "Human prompt for AOS-FARM.449 explicitly states: Risk Profile assigned: MEDIUM_RISK_GUIDED"
```

## Context

AOS-FARM.448 (First Controlled Task Lifecycle Dogfood) has been completed and
pushed to origin/dev at commit `fac85dbd54c878aed8466a2bdffa8cf10a8181c8`.

The existing `aos/scripts/aos_tasks.py` and
`aos/tools/optional/task_registry_validator.py` provide a partial read-only
CLI. AOS-FARM.449 hardens this layer so the agent and user can clearly see
current task, next candidate, blocked tasks, done tasks, invalid transitions,
human action required, and whether execution/commit/push are authorized.

## Goal

Harden the Task Registry / Queue helper layer with:

1. A new `aos/scripts/aos_task_queue_helper.py` CLI that exposes
   `validate`, `show-current`, `show-next`, `show-summary` subcommands
   with clear human-readable output and explicit invariant warnings.
2. Fixtures for valid and invalid queue states.
3. Tests covering all required invariant behaviors.
4. Phase 4–8 reports and Evidence artifacts.

## Scope

- Inspect current task registry / queue docs and helpers
- Create or harden a read-only task queue helper
- Add minimal fixtures/examples for valid and invalid queue states
- Add tests for helper behavior
- Create AOS-FARM.449 reports/Evidence artifacts
- Propose AOS-FARM.450 as Next Task Candidate only

## Rules

- Helper must be strictly read-only
- Helper must not authorize execution
- Helper must not approve tasks
- Helper must not assign Risk Profiles
- Helper must not start next task
- Helper must return non-zero exit code for invalid states
- Helper must detect invalid transitions
- Helper must warn that Next Task Candidate is not an approved task
- Helper must warn that Queue position is not approval
- Helper must warn that PASS/Evidence are not approval
- Helper must treat UNKNOWN as blocking or not OK
- Helper must treat NOT_RUN as not PASS

## Allowed Changes

- `aos/scripts/aos_task_queue_helper.py` — CREATE
- `aos/tools/optional/task_registry_validator.py` — HARDEN (add missing checks only)
- `tests/fixtures/task_queue_valid.yaml` — CREATE
- `tests/fixtures/task_queue_invalid_candidate_as_approved.yaml` — CREATE
- `tests/fixtures/task_queue_invalid_transition.yaml` — CREATE
- `tests/fixtures/task_queue_missing_human_authorization.yaml` — CREATE
- `tests/test_aos_task_queue_helper.py` — CREATE
- `reports/aos-farm-449-*.md` and `reports/aos-farm-449-*.yaml` — CREATE

## Forbidden Changes

- `00_AOS_Core_Control.md` — NO TOUCH (protected/canonical)
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` — NO TOUCH (protected/canonical)
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md` — NO TOUCH (protected/canonical)
- Any runner, autonomous execution, or automatic task start
- Any automatic approval or Risk Profile assignment
- RAG, SQLite, vector DB, SaaS
- CI expansion
- Release, merge, commit, push
- AOS-FARM.450 execution
- Storage of Evidence/reports/checkpoints in `/.aos-tmp/`
- Cleanup of pre-existing unrelated files

## Validation Plan

1. Run `python3 aos/scripts/aos_task_queue_helper.py validate --registry <valid-registry> --queue <valid-queue>` — expect exit 0 and PASS output.
2. Run same with invalid fixture — expect exit 1 and BLOCKED output.
3. Run `show-current`, `show-next`, `show-summary` — verify invariants are printed.
4. Run `python3 -m unittest tests/test_aos_task_queue_helper.py` — all 8 tests pass.
5. Run `python3 -m unittest discover -s tests` if safe — record NOT_RUN if skipped.
6. Verify `git diff -- 00_AOS_Core_Control.md 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md 02_AOS_Governance_Control_Module_and_Safety_Rules.md` is empty.
7. Verify `git diff --check` passes (no whitespace/conflict markers).

## Expected Evidence

- `reports/aos-farm-449-changed-files.yaml`
- `reports/aos-farm-449-execution-report.md`
- `reports/aos-farm-449-evidence-report.md`
- `reports/aos-farm-449-evidence-review.md`
- `reports/aos-farm-449-lessons-learned.md`
- `reports/aos-farm-449-next-task-candidate.md`
- `reports/aos-farm-449-final-closure-report.md`
- Test output from `python3 -m unittest tests/test_aos_task_queue_helper.py`

## UNKNOWN Policy

Any UNKNOWN state is treated as BLOCKED. Not OK. Not PASS.

## NOT_RUN Policy

NOT_RUN ≠ PASS. Any check not run must be explicitly recorded as NOT_RUN.

## Final Status

```yaml
final_status: READY_FOR_EXECUTION_UNDER_MEDIUM_RISK_GUIDED_NO_COMMIT_NO_PUSH
```
