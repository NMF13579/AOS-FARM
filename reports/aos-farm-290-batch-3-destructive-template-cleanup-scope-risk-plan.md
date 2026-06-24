# AOS-FARM.290 — Batch 3 Destructive Template Cleanup Scope/Risk Plan

## Exact Duplicate Inventory
There are 41 files with the ` 2.md` suffix in the `templates/` directory. For each, the canonical counterpart exists.

1. `templates/allowed-forbidden-code-change-template 2.md` -> `templates/allowed-forbidden-code-change-template.md` (Exists: true)
2. `templates/aos-farm-task-verification-input-template 2.md` -> `templates/aos-farm-task-verification-input-template.md` (Exists: true)
3. `templates/aos-farm-task-verification-output-template 2.md` -> `templates/aos-farm-task-verification-output-template.md` (Exists: true)
4. `templates/build-plan-template 2.md` -> `templates/build-plan-template.md` (Exists: true)
5. `templates/build-step-batch-scope-template 2.md` -> `templates/build-step-batch-scope-template.md` (Exists: true)
6. `templates/build-step-batch-verification-template 2.md` -> `templates/build-step-batch-verification-template.md` (Exists: true)
7. `templates/clarification-gate-template 2.md` -> `templates/clarification-gate-template.md` (Exists: true)
8. `templates/code-assembly-mvp-evidence-report-template 2.md` -> `templates/code-assembly-mvp-evidence-report-template.md` (Exists: true)
9. `templates/code-assembly-mvp-execution-report-template 2.md` -> `templates/code-assembly-mvp-execution-report-template.md` (Exists: true)
10. `templates/code-assembly-mvp-human-review-template 2.md` -> `templates/code-assembly-mvp-human-review-template.md` (Exists: true)
11. `templates/code-assembly-mvp-input-template 2.md` -> `templates/code-assembly-mvp-input-template.md` (Exists: true)
12. `templates/code-assembly-traceability-matrix-template 2.md` -> `templates/code-assembly-traceability-matrix-template.md` (Exists: true)
13. `templates/code-assembly-verification-report-template 2.md` -> `templates/code-assembly-verification-report-template.md` (Exists: true)
14. `templates/code-change-scope-template 2.md` -> `templates/code-change-scope-template.md` (Exists: true)
15. `templates/code-diff-evidence-template 2.md` -> `templates/code-diff-evidence-template.md` (Exists: true)
16. `templates/code-execution-package-template 2.md` -> `templates/code-execution-package-template.md` (Exists: true)
17. `templates/documentation-assembly-input-template 2.md` -> `templates/documentation-assembly-input-template.md` (Exists: true)
18. `templates/documentation-assembly-output-template 2.md` -> `templates/documentation-assembly-output-template.md` (Exists: true)
19. `templates/documentation-assembly-report-template 2.md` -> `templates/documentation-assembly-report-template.md` (Exists: true)
20. `templates/execution-authorization-package-template 2.md` -> `templates/execution-authorization-package-template.md` (Exists: true)
21. `templates/feature-intake-template 2.md` -> `templates/feature-intake-template.md` (Exists: true)
22. `templates/feature-spec-template 2.md` -> `templates/feature-spec-template.md` (Exists: true)
23. `templates/final-build-step-commit-candidate-template 2.md` -> `templates/final-build-step-commit-candidate-template.md` (Exists: true)
24. `templates/governance-control-gate-matrix-template 2.md` -> `templates/governance-control-gate-matrix-template.md` (Exists: true)
25. `templates/governance-control-module-contract-template 2.md` -> `templates/governance-control-module-contract-template.md` (Exists: true)
26. `templates/human-approval-boundary-template 2.md` -> `templates/human-approval-boundary-template.md` (Exists: true)
27. `templates/ide-controller-next-task-template 2.md` -> `templates/ide-controller-next-task-template.md` (Exists: true)
28. `templates/ide-controller-review-report-template 2.md` -> `templates/ide-controller-review-report-template.md` (Exists: true)
29. `templates/manual-code-review-checkpoint-template 2.md` -> `templates/manual-code-review-checkpoint-template.md` (Exists: true)
30. `templates/minimal-safety-floor-checklist-template 2.md` -> `templates/minimal-safety-floor-checklist-template.md` (Exists: true)
31. `templates/model-routing-decision-template 2.md` -> `templates/model-routing-decision-template.md` (Exists: true)
32. `templates/multi-environment-handoff-template 2.md` -> `templates/multi-environment-handoff-template.md` (Exists: true)
33. `templates/multi-environment-session-start-template 2.md` -> `templates/multi-environment-session-start-template.md` (Exists: true)
34. `templates/safety-gate-matrix-template 2.md` -> `templates/safety-gate-matrix-template.md` (Exists: true)
35. `templates/session-limit-handoff-template 2.md` -> `templates/session-limit-handoff-template.md` (Exists: true)
36. `templates/spec-to-execution-traceability-matrix-template 2.md` -> `templates/spec-to-execution-traceability-matrix-template.md` (Exists: true)
37. `templates/step-safety-verification-report-template 2.md` -> `templates/step-safety-verification-report-template.md` (Exists: true)
38. `templates/task-brief-chain-template 2.md` -> `templates/task-brief-chain-template.md` (Exists: true)
39. `templates/token-budget-task-header-template 2.md` -> `templates/token-budget-task-header-template.md` (Exists: true)
40. `templates/unknown-not-run-pass-semantics-template 2.md` -> `templates/unknown-not-run-pass-semantics-template.md` (Exists: true)
41. `templates/verification-evidence-report-template 2.md` -> `templates/verification-evidence-report-template.md` (Exists: true)

## Exact Proposed Deletion Candidate List
All 41 files ending in ` 2.md` listed above are proposed for deletion via `git rm`.

## Exact Files That Must Be Preserved
All corresponding canonical template files (those without the ` 2.md` suffix) must be preserved without modification. Core governance files (`00`, `01`, `02`) and user guides must not be touched.

## Why Cleanup is Destructive
The operation requires permanently removing untracked and/or tracked files from the file system and Git history (if previously committed). Removing any files from `templates/` is defined as a Protected/Canonical modification.

## Why Cleanup is Required Before Release Preparation
These duplicates cause "Source of Truth ambiguity." They confuse human users doing manual template selection and can cause AI agents to pick the wrong template context, directly blocking safe and clean minimal public release preparation.

## Fallback Plan If Ambiguity Is Found
If any canonical template counterpart is found to be missing or mismatched during execution, the operation must immediately HALT and fail closed (`BLOCKED`), requiring human review to resolve the discrepancy before any deletion.

## Risk Profile
agent_proposed_risk_profile: HIGH_RISK_PROTECTED
human_assignment_required: true
