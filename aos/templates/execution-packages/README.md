# Execution Package Templates

This directory separates neutral handoff context from authorized execution
context.

## Executor Handoff Package

`executor-handoff-package-template.yaml` is a neutral pre-authorization handoff
artifact. It can carry bounded context from a user/controller to an executor
agent, but it does not grant approval, execution authorization, commit
authorization, push authorization, merge authorization, release authorization,
lifecycle mutation authorization, destructive operation authorization,
protected/canonical mutation permission, or scope expansion permission.

All unsafe authorization booleans in the neutral handoff template default to
`false`. It requires human review and separate explicit human execution
authorization before any execution context can exist.

## Controlled Execution Package

Controlled Execution Package is the input artifact for Controlled Execution Guard `precheck`, `scopecheck`, and `postcheck`.

It does not authorize execution by itself. It must reference a real Human Execution Authorization, define the exact authorized files and scope, define forbidden files and actions, and name expected report and evidence paths.

Controlled Execution Package is the authorized execution context only after
explicit human execution authorization exists and is referenced by the package.

Safety boundary:
- PASS is not approval.
- Evidence is not approval.
- Commit requires separate human authorization.
- Push requires separate human authorization.

Copy `controlled-execution-package-template.yaml` into the working report/package location for your task before use, then replace every `REPLACE_WITH_...` field with concrete task data.

Example precheck command:

```bash
python3 aos/scripts/aos_controlled_execution_guard.py --project-root . --aos-root aos precheck --package aos/templates/execution-packages/controlled-execution-package-template.yaml
```

Do not run the template as a real task package until it has been copied and filled with a real Controlled Task Brief path, Human Execution Authorization path, authorized scope, forbidden scope, and expected output paths.
