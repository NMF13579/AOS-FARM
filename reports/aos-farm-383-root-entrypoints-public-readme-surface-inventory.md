# AOS-FARM-383 Root Entrypoints and Public README Surface Inventory

## Preflight Results
- **Branch**: dev
- **HEAD Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **Staged Changes**: None.
- **Root/Protected files**: Unmodified.
- **Old `docs/`/`templates/`/`agentos/`**: Unmodified by this task.

## Required Sources Read Confirmation
- `00_AOS_Core_Control.md`: Read
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Read
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Read
- `reports/aos-farm-370-aos-consumer-kit-architecture-layout-plan.md`: Read
- `reports/aos-farm-374-aos-consumer-kit-skeleton-post-execution-verification.md`: Read
- `reports/aos-farm-378-consumer-docs-migration-batch-1-post-execution-verification.md`: Read
- `reports/aos-farm-382-consumer-templates-prompts-examples-config-batch-2-post-execution-verification.md`: Read

## Current Surface Assessment
- `README.md`: Currently acts as the development manifest for AOS-FARM. Highly complex, focuses on the Build Step roadmap and history. Unsuitable for the final public consumer release.
- `README.ru.md`: Russian translation of the same complex history.
- `AGENTS.md`: Currently enforces strict rules based on `00/01/02/03`. This is crucial for protecting AOS-FARM development, but does not point public users' agents to the `aos/` consumer kit.
- `aos/root/*`: Contains the templates (`AGENTS.md`, `README_AOS_SECTION.md`, etc.) that consumer users will copy to their own projects.

## Inventory Classification

### 1. UPDATE_NOW
*Safe, bounded changes for AOS-FARM.384.*
- `README.md`: Rewrite to become the public-facing storefront for the AOS project. Describe what it is, how to use the `aos/` folder, and key safety rules.
- `README.ru.md`: Rewrite to mirror the new English README.
- `AGENTS.md`: Append instructions directing visiting AI agents to `aos/AGENT_CONTEXT.md` and `aos/START_HERE.md` to understand the public product, while strictly retaining `00/01/02/03` as internal development rules.

### 2. DEFER
*Useful changes waiting until final public-release polishing.*
- `llms.txt`: Defer. `aos/AGENT_CONTEXT.md` serves this purpose for now. An official standard `llms.txt` should be generated at the final stage when all docs are perfectly stable.

### 3. DO_NOT_CHANGE
*Must not be touched in AOS-FARM.384.*
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md`
- `aos/root/*` templates (these are part of the kit, not the repo's own active root).
- Old `docs/`, `templates/`, `agentos/`.

### 4. BLOCKED_UNKNOWN
- None.

## Batch 3 Recommendation
AOS-FARM.384 should execute the bounded update to `README.md`, `README.ru.md`, and `AGENTS.md`. No commit/push should be performed.
