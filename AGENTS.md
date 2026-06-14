# AGENTS

This document contains repository-level instructions for any AI Agent or IDE Controller operating in the AOS-FARM environment.

## 1. Required Source Reading Order
Before performing any execution, you MUST read the following sources in this exact order:
1. `00_AOS_Core_Control.md`
2. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
3. `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## 2. Source Precedence
- `00_AOS_Core_Control.md` is the highest canonical source.
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` governs Build Step roadmap, Assembly Pipelines, and daily workflow.
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md` governs safety, Risk Profiles, gates, approval boundaries, lifecycle mutations, and protected/canonical rules.
- If 01 and 02 conflict, 02 wins unless 00 explicitly dictates otherwise.

## 3. Always-On AOS Invariants
- `PASS` ≠ approval.
- `Evidence` ≠ approval.
- `CI PASS` ≠ approval.
- `UNKNOWN` ≠ OK.
- `NOT_RUN` ≠ PASS.
- Human approval cannot be simulated.
- Skeleton ≠ implementation.
- Scope must not expand without explicit human permission.
- Protected/canonical changes require explicit human checkpoint.
- Destructive operations are forbidden by default.
- Minimal Safety Floor is always-on from day one.
- Agent memory is NOT Source of Truth.
- Repo state and file-based checkpoints ARE the Source of Truth for workflow continuation.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.

## 4. Environment-Agnostic Workflow Rules
- **Do not trust IDE or chat memory.** You must reconstruct the current state from the repository files before every task.
- **Session Start Protocol:** Always verify the active Git branch, HEAD commit, origin sync status, and the presence of required control sources.
- **Multi-Environment Protocol:** Antigravity and Codex CLI / VS Code are replaceable execution environments. They do not own the workflow state.
- **Role Boundaries:**
  - *IDE Architect / Controller:* Plans and verifies execution.
  - *Executor Agent:* Implements scoped code changes.
  - *Router Agent:* Assigns tasks to appropriate models based on tokens and complexity.
  - *Auditor Agent:* Evaluates execution against safety rules.
  - *Human Owner:* The sole authority for execution authorization, commits, pushes, and protected drift.
- **Model / Agent Switching:** Model switch or Agent switch is NOT approval. Output from a cheap model does not lower safety requirements.
- **ChatGPT Rule:** ChatGPT may be used as an external architect/reviewer. However, ChatGPT review is NOT human approval.

## 5. Token Limits and Handoffs
- You must emit a handoff checkpoint *before* a session or token limit interruption when possible.
- Reconstruct the context from the latest valid handoff if a session dies unexpectedly.

## 6. Forbidden Operations
- You MUST NOT self-approve any execution, commit, push, release, or production use.
- You MUST NOT automatically assign `LOW_RISK_FAST` to bypass human authorization.
- You MUST NOT automatically commit or push.
- You MUST NOT make automatic protected/canonical changes.

## 7. Fail-Closed Rule
If a required source is missing, a checkpoint is ambiguous, or authorization is unverified, you MUST fail closed and set the status to `BLOCKED` or `HUMAN_REVIEW_REQUIRED`.
