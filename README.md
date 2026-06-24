# AgentOS Project Template

This repository contains a clean AgentOS project template.

## Canonical Sources

- AOS-1 canonical control starts from `00_AOS_Core_Control.md`.
- Roadmap and Assembly Pipeline authority are in `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`.
- Governance and safety authority are in `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md` is optional reference only.
- Old Stage documents are not demoted by this task.
- This task does not approve, merge, release, or start Build Step 1.

## Start / Quickstart

The first-user path for this template is:
`README` → `Quickstart` → `First Task`

**Start here**: [Quickstart](docs/user-guide/quickstart.md)

Essential references:
- [Project Map](docs/user-guide/project-map.md)
- [Glossary](docs/user-guide/glossary.md)
- [First Consumer Workflow](docs/user-guide/first-consumer-workflow.md)

### Safety Notice
- Quickstart is an entrypoint, not approval.
- PASS, Evidence, and CI PASS are not approval.
- Commit, push, release, and production use require explicit Human Authorization.
- Canonical sources 00/01/02 remain authoritative (if README or Quickstart conflicts with 00/01/02, canonical sources win).
- Runner/autonomous execution is not part of the current safe path.

## Repository Structure

| Файл / Папка | Роль |
|---|---|
| 00_AOS_Core_Control.md | Canonical: core control |
| 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md | Canonical: pipeline и roadmap |
| 02_AOS_Governance_Control_Module_and_Safety_Rules.md | Canonical: governance и safety |
| 03_AOS_Future_and_Legacy_Reference_OPTIONAL.md | Опциональный референс, не читать при первом запуске агента |
| llms.txt | Машиночитаемый контекст для LLM-агентов |
| docs/ | Нормализованные черновые заметки |
| archive/ | Оригинальные .txt файлы (read-only) |

## Safety

- AgentOS does not auto-execute tasks.
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- Metrics are not approval.
- Human approval is required for protected changes.
- Release and production use require explicit Human approval.
- Runtime may be blocked if this is only a skeleton template.
