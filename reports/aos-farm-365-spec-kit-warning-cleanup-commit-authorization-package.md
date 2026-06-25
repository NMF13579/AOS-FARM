# AOS-FARM.365 Cleanup Commit Authorization Package

## Goal
Request human authorization to commit the staged destructive cleanup (Spec Kit removal) and the accompanying execution/verification reports to the local `dev` branch.

## Commit Candidate Set
The exact files to be committed:
1. **Staged Deletions (Tracked Spec Kit removal)**:
   - `.specify/` (all contents)
   - `.github/prompts/speckit.*`
   - `.github/agents/speckit.*`
   - `specs/` (all contents)
   - `constitution.md`
   - `scripts/validate-spec.sh`
   - `docs/references/spec-kit-reference.md`
   - `docs/boundaries/spec-kit-implement-boundary.md`
2. **Execution and Authorization Evidence**:
   - `reports/aos-farm-362-spec-kit-warning-cleanup-authorization-package.md`
   - `reports/human-checkpoints/aos-farm-362-spec-kit-warning-cleanup-authorization.md`
   - `reports/aos-farm-364-controlled-spec-kit-warning-cleanup-execution.md`
   - `reports/aos-farm-365-spec-kit-warning-cleanup-verification.md`
   - `reports/aos-farm-365-spec-kit-warning-cleanup-commit-authorization-package.md`
   - `reports/human-checkpoints/aos-farm-365-spec-kit-warning-cleanup-commit-authorization.md`

## Safety Checks
- The deletion strictly followed the `HIGH_RISK_PROTECTED` authorization from AOS-FARM.363.
- Untracked warning clutter was permanently deleted from the working tree (does not require commit).
- Canonical files were untouched.
- No unauthorized edits were introduced.

## Proposed Commit Message
`docs: remove spec kit remnants and cleanup warnings`

## Next Action Required
Human: Review the verification report and commit candidates. If approved, change the status in `reports/human-checkpoints/aos-farm-365-spec-kit-warning-cleanup-commit-authorization.md` to `APPROVED_FOR_COMMIT`.
