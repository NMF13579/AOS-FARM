# AOS-FARM Consumer Entry Flow Review

## 1. Task Metadata
- **Task ID:** AOS-FARM.409
- **Name:** Consumer Entry Flow Review
- **Mode:** Read-only product usability audit
- **Target Branch:** dev

## 2. Preflight Results
- **Branch:** dev
- **HEAD:** b295e5103ff62f051f378a9a317ff0dc411bb9aa (Matches origin/dev)
- **Status:** Clean (0 ahead, 0 behind, no staged changes)
- **Sources Check:** All required control sources and consumer entry candidates are present.

## 3. Required Sources Read Confirmation
Confirmed read and understood:
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## 4. Audited Files List
- `README.md`
- `README.ru.md`
- `AGENTS.md`
- `aos/START_HERE.md`
- `aos/README.md`
- `aos/docs/workflow/problem-intake-workflow.md`
- `aos/docs/workflow/technical-assignment-workflow.md`
- `aos/prompts/problem-intake.md`
- `aos/prompts/technical-assignment-builder.md`
- `aos/tools/optional/problem-intake-runner/README.md`

## 5. User Entry Path Assessment
The intended entry path (`README` → `START_HERE` → `Problem Intake` → `Technical Assignment` → `optional runner`) is broken. The root documents do not guide the user towards the Problem Intake workflow, instructing them instead to skip directly to a controlled task brief.

## 6. README Assessment
- **Finding:** The root `README.md` correctly explains what AOS is and directs consumers to the `aos/` directory.
- **Issue (BLOCKER):** The "Quick Start" section instructs the user to "Create your first task brief from `aos/templates/task-briefs/controlled-task-brief-template.md`". It completely omits the Problem Intake and Technical Assignment phases, establishing a dangerous "do not start here" path as the default.

## 7. START_HERE Assessment
- **Finding:** `aos/START_HERE.md` exists but lacks all workflow guidance.
- **Issue (BLOCKER):** It does not explain the step-by-step entry flow. It contains only a list of rules (Safety Invariants). It completely fails to instruct the user on Step 1 (Problem Intake), Step 2 (Technical Assignment), or the existence of the optional runner.

## 8. Problem Intake Path Assessment
- **Finding:** The Problem Intake path is well-documented in `aos/docs/workflow/problem-intake-workflow.md`. The prompt (`aos/prompts/problem-intake.md`) is highly detailed, adaptive, enforces the "One question at a time" rule, supports EXPRESS/FULL modes, and captures UNKNOWNs without simulating approval.
- **Issue (HIGH):** The path is invisible to new users because neither `README.md` nor `START_HERE.md` links to it.

## 9. Technical Assignment Path Assessment
- **Finding:** The `aos/docs/workflow/technical-assignment-workflow.md` explicitly shows the correct happy path: `Idea → Problem Intake → Technical Assignment → Controlled Task Brief`. The prompt correctly bounds scope, avoids implementation, and emphasizes readiness vs. approval.
- **Issue (HIGH):** Like Problem Intake, it is orphaned and unreachable from the main consumer entry points.

## 10. Optional Runner Discoverability Assessment
- **Finding:** The runner is positioned appropriately in `aos/tools/optional/problem-intake-runner/`.
- **Issue (MEDIUM):** It is not mentioned in any main entry flow documents, making it fully undiscoverable unless the user manually searches the directory tree. 

## 11. Optional Runner Safety Boundary Assessment
- **Finding:** The runner safety boundaries are excellently defined in `aos/tools/optional/problem-intake-runner/README.md`. It clearly states it has no approval authority, does not commit/push, and is entirely optional.

## 12. First-Session Simulation
A new user arrives with a vague idea and reads `README.md`. They are told to read `aos/START_HERE.md` and then immediately start coding using `controlled-task-brief-template.md`. The user completely misses the Problem Intake and Technical Assignment workflows. They do not know which prompt to copy, where to paste it, or what to do next. The happy path is broken.

## 13. Navigation Consistency Findings
- **Issue (MEDIUM):** `aos/README.md` and `aos/START_HERE.md` contain identical content. 
- **Issue (HIGH):** The distinction between "methodology" and "workflow" is clear in the docs, but the lack of an index or proper `START_HERE` makes the `aos/` directory confusing to navigate.

## 14. Language/Audience Findings
- **Finding:** The Problem Intake prompt supports multi-language fallback, which is excellent. The general tone is appropriate for vibe-coders and non-programmers. The optional runner is properly cordoned off as an advanced tool.

## 15. Safety Invariant Findings
- **Finding:** All checked entry docs successfully preserve the invariant rules (`PASS ≠ approval`, `UNKNOWN ≠ OK`, no simulated approval). The invariants are heavily reinforced across all levels.

## 16. Blockers
- **BLOCKER 1:** Root `README.md` instructs users to skip Problem Intake and Technical Assignment and jump directly to creating a Controlled Task Brief.
- **BLOCKER 2:** `aos/START_HERE.md` fails to provide the step-by-step entry sequence, leaving the user with no actionable way to begin the methodology.

## 17. Warnings
- **HIGH:** The happy path (`Idea → Problem Intake → Technical Assignment → Controlled Task Brief`) is only documented inside `technical-assignment-workflow.md`, which users are unlikely to find without a proper `START_HERE.md`.
- **MEDIUM:** Duplicate `aos/README.md` and `aos/START_HERE.md` files cause unnecessary confusion.

## 18. Recommended Fixes
1. **Rewrite `README.md` Quick Start:** Remove the instruction to jump directly to the controlled task brief. Point users to the Problem Intake workflow as the mandatory first step.
2. **Rewrite `aos/START_HERE.md`:** Transform it from a rules dump into a step-by-step guide:
   - Step 1: `aos/docs/workflow/problem-intake-workflow.md`
   - Step 2: `aos/docs/workflow/technical-assignment-workflow.md`
   - Step 3: Controlled Task Brief
   - Mention the optional runner for advanced users.
3. **Resolve Duplication:** Decide whether `aos/README.md` should redirect to `aos/START_HERE.md` or be removed/consolidated.

## 19. Recommended Next Task
- AOS-FARM.410 — Consumer Entry Flow Blocking Remediation Authorization Preparation

## 20. Final Status
AOS_FARM_409_CONSUMER_ENTRY_FLOW_REVIEW_NEEDS_REMEDIATION
