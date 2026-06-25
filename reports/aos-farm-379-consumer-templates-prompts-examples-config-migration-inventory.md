# AOS-FARM-379 Templates/Prompts/Examples/Config Migration Inventory

## Preflight Results
- **Branch**: dev
- **HEAD Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **origin/dev Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **Staged Changes**: None.
- **Root/Protected**: Unmodified.
- **Old `docs/`/`templates/`/`agentos/`**: Unmodified by this task.

## Required Sources Read Confirmation
- `00_AOS_Core_Control.md`: Read
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Read
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Read
- `reports/aos-farm-370-aos-consumer-kit-architecture-layout-plan.md`: Read
- `reports/aos-farm-374-aos-consumer-kit-skeleton-post-execution-verification.md`: Read
- `reports/aos-farm-375-consumer-docs-templates-migration-inventory.md`: Read
- `reports/aos-farm-378-consumer-docs-migration-batch-1-post-execution-verification.md`: Read

## Full Migration Classification

### 1. REWRITE_FOR_AOS_CONSUMER_KIT
*Existing templates/prompts that are conceptually useful but contain internal AOS-FARM history, Build Step tracking, dogfood cases, or project-specific runner logic.*
- `templates/task-brief-chain-template.md` -> `aos/templates/task-briefs/controlled-task-brief-template.md`
- `templates/execution-report-template.md` -> `aos/templates/reports/execution-report-template.md`
- `templates/post-execution-verification-template.md` -> `aos/templates/verification/post-execution-verification-template.md`
- `templates/execution-authorization-package-template.md` -> `aos/templates/authorization/execution-authorization-package-template.md`
- `templates/human-review.md` -> `aos/templates/checkpoints/human-execution-authorization-template.md`
- `templates/session-handoff-template.md` -> `aos/templates/handoff/session-handoff-template.md`

### 2. COPY_TO_AOS_AS_IS
*Files that require virtually no changes. Very rare.*
- (None recommended. Even simple templates require stripping internal context.)

### 3. AUTHOR_NEW_FOR_AOS_CONSUMER_KIT
*Missing files in the old repository that are needed for a clean consumer experience.*
- `aos/examples/first-controlled-task/README.md`
- `aos/examples/first-dry-run/README.md`
- `aos/config/aos-project-profile.md`
- `aos/config/aos-local-policy.md`
- `aos/config/risk-profile-policy.md`
- `aos/config/lifecycle-policy.md`
- `aos/config/protected-files-policy.md`
- `aos/config/cleanup-policy.md`
- `aos/prompts/first-task.md`
- `aos/prompts/tutor-start.md`
- `aos/prompts/review-before-commit.md`
- `aos/prompts/review-before-push.md`
- `aos/prompts/handoff.md`
- `aos/tools/dry-run-only/README.md`

### 4. KEEP_INTERNAL_ONLY
*Needed only for AOS-FARM development.*
- `00_AOS_Core_Control.md`, `01_AOS_Assembly_...`, `02_AOS_Governance_...`, `03_AOS_Future_...`
- Historical `reports/` and `reports/human-checkpoints/` before stage 370.

### 5. DO_NOT_MIGRATE
*Must never enter the consumer kit.*
- Spec Kit remnants.
- Internal python pipelines (`agentos/pipelines/`, `agentos/scripts/`).
- Historical `agentos/reports/` (dogfood outputs).

### 6. KEEP_ROOT
- `AGENTS.md`
- `README.md`
- `README.ru.md`

### 7. BLOCKED_UNKNOWN
- None.

## Batch 2 Recommendation
AOS-FARM.380 should strictly rewrite or newly author the identified consumer-facing templates, prompts, config, and examples directly inside the `aos/` folder.
