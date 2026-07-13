# Integration Shadow CI

The integration shadow workflow is an advisory GitHub Actions process for
AOS-FARM build branches and pull requests into `dev`.

It runs the same technical checks that are expected before integration review,
but it does not make those checks required, does not protect a branch, and does
not authorize integration.

Simple rule:

The shadow process runs checks on GitHub and shows the result, but it does not
block merging yet. A green result confirms only that the checks executed
successfully. It is not approval and does not authorize integration.

## Source of Truth

The workflow source is `.github/workflows/aos-advisory.yml`.

The workflow was fully replaced because the previous advisory workflow used
floating Action refs, a floating Python version, did not install development
dependencies, and could fail before `pytest` was available.

This document explains the static contract for the workflow. GitHub platform
execution is a future post-push observation, not something this local
implementation can prove before commit and push.

## Triggers

The workflow is allowed to run only on:

- manual `workflow_dispatch`
- pushes to `build/**`
- pull requests targeting `dev`

It must not use `pull_request_target`, `workflow_run`, schedules, release
events, deployment events, comments, repository dispatch, tags, or direct pushes
to `dev` or `main`.

## Permissions

The workflow has top-level read-only permissions:

```yaml
permissions:
  contents: read
```

Job-level permission expansion is not allowed. Write permissions, custom tokens,
SSH keys, GitHub App private keys, and `secrets.*` references are not allowed.

## Pinned Actions

Only first-party Actions are allowed:

- `actions/checkout`
- `actions/setup-python`

Both must be pinned to full 40-character commit SHAs. Floating refs such as
`@v4`, `@v5`, `@main`, or `@latest` are not allowed.

## Python and Dependencies

The workflow uses the repository-selected Python major.minor version and
installs dependencies only from `requirements-dev.txt`:

```bash
python -m pip install --requirement requirements-dev.txt
```

It does not use dependency caching in this first shadow stage. The goal is to
prove baseline repeatability without cache state.

## Check Sequence

The workflow runs these checks in order:

1. checkout with credentials persistence disabled
2. exact Python setup
3. environment report
4. development dependency installation
5. static workflow contract validation
6. integration contract verifier focused tests
7. control checks
8. full pytest

Every shell step starts with `set -euo pipefail`.

## Failure Semantics

Failure suppression is forbidden. The workflow must not use:

- `continue-on-error: true`
- `if: always()`
- `|| true`
- `set +e`
- a final `exit 0` after a failed validation

Any failed command must fail the job visibly on GitHub.

The job is advisory:

```yaml
workflow_failure:
  visible_on_GitHub: true
  merge_blocking: false
  reason: NO_REQUIRED_CHECK_OR_BRANCH_PROTECTION
workflow_success:
  approval: false
  integration_authorization: false
  merge_authorization: false
```

## Static Checker

`aos/scripts/aos_integration_shadow_workflow_check.py` checks the workflow
contract without network access and without repository writes.

It verifies path safety, line endings, triggers, permissions, pinned Action
refs, Python selection, required steps, forbidden commands, and failure
suppression.

The checker is intentionally static. It does not claim that GitHub accepted,
parsed, or executed the workflow. That can only be observed after the workflow
is committed, pushed, and GitHub creates a run.

## Future Platform Use

This stage reserves the path toward future deterministic platform checks, but it
does not create required check names and does not enable branch protection.

Future stages may split the shadow job into separately named checks such as:

- `aos-integration / contract`
- `aos-integration / candidate-binding`
- `aos-integration / protected-paths`
- `aos-integration / semantic-guard`
- `aos-integration / focused-tests`
- `aos-integration / full-pytest`

Those names are not created by this shadow workflow.

## Human Boundary

Workflow PASS is not approval.
CI PASS is not approval.
Shadow workflow creation is not platform enforcement.
Required checks are not enabled.
Branch protection is not enabled.
Integration, merge, release, and lifecycle mutation require separate human
authorization.
