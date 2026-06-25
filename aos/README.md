# AOS Consumer Kit - Start Here

Welcome to AOS. To ensure safe and controlled AI development, you must follow the strict entry flow. 

**Do not write code or create a task brief yet.**

## Key Navigation
- [Start Here](START_HERE.md)
- [First Session Guide](docs/workflow/first-session-guide.md)
- [Problem Intake Workflow](docs/workflow/problem-intake-workflow.md)
- [Technical Assignment Workflow](docs/workflow/technical-assignment-workflow.md)
- [Consumer-to-Runtime Handoff](docs/workflow/consumer-runtime-handoff.md)

## The AOS Happy Path

Before your agent can write any code, you must define the problem and establish technical boundaries. Follow this exact sequence:

### Step 1: Problem Intake
Start by clearly defining what you are trying to build and the problems you are solving.
- **What to do:** Have your AI agent read the guide at `aos/docs/workflow/first-session-guide.md` and initialize using `aos/prompts/problem-intake.md`. 
- **What it does:** The agent will interview you one question at a time to uncover risks and requirements.
- **Output:** A structured `Problem Intake Summary`.

### Step 2: Technical Assignment
Convert the problem definition into strict technical boundaries.
- **What to do:** Give your agent the `Problem Intake Summary` and `aos/prompts/technical-assignment-builder.md`.
- **What it does:** The agent will bound the scope, define what NOT to do, and identify target files.
- **Output:** A `Technical Assignment` document.

### Step 3: Controlled Execution
Only after the Technical Assignment is ready can you begin execution.
- **What to do:** Create a task using `aos/templates/task-briefs/controlled-task-brief-template.md`. 

---

## Optional: Python Runner
For advanced or local guided execution, there is an optional Python runner located in `aos/tools/optional/problem-intake-runner/`.
- **Note:** This is purely optional. The markdown-only workflow described above works perfectly.
- **Note:** The runner does not have approval authority, and a successful run does not authorize implementation.

---

## AOS Core Rules & Boundaries
The following invariants govern all agent behavior in this repository:
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
