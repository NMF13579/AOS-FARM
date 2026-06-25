# AOS-FARM-403 Combined Commit Authorization Package

## Target Tasks
- **AOS-FARM.404** — Controlled Final AOS Consumer Kit Methodology Addendum Commit
- **AOS-FARM.405** — Controlled Final AOS Consumer Kit Methodology Addendum Push

## Context
AOS-FARM.400 and AOS-FARM.401 successfully restored the full runbook-level methodology and the optional Python runner. AOS-FARM.402 verified that parity was maintained, and no forbidden modifications occurred. This package prepares the human authorization to commit and push these finalized files.

## Target Branch
- `dev`

## Permitted Commit Scope
Only the following areas are authorized for `git add` and `git commit`:
- `aos/docs/methodology/`
- `aos/docs/workflow/`
- `aos/prompts/`
- `aos/templates/task-briefs/`
- `aos/examples/problem-intake-to-controlled-task/`
- `aos/tools/optional/problem-intake-runner/`
- `reports/aos-farm-398-combined-methodology-runner-recovery-authorization-package.md`
- `reports/human-checkpoints/aos-farm-398-combined-methodology-runner-recovery-authorization.md`
- `reports/aos-farm-402-combined-methodology-runner-verification-report.md`
- `reports/aos-farm-403-combined-commit-authorization-package.md`
- `reports/human-checkpoints/aos-farm-403-combined-commit-authorization.md`

## Safety Invariants Checked
- **PASS ≠ approval**: CI/Testing pass on the runner does not mean we commit. We explicitly require this checkpoint.
- **Root Files Clean**: No changes to `00/01/02/03`, `AGENTS.md`, `README.md`, etc.
- **Legacy Files Clean**: No changes to `agentos/`.

## Proposed Commit Message
`docs: add full problem intake methodology and optional runner`

## Proposed Push Command
`git push origin HEAD:dev`

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**

## Final Status
**AOS_FARM_403_COMBINED_COMMIT_AUTHORIZATION_PREPARED**
