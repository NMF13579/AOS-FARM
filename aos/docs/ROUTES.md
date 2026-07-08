# ROUTES

> **GUIDANCE BOUNDARY:**
> This document is guidance and navigation only.
> Canonical governance remains in `00_AOS_Core_Control.md`,
> `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and
> `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
> This document does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.
> ROUTES.md is navigation only. It is not lifecycle authority or approval authority.

---

## Purpose

This document maps known situations to safe routes. Use it to determine where
to start, what to read first, what action is allowed, when to stop, and
whether a human checkpoint is required.

```text
Known situation → route.
Unknown route   → HUMAN_REVIEW_REQUIRED or UNKNOWN_BLOCKED.
```

If your situation is not listed, do not proceed by assumption. Stop and report
to the human owner.

---

## First-Interaction Route Matrix

Use this matrix for the first vague user phrase before selecting any execution,
approval, merge, release, destructive, protected/canonical, lifecycle, or
scope-expansion route.

Vague first-interaction phrases do not authorize execution. A plan is not
approval. A Task Brief draft is not approval. An Execution Package draft is
not approval. An Executor Handoff Package is not approval. Readiness is not
approval. Evidence is not approval. Validator PASS is not approval.

If the route remains unclear after reading the phrase and current repository
context, stop with `UNKNOWN_BLOCKED` or `HUMAN_REVIEW_REQUIRED`.

| User phrase | Safe default route | Must not imply |
|---|---|---|
| `сделай` | Clarify scope, or create a plan/task draft if the context already identifies a bounded artifact. | Execution authorization, approval, broad repo mutation, protected/canonical mutation, lifecycle mutation, merge, release, destructive operation, or scope expansion. |
| `исправь` | Rewrite the named artifact fully, or prepare a scoped fix plan if the target is a repo/code/doc change. | Broad repo mutation, execution authorization, protected/canonical mutation, destructive operation, lifecycle mutation, merge, release, or scope expansion. |
| `проверь` | Audit, validation, or read-only inspection. | Approval, execution authorization, lifecycle mutation, commit authorization, push authorization, merge authorization, release authorization, or destructive operation permission. |
| `собери задачу` | Task Brief draft or Execution Package draft for human review. | Execution authorization, approval, merge, release, protected/canonical mutation, destructive operation, lifecycle mutation, or scope expansion. |
| `передай агенту` | Executor handoff readiness check and neutral handoff package preparation using `aos/templates/execution-packages/executor-handoff-package-template.yaml` when a package is needed. | Approval, execution authorization, commit authorization, push authorization, merge authorization, release authorization, lifecycle mutation, or scope expansion. |
| `можно выполнять?` | Readiness and human review boundary check. | Automatic approval, execution authorization, commit authorization, push authorization, merge authorization, release authorization, destructive operation permission, or protected/canonical mutation permission. |
| `готово?` | Status review and Evidence review. | Lifecycle mutation, approval, execution authorization, commit authorization, push authorization, merge authorization, release authorization, or release readiness. |
| unknown / ambiguous request | Stop and ask for clarification; record `UNKNOWN_BLOCKED` or `HUMAN_REVIEW_REQUIRED`. | Any inferred permission, including execution, approval, merge, release, destructive operation, protected/canonical mutation, lifecycle mutation, or scope expansion. |

Forbidden implicit permissions:

- `сделай` must not create execution authorization.
- `проверь` must not create approval.
- `исправь` must not create broad repo mutation.
- `собери задачу` must not authorize execution.
- `передай агенту` must not grant approval or execution authorization.
- `можно выполнять?` must not create automatic approval.
- `готово?` must not mutate lifecycle.
- Vague wording must not create merge authorization.
- Vague wording must not create release authorization.
- Vague wording must not create destructive operation authorization.
- Vague wording must not create protected/canonical mutation authorization.
- Vague wording must not create scope expansion.

Commit authorization requires an explicit commit phrase. Push authorization
requires a separate explicit push phrase. Merge authorization requires a
separate explicit merge phrase. Release authorization requires a separate
explicit release phrase. Destructive operations are forbidden by default.
Protected/canonical changes require a human checkpoint. Human unavailable for
required review, approval, checkpoint, or Risk Profile assignment means
`BLOCKED` or `HUMAN_REVIEW_REQUIRED`.

This matrix is documentation/control guidance only. It is not a runtime
natural-language classifier, AI auto-approval logic, execution router, approval
router, merge automation, release automation, lifecycle model, approval model,
or Risk Profile assignment model.

---

## Route Map

> **Product Folder Completeness Note:**
> Ordinary consumer first-start must remain available through `/aos/`.
> Root `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and `02_AOS_Governance_Control_Module_and_Safety_Rules.md` are AOS-FARM development canonical sources.
> They are not required consumer first-start prerequisites.
> Development agents working inside AOS-FARM may read them for governance orientation.

| Situation | Route | Read First | Allowed Action | Stop Condition | Human Checkpoint Required? |
|---|---|---|---|---|---|
| **New user start** | `aos/START_HERE.md` → `aos/docs/user-guide/first-run.md` | `aos/START_HERE.md`, `aos/docs/user-guide/first-run.md` | Read only; orient | Any uncertainty about scope | No (reading) |
| **Task Intake** | `aos/docs/TASK-INTAKE-WIZARD.md` | `00`, `01`, `02` | Classify raw ideas | Medical domain | No |
| **Russian new user start** | `aos/docs/START-RU.md` | `00`, `01`, `02` | Read only; orient | Any uncertainty about scope | No (reading) |
| **Installation Guide** | `aos/docs/INSTALL.md` | `02` | Read only | Dry-run only | No (reading) |
| **First Start Guide** | `aos/docs/FIRST-START.md` | `02` | Read only | N/A | No (reading) |
| **Storage docs** | `aos/docs/STORAGE.md` | `02` | Read only | N/A | No (reading) |
| **Agent entrypoints** | `aos/docs/AGENT-ENTRYPOINTS.md` | `02` | Read only | N/A | No (reading) |
| **Consumer Self-Test** | `aos/docs/SELF-TEST.md` | `02` | Read only | N/A | No (reading) |
| **Workspace Boundary** | `aos/docs/WORKSPACE-BOUNDARY.md` | `02` | Read only | N/A | No (reading) |
| **Tutor docs** | `aos/docs/TUTOR.md` | `02` | Read only | N/A | No (reading) |
| **Authorization Commands** | `aos/docs/AUTHORIZATION-COMMANDS.md` | `02` | Read only | N/A | No (reading) |
| **Unified Validate** | `aos/docs/VALIDATION.md` | `02` (Evidence Gate) | Run validation checks | Command unavailable (report NOT_RUN) | No (validation is not approval) |
| **AOS Validate Script** | `aos/scripts/aos_validate.py` | `02` | Read only | Validation only | No (validation is not approval) |
| **AOS Doctor** | `aos/scripts/aos_doctor.py` | `02` | Read only | Validation only | No (validation is not approval) |
| **Queue Dashboard** | `aos/scripts/aos_queue_dashboard.py` | `02` | Read only | Dashboard view only | No (derived view only) |
| **Prompt Packs** | `aos/prompt-packs/README.md` | `02` | Read only | Orient prompt context | No (reading) |
| **Tutor Scenarios** | `aos/docs/TUTOR-SCENARIOS.md` | `02` | Read only | Orient practical scenarios | No (reading) |
| **Agent startup** | `aos/root/AGENTS.md` → read canonical sources → check branch state | `00`, `01`, `02`, `aos/root/AGENTS.md` | Read only; inspect branch | Dirty protected files, unknown branch, missing task brief | No (reading) |
| **Task drafting** | `aos/docs/workflow/task-brief-compiler.md` → `aos/templates/task-briefs/` | `02` (Risk Profile rules) | Draft task brief | Scope unclear, Risk Profile unknown | No (drafting only) |
| **Architecture Intake** | `aos/docs/workflow/architecture-input-intake.md` | `aos/docs/workflow/architecture-decision-layer.md` | Draft candidate architecture inputs | Missing Technical Assignment; unresolved UNKNOWN | **Yes** — before decision or promotion |
| **Architecture Brief Drafting** | `aos/docs/workflow/architecture-decision-layer.md` | `aos/docs/workflow/architecture-input-intake.md` | Draft Architecture Brief DRAFT | Missing TA ref; UNKNOWN state; unresolved conflict | **Yes** — before task breakdown affects implementation |
| **Architecture Evidence Review** | `aos/docs/architecture/review/architecture-decision-evidence-packet.md` | Evidence packet + criteria | Read Evidence; prepare human review package | Evidence missing; recommendation treated as approval | **Yes** |
| **Human Architecture Checkpoint** | `aos/docs/architecture/review/human-architecture-checkpoint-template.md` | Evidence packet + criteria | Human answers checkpoint questions | Human unavailable | **Yes — human only** |
| **Architecture Validator** | `aos/scripts/aos_architecture_document_check.py` | Architecture docs | Run architecture validation commands | BLOCKED, UNKNOWN_BLOCKED, NOT_RUN | No — validation is not approval |
| **Architecture-to-Task Export** | Architecture Decision Layer / Human Architecture Checkpoint → Task Breakdown / Task Brief Builder | architecture decision Evidence, human review status, unresolved UNKNOWN list, constraints / scope boundary | Draft task breakdown with traceability | Missing architecture decision Evidence; missing architecture checkpoint; unresolved UNKNOWN not carried forward; human approval required but unavailable; agent would need to infer approval | **Yes** — task review required |
| **Architecture UNKNOWN state** | Stop → report UNKNOWN → wait for human | Architecture docs | Report only | Default `UNKNOWN_BLOCKED` | **Yes** |
| **Architecture promotion request** | Stop → prepare clarification → wait for human | Root canonical sources + architecture Evidence | None without explicit human approval | Default `BLOCKED` | **Yes — HIGH_RISK_PROTECTED** |
| **Task review** | `aos/templates/reports/evidence-review-template.md` | `02` (Evidence Gate) | Prepare Evidence report | Missing Evidence, UNKNOWN state | **Yes** — human reviews Evidence |
| **Execution request** | Human provides Task Brief → Risk Profile assignment → human checkpoint | `02` (Approval Boundary) | Execute only scoped task after human authorization | No human checkpoint, scope unclear, blockers present | **Yes** — required before any execution |
| **Validation request** | `aos/docs/FIRST-SAFE-COMMANDS.md` | `02` (Evidence Gate) | Run safe validator commands | Command unavailable (report NOT_RUN) | No (validation is not approval) |
| **Evidence review** | `aos/templates/reports/evidence-review-template.md` | `02` (Evidence Boundary) | Prepare and present Evidence | Evidence missing or unknown | **Yes** — human reviews before decision |
| **Commit request** | Human provides commit authorization checkpoint | `02` (Approval Boundary), `00` (invariants) | Commit only authorized scoped change | No human commit authorization | **Yes** — explicit commit authorization required |
| **Push request** | Human provides push authorization checkpoint | `02` (Approval Boundary), `00` (invariants) | Push only authorized commit/ref | No push authorization; commit auth ≠ push auth | **Yes** — explicit push authorization required |
| **Merge/release request** | Human provides merge/release authorization | `02`, `00` | Merge or release only with explicit human authorization | Any ambiguity; push auth ≠ merge auth | **Yes** — highest checkpoint level |
| **UNKNOWN state** | Stop → report unknown → wait for human | `02` (UNKNOWN_BLOCKED) | Report; do not proceed by assumption | Default stop — UNKNOWN_BLOCKED | **Yes** — human must resolve UNKNOWN |
| **Protected/canonical change request** | Stop → create clarification artifact → wait for human | `00`, `02` (Protected/Canonical Gate) | Read only; prepare clarification report | Do not touch protected files without checkpoint | **Yes** — HIGH_RISK_PROTECTED + human checkpoint |
| **Destructive operation request** | Stop → report → wait for human authorization + rollback plan | `02` (DESTRUCTIVE_OR_CANONICAL) | None without explicit authorization | Default: BLOCKED | **Yes** — explicit authorization + rollback plan required |
| **CI workflow request** | Stop → draft proposal → wait for human | `02` (CI/CD Boundary) | Draft CI config only | Do not enable/disable checks without human approval | **Yes** — HIGH_RISK_PROTECTED |
| **Validator change request** | Stop → draft proposal → wait for human | `02` (CI/CD Boundary) | Draft validator config only | Do not weaken or bypass validators without human approval | **Yes** — HIGH_RISK_PROTECTED |
| **Need GitHub advisory CI in a target project?** | Use `/aos/root/.github/workflows/aos-advisory.yml` as the template. Copy it to target project root `.github/workflows/aos-advisory.yml`. Then review it before enabling any branch protection or required checks. | `02` (CI/CD Boundary) | Copy template | Do not describe as mandatory or approval authority | **Yes** — HIGH_RISK_PROTECTED |

---

## Stop Conditions (Universal)

Stop immediately and report `UNKNOWN_BLOCKED` or `HUMAN_REVIEW_REQUIRED` if:

- Required canonical source is missing or unreadable
- Current branch is unknown or unexpected
- Protected/canonical files (`00`, `01`, `02`) are dirty
- Task brief is absent or scope is unclear
- Risk Profile has not been assigned by a human
- A validation command produces UNKNOWN output
- Any required human checkpoint is absent
- Situation is not in the route map above

---

## Route Unknown

If a situation is not covered by the table above:

```text
status: UNKNOWN_BLOCKED
```

or:

```text
status: HUMAN_REVIEW_REQUIRED
```

Do not invent a route. Do not proceed by assumption. Report to the human owner
with a description of the unknown situation and what clarification is needed.

---

*This document is navigation only. It does not grant execution, commit, push,
merge, release, or approval permission. Canonical governance in 00/01/02
always takes precedence.*

---

## Architecture-to-Task Export Semantics

**Required distinction:**
- Architecture route exists only to guide review-safe planning.
- Architecture route has no automatic execution authority.
- Route existence ≠ execution authorization.
- Route PASS ≠ approval.
- Architecture Evidence ≠ Task Brief approval.
- Task Brief readiness ≠ Build Step authorization.
- Architecture-to-Task Export route does not authorize implementation, Build Step execution, release, or merge to main.
