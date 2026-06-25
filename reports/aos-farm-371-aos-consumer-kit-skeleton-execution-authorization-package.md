# AOS-FARM-371 AOS Consumer Kit Skeleton Creation Authorization Package

## Preflight Results
- **Branch**: dev
- **HEAD Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **origin/dev Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **Ahead/Behind**: 0 0
- **`aos/` Directory**: Does not exist.
- **Required Sources**: Verified and readable.
- **AOS-FARM.370 Report**: Verified and readable.

## Required Sources Read Confirmation
- `00_AOS_Core_Control.md`: Read
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Read
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Read
- `reports/aos-farm-370-aos-consumer-kit-architecture-layout-plan.md`: Read

## Proposed AOS-FARM.372 Execution Rules

### Goal
Execute the controlled creation of the initial `aos/` consumer kit skeleton, strictly matching the approved layout plan.

### Content Boundaries
Skeleton documents will be created as minimal but useful placeholders defining:
- AOS as a self-contained consumer kit.
- `aos/` as the installable/removable unit.
- Root `AGENTS.md` as the primary required root entrypoint.
- Optional `README.md` and `.gitignore` marker blocks.
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit/push/merge/release/destructive operations require explicit human authorization.
- Exclusions: No runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution included by default.

### Excluded from Skeleton Creation Task (AOS-FARM.372)
- Historical AOS-FARM reports.
- AOS-FARM internal development sources (`00`, `01`, `02`, `03`).
- Migration of existing `docs/` and `templates/`.
- Modifications to current repository root files (`AGENTS.md`, `README.md`, `README.ru.md`).

### Proposed Directory List
```text
aos/
aos/root/
aos/docs/
aos/docs/user-guide/
aos/docs/governance/
aos/docs/workflow/
aos/docs/assembly/
aos/docs/operations/
aos/docs/lifecycle/
aos/docs/reference/
aos/templates/
aos/templates/task-briefs/
aos/templates/checkpoints/
aos/templates/reports/
aos/templates/verification/
aos/templates/authorization/
aos/templates/handoff/
aos/prompts/
aos/examples/
aos/examples/first-controlled-task/
aos/examples/first-dry-run/
aos/reports/
aos/reports/examples/
aos/reports/human-checkpoints/
aos/reports/human-checkpoints/examples/
aos/config/
aos/tools/
aos/tools/dry-run-only/
```

### Proposed Skeleton File List
```text
aos/README.md
aos/START_HERE.md
aos/INSTALL.md
aos/ADOPTION.md
aos/UNINSTALL.md
aos/REMOVAL_CHECKLIST.md
aos/MANIFEST.md
aos/VERSION.md
aos/CHANGELOG.md
aos/COMPATIBILITY.md
aos/SELF_TEST.md
aos/AGENT_CONTEXT.md
aos/root/AGENTS.md
aos/root/README_AOS_SECTION.md
aos/root/gitignore.snippet
aos/root/ROOT_FILES_MANIFEST.md
aos/root/ROOT_INSTALL_GUIDE.md
aos/docs/README.md
aos/docs/user-guide/README.md
aos/docs/governance/README.md
aos/docs/workflow/README.md
aos/docs/assembly/README.md
aos/docs/operations/README.md
aos/docs/lifecycle/README.md
aos/docs/reference/README.md
aos/docs/reference/agent-reading-order.md
aos/templates/README.md
aos/templates/task-briefs/README.md
aos/templates/checkpoints/README.md
aos/templates/reports/README.md
aos/templates/verification/README.md
aos/templates/authorization/README.md
aos/templates/handoff/README.md
aos/prompts/README.md
aos/prompts/tutor-start.md
aos/prompts/first-task.md
aos/prompts/review-before-commit.md
aos/prompts/review-before-push.md
aos/prompts/handoff.md
aos/examples/README.md
aos/examples/first-controlled-task/README.md
aos/examples/first-dry-run/README.md
aos/reports/README.md
aos/reports/.gitkeep
aos/reports/examples/README.md
aos/reports/human-checkpoints/README.md
aos/reports/human-checkpoints/.gitkeep
aos/reports/human-checkpoints/examples/README.md
aos/config/README.md
aos/config/aos-project-profile.md
aos/config/aos-local-policy.md
aos/config/risk-profile-policy.md
aos/config/lifecycle-policy.md
aos/config/protected-files-policy.md
aos/config/cleanup-policy.md
aos/tools/README.md
aos/tools/dry-run-only/README.md
```

### Commit / Push Deferral Rule
Commit and push operations are deferred until the final stage verification for the whole AOS consumer kit migration stage. AOS-FARM.372 must not commit or push.

### Risk Profile Proposal
**HIGH_RISK_PROTECTED**

*Reasoning: This establishes a new public product architecture skeleton. While creating new files is generally low risk to existing operation, it establishes the new canonical architecture layout.*

## Status
- **Authorization**: PENDING
- **Blocking Issues**: None.
- **Warnings**: None.
- **Final Status**: **AOS_FARM_371_AOS_CONSUMER_KIT_SKELETON_EXECUTION_AUTHORIZATION_PREPARED**
