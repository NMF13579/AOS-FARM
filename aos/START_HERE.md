# AOS Consumer Kit - Start Here

Welcome to AOS. **This is the primary consumer entrypoint.** To ensure safe and controlled AI development, you must follow the strict entry flow.

**Product Folder Boundary:**
- The `AOS Product folder` is strictly `/aos/`.
- The file `/aos/root/AGENTS.md` is a **template** meant to be copied to the root of your target project as `AGENTS.md`. It is not the product folder itself.
- Internal reference directories like `agentos/` are strictly for internal/reference use and are not part of the consumer first-start path.

**Do not write code or create a task brief yet.**

## The AOS Happy Path

Before your agent can write any code, you must define the problem and establish technical boundaries. Follow this exact sequence:

### Step 0: Task Intake Wizard
Classify raw ideas before starting formal intake.
- **What to do:** Evaluate the idea using `aos/templates/intake/task-intake-classification-template.md`.
- **What it does:** Classifies the idea into explicit statuses (e.g., `NEEDS_PROBLEM_INTERVIEW`, `READY_FOR_TASK_CANDIDATE`). It enforces a strict medical-domain fast-exit (`HUMAN_REVIEW_REQUIRED`) if the request touches clinical or patient data.

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

### Step 3: Architecture Need Check / Architecture Input Intake
Before breaking the Technical Assignment into tasks, check whether architecture input is required.
- **When is it required?** Architecture input is required if the task affects system structure, stack, integration boundary, runtime behavior, validator behavior, lifecycle behavior, safety/control semantics, or product folder structure.
- **If required:** Run Architecture Input Intake using [Architecture Input Intake](docs/workflow/architecture-input-intake.md) and [Architecture Decision Layer](docs/workflow/architecture-decision-layer.md), and prepare Architecture Brief / Evidence for human review.
- **If not required:** Record that no architecture intake was required and continue directly to Task Brief Builder.

### Step 4: Human Architecture Checkpoint, if architecture input is required
Review the architecture evidence before allowing decisions to cascade.
- **What to do:** Use the [Human Architecture Checkpoint Template](docs/architecture/review/human-architecture-checkpoint-template.md) to record the decision.
- **Important:** Human Architecture Checkpoint is required before architecture decisions can affect task breakdown, stack selection, pattern promotion, or implementation planning.

### Step 5: Task Brief Builder / Task Breakdown
Decompose the Technical Assignment into granular, traceable tasks.
- **What to do:** Give your agent the completed `Technical Assignment` (and `Architecture Brief` if applicable) and the prompt `aos/prompts/task-brief-builder.md`.
- **What it does:** The agent extracts task drafts, traces them back to the Technical Assignment, proposes priorities, and creates a manual task queue. It **does not write code**.
- **Output:** A `Task Breakdown` and a `Task Queue`.

### Step 6: Human Task Review
Review the proposed tasks before authorizing any work.
- **What to do:** Manually review the `Task Queue` generated in Step 5.
- **What it does:** Ensures no tasks were invented by the agent and that everything aligns with the Technical Assignment. Task drafts require human review!

### Step 7: Controlled Execution
Only after a task is reviewed and selected from the queue can you begin execution.
- **What to do:** Create a task using `aos/templates/task-briefs/controlled-task-brief-template.md` for the selected task.
- **Reference:** See the [Consumer-to-Runtime Handoff](docs/workflow/consumer-runtime-handoff.md) for details on saving artifacts and workflow boundaries.
- **Next step guide:** See [First Controlled Execution](docs/workflow/first-controlled-execution.md) for the safe path from `Controlled Task Brief` to Human Execution Authorization, Controlled Execution Guard `precheck`, controlled execution, `scopecheck`, `postcheck`, and Evidence Review.
- **Post-execution learning:** After Evidence Review, see the [Evidence-to-Backlog Loop](docs/workflow/evidence-to-backlog-loop.md) to capture lessons learned, backlog candidates, and a Next Task Candidate for human review.
- **Important:** Controlled execution still requires explicit human authorization. The brief alone is not approval.
- **Important:** Guard PASS is not approval. Guard PASS does not authorize commit or push.
- **Important:** Lessons Learned, Pipeline Hardening Backlog Items, and Next Task Candidates do not authorize execution.

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
- Architecture Brief ≠ approval.
- Architecture Evidence ≠ approval.
- ADR PROPOSED ≠ approval.
- Architecture validator PASS ≠ approval.
- Human Architecture Checkpoint is required before promotion or implementation planning.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit, push, merge, release, and destructive operations require explicit human authorization.
- Exclusions: No runner, CI, DB/RAG/vector, Spec Kit, release artifacts, production use, or autonomous execution are included by default. Historical AOS-FARM reports and internal development sources are strictly excluded.
- Installer safe `--apply` is limited to creation and `.gitignore` append; manual transfer remains supported; dry-run is default.
- Existing `AGENTS.md`, `llms.txt`, `README.md`, and workflows are never modified automatically.
- Tutor output is explanation only and is not approval.
- Apply DONE is not approval.
- READY_FOR_FIRST_START is not execution authorization.
