# AOS-FARM-375 Consumer Docs/Templates Migration Inventory

## Preflight Results
- **Branch**: dev
- **HEAD Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **origin/dev Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **Staged Changes**: None.
- **Root/Protected**: Unmodified.
- **`aos/` Skeleton**: Present and untracked.

## Required Sources Read Confirmation
- `00_AOS_Core_Control.md`: Read
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Read
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Read
- `reports/aos-farm-370-aos-consumer-kit-architecture-layout-plan.md`: Read
- `reports/aos-farm-374-aos-consumer-kit-skeleton-post-execution-verification.md`: Read

## Full Migration Classification

### 1. COPY_TO_AOS_AS_IS
*Very few files are perfectly generic without AOS-FARM references. These will be heavily scrutinized.*
- (None identified initially; assuming all need at least minor rewrite to strip "AOS-FARM" repo context)

### 2. REWRITE_FOR_AOS_CONSUMER_KIT
*Files whose ideas/structures are essential for the consumer kit but contain internal AOS-FARM development history, roadmap logic, or specific project dogfood language.*
- `docs/` (all contents)
- `templates/` (all contents)
- `agentos/docs/minimal-safety-floor.md`
- `agentos/docs/strategy-lock.md`
- `agentos/docs/methodology/technical-assignment/` (all guides and runbooks)
- `agentos/templates/` (some generic ones like project-brief)

### 3. KEEP_INTERNAL_ONLY
*Internal development logic, governance for the AOS-FARM repo itself.*
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md`
- `reports/` (all historical `aos-farm-*` reports before 370)
- `reports/human-checkpoints/` (all historical checkpoints before 370)
- Local-only closure reports.

### 4. DO_NOT_MIGRATE
*Historical artifacts, runners, pipelines, dogfood evidence.*
- `agentos/reports/` (all build step reports and problem intake runs)
- `agentos/tasks/` (internal dev tasks)
- `agentos/scripts/` (python runners, validators)
- `agentos/pipelines/` (python pipelines)
- Spec Kit remnants (none found).
- Stale evidence-tail files.

### 5. KEEP_ROOT
*Root entrypoints that remain in the repo root.*
- `AGENTS.md`
- `README.md`
- `README.ru.md`

### 6. BLOCKED_UNKNOWN
- None.

## Batch 1 Recommendation
A bounded migration focusing only on the most critical user-facing onboarding and governance essentials.
