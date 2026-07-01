# AOS-FARM.502 User Workflow Stage Gap Audit

```yaml
report_id: AOS-FARM.502
cycle: AOS-FARM-CYCLE-0001
report_type: planning_cycle_gap_audit
status: READY_FOR_HUMAN_REVIEW
approval_granted: false
execution_authorized: false
source_of_truth: report_only
```

## Baseline Repo State

- Repository: `NMF13579/AOS-FARM`
- Branch: `dev`
- HEAD: `80a20aa2589c1cde7a0324bfa2306b5e09436184`
- Local `origin/dev`: `80a20aa2589c1cde7a0324bfa2306b5e09436184`
- Required sources present: `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `git diff --stat` before report creation: no tracked modifications reported.
- Worktree note: `git status -sb` contains many pre-existing untracked copied files, including forbidden-area paths such as `aos/** 2.*`, `tasks/** 2.*`, and report copies. They were not touched by this planning cycle.

## Current Git Status -sb

```text
## dev...origin/dev
?? many pre-existing untracked copied files
```

The full status is intentionally summarized here because the pre-existing list is very large. Final validation records the current `git status -sb`.

## Source Precedence Used

1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

Domain-specific safety/control semantics from `02` are preserved where they govern approval, lifecycle, protected/canonical files, destructive operations, UNKNOWN, NOT_RUN, PASS/Evidence/approval, and Risk Profile semantics.

## Audit Scope

The audit covers six user workflow stages:

1. Onboarding AOS into a user project.
2. Project intake / read-only project understanding.
3. Problem interview.
4. Problem Brief / TZ to Implementation Plan to DRAFT task candidates.
5. Task review / queue / acceptance boundary.
6. Agent execution / validation / Evidence / human review boundary.

## Six-Stage Workflow Audit

| Stage | Current support | Manual readiness | Code readiness | Third Pass direction |
|---|---|---|---|---|
| 1. Onboarding AOS into a user project | `README.md`, `aos/START_HERE.md`, `aos/INSTALL.md`, `aos/ADOPTION.md`, `aos/AGENT_CONTEXT.md`, root `AGENTS.md` template | MANUAL_READY | PARTIAL | Improve first-run checklist and adoption verification without changing approval semantics. |
| 2. Project intake / read-only project understanding | `aos/docs/workflow/problem-intake-workflow.md`, `aos/prompts/problem-intake.md`, methodology runbooks | PARTIAL | PARTIAL | Add read-only repository discovery package and intake-output trace fields. |
| 3. Problem interview | `aos/prompts/problem-intake.md`, `aos/docs/methodology/problem-intake-methodology.md`, runbooks | MANUAL_READY | PARTIAL | Add structured interview-to-brief traceability report/template. |
| 4. Problem Brief / TZ to plan to DRAFT task candidates | `aos/prompts/technical-assignment-builder.md`, `aos/prompts/task-brief-builder.md`, task breakdown and queue templates | PARTIAL | PARTIAL | Highest-priority gap: deterministic planning-cycle package, traceability matrix, and candidate validator. |
| 5. Task review / queue / acceptance boundary | `aos/prompts/task-brief-builder.md`, `aos/templates/tasks/task-queue-template.md`, task quality acceptance docs, existing task examples | PARTIAL | PARTIAL | Clarify queue acceptance and candidate promotion boundary. |
| 6. Agent execution / validation / Evidence / human review boundary | `aos/docs/workflow/controlled-task-workflow.md`, `aos/prompts/controlled-execution.md`, controlled guard docs, Evidence-to-Backlog loop | MANUAL_READY | PARTIAL | Improve guard package UX and result review traceability; runtime enforcement remains later. |

## Gaps

- Planning cycle artifacts are not yet packaged as one repeatable flow from audit to DRAFT task candidates.
- External best-practices research can be prompted, but external output is not currently integrated into a guarded report-only package.
- DRAFT candidate traceability exists as a prompt rule, but there is no dedicated planning-cycle traceability validation report.
- Candidate promotion boundary needs a visible human checkpoint: `DRAFT_CANDIDATE -> real task file -> READY_FOR_EXECUTION`.
- Code helpers exist for later controlled task documents, but not for this planning-cycle candidate package.
- Large pre-existing untracked copies can obscure audit status; this planning cycle must remain path-scoped.

## Blockers

- No blocker prevents creating the report-only planning-cycle package.
- Any future mutation of `/aos/`, `aos/scripts/`, `aos/templates/`, `aos/schemas/`, `.github/workflows/`, `tasks/`, or canonical root sources requires a separate human checkpoint.
- Human Risk Profile assignment is unavailable in this planning cycle; candidates therefore remain proposals only.

## UNKNOWN / NOT_RUN Items

- `PERPLEXITY_OUTPUT_NOT_PROVIDED`: external research output was not provided.
- `NOT_RUN_EXTERNAL_REFERENCE`: external search was not run by this agent.
- Remote freshness beyond local `origin/dev` was not fetched because the scoped task only required read-only local checks and no push/commit workflow.
- Broad validator mutation behavior was not deeply audited; validator execution is handled in the validation report.

## Third Pass Candidate Areas

1. Planning-cycle report package helper and templates.
2. Problem-intake to Technical Assignment traceability matrix.
3. Technical Assignment to DRAFT task candidate decomposition helper.
4. Candidate promotion checklist and human checkpoint template.
5. Queue acceptance boundary report.
6. Read-only validation package for planning reports and DRAFT candidates.

## Forbidden Automation Areas

- Human approval, Risk Profile assignment, task promotion, execution authorization, commit authorization, push authorization, merge, release, production use, protected/canonical changes, destructive operations, lifecycle mutation, validator weakening, CI gate changes.

## Final Boundary

This report is not approval. It does not authorize execution, commit, push, merge, release, or promotion of any candidate to an executable task.
