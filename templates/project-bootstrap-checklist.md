# Project Bootstrap Checklist

Use this checklist to initialize your new project safely.

## Project Details
- **Project Name**: [Project Name]
- **Repository URL**: [URL]
- **Project Idea**: [Brief description]
- **Problem Statement**: [What problem does this solve?]
- **Target User**: [Who is the end user?]

## Boundaries
- **MVP Boundary**: [What is strictly included in the first version?]
- **Explicit Non-Goals**: [What are we definitely NOT building right now?]
- **Forbidden Scope**: [e.g., No external databases, no automated deployment scripts]

## Roles & Setup
- **Preferred IDE / Agent Setup**: [e.g., VS Code + Antigravity]
- **Agent Tutor Role**: [e.g., ChatGPT-4o]
- **Executor Agent Role**: [e.g., Antigravity]
- **Human Approval Owner**: [Your Name]

## State & Constraints
- **Initial Branch Strategy**: `dev` as main integration branch, features built on `build/*` branches.
- **Known UNKNOWNs**: [What is currently unclear?]
- **Known Constraints**: [e.g., Must use purely Markdown docs]

## First Safe Next Step
- **Next Action**: Prepare a Problem Intake MVP and wait for execution authorization.

## Default Safety Fields
Ensure these remain false until explicitly authorized for a specific task:
- `execution_authorized_now`: false
- `commit_authorized_now`: false
- `push_authorized_now`: false
- `production_use_authorized_now`: false
