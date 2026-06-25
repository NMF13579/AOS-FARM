# AOS-FARM-410 Execution Authorization Package: Consumer Entry Flow Remediation

## Proposed Plan
The goal of this remediation is to fix the consumer entry flow blockers identified in AOS-FARM.409. The remediation will establish a clear, linear "happy path" for new users: `README` → `START_HERE` → `Problem Intake` → `Technical Assignment` → `optional runner`.

Specific actions planned for execution (once authorized):
1. **Modify `README.md` and `README.ru.md`**:
   - Remove the misleading instruction to skip directly to a controlled task brief.
   - Point the user explicitly to `aos/START_HERE.md` as the single mandatory starting point.
2. **Modify `aos/START_HERE.md`**:
   - Rewrite it from a flat list of rules into a clear, step-by-step onboarding document.
   - Maintain the core invariants but add explicit routing for Step 1 (Problem Intake) and Step 2 (Technical Assignment).
   - Point the user to the detailed first-session guide.
3. **Create `aos/docs/workflow/first-session-guide.md`**:
   - Provide a 5–10 minute concise onboarding guide explaining:
     - What prompt to copy first (`aos/prompts/problem-intake.md`).
     - What the agent will do (interview the user one question at a time).
     - How to manually capture the output into `problem-intake-template.md`.
     - How to feed that output into `technical-assignment-builder.md`.
     - That the Python runner is completely optional.
     - That PASS / Evidence / outputs are not approval for implementation.
4. **Modify `aos/README.md`**: 
   - Ensure the duplicate `aos/README.md` redirects to or mirrors the new `START_HERE.md` to prevent navigation confusion.

## Exact Target List
- [MODIFY] `README.md`
- [MODIFY] `README.ru.md`
- [MODIFY] `aos/START_HERE.md`
- [MODIFY] `aos/README.md`
- [NEW] `aos/docs/workflow/first-session-guide.md`

## Proposed Risk Profile
- **LOW_RISK_FAST**
- **Rationale:** This is a documentation-only change to consumer-facing entry guides. It does not modify code, internal methodologies, prompts, templates, safety invariants, CI, or execution environments. 

## Forbidden Operations
During the execution phase of this task, the agent MUST NOT:
- Edit prompts (`aos/prompts/`).
- Edit templates (`aos/templates/`).
- Edit core methodology docs.
- Change safety invariants.
- Commit, push, or release automatically.
- Modify `00_AOS_Core_Control.md`, `01`, or `02` control documents.

## Lifecycle Status
- Execution is strictly read-only and planning-only until human approval is provided.
- Commit and push remain deferred pending human review of the execution output.

## Final Next Task
Upon approval of the Human Checkpoint, the next task will be:
**AOS-FARM.411 — Consumer Entry Flow Blocking Remediation Execution**
