# AOS-FARM.362 Spec Kit and Warning Cleanup Authorization Package

## Context
AOS-FARM requires a clean consumer install model (a self-contained `agentos/` kit plus minimal root `AGENTS.md`). Spec Kit active remnants and recurring warnings (duplicate docs, stale local reports) clutter this surface and must be cleaned up. This package authorizes the destructive cleanup.

## Destructive Operation Boundary
- **Proposed Risk Profile**: `HIGH_RISK_PROTECTED` or `DESTRUCTIVE_OR_CANONICAL`
- **Execution Authorized by this Package**: None (DRAFT). Human must approve the exact candidate lists below.

## 1. DELETE_SPEC_KIT_CANDIDATES
Exact paths to be permanently removed from the repository using `git rm -r`:
- `.specify/`
- `.github/prompts/speckit.agent-context.update.prompt.md`
- `.github/prompts/speckit.analyze.prompt.md`
- `.github/prompts/speckit.checklist.prompt.md`
- `.github/prompts/speckit.clarify.prompt.md`
- `.github/prompts/speckit.constitution.prompt.md`
- `.github/prompts/speckit.implement.prompt.md`
- `.github/prompts/speckit.plan.prompt.md`
- `.github/prompts/speckit.specify.prompt.md`
- `.github/prompts/speckit.tasks.prompt.md`
- `.github/prompts/speckit.taskstoissues.prompt.md`
- `.github/agents/speckit.agent-context.update.agent.md`
- `.github/agents/speckit.analyze.agent.md`
- `.github/agents/speckit.checklist.agent.md`
- `.github/agents/speckit.clarify.agent.md`
- `.github/agents/speckit.constitution.agent.md`
- `.github/agents/speckit.implement.agent.md`
- `.github/agents/speckit.plan.agent.md`
- `.github/agents/speckit.specify.agent.md`
- `.github/agents/speckit.tasks.agent.md`
- `.github/agents/speckit.taskstoissues.agent.md`
- `specs/`
- `constitution.md`
- `scripts/validate-spec.sh`

## 2. DELETE_WARNING_CANDIDATES
Exact untracked or stale files to be permanently removed from the working tree (`rm -rf`):
- `docs/assembly/aos-native-build-step-batch-strategy-mvp 2.md`
- `docs/assembly/aos-native-spec-to-execution-pattern-pack-mvp 2.md`
- `docs/assembly/code-assembly-pipeline-contract 2.md`
- `docs/assembly/code-assembly-pipeline-mvp 2.md`
- `docs/assembly/code-diff-evidence-expectations 2.md`
- `docs/assembly/documentation-assembly-pipeline-mvp 2.md`
- `docs/assembly/documentation-assembly-pipeline-skeleton 2.md`
- `docs/assembly/task-brief-to-scoped-code-change 2.md`
- `docs/governance/governance-control-module-contract 2.md`
- `docs/governance/human-checkpoint-boundary 2.md`
- `docs/governance/minimal-safety-floor 2.md`
- `docs/governance/pass-evidence-approval-boundary 2.md`
- `docs/governance/unknown-not-run-pass-semantics 2.md`
- `docs/operations/agent-routing-policy 2.md`
- `docs/operations/ide-architect-controller-mode 2.md`
- `docs/operations/multi-environment-agent-workflow 2.md`
- `docs/operations/token-budget-and-model-routing-policy 2.md`
- `docs/validation/aos-farm-task-verification-checker-contract 2.md`
- `reports/aos-farm-351-remediation-commit-push-authorization-package.md`
- `reports/aos-farm-353-remediation-push-and-remote-closure.md`
- `reports/aos-farm-356-installation-guide-commit-push-authorization-package.md`
- `reports/aos-farm-359-installation-guide-push-and-remote-closure.md`
- `reports/aos-farm-361-readme-landing-page-commit-push-authorization-package.md`
- `reports/aos-farm-364-readme-landing-page-push-and-remote-closure.md`
- `reports/human-checkpoints/aos-farm-351-remediation-commit-push-authorization.md`
- `reports/human-checkpoints/aos-farm-356-installation-guide-commit-push-authorization.md`
- `reports/human-checkpoints/aos-farm-361-readme-landing-page-commit-push-authorization.md`
- `agentos/reports/problem-intake/`

## 3. MOVE_TO_INTERNAL_OR_LEGACY_CANDIDATES
Exact files to be moved to an `internal/legacy/` directory (or deleted if preferred):
- `docs/references/spec-kit-reference.md`
- `docs/boundaries/spec-kit-implement-boundary.md`

## 4. KEEP_AS_ACTIVE
AOS-native template files containing "spec", which will NOT be removed:
- `templates/feature-spec-template.md`
- `templates/spec-to-execution-traceability-matrix-template.md`
- `docs/assembly/aos-native-spec-to-execution-pattern-pack-mvp.md`

## 5. KEEP_AS_REFERENCE
Tracked historical reports containing Spec Kit keywords, which will NOT be removed:
- `reports/aos-farm-96-4-spec-to-execution-pattern-pack-post-execution-verification.md`
- `reports/aos-farm-constitution-alignment-edit-report.md`
- `reports/aos-farm-constitution-alignment-plan.md`
- `reports/aos-farm-constitution-human-checkpoint-intake.md`
- `reports/aos-farm-constitution-human-checkpoint-package.md`
- `reports/aos-farm-post-constitution-alignment-validation.md`
- `reports/aos-farm-spec-to-execution-pattern-pack-mvp-report.md`
- `reports/human-checkpoints/aos-farm-constitution-alignment-approval.md`

## 6. BLOCKED_UNKNOWN
- None.

## Commit Message Proposal
`chore: remove Spec Kit remnants and clean up untracked local warnings`

## Next Action Required
Human: Please review the candidate lists above. If approved, change the status in `reports/human-checkpoints/aos-farm-362-spec-kit-warning-cleanup-authorization.md` to `APPROVED_FOR_CLEANUP` and assign the Risk Profile.
