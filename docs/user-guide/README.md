# AOS-FARM User Guide

Welcome to AOS-FARM (Agent Operating System Framework & Runtime Model).

## What is AOS-FARM?
AOS-FARM is a governance framework and GitHub template designed for safe, AI-assisted project building. It provides strict boundaries (rules, checkpoints, and documentation structures) to ensure that AI agents (like GPT, Codex, or Antigravity) act predictably and never execute unauthorized or destructive operations. 

## Who is it for?
This framework is built for the **non-programmer, vibe-coder, or AI-assisted project builder**. It allows you to use a powerful AI agent as your "Controller" and "Executor" while you retain absolute authority as the "Approver."

## Where to start
- Have a new idea? Use the [New Project Start Template](../../templates/new-project-start-template.md).
- Need to know how to build a feature? Read the [Non-Programmer Workflow](non-programmer-workflow.md).
- Confused about approvals? Read the [Commit & Push Approval Workflow](commit-push-approval-workflow.md).

## Navigating the Project
- **Features**: `docs/features/` contains documentation explaining what each feature does.
- **Status**: `docs/project-status/` contains the registries that track what stages and features have been completed.
- **Templates**: `templates/` holds reusable Markdown forms for planning and executing work safely.

## Agent Tutor Mode
If you ever get lost, you can ask your AI agent to act as an "Agent Tutor."
- **How to ask**: Open a new chat session and paste the [Agent Tutor Session Template](../../templates/agent-tutor-session-template.md).
- The Tutor will explain the project status, route your questions to the correct documentation, and help you prepare safe prompts for building.
- Read more about [Agent Tutor Mode](agent-tutor-mode.md).

## What NOT to expect
- **AOS-FARM is NOT a RAG product.** It does not use vector databases or hidden automatic retrieval engines. Everything is based on reading visible Markdown files.
- **AOS-FARM is NOT an autonomous coding system.** The agent will stop and ask for your explicit approval at critical boundaries (like commits and pushes).
- **AOS-FARM DOES NOT replace Human approval.** If an action requires your approval, you must explicitly give it. The agent cannot simulate your permission.
