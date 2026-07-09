# AOS Consumer Kit - Start Here

Welcome to AOS. **This is the primary consumer entrypoint.** To ensure safe and controlled AI development, you must follow the strict entry flow.

**Product Folder Boundary:**
- The `AOS Product folder` is strictly `/aos/`.
- The file `/aos/root/AGENTS.md` is a **template** meant to be copied to the root of your target project as `AGENTS.md`. It is not the product folder itself.
- Internal reference directories like `agentos/` are strictly for internal/reference use and are not part of the consumer first-start path.

**Do not write code or create a task brief yet.**

## First-Contact Guidance (If you are not a programmer)
1. Describe your idea in normal language.
2. Do not ask the agent to write code immediately.
3. First ask for Task Intake, Project Brief, or the next safe step.
4. If the system says UNKNOWN or BLOCKED, this is a safety stop, not a system failure.
5. PASS means a check passed; it does not mean approval.
6. Evidence shows facts; it does not approve anything.
7. Human approval is required wherever an approval boundary exists.

## What AOS-FARM can and cannot do

**AOS-FARM can:**
1. Turn a raw idea into a structured task.
2. Identify missing information.
3. Propose a safe next step.
4. Collect Evidence.
5. Prepare a human review surface.

**AOS-FARM cannot:**
1. Approve its own work.
2. Simulate human approval.
3. Treat PASS as approval.
4. Treat Evidence as approval.
5. Assign LOW_RISK_FAST to itself.
6. Change protected/canonical files without a human checkpoint.
7. Commit, push, merge, release, or deploy without explicit authorization.
8. Treat UNKNOWN or NOT_RUN as OK.

## Plain-Language Status Glossary
- **PASS**: A check passed. This is not approval.
- **Evidence**: Facts and check results. This is not approval.
- **CI PASS**: CI checks passed. This is not approval.
- **HUMAN_REVIEW_REQUIRED**: A human must make a scoped decision.
- **UNKNOWN_BLOCKED**: The system does not know enough to continue safely.
- **NOT_RUN**: A check did not run. This is not PASS.
- **BLOCKED**: Work must stop until the blocker is resolved.
- **DRAFT**: Draft only. Not execution-ready.
- **READY_FOR_EXECUTION**: May be used only if required gates and human authorization are satisfied.
- **APPROVED**: Only explicit human approval. The agent cannot create it for itself.

## Future Compact Path Note
Some small tasks may later use a shortest safe path. This stage does not define or authorize that path. Any Compact Path contract belongs to a separate stage.

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
- **Important:** Missing architecture checkpoint must not be treated as OK.

### Step 5: Task Breakdown from Architecture
Decompose the Technical Assignment and architecture decisions into granular, traceable task candidates.
- **What to do:** Give your agent the completed `Technical Assignment` and `Architecture Brief` (including human checkpoint status) and follow [Task Breakdown from Architecture](docs/workflow/task-breakdown-from-architecture.md).
- **What it does:** The agent extracts task candidates and traces them back to the Technical Assignment and Architecture Decision.
- **Important:** Architecture checkpoint must be visible before Task Breakdown.

### Step 6: Task Brief Builder
Draft executable Task Briefs from the broken-down candidates.
- **What to do:** Give your agent the `Task Breakdown` and the prompt `aos/prompts/task-brief-builder.md`.
- **What it does:** The agent creates a manual task queue and drafts Task Briefs. It **does not write code**.
- **Important:** Task Brief Builder must not be presented as directly following TA without architecture checkpoint when architecture stage is applicable.
- **Important:** Task Brief creation remains separate from Build Step execution.
- **Output:** A `Task Queue` and Draft Task Briefs.

### Step 7: Human Task Review
Review the proposed tasks before authorizing any work.
- **What to do:** Manually review the `Task Queue` generated in Step 6.
- **What it does:** Ensures no tasks were invented by the agent and that everything aligns with the Technical Assignment. Task drafts require human review!

### Step 8: Controlled Execution
Only after a task is reviewed and selected from the queue can you begin execution.
- **What to do:** Create a task using `aos/templates/task-briefs/controlled-task-brief-template.md` for the selected task.
- **Reference:** See the [Consumer-to-Runtime Handoff](docs/workflow/consumer-runtime-handoff.md) for details on saving artifacts and workflow boundaries.
- **Next step guide:** See [First Controlled Execution](docs/workflow/first-controlled-execution.md) for the safe path from `Controlled Task Brief` to Human Execution Authorization, Controlled Execution Guard `precheck`, controlled execution, `scopecheck`, `postcheck`, and Evidence Review.
- **Post-execution learning:** After Evidence Review, see the [Evidence-to-Backlog Loop](docs/workflow/evidence-to-backlog-loop.md) to capture lessons learned, backlog candidates, and a Next Task Candidate for human review.
- **Important:** Build Step planning/execution only after separate authorization. Controlled execution still requires explicit human authorization. The brief alone is not approval.
- **Important:** Guard PASS is not approval. Guard PASS does not authorize commit or push. Human approval remains separate from PASS/Evidence.
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
