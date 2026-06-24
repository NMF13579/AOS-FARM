# AgentOS Project Template

This repository contains a clean AgentOS project template.

## Canonical Sources

- AOS-1 canonical control starts from `00_AOS_Core_Control.md`.
- Roadmap and Assembly Pipeline authority are in `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`.
- Governance and safety authority are in `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- `03_AOS_Future_and_Legacy_Reference_OPTIONAL.md` is optional reference only.
- Old Stage documents are not demoted by this task.
- This task does not approve, merge, release, or start Build Step 1.

## Start

The first-user path for this template is:
`README` → `User Guide` → `Bootstrap` → `Agent Tutor` → `First Task` → `Manual Task Queue` → `Handoff` → `Verification`

To get started, follow these steps:
1. Read the [User Guide](docs/user-guide/README.md).
2. Complete the [Bootstrap Agent Workflow](docs/user-guide/bootstrap-agent-workflow.md).
3. Engage the [Agent Tutor Mode](docs/user-guide/agent-tutor-mode.md) to formulate your first task brief.

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
