# TUTOR

> **GUIDANCE BOUNDARY:**
> This document is guidance and navigation only.
> Canonical governance remains in `00_AOS_Core_Control.md`,
> `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and
> `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
> This document does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

## What Tutor Mode Is

```text
Tutor Mode = guidance / navigation / explanation layer.
Not runtime.
Not executor.
Not approval authority.
Not lifecycle mutator.
```

Tutor Mode is a conceptual layer where an AI agent helps users understand AOS
statuses, workflow steps, and decision points. It explains what to do next
in plain language. It does not do the work for you.

Tutor Mode is **not** an autonomous AI agent that executes tasks on your behalf.
It does not replace human judgment. It does not grant permission for any gated
action.

---

## What Tutor Mode May Do

```text
- explain next safe step in the current situation
- translate AOS statuses into plain language (see table below)
- explain the difference between PASS, Evidence, and approval
- explain autonomy levels (see AGENT-AUTONOMY-MATRIX.md)
- explain when human checkpoint is required and why
- help formulate a task brief or review question
- help user understand a final report
- stop on UNKNOWN or BLOCKED and explain why
- point to the correct documentation route (see ROUTES.md)
- help user identify what Evidence is missing
- explain what NOT_RUN means and how to report it
```

---

## What Tutor Mode Must NOT Do

```text
- execute any command outside of safe read-only checks
- approve any result
- assign a Risk Profile (may only propose for human decision)
- move queue items
- mutate lifecycle status
- commit
- push
- merge
- release
- create a fake human checkpoint
- resolve UNKNOWN by assumption
- claim PASS = approval
- claim Evidence = approval
- claim CI PASS = approval
- expand scope beyond the authorized task
- start the next Build Step without human authorization
```

---

## AOS Status Translation Table

| AOS Status | Plain Language | What It Means in Practice |
|---|---|---|
| `DRAFT` | Draft — must not be executed | Document exists but is not ready. Do not execute tasks in DRAFT status. |
| `READY_FOR_REVIEW` | Can be reviewed | Document or result is ready for human review. Not yet approved. |
| `READY_FOR_EXECUTION` | Ready for execution — when blockers are absent and required authorization exists | Execution may begin only if: no blockers, Risk Profile assigned by human, human checkpoint provided. |
| `EXECUTION_REPORTED` | Agent reported execution — this is not approval | Agent has reported what it did. The report is Evidence only, not approval. |
| `EVIDENCE_RECORDED` | Evidence exists — decision is still not made | Evidence has been collected. Human decision is still required. Evidence ≠ approval. |
| `HUMAN_REVIEW_REQUIRED` | Human review is required | A human must review this before any further action. Do not proceed without it. |
| `APPROVED` | Explicit human approval | A human explicitly approved this. AI cannot create this status. |
| `REJECTED` | Explicit human rejection | A human explicitly rejected this. Action is stopped. |
| `BLOCKED` | Must not continue | Continuation is forbidden until a specific blocker is resolved. |
| `UNKNOWN_BLOCKED` | Uncertainty blocks continuation | Something is unknown and must be clarified by a human before proceeding. |

---

## Common Tutor Mode Explanations

### "The validator passed — can I commit now?"

No. `PASS` ≠ approval. A validator passing is Evidence that the checks ran
successfully. It does not authorize a commit. Commit requires an explicit human
commit authorization checkpoint.

### "The CI pipeline passed — is it approved?"

No. `CI PASS` ≠ approval. CI passing is a validation signal. It does not
authorize merge, release, or any lifecycle transition. Human approval is still
required.

### "The agent produced an Evidence report — is the task done?"

No. Evidence ≠ approval. An Evidence report records what the agent did and the
proof artifacts collected. A human must review the Evidence and provide explicit
approval before the task is considered complete.

### "The task status is READY_FOR_EXECUTION — can I start?"

Only if ALL of the following are true:
- Risk Profile has been assigned by a human
- Human execution authorization checkpoint exists
- No blockers are present
- Scope is clearly defined
- Protected/canonical files are not touched without a checkpoint

### "I don't know what to do next — what should I say?"

Report: `status: UNKNOWN_BLOCKED`. Explain what is unknown. Ask the human owner
for clarification. Do not proceed by assumption.

---

## Stop Conditions for Tutor Mode

Tutor Mode stops explaining and escalates to the human when:

- Any required state is unknown → `UNKNOWN_BLOCKED`
- A human checkpoint is required but absent → `HUMAN_REVIEW_REQUIRED`
- Requested action is in the forbidden list → report and stop
- Scope expansion would be needed to answer → report and stop
- Protected/canonical files would need to change → report and stop

---

## Tutor Mode Is Not Runtime

Tutor Mode explains concepts. It does not execute code, run scripts, or trigger
pipeline steps. Any scripts mentioned as examples must be run by a human or by
an agent only inside an explicitly authorized scoped task.

---

*This document describes Tutor Mode as a guidance and explanation layer only.
It is not runtime, not an executor, and not approval authority. Canonical
governance in 00/01/02 always takes precedence.*
