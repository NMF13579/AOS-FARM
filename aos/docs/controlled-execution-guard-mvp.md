# Controlled Execution Guard MVP

## Purpose

The Controlled Execution Guard MVP is an optional transferable AOS tool for deterministic controlled-task boundary checks. It validates package completeness, scope boundaries, evidence disclosures, and the separation between technical PASS and human approval.

## What The Guard Checks

- `precheck` fails closed unless the execution package declares human authorization, human-assigned Risk Profile, scoped files, forbidden files, validation plan, expected evidence, and execution boundaries that keep commit, push, merge, release, next-task execution, and approval claims disabled.
- `scopecheck` validates that changed files are known, stay inside `authorized_files`, do not touch `forbidden_files`, and do not modify protected development/canonical files without a separate human checkpoint.
- `postcheck` validates that the execution or evidence report discloses changed files, diff summary, commands run, PASS, NOT_RUN, UNKNOWN, and BLOCKED lists, forbidden actions not performed, and the final `human_review_required: true` boundary.

## What The Guard Does Not Do

- It does not execute implementation tasks.
- It does not modify source files during checks.
- It does not commit, push, merge, release, or start the next task.
- It does not assign Risk Profile.
- It does not claim approval.
- It is not a runner and it is not an autonomous task system.

## CLI Usage

Precheck:

```bash
python aos/scripts/aos_controlled_execution_guard.py precheck \
  --project-root . \
  --aos-root aos \
  --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml
```

Postcheck:

```bash
python aos/scripts/aos_controlled_execution_guard.py postcheck \
  --project-root . \
  --aos-root aos \
  --package aos/reports/examples/controlled-execution-guard/fixtures/valid_package.yaml \
  --report aos/reports/examples/controlled-execution-guard/fixtures/reports/valid_report.md
```

Scopecheck:

```bash
python aos/scripts/aos_controlled_execution_guard.py scopecheck \
  --project-root . \
  --aos-root aos \
  --package aos/reports/examples/controlled-execution-guard/fixtures/changed_file_outside_scope.yaml \
  --changed-files aos/reports/examples/controlled-execution-guard/fixtures/changed_file_outside_scope.yaml
```

## Path Model

- `--project-root` points to the host project root.
- `--aos-root` points to the embedded transferable `aos/` folder inside that host project.
- Relative package, report, and changed-files paths are resolved against `project_root` first and `aos_root` second.

This allows a host project shape such as:

```text
my-project/
  aos/
  src/
  tests/
```

## Development Sources Versus Transferable Bundle

The runtime guard does not require `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, or `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md` to exist inside `aos/` or inside a user project.

Those files are AOS-FARM development authority only. The guard may still detect those filenames as protected development files when they appear in a development-context diff, but it does not require them for user-project runtime operation.

## Safety Semantics

- PASS is only evidence that a programmed check succeeded. PASS is not approval.
- Evidence is not approval. A complete report still cannot authorize commit, push, merge, release, or lifecycle mutation.
- NOT_RUN is not PASS. If a command was not run, the guard requires that it stays disclosed as `NOT_RUN`.
- UNKNOWN is blocked. Unknown state cannot be silently accepted as OK.
- Commit and push remain separate human-authorized gates even when the guard returns PASS.

## Boundary Notes

- This MVP intentionally stops at deterministic protocol verification.
- RAG-light and SQLite are out of scope because this task is not building a retrieval layer, database, runner, memory system, or background execution loop.
- The guard focuses on controlled execution boundaries, not on rewriting AOS-FARM development control sources.
