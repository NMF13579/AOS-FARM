# AOS-FARM-406 Combined Methodology and Runner Commit Authorization Package

## Target Tasks
- **AOS-FARM.407** — Controlled Final AOS Consumer Kit Methodology Addendum Commit
- **AOS-FARM.408** — Controlled Final AOS Consumer Kit Methodology Addendum Push

## Context
AOS-FARM.404 successfully eliminated prior compression by mirroring 100% of the Problem Intake and Technical Assignment methodology (11 core files, 7 runbooks, 4 extensions) into the AOS Consumer Kit. AOS-FARM.405 verified that this restoration maintains strict source parity while isolating the legacy Python runners as optional, powerless tools. 

This package formally requests explicit human authorization to commit and push this finalized, uncompressed methodology to the `dev` branch.

## Permitted Commit Scope
Only the following paths are authorized for `git add` and `git commit`:
- `aos/docs/methodology/` (including all new subdirectories, runbooks, and extensions)
- `aos/docs/workflow/`
- `aos/prompts/`
- `aos/templates/task-briefs/`
- `aos/examples/problem-intake-to-controlled-task/`
- `aos/tools/optional/problem-intake-runner/`
- `reports/aos-farm-404-full-methodology-source-parity-remediation-report.md`
- `reports/aos-farm-405-combined-methodology-runner-final-verification-report.md`
- `reports/aos-farm-406-combined-methodology-runner-commit-authorization-package.md`
- `reports/human-checkpoints/aos-farm-406-combined-methodology-runner-commit-authorization.md`

## Safety Invariants Checked
- **PASS ≠ approval**: Completion of this task series does not automate a commit. Human authorization is strictly required.
- **Root/Legacy Clean**: No modifications were made outside the authorized `aos/` targets and `reports/`.

## Proposed Commit Message
`docs: add full uncompressed problem intake methodology and optional runner`

## Proposed Push Command
`git push origin HEAD:dev`

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**

## Final Status
**AOS_FARM_406_COMBINED_METHODOLOGY_RUNNER_COMMIT_AUTHORIZATION_PREPARED**
