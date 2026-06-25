# Installation, Clone, and First Run Guide

Welcome to AOS-FARM! If you are new here, this guide will help you safely get the project onto your local machine and run your first controlled task.

## What is AOS-FARM?
AOS-FARM (AgentOS - Future Architecture Reference Model) is a Markdown-first system for managing AI-assisted development. It is a strict governance framework designed to prevent autonomous AI agents from making unapproved changes, hiding work, or simulating human decisions.

## Who is this for?
This framework is for non-programmers, product owners, and developers who want to use powerful AI agents (like ChatGPT or IDE assistants) safely. It enforces explicit human approval boundaries and strict evidence-based verification before any code is committed.

## Step 1: Clone the Repository
AOS-FARM is distributed as a GitHub template or repository.

1. Open your terminal.
2. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AOS-FARM.git
   ```
3. Navigate into the project folder:
   ```bash
   cd AOS-FARM
   ```

## Step 2: Open it in your IDE
Open the `AOS-FARM` folder in your preferred code editor (e.g., VS Code, Cursor, or any IDE with an AI assistant).

## Step 3: What to Read First
Before you ask the AI to do anything, you must understand the rules. The AI will also be required to read these files.

**Canonical Control Sources (The Rules):**
- `00_AOS_Core_Control.md`: The absolute highest authority. Defines project control and safety invariants.
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: Defines the assembly pipelines and roadmap.
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: Defines risk profiles, control gates, and the Minimal Safety Floor.

**User Guides:**
- `README.md`: The top-level entry point.
- `docs/user-guide/quickstart.md`: High-level overview of getting started.
- `docs/user-guide/project-map.md`: Where things are located.
- `docs/user-guide/glossary.md`: Important terminology.

**Templates:**
- Look in the `templates/` folder for task briefs and project bootstrap checklists.

## Step 4: The First Safe Dry-Run (Controlled Task Path)
AOS-FARM does not allow you to just tell the AI to "build an app." You must follow the Assembly Pipeline.

1. **Create a Task Brief**: Copy `templates/first-controlled-task-brief-template.md` to a new file (e.g., `docs/task-briefs/my-first-task.md`).
2. **Define Boundaries**: Fill out the brief. Explicitly state the Goal, Allowed Changes, and Forbidden Changes.
3. **Assign Risk Profile**: You (the human) must explicitly assign a Risk Profile (e.g., `LOW_RISK_FAST` or `MEDIUM_RISK_GUIDED`). The AI cannot do this.
4. **Instruct the Agent**: Point your AI assistant to the Task Brief. The AI will read the canonical rules and execute the task strictly within the defined scope.
5. **Review Evidence**: The AI will produce an Evidence Report.
6. **Human Checkpoint**: You must review the evidence and explicitly grant approval in a Human Checkpoint document.

## Critical Concepts: Approval vs. Evidence
- **PASS ≠ Approval**: Just because a test passes does not mean the change is approved for commit.
- **Evidence ≠ Approval**: The AI generates evidence of its work, but it cannot approve its own work.
- **CI PASS ≠ Approval**: Automated checks do not replace your explicit permission.
- **Human Approval Cannot Be Simulated**: The AI is forbidden from forging your approval. You must manually change the status in a checkpoint file to `APPROVED_FOR_COMMIT`.

## What NOT to Run
AOS-FARM currently operates in a progressive, safe mode.
- **Do not enable autonomous runners** (no crons, no daemons).
- **Do not let the AI force push, merge to main, or create releases.**
- **Do not delete or rename the `00`, `01`, `02` canonical files.**

## What to do if you get stuck?
If the AI refuses to proceed and reports `UNKNOWN_BLOCKED` or `HUMAN_REVIEW_REQUIRED`:
1. This is normal! It means the AI encountered a boundary it is not allowed to cross.
2. Read the AI's explanation.
3. Provide explicit, scoped human authorization or clarification to unblock it. Do not tell the AI to "just ignore the rules."
