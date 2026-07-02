# AGENT-AUTONOMY-MATRIX

> **GUIDANCE BOUNDARY:**
> This document is guidance and navigation only.
> Canonical governance remains in `00_AOS_Core_Control.md`,
> `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and
> `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
> This document does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

## Critical Rule

```text
Autonomy level does not replace Risk Profile.
Autonomy level controls how much operational freedom the agent has.
Risk Profile controls how dangerous the task is.
Human approval controls whether a gated decision is allowed.
```

These three dimensions are independent and must all be satisfied before
any gated action is taken.

---

## Mandatory Boundaries

```text
A4_COMMIT_AUTHORIZED does not authorize push.
A5_PUSH_AUTHORIZED does not authorize merge or release.
A6_RELEASE_AUTHORIZED requires explicit human release/merge approval.
```

Reaching a higher autonomy level does not grant all permissions of levels
below it automatically. Each gated action requires its own explicit human
authorization for that specific action.

---

## Autonomy Levels

---

### A0_READ_ONLY

**Plain-language meaning:** Agent only inspects and explains. No changes are
made to any file.

| Field | Detail |
|---|---|
| **Allowed actions** | Read files; inspect git state; run read-only git commands; explain content; produce summaries |
| **Forbidden actions** | Write, create, delete, move, or rename any file; commit; push; merge; release; run mutating scripts |
| **Required human input** | None for reading; human must provide explicit direction to advance to A1+ |
| **Allowed outputs** | Text summaries, status reports, read-only git command outputs |
| **Required Evidence** | None beyond read confirmation |
| **Stop conditions** | Unknown state; missing canonical sources; unexpected dirty files |
| **Relation to Risk Profiles** | Compatible with any Risk Profile for read-only inspection |

---

### A1_DRAFT_ONLY

**Plain-language meaning:** Agent may write drafts but must not change
working project files. Drafts are clearly marked as non-canonical.

| Field | Detail |
|---|---|
| **Allowed actions** | Create new draft documents in explicitly allowed draft paths; write task brief drafts; write Evidence draft templates |
| **Forbidden actions** | Edit existing tracked project files; commit; push; merge; release; change protected/canonical files; change any file not in authorized draft scope |
| **Required human input** | Human must define draft scope and allowed draft paths; human reviews drafts before promotion |
| **Allowed outputs** | Draft documents with explicit draft/non-canonical status markers |
| **Required Evidence** | List of draft files created; confirmation no tracked files were modified |
| **Stop conditions** | Scope unclear; draft path not defined; risk of touching tracked files |
| **Relation to Risk Profiles** | Typically LOW_RISK_FAST or MEDIUM_RISK_GUIDED (human-assigned) |

---

### A2_GUIDED_EDIT

**Plain-language meaning:** Agent may edit scoped files only inside a
human-authorized task.

| Field | Detail |
|---|---|
| **Allowed actions** | Create or modify files explicitly listed in an authorized Task Brief; run safe read-only validation; produce diff |
| **Forbidden actions** | Edit files not in the explicit allowed list; commit; push; merge; release; expand scope; touch protected/canonical files without checkpoint |
| **Required human input** | Human-authorized Task Brief with explicit allowed/forbidden file list; Risk Profile assigned by human |
| **Allowed outputs** | Modified files (within scope); diff; Execution Report |
| **Required Evidence** | Diff of all changed files; list of files touched; list of files not touched; any NOT_RUN validation |
| **Stop conditions** | Scope unclear; file not in allowed list; unexpected tracked changes; UNKNOWN state |
| **Relation to Risk Profiles** | Typically MEDIUM_RISK_GUIDED; HIGH_RISK_PROTECTED for sensitive edits |

---

### A3_VALIDATED_CHANGE

**Plain-language meaning:** Agent may run validation after a scoped change,
but validation output is not approval.

| Field | Detail |
|---|---|
| **Allowed actions** | All A2 actions; additionally run explicitly authorized validation commands; collect and record Evidence |
| **Forbidden actions** | Treat validation PASS as approval; commit; push; merge; release; run validators outside authorized scope |
| **Required human input** | Explicit authorization to run validation; validation scope defined in Task Brief |
| **Allowed outputs** | Validation results; Evidence Report; NOT_RUN disclosures |
| **Required Evidence** | Full validation output or NOT_RUN report; diff; changed file list |
| **Stop conditions** | PASS output interpreted as approval; UNKNOWN validation state; validator unavailable (report NOT_RUN) |
| **Relation to Risk Profiles** | MEDIUM_RISK_GUIDED minimum; HIGH_RISK_PROTECTED for validator changes |

---

### A4_COMMIT_AUTHORIZED

**Plain-language meaning:** Agent may commit only the authorized scoped change.
Commit authorization does not authorize push.

| Field | Detail |
|---|---|
| **Allowed actions** | `git commit` of the specifically authorized staged change only |
| **Forbidden actions** | Push; merge; release; commit files outside authorized scope; amend without authorization; force-push |
| **Required human input** | Explicit human commit authorization checkpoint for this specific commit |
| **Allowed outputs** | Commit hash; post-commit verification report |
| **Required Evidence** | Commit hash; diff of committed files; confirmation of scope adherence |
| **Stop conditions** | No commit authorization; staged files outside scope; protected/canonical files in staged set |
| **Relation to Risk Profiles** | HIGH_RISK_PROTECTED minimum for protected files; MEDIUM_RISK_GUIDED for scoped documentation |

---

### A5_PUSH_AUTHORIZED

**Plain-language meaning:** Agent may push only the authorized commit/ref.
Push authorization does not authorize merge or release.

| Field | Detail |
|---|---|
| **Allowed actions** | `git push` of the specifically authorized commit/ref to the authorized remote/branch |
| **Forbidden actions** | Merge; release; push additional commits; force-push; push to different branch than authorized |
| **Required human input** | Explicit human push authorization checkpoint for this specific ref and target |
| **Allowed outputs** | Push confirmation; post-push remote baseline closure report |
| **Required Evidence** | Push output; remote HEAD confirmation; diff between pre- and post-push state |
| **Stop conditions** | No push authorization; commit auth ≠ push auth; unexpected commits in push |
| **Relation to Risk Profiles** | HIGH_RISK_PROTECTED minimum |

---

### A6_RELEASE_AUTHORIZED

**Plain-language meaning:** Agent may perform a release or merge only with
explicit human release/merge approval. This is the highest gated level.

| Field | Detail |
|---|---|
| **Allowed actions** | Merge or release only the explicitly authorized ref/branch per human release authorization |
| **Forbidden actions** | Auto-release; auto-merge without authorization; release additional refs; modify release scope |
| **Required human input** | Explicit human release/merge authorization checkpoint; release scope defined; rollback plan present |
| **Allowed outputs** | Merge/release confirmation; post-release baseline report |
| **Required Evidence** | Full Evidence package; pre-release diff; post-release state confirmation |
| **Stop conditions** | No release authorization; push auth ≠ release auth; scope ambiguity; missing rollback plan |
| **Relation to Risk Profiles** | HIGH_RISK_PROTECTED always; DESTRUCTIVE_OR_CANONICAL if rollback is complex |

---

## Summary Table

| Level | Name | One-Line Summary | Can Commit? | Can Push? | Can Release? |
|---|---|---|---|---|---|
| A0 | READ_ONLY | Inspect and explain only | No | No | No |
| A1 | DRAFT_ONLY | Write drafts, no project file changes | No | No | No |
| A2 | GUIDED_EDIT | Edit authorized files inside Task Brief | No | No | No |
| A3 | VALIDATED_CHANGE | Run validation; report results; not approval | No | No | No |
| A4 | COMMIT_AUTHORIZED | Commit authorized scope only | **Yes** (authorized scope only) | No | No |
| A5 | PUSH_AUTHORIZED | Push authorized ref only | Yes (prior) | **Yes** (authorized ref only) | No |
| A6 | RELEASE_AUTHORIZED | Merge/release with explicit authorization | Yes (prior) | Yes (prior) | **Yes** (explicit auth only) |

---

## Relation to Risk Profiles

Risk Profile is assigned by the **human owner**, not by the agent. It controls
the minimum safety requirements for a task:

- `LOW_RISK_FAST` — low-impact advisory tasks (human-assigned only)
- `MEDIUM_RISK_GUIDED` — documentation, template, Evidence tasks
- `HIGH_RISK_PROTECTED` — lifecycle, validators, CI, protected files, merge, release
- `DESTRUCTIVE_OR_CANONICAL` — delete, rename, force-push, canonical rewrite
- `UNKNOWN_BLOCKED` — default when risk cannot be determined

Autonomy level controls **what the agent is operationally allowed to do**.
Risk Profile controls **how much governance scrutiny applies**.
Human approval controls **whether a gated action is authorized**.

All three must align before a gated action is taken.

---

*This document is guidance only. It does not grant execution, commit, push,
merge, release, or approval permission. Canonical governance in 00/01/02
always takes precedence.*
