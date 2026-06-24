# AOS-FARM User Guide

Welcome to AOS-FARM (Agent Operating System Framework & Runtime Model).

## What is AOS-FARM?
AOS-FARM is a governance framework and GitHub template designed for safe, AI-assisted project building. It provides strict boundaries (rules, checkpoints, and documentation structures) to ensure that AI agents (like GPT, Codex, or Antigravity) act predictably and never execute unauthorized or destructive operations. 

## Who is it for?
This framework is built specifically for the **non-programmer, vibe-coder, or AI-assisted project builder**. It allows you to use powerful AI agents as your "Tutor" and "Executor" while you retain absolute authority as the "Approver."

## Where to Start: The First-User Journey (Safe Path)
If you are new here, follow this step-by-step safe path to build your project without breaking things:

1. **Understand the Workflow:** Read the [Bootstrap Agent Workflow](bootstrap-agent-workflow.md) to understand the separation of roles (You, the Tutor, and the Executor).
2. **Meet Your Tutor:** Learn how to use [Agent Tutor Mode](agent-tutor-mode.md) to ask questions and plan your work.
3. **Queue Tasks:** The Tutor will help you draft a task and place it in the **Manual Task Queue**.
4. **Dry-Run (Thin Helper):** Use the Thin Task Queue Helper to validate your task for missing approvals before any real coding starts.
5. **Handoff & Execute:** Pass the validated task to the Executor Agent. The agent writes the code and self-verifies.
6. **Authorize (Commit & Push):** Review the verification report and explicitly grant Commit and Push authorization through Human Checkpoints.

*Have a completely new idea right now? You can jump straight to the [New Project Start Template](../../templates/new-project-start-template.md).*

## Navigating the Project
- **Features**: `docs/features/` contains documentation explaining what each feature does.
- **Status**: `docs/project-status/` contains the registries that track what stages and features have been completed.
- **Templates**: `templates/` holds reusable Markdown forms for planning and executing work safely.

## What NOT to expect
- **AOS-FARM is NOT a RAG product.** It does not use vector databases or hidden automatic retrieval engines. Everything is based on reading visible Markdown files.
- **AOS-FARM is NOT an autonomous coding system.** The agent will stop and ask for your explicit approval at critical boundaries (like commits and pushes).
- **AOS-FARM DOES NOT replace Human approval.** If an action requires your approval, you must explicitly give it. The agent cannot simulate your permission.
