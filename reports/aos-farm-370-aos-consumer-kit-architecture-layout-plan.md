# AOS-FARM-370 AOS Consumer Kit Architecture Layout Plan

## Preflight Results
- **Branch**: dev
- **HEAD Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **origin/dev Commit**: 445e3f1ec5c01fdacf65cc426500c8528d28bc48
- **Ahead/Behind**: 0 0
- **Status**: Clean baseline, remote baseline is closed.

## Required Sources Read Confirmation
- `00_AOS_Core_Control.md` - Read
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` - Read
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md` - Read

## 1. Naming Decision
**Recommendation: `aos/`**

- **Product Clarity**: `aos/` provides a shorter, cleaner prefix that directly aligns with the AOS identity, signaling it as the modern active consumer directory.
- **Compatibility with Current Repository**: Using `aos/` cleanly isolates the new consumer kit from the legacy `agentos/` internal development folder, allowing a safe, parallel migration without immediately breaking the internal workflow.
- **Migration Cost**: Low. By establishing a new folder, we avoid destructive inplace renames of existing directories.
- **User Comprehension**: `aos/` is concise and recognizable as a tool-specific dot-folder alternative (even without the dot).
- **Uninstall Clarity**: Easy to identify and remove entirely by deleting the `aos/` folder.
- **Long-term Branding**: It shifts away from generic "agentos" to the specific product name "AOS".

*Note: Treat `agentos/` as legacy/current internal naming unless a later migration plan decides otherwise.*

## 2. Target Consumer Kit Structure
The target directory structure for the consumer kit (`aos/`) is designed to be completely self-contained.

### `aos/` Root Files
- `README.md`: Internal consumer kit guide, explaining the structure and logic of the `aos/` directory itself.
- `START_HERE.md`: The absolute entrypoint for a new user trying to use AOS in their project.
- `INSTALL.md`: Instructions for installing/adopting AOS into new or existing projects.
- `ADOPTION.md`: Guidance on adopting AOS into an already mature, non-AOS project.
- `UNINSTALL.md`: Steps to safely remove AOS and revert the project state.
- `REMOVAL_CHECKLIST.md`: A verification checklist to ensure all AOS components are cleanly removed.
- `MANIFEST.md`: An index of all files and their expected roles within the consumer kit.
- `VERSION.md`: Tracks the specific version of the consumer kit installed.
- `CHANGELOG.md`: Tracks updates and changes to the consumer kit.
- `COMPATIBILITY.md`: Documents required model capabilities, IDEs, and environments.
- `SELF_TEST.md`: Instructions and scripts (or safe dry-runs) to verify the kit is functioning correctly.
- `AGENT_CONTEXT.md`: System orientation file for the AI agent to read first when operating inside the kit.

### `aos/` Directories
- `root/`: Contains templates or snippets that must be placed in the project root (e.g. the root `AGENTS.md`).
- `docs/`: The core framework documentation, rules, and user guides for the consumer.
- `templates/`: Blank templates for tasks, checkpoints, and reports for consumer use.
- `prompts/`: Standardized system prompts and tutor prompts.
- `examples/`: Sample `task.md` or reports demonstrating correct usage.
- `reports/`: The default directory where the consumer's agent will place execution and execution reports.
- `config/`: Configurations for validators, linting, or CI integration.
- `tools/`: Utility scripts, validators, and helpers for the framework.

## 3. Root Entrypoint Model
The root entrypoint defines how AOS integrates into the consumer's root directory.

- **Mandatory Root Files**: 
  - Root `AGENTS.md` (or an AOS block inside an existing `AGENTS.md`).
- **Optional Root Files**: 
  - README AOS section (in the project's root `README.md`).
  - `.gitignore` snippet for AOS temporary files.
  - Root `llms.txt` (to be considered later once the layout stabilizes).
- **Deployment Model from `aos/root/`**: Files in `aos/root/` act as pristine sources that the user copies to their project root.
- **Uninstall Model for Root Files**: The user removes `AGENTS.md` (or the AOS marker block), and strips any AOS marker blocks from `README.md` and `.gitignore`.
- **Marker Block Policy**: All injected content in root files must be wrapped in standard markers to guarantee clean removal.
  - `<!-- AOS-START -->` and `<!-- AOS-END -->`
  - `<!-- AOS-AGENTS-START -->` and `<!-- AOS-AGENTS-END -->`

## 4. Install Model
AOS does not use active runners or automation as the required install path. Instead, it relies on file copying and AI Tutor guidance.

- **Clean new project**: Copy the entire `aos/` folder to the project, copy `aos/root/AGENTS.md` to root.
- **Existing project adoption**: Copy `aos/` folder, insert `<!-- AOS-AGENTS-START -->` block into existing `AGENTS.md` and optionally `README.md`/`.gitignore`.
- **Temporary use**: Copy `aos/`, use for a specific refactor, then remove according to `UNINSTALL.md`.
- **AI Tutor guided install**: The user pastes a prompt to their IDE agent (e.g., "Act as AOS Tutor and guide me through installation using `aos/START_HERE.md`").
- **Future dry-run helper**: A potential safe script to verify paths without mutating.

## 5. Uninstall Model
Uninstalling AOS must be deterministic and leave zero traces.

1. Delete the `aos/` directory entirely.
2. Delete the root `AGENTS.md` if it was created exclusively for AOS.
3. Otherwise, remove the `<!-- AOS-AGENTS-START -->` to `<!-- AOS-AGENTS-END -->` block from the existing root `AGENTS.md`.
4. Remove the `<!-- AOS-START -->` to `<!-- AOS-END -->` block from `README.md` (if inserted).
5. Remove the `<!-- AOS-START -->` to `<!-- AOS-END -->` block from `.gitignore` (if inserted).
6. Verify no AOS-managed files remain (using `REMOVAL_CHECKLIST.md`).

## 6. Current Repo Migration Inventory

| Asset | Classification | Justification |
|-------|----------------|---------------|
| `docs/` | REWRITE_FOR_CONSUMER_KIT | Contains valuable material but is heavily tied to internal AOS-FARM processes. Must be generalized. |
| `templates/` | REWRITE_FOR_CONSUMER_KIT | Must be generalized to strip AOS-FARM internal context. |
| `agentos/` | KEEP_INTERNAL_ONLY | Legacy internal workspace. Retained for historical reference but excluded from consumer kit. |
| `reports/` | KEEP_INTERNAL_ONLY | Contains internal AOS-FARM execution history. |
| `AGENTS.md` | REWRITE_FOR_CONSUMER_KIT | Needs to be split: internal rules stay in repo, generic rules move to `aos/root/AGENTS.md`. |
| `README.md` | REWRITE_FOR_CONSUMER_KIT | Current README is for the AOS-FARM repository. Consumer kit needs a separate README and a snippet for the user's project README. |
| `README.ru.md` | REWRITE_FOR_CONSUMER_KIT | Same as English README. |
| `00_AOS_Core_Control.md` | KEEP_INTERNAL_ONLY | Core internal governance source. |
| `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` | KEEP_INTERNAL_ONLY | Internal assembly roadmap. |
| `02_AOS_Governance_Control_Module_and_Safety_Rules.md` | KEEP_INTERNAL_ONLY | Internal safety rules. |
| `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md` | KEEP_INTERNAL_ONLY | Legacy reference. |
| Spec Kit references (in reports) | KEEP_INTERNAL_ONLY | Only historical reports remain. Exclude completely. |
| Historical AOS-FARM reports | KEEP_INTERNAL_ONLY | Exclude completely. |
| `reports/aos-farm-369-cleanup-push-remote-baseline-closure.md` | KEEP_INTERNAL_ONLY | Local closure report for internal use. |

## 7. Consumer Kit Exclusions
The following items **MUST NOT** enter the clean consumer kit:
- Historical AOS-FARM reports (e.g. anything in `reports/` with `aos-farm-` prefix).
- AOS-FARM internal development sources (`00`, `01`, `02`, `03`).
- Spec Kit remnants.
- Runner or CI workflows from AOS-FARM development.
- DB / RAG / vector logic.
- Release / tag artifacts.
- Project-specific dogfood reports or fixtures.
- Local-only closure reports.
- Old evidence-tail files.

## 8. Migration Batch Plan
Execution of this layout will be staged. Each batch requires human authorization.

- **Batch 1: Skeleton Creation**
  - **Scope**: Create `aos/` folder skeleton only.
  - **Expected Files**: Empty directories inside `aos/`.
  - **Risk**: LOW_RISK_FAST
  - **Required Checkpoint**: Post-creation validation.
  - **Forbidden**: Modifying existing files.

- **Batch 2: Core Documentation**
  - **Scope**: Add install/uninstall/manifest/self-test docs.
  - **Expected Files**: `README.md`, `START_HERE.md`, `INSTALL.md`, `UNINSTALL.md`, `MANIFEST.md`, `SELF_TEST.md`.
  - **Risk**: MEDIUM_RISK_GUIDED
  - **Required Checkpoint**: Review of document content.
  - **Forbidden**: Moving current `docs/`.

- **Batch 3: User Guides Migration**
  - **Scope**: Migrate or rewrite user-guide docs into `aos/docs/`.
  - **Expected Files**: Consumer-facing guides.
  - **Risk**: MEDIUM_RISK_GUIDED
  - **Required Checkpoint**: Review of rewritten guides.
  - **Forbidden**: Deleting internal `docs/`.

- **Batch 4: Governance Docs Migration**
  - **Scope**: Migrate or rewrite governance/workflow docs into `aos/docs/`.
  - **Expected Files**: Generalized safety floor and governance rules.
  - **Risk**: HIGH_RISK_PROTECTED
  - **Required Checkpoint**: Strict review to ensure no internal control logic leaked.
  - **Forbidden**: Modifying `00/01/02/03`.

- **Batch 5: Templates Migration**
  - **Scope**: Migrate or rewrite templates into `aos/templates/`.
  - **Expected Files**: Task briefs, checkpoints, review templates.
  - **Risk**: MEDIUM_RISK_GUIDED
  - **Required Checkpoint**: Review of generalized templates.
  - **Forbidden**: None.

- **Batch 6: Context Setup**
  - **Scope**: Add prompts/examples/reports skeleton/config.
  - **Expected Files**: `aos/prompts/`, `aos/AGENT_CONTEXT.md`.
  - **Risk**: MEDIUM_RISK_GUIDED
  - **Required Checkpoint**: Review AI-facing context.
  - **Forbidden**: Implementing RAG/Vector stores.

- **Batch 7: Root Public Surface**
  - **Scope**: Update root entrypoints and README public surface.
  - **Expected Files**: `aos/root/AGENTS.md`.
  - **Risk**: HIGH_RISK_PROTECTED
  - **Required Checkpoint**: Strict root file modification boundary review.
  - **Forbidden**: Modifying internal `AGENTS.md` before approval.

- **Batch 8: Verification**
  - **Scope**: Final path/link/install/uninstall verification.
  - **Expected Files**: Test dry-runs (no commits).
  - **Risk**: LOW_RISK_FAST
  - **Required Checkpoint**: Review of verification logs.
  - **Forbidden**: Commits or pushes.

- **Batch 9: Lifecycle Release**
  - **Scope**: Commit/push lifecycle.
  - **Expected Files**: None.
  - **Risk**: DESTRUCTIVE_OR_CANONICAL
  - **Required Checkpoint**: Explicit human commit/push authorization.
  - **Forbidden**: Pushing without authorization.

## 9. LLMs / Agent Context Recommendation
- **`llms.txt`**: Do not make `llms.txt` required at this stage. Consider root `llms.txt` later after the public layout stabilizes.
- **`aos/AGENT_CONTEXT.md`**: Add this to the consumer kit. It is essential for orienting the AI agent when operating inside the kit folder.
- **RAG/Vector Store**: Do not add RAG, vector store, DB, generated context pipeline, or `llms-full.txt` in this phase. The kit must remain static file-based.

## 10. Risk Assessment
- **Risk Level**: This layout architecture poses zero direct risk as it is read-only.
- The actual execution of the migration batches involves `HIGH_RISK_PROTECTED` and `DESTRUCTIVE_OR_CANONICAL` phases that require strict boundaries to prevent corrupting the internal AOS-FARM governance structure while creating the consumer kit.

## 11. Required Future Human Checkpoints
- Approval of this Architecture Layout Plan.
- Independent approval for each Batch (1-9) execution.
- Final commit and push authorizations for the implementation.

## 12. Blocking Issues
None. The repository is in a clean baseline state.

## 13. Warnings
None. All preflight expectations are met and Spec Kit artifacts are verified removed from active codebase.

## 14. Final Status
**AOS_FARM_370_AOS_CONSUMER_KIT_LAYOUT_PLAN_COMPLETE**
