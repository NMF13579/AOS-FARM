# Problem Intake Workflow

The Problem Intake workflow is the crucial "Top-of-Funnel" step in the AOS Consumer Kit. It prevents building the wrong thing by strictly separating problem discovery from technical implementation.

## Purpose
- Turn a vague idea or pain point into a structured problem statement.
- Identify the user goal, current constraints, intended actors, success criteria, and risks.
- Adaptively probe the depth of the problem using modes (EXPRESS / FULL).

## How it works
1. **Initialize the Agent**: Use the `aos/prompts/problem-intake.md` prompt to start a session.
2. **Select Mode**: Choose between EXPRESS (fast scoping) or FULL (deep discovery).
3. **Interview Process**: The agent will ask you one question at a time. It uses frameworks like "Five Whys" or "JTBD" to adaptively follow up on short answers.
4. **Grey-Zone Discovery**: The agent will map contradictions, assumptions, and risks.
5. **Capture Output**: The outcome is a structured document based on `aos/templates/task-briefs/problem-intake-template.md`.

## Methodology Integration
This workflow relies on the deep rules established in `aos/docs/methodology/problem-intake-methodology.md`. 
No Python runners are used; the logic is entirely embedded in the interaction between the user and the prompt.

## Safety Semantics
- Problem Intake is an exploratory phase. Completing it does not authorize implementation.
- **PASS ≠ approval**. A complete Problem Intake document is just raw material for the next phase.
- Missing information must be explicitly marked as `UNKNOWN` rather than guessed. `UNKNOWN ≠ OK`.
