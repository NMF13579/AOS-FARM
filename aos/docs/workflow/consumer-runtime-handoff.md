# Consumer-to-Runtime Handoff Contract

## Purpose
This document defines the strict bridge between the consumer-facing Markdown workflow and the underlying runtime code layer. It clarifies artifact locations, expected handoff paths, and the exact boundaries of optional python tooling.

## Layer Boundaries
- **`aos/` Layer:** This is the consumer-facing kit. It is the primary, default starting path for all workflows.
- **`agentos/` Layer:** Contains implementation/runtime-side code slices. It is **not** the first-start path and should not be invoked directly by consumers during standard onboarding.

## Manual Markdown-First Happy Path
The expected flow for moving from an idea to execution is entirely Markdown-based:
1. Idea
2. Problem Intake prompt (`aos/prompts/problem-intake.md`)
3. Saved Problem Intake markdown artifact
4. Technical Assignment prompt (`aos/prompts/technical-assignment-builder.md`)
5. Saved Technical Assignment markdown artifact
6. Controlled task brief / execution package
7. Human review / approval checkpoint
8. Optional local document ingestion

## Default Artifact Locations & Naming Conventions
All artifacts generated during the handoff process should be saved using the following path and file naming conventions:
- **Problem Intake Output:** `aos/reports/problem-intake/<project-or-feature-name>.md`
- **Technical Assignment Output:** `aos/reports/technical-assignments/<project-or-feature-name>.md`
- **Task Briefs:** `aos/reports/task-briefs/<project-or-feature-name>.md`

## Problem Intake to Technical Assignment Handoff
When transitioning from Problem Intake to Technical Assignment, the user or agent must copy the contents of the saved Problem Intake artifact directly into the Technical Assignment builder prompt context.

**Required fields to preserve:**
Problem statement, target user, desired outcome, scope, non-goals, constraints, UNKNOWN items, risks, assumptions, success criteria, and pending human decisions.

## Technical Assignment to Controlled Task Boundary
The Technical Assignment artifact serves as the direct input for creating a controlled task brief. 
- It establishes the technical boundaries.
- **Critical:** Technical Assignment output is **readiness/planning evidence**, not an approval to execute.

## Optional Role of Document Pipeline
`agentos/pipelines/document_pipeline.py` is an **optional local document ingestion helper**.
- It is **not** approval authority.
- It is **not** lifecycle authority.
- Document ingestion success is **not** approval.
- `ready_for_local_index` does **not** mean ready for execution.

## Optional Runner Boundary
The problem intake runner located at `aos/tools/optional/problem-intake-runner/` is purely optional.
- The runner does **not** approve anything.
- It does **not** commit, push, or authorize lifecycle events.

## Safety Invariants
- **PASS / Evidence / runner output / parser output are not approval.**
- `UNKNOWN` items must remain explicit and never be guessed.
- Scope must not expand without explicit human permission.
- Human approval cannot be simulated.

## Non-Goals
This handoff contract does **not** aim to activate runtime behavior, replace CI/CD pipelines, or mandate the usage of any specific local Python environments. It exists solely to structure the Markdown-driven workflow.
