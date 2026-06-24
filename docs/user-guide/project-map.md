# Project Map

AOS-FARM is structured around a strict governance model. Here is the layout of the repository:

## Core Directories and Files
- `README.md`: High-level entry point. Do not casually edit without approval.
- `docs/`: User guides, assembly documentation, and system maps.
- `templates/`: Blueprints for tasks, checklists, and pipelines.
- `reports/`: Execution evidence, verification reports, and authorization packages.
- `reports/human-checkpoints/`: DRAFT and APPROVED explicit human authorization files.

## Canonical Sources (Protected)
These files govern the entire repository and safety invariants. **Never edit these casually. They require explicit, separate authorization.**
- `00_AOS_Core_Control.md`: The highest priority governance foundation.
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Defines build steps and roadmaps.
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Defines safety rules, gates, and risk profiles.

## What Users Should Edit
- You should create new files in `reports/` and `reports/human-checkpoints/` as you execute tasks.
- You should use the files in `templates/` as starting points.
- You can edit specific files within `docs/` if explicitly authorized by a task brief.
