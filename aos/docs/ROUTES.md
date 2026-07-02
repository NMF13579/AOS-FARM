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

## Route Map

| Situation | Route | Read First | Allowed Action | Stop Condition | Human Checkpoint Required? |
|---|---|---|---|---|---|
| **New user start** | `aos/START_HERE.md` → `aos/docs/user-guide/first-run.md` | `00`, `01`, `02`, `aos/START_HERE.md` | Read only; orient | Any uncertainty about scope | No (reading) |
| **Russian new user start** | `aos/docs/START-RU.md` | `00`, `01`, `02` | Read only; orient | Any uncertainty about scope | No (reading) |
| **Installation Guide** | `aos/docs/INSTALL.md` | `02` | Read only | Dry-run only | No (reading) |
| **First Start Guide** | `aos/docs/FIRST-START.md` | `02` | Read only | N/A | No (reading) |
| **Storage docs** | `aos/docs/STORAGE.md` | `02` | Read only | N/A | No (reading) |
| **Agent entrypoints** | `aos/docs/AGENT-ENTRYPOINTS.md` | `02` | Read only | N/A | No (reading) |
| **Consumer Self-Test** | `aos/docs/SELF-TEST.md` | `02` | Read only | N/A | No (reading) |
| **Workspace Boundary** | `aos/docs/WORKSPACE-BOUNDARY.md` | `02` | Read only | N/A | No (reading) |
| **Tutor docs** | `aos/docs/TUTOR.md` | `02` | Read only | N/A | No (reading) |
| **Authorization Commands** | `aos/docs/AUTHORIZATION-COMMANDS.md` | `02` | Read only | N/A | No (reading) |
| **Agent startup** | `aos/root/AGENTS.md` → read canonical sources → check branch state | `00`, `01`, `02`, `aos/root/AGENTS.md` | Read only; inspect branch | Dirty protected files, unknown branch, missing task brief | No (reading) |
| **Task drafting** | `aos/docs/workflow/task-brief-compiler.md` → `aos/templates/task-briefs/` | `02` (Risk Profile rules) | Draft task brief | Scope unclear, Risk Profile unknown | No (drafting only) |
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
