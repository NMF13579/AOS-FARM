# Template Repository Usage

AOS-FARM is distributed as a GitHub template repository. This means you click "Use this template" on GitHub to create your own fresh copy.

## How to use this template
When you generate a new repository from AOS-FARM, you get an empty shell containing only governance rules, templates, and basic documentation. It is a clean slate with a strict rulebook.

## What NOT to delete
Do not delete or modify the core canonical files located in the root of the project:
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

These files define the fundamental safety invariants. If you delete them, the AI agent will fail-closed and refuse to operate (yielding a `BLOCKED` or `UNKNOWN_BLOCKED` status).

## Why Canonical Docs Matter
The AI agent doesn't have a perfect memory. Every time it starts a new task or a new chat session, it reads `00`, `01`, and `02` to remind itself of the rules. These files are the **Source of Truth**.

## Why Reports and Human Checkpoints Exist
AOS-FARM uses a "compressed governance pattern". Instead of relying on external CI/CD tools or complex databases, everything is managed via Markdown files.
- **Reports** are the agent's proof of work (Evidence).
- **Human Checkpoints** are explicit lock-and-key files where the agent stops and waits for you to type `true`.

## Why the first stage should be planning
Do not jump straight into coding. AOS-FARM forces you to write `PROJECT_SPEC` and `REQUIREMENTS` first. This prevents the AI from writing thousands of lines of useless code and hallucinating features you don't need.

## Why cleanup is not a first step
You will notice old reports and checkpoints in the `reports/` directory from the original AOS-FARM template development. **Do not aggressively delete them.** They are evidence trails. If you want to clean them up, you must explicitly authorize a cleanup task.

## Why Protected Changes Require Human Checkpoints
If you ever want to change how AOS-FARM works (e.g., editing `00_AOS_Core_Control.md`), the agent requires explicit permission. It cannot rewrite its own rules autonomously.
