# AOS Consumer Kit - Start Here

Welcome to AOS. To ensure safe and controlled AI development, you must follow the strict entry flow. 

**Do not write code or create a task brief yet.**

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

### Step 3: Task Brief Builder / Task Breakdown
Decompose the Technical Assignment into granular, traceable tasks.
- **What to do:** Give your agent the completed `Technical Assignment` and the prompt `aos/prompts/task-brief-builder.md`.
- **What it does:** The agent extracts task drafts, traces them back to the Technical Assignment, proposes priorities, and creates a manual task queue. It **does not write code**.
- **Output:** A `Task Breakdown` and a `Task Queue`.

### Step 4: Human Task Review
Review the proposed tasks before authorizing any work.
- **What to do:** Manually review the `Task Queue` generated in Step 3.
- **What it does:** Ensures no tasks were invented by the agent and that everything aligns with the Technical Assignment. Task drafts require human review!

### Step 5: Controlled Execution
Only after a task is reviewed and selected from the queue can you begin execution.
- **What to do:** Create a task using `aos/templates/task-briefs/controlled-task-brief-template.md` for the selected task. 
- **Reference:** See the [Consumer-to-Runtime Handoff](docs/workflow/consumer-runtime-handoff.md) for details on saving artifacts and workflow boundaries.
- **Next step guide:** See [First Controlled Execution](docs/workflow/first-controlled-execution.md) for the safe path from `Controlled Task Brief` to Human Execution Authorization, Controlled Execution, and Evidence Review.
- **Important:** Controlled execution still requires explicit human authorization. The brief alone is not approval.

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
