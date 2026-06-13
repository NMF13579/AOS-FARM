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

Use one of these options:

1. Ask the agent:

   Начнём проект

2. Or run:

   python3 agentos/agentos.py start

## Safety

- AgentOS does not auto-execute tasks.
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- Metrics are not approval.
- Human approval is required for protected changes.
- Runtime may be blocked if this is only a skeleton template.
