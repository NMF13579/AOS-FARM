# AOS-FARM-379 Batch 2 Authorization Package: Templates/Prompts/Examples/Config

## Target Task
AOS-FARM.380 — Controlled Consumer Templates Prompts Examples Config Migration Batch 2

## Migration Scope
This batch focuses on creating generic, consumer-safe templates, AI prompts, examples, and config logic within the `aos/` kit.

**Rules:**
- Keep old files in place (no deletion or moving).
- Do not touch root `AGENTS.md`, `README.md`, `README.ru.md`.
- Do not commit or push.
- Ensure all target files are stripped of AOS-FARM internal development history, build step assumptions, and dogfood context.

## Recommended Exact Target File List

| Target File | Decision | Required Consumer Content | Forbidden Internal Content |
|-------------|----------|---------------------------|----------------------------|
| `aos/templates/task-briefs/controlled-task-brief-template.md` | REWRITE | Standard fields for a generic dev task | "Build Step" fields, AOS-FARM roadmap links |
| `aos/templates/task-briefs/read-only-audit-task-template.md` | NEW | Explicit read-only task constraints | Modifying/committing instructions |
| `aos/templates/checkpoints/human-execution-authorization-template.md` | REWRITE | Checkpoint structure, Risk Profile checkboxes | Old dogfood fixture names |
| `aos/templates/checkpoints/human-commit-authorization-template.md` | NEW | Specific checkboxes for commit verification | AOS-FARM specific release tags |
| `aos/templates/checkpoints/human-push-authorization-template.md` | NEW | Specific checkboxes for push/merge verification | - |
| `aos/templates/reports/execution-report-template.md` | REWRITE | standard report fields (created paths, verification checkboxes) | - |
| `aos/templates/reports/verification-report-template.md` | REWRITE | fields to verify the execution vs plan | - |
| `aos/templates/reports/final-stage-report-template.md` | NEW | for grouping multiple tasks before a commit | - |
| `aos/templates/verification/post-execution-verification-template.md` | REWRITE | detailed boundary checks | - |
| `aos/templates/authorization/execution-authorization-package-template.md` | REWRITE | plan proposal format | - |
| `aos/templates/authorization/commit-authorization-package-template.md` | NEW | grouping of tasks for commit | - |
| `aos/templates/authorization/push-authorization-package-template.md` | NEW | grouping of commits for push | - |
| `aos/templates/handoff/session-handoff-template.md` | REWRITE | fields to pass context to the next AI session | Spec Kit context arrays |
| `aos/prompts/tutor-start.md` | NEW | "Act as AOS Tutor" prompt instructions | - |
| `aos/prompts/first-task.md` | NEW | Safe prompt to test agent compliance | - |
| `aos/prompts/review-before-commit.md` | NEW | Prompt to ask agent to generate a commit authorization | - |
| `aos/prompts/review-before-push.md` | NEW | Prompt to verify safe push | - |
| `aos/prompts/handoff.md` | NEW | Prompt to instruct agent to write handoff | - |
| `aos/examples/first-controlled-task/README.md` | NEW | Step-by-step example of a successful workflow | - |
| `aos/examples/first-dry-run/README.md` | NEW | Step-by-step example of a dry run | - |
| `aos/config/aos-project-profile.md` | NEW | Generic definition of the consumer's project | AOS-FARM's profile |
| `aos/config/aos-local-policy.md` | NEW | How the consumer project adapts the safety floor | - |
| `aos/config/risk-profile-policy.md` | NEW | Project-specific risk profile definitions | - |
| `aos/config/lifecycle-policy.md` | NEW | How the project handles staging and commits | - |
| `aos/config/protected-files-policy.md` | NEW | List of files that trigger high risk | - |
| `aos/config/cleanup-policy.md` | NEW | Rules for deleting old reports | - |
| `aos/tools/README.md` | NEW | Disclaimer that AOS relies on AI adherence, not runners | Python runner code |
| `aos/tools/dry-run-only/README.md` | NEW | Explanation of dry-run mode | Active execution scripts |

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**
*Reasoning: These files constitute the canonical methodology templates and prompts the consumer will use. They define the structural safety of the public kit.*

## Status
- **Authorization**: PENDING
- **Blocking Issues**: None.
- **Warnings**: None.
- **Final Status**: **AOS_FARM_379_CONSUMER_TEMPLATES_PROMPTS_EXAMPLES_CONFIG_MIGRATION_AUTHORIZATION_PREPARED**
