# AOS-FARM-375 Consumer Docs/Templates Migration Batch 1 Authorization Package

## Target Task
AOS-FARM.376 — Controlled Consumer Docs/Templates Migration Batch 1

## Migration Scope
This batch focuses strictly on migrating the core user-facing onboarding and governance documentation into `aos/`. 

**Rules:**
- Keep old files in place (no deletion or moving yet).
- Do not touch root `AGENTS.md`, `README.md`, `README.ru.md`.
- Do not commit or push.
- Ensure all target files are stripped of AOS-FARM repository internal development history, roadmap specifics, and internal dogfood contexts.

## Recommended Exact Target File List

| Target File | Source File(s) | Action | Required Consumer Content | Forbidden Internal Content |
|-------------|----------------|--------|---------------------------|----------------------------|
| `aos/docs/user-guide/quickstart.md` | `README.md` (partial logic), `docs/boundaries/...` | REWRITE | Fast start guide for a new consumer user | Mentions of AOS-FARM dev roadmap, build steps |
| `aos/docs/user-guide/first-run.md` | `templates/first-agent-session-template.md` | REWRITE | Instructions for first AI agent invocation | AOS-FARM specific git branching strategies |
| `aos/docs/user-guide/project-map.md` | N/A | NEW/REWRITE | Overview of `aos/` layout | References to `agentos/` or old `docs/` |
| `aos/docs/user-guide/glossary.md` | `agentos/docs/methodology/...` | REWRITE | Definitions of Task Brief, Evidence, etc. | Internal terminology not used by consumers |
| `aos/docs/governance/minimal-safety-floor.md` | `agentos/docs/minimal-safety-floor.md`, `02_AOS_...` (extracts) | REWRITE | The PASS ≠ approval rules, boundary rules | Internal gate matrices, CI/Runner rules |
| `aos/docs/governance/approval-boundary.md` | `templates/human-approval-boundary-template.md` | REWRITE | How human checkpoints work | Spec Kit references |
| `aos/docs/governance/human-checkpoint-boundary.md` | `templates/manual-code-review-checkpoint-template.md` | REWRITE | Structure of a human checkpoint | AOS-FARM historical checkpoints |
| `aos/docs/governance/unknown-not-run-pass.md` | `templates/unknown-not-run-pass-semantics-template.md` | REWRITE | Strict failure semantics | AOS-FARM internal CI specifics |
| `aos/docs/governance/risk-profiles.md` | `02_AOS_...` (extracts) | REWRITE | Definitions of Risk Profiles (e.g. LOW_RISK_FAST) | Internal AOS-FARM dogfood profiles |
| `aos/docs/workflow/controlled-task-workflow.md` | `agentos/docs/methodology/...` | REWRITE | The standard brief -> plan -> execution loop | Internal `build-step-X` references |
| `aos/docs/workflow/commit-push-workflow.md` | `docs/boundaries/commit-boundary.md` | REWRITE | Deferred commit strategies | AOS-FARM release tagging rules |
| `aos/docs/reference/common-mistakes.md` | N/A | NEW/REWRITE | Common failure modes (e.g. simulating approval) | Internal developer names/history |
| `aos/docs/reference/troubleshooting.md` | N/A | NEW/REWRITE | Fixing stuck states | Fixing the internal python scripts/runners |

## Proposed Risk Profile
**HIGH_RISK_PROTECTED**
*Reasoning: This involves creating the public canonical documentation for the product. While technically low risk to the current repo functioning, it defines the consumer safety boundary and thus requires high protection.*

## Status
- **Authorization**: PENDING
- **Blocking Issues**: None.
- **Warnings**: None.
- **Final Status**: **AOS_FARM_375_CONSUMER_DOCS_TEMPLATES_MIGRATION_AUTHORIZATION_PREPARED**
