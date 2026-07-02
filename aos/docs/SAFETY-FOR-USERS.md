# SAFETY-FOR-USERS

> **GUIDANCE BOUNDARY:**
> This document is guidance and navigation only.
> Canonical governance remains in `00_AOS_Core_Control.md`,
> `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and
> `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
> This document does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

## Who This Document Is For

This document explains AOS-FARM safety concepts in plain language for
non-programmers and first-time users. It does not duplicate the full
governance rules. For complete rules, read the canonical sources in
`00_AOS_Core_Control.md`, `01`, and `02`.

---

## What "PASS" Means

When a validation tool or test runs and produces a **PASS** result, it means
the check completed without finding errors under that specific check.

**PASS does not mean "approved".**

A validator passing is like a spell checker finding no typos — it does not
mean the document is ready to publish. A human still needs to review and
decide.

---

## What "Evidence" Means

Evidence is the collection of outputs, logs, diffs, validation results, and
records that prove what an agent did.

**Evidence does not mean "approved".**

Evidence is the record. A human reviews the Evidence and then makes a decision.
Evidence on its own does not authorize any action.

---

## What "Approval" Means

Approval is an **explicit human decision** to authorize a specific scoped
action. It is recorded in a human checkpoint document.

```text
Only a human can approve.
An AI cannot simulate, infer, or create approval.
"It looks good" is not approval.
"The tests passed" is not approval.
Silence is not approval.
```

---

## Why "CI PASS" Is Not Approval

CI (Continuous Integration) pipelines run automated checks. When they pass,
it means the automated checks found no errors.

**CI PASS is not approval.** It is a validation signal. A human must still
review the results and provide explicit authorization before any merge,
release, or lifecycle change.

---

## Why "UNKNOWN" Blocks Continuation

If something is unknown — a missing file, an unclear scope, an unconfirmed
state — the safe response is to **stop**.

Proceeding with an unknown state risks making incorrect changes that are
hard to reverse. AOS-FARM requires explicit clarification from a human
before any UNKNOWN can be resolved.

```text
UNKNOWN ≠ OK.
UNKNOWN_BLOCKED = stop and wait for human clarification.
```

---

## Why "NOT_RUN" Is Not PASS

If a validation step was not executed (because it was skipped, unavailable,
or outside scope), the correct status is `NOT_RUN`.

**NOT_RUN is not PASS.** It means the check was not done. Reporting NOT_RUN
honestly is required. Reporting PASS for a check that was never run is a
false claim.

---

## Why the Agent Cannot Decide By Itself

AOS-FARM separates agent actions from human decisions. The agent can:

- inspect files
- draft documents
- run safe validation commands
- prepare Evidence
- explain options

The agent **cannot**:

- approve its own work
- authorize execution
- commit or push code
- merge branches
- release to production
- assign itself a risk level

These are human decisions. This boundary exists to prevent false confidence
and hidden mistakes.

---

## What Protected/Canonical Files Are

Certain files in AOS-FARM are "protected" or "canonical." These are the
source-of-truth documents that define how the entire system works:

```text
00_AOS_Core_Control.md
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
02_AOS_Governance_Control_Module_and_Safety_Rules.md
```

These files:
- must not be edited by an agent without explicit human checkpoint
- must not be deleted, moved, or renamed without explicit human authorization
- are the highest-authority documents in the project
- if they conflict with any other document, they win

---

## Why Commit, Push, Merge, and Release Are Separate Permissions

Each step in getting code from your computer to production is a separate
gate, each requiring its own explicit human decision:

| Action | What It Does | Why It's Separate |
|---|---|---|
| **Commit** | Saves a snapshot of changes locally | Does not affect remote; reversible locally |
| **Push** | Sends the local commit to the remote server | Affects the shared repository; harder to undo |
| **Merge** | Combines branches in the shared repository | Can affect many users; requires careful review |
| **Release** | Makes changes available in production | Highest impact; typically irreversible quickly |

```text
Commit authorization ≠ push authorization.
Push authorization ≠ merge authorization.
Merge authorization ≠ release authorization.
```

Each requires a separate explicit human decision.

---

## How to Safely Give a Task to the Agent

1. **Write a Task Brief** — describe the goal, scope, allowed changes, and
   forbidden changes clearly.
2. **Assign a Risk Profile** — decide how risky the task is
   (LOW_RISK_FAST / MEDIUM_RISK_GUIDED / HIGH_RISK_PROTECTED).
   The agent cannot assign this for you.
3. **Provide an execution authorization checkpoint** — explicitly say "proceed
   with this task" in a human checkpoint document.
4. **Review the agent's Evidence report** when it finishes.
5. **Decide explicitly** whether to accept the result, request changes, or
   reject it.
6. **Provide separate commit and push authorizations** if you want the
   changes saved and shared.

Do not rely on "it looks correct" or "the tests passed" as a substitute
for explicit review and decision.

---

*This document is a plain-language guide. It does not replace the canonical
governance sources (00/01/02), which always take precedence. When in doubt,
read the canonical sources or ask the human owner.*
