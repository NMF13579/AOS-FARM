# AOS-FARM.574 Final Review Package

## Review purpose
To evaluate the implementation of the Consumer Advisory CI Template and authorize the next lifecycle stage (commit).

## What changed
- Created `aos/root/.github/workflows/aos-advisory.yml` to serve as a template for target projects.
- Updated `aos/docs/FIRST-SAFE-COMMANDS.md` with instructions on how to use the consumer advisory CI template.
- Updated `aos/docs/ROUTES.md` with a new route covering the setup of the consumer CI template.

## Why it matters
Target projects can now adopt a standard advisory validation workflow that runs compile checks, semantic guard validations, and unit tests, ensuring code quality without imposing mandatory gates or false approvals.

## Consumer installation impact
Consumers can copy `/aos/root/.github/workflows/aos-advisory.yml` to `.github/workflows/aos-advisory.yml` in their projects to enable advisory CI on `pull_request` and `push` to `dev`.

## Advisory CI impact
Provides early validation signals in the target project without functioning as an approval gate.

## Safety impact
Preserves the core safety boundary: CI PASS is not an approval. The template explicitly states it should not be configured as a required check and does not authorize execution or mutations.

## Residual risks
If a consumer fails to copy the `/tests/` directory, the unit test step will fail or skip (reporting NOT_RUN). This caveat is noted, and consumer instructions may need further adaptation if testing structures diverge.

## Validation summary
All local python validation and task document checks passed. No canonical or protected files were modified.

## Required human decisions
The human owner must review these changes and provide explicit authorization to commit.

## Recommended next stage
Grant commit authorization for the `build/aos-farm-574-consumer-advisory-ci-template` branch.

## Explicit non-approval statement
This final review package is not approval.
Consumer Advisory CI PASS is not approval.
The consumer workflow template does not authorize execution, lifecycle mutation, commit, push, merge, release, or next-stage transition.
The consumer workflow template does not enable branch protection or required checks by itself.
Human decision is still required.
