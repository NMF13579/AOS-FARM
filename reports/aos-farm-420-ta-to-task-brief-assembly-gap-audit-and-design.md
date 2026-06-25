# AOS-FARM.420 — Technical Assignment to Task Brief Assembly Gap Audit & Design Plan

## 1. Task Metadata and Preflight
- **final_status:** AOS_FARM_420_TA_TO_TASK_BRIEF_ASSEMBLY_AUDIT_PASS
- **branch:** dev
- **HEAD:** 55c070224f67a09a52a796d3dc25f0080a4bd510
- **origin/dev:** 55c070224f67a09a52a796d3dc25f0080a4bd510
- **ahead/behind:** 0 0
- **required sources exist:** Yes (`00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`)
- **files inspected:** `00`, `01`, `02` (via preflight), `README.md`, `aos/START_HERE.md`, `aos/docs/workflow/first-session-guide.md`, `aos/prompts/technical-assignment-builder.md`, `aos/templates/task-briefs/technical-assignment-template.md`, `aos/templates/task-briefs/controlled-task-brief-template.md`, `aos/AGENT_CONTEXT.md`, `aos/INSTALL.md`, `aos/ADOPTION.md`.
- **execution authorized:** false
- **files modified:** false
- **commit/push performed:** false
- **BLOCKED items:** None
- **warnings:** This is a design plan only. Implementation is strictly unauthorized in this stage.

## 2. Current Workflow Summary
Currently, the consumer workflow dictates moving from Idea → Problem Intake → Technical Assignment → Controlled Task Brief. However, there is a missing operational layer for translating a broad Technical Assignment into manageable, tracked, and prioritized individual task briefs.

### Present Components
- Problem Intake Prompt & Template
- Technical Assignment Builder Prompt & Template
- A basic, very thin `controlled-task-brief-template.md` (16 lines).
- Governance rules and general workflow guides (`first-session-guide.md`).

### Missing Components
- A workflow document covering the transition from Technical Assignment to Task Briefs.
- A prompt specifically for Task Brief generation/breakdown.
- Templates for task breakdown and task queues.
- Traceability matrices, dependency maps, priority guidelines, and batch planning rules.
- Stale-task detection mechanisms.

### Thin/Insufficient Components
- `aos/templates/task-briefs/controlled-task-brief-template.md`: Too brief to enforce safety semantics, validations, and evidence requirements.
- `aos/START_HERE.md` and `aos/docs/workflow/first-session-guide.md`: Lack the specific handoff steps for the Task Assembly layer.

## 3. Required Audit Questions
1. **Does the project currently have a dedicated Technical Assignment → Task Brief Assembly workflow?** No.
2. **Does the project currently have a prompt for converting Technical Assignment into task drafts?** No.
3. **Does the project currently have a task breakdown template?** No.
4. **Does the project currently have a task queue template?** No.
5. **Does the project currently have task-to-Technical-Assignment traceability?** No.
6. **Does the project currently have dependency mapping for tasks?** No.
7. **Does the project currently have task priority rules?** No.
8. **Does the project currently have batch planning rules?** No.
9. **Does the project currently have stale-task detection if Technical Assignment changes?** No.
10. **Does the project currently separate task draft, task candidate, approved task, and execution authorization?** No.
11. **Does the project currently require human review before task execution?** Yes, governed by general rules, but lacks a formal structural queue mechanism for it.
12. **Does the project currently preserve Risk Profile proposal vs human-assigned Risk Profile?** No, not explicitly within the task generation layer.
13. **Does the current controlled task brief template contain enough fields for safe execution?** No, it is insufficient.
14. **Does START_HERE make the user path clear enough for a non-programmer?** Yes for the initial entry, but it skips over how exactly to assemble executable tasks.
15. **Does the current flow accidentally imply that Technical Assignment readiness is enough to start implementation?** Yes, due to the missing breakdown layer.

## 4. Risk Analysis
The absence of a structured assembly layer creates a high risk of scope drift, missing dependencies, and premature execution. Without an explicit task queue and human review layer separating drafts from authorization, an agent might attempt to implement an entire Technical Assignment monolithically, bypassing granular safety checks and Risk Profile assessments.

## 5. Proposed Implementation File Plan

### Expected New Files
- `aos/docs/workflow/technical-assignment-to-task-brief.md`: **required**
- `aos/prompts/task-brief-builder.md`: **required**
- `aos/templates/task-briefs/task-breakdown-template.md`: **required**
- `aos/templates/task-queue-template.md`: **required**

### Expected Modified Files
- `aos/START_HERE.md`: **needs strengthening**
- `aos/docs/workflow/first-session-guide.md`: **needs strengthening**
- `aos/templates/task-briefs/controlled-task-brief-template.md`: **needs strengthening**

### Optional Files
- `aos/AGENT_CONTEXT.md`: **already sufficient / not needed**
- `aos/ADOPTION.md`: **already sufficient / not needed**

## 6. Proposed Lifecycle States
To explicitly separate drafting from authorization, the task queue must support the following states:
1. `DRAFT`
2. `READY_FOR_REVIEW`
3. `NEEDS_REVISION`
4. `REJECTED`
5. `BLOCKED`
6. `READY_FOR_EXECUTION_AUTHORIZATION`
7. `APPROVED_FOR_EXECUTION`
8. `EXECUTED`
9. `VERIFIED`

**Crucial Clarifications:**
- `READY_FOR_EXECUTION_AUTHORIZATION` ≠ `APPROVED_FOR_EXECUTION`
- Task queue inclusion ≠ approval
- Priority ≠ approval
- Validation plan ≠ validation PASS
- Evidence requirements ≠ collected Evidence
- Risk Profile proposal ≠ human-assigned Risk Profile

## 7. Proposed Validation & Evidence Requirements
- **Validation Expectations per Task:** Every task brief must include a strict validation plan outlining exact commands or checks to run *before* declaring success. 
- **Evidence Expectations per Task:** Every task must output specific evidence artifacts (e.g., test outputs, diffs, log snippets) that a human can review to confirm the validation plan passed.

## 8. Exact Next Recommended Task
**AOS-FARM.421 — Technical Assignment to Task Brief Assembly Layer Implementation**
