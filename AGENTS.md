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

## 8. Mandatory Architect/Auditor Mode
- Architect/Auditor pass is mandatory before finalization for execution, remediation, implementation, contract/template creation, and final verification + authorization preparation tasks.
- Response/task mode remains adaptive.
- Self-verification is mandatory.
- Bounded self-correction is mandatory when an issue can be corrected within exact allowed files and exact authorized scope.
- If correction requires scope expansion, human approval, protected/canonical change without checkpoint, staging, commit, push, release, production use, runtime implementation, validator implementation, CI workflow changes, or approval simulation, the agent must fail closed.
- Read-only verification tasks must detect and report only.
- Human checkpoint tasks must not simulate human approval or assign Risk Profile as human.
- Commit/push tasks have restricted correction boundaries.
- PASS does not equal approval.
- Evidence does not equal approval.
- CI PASS does not equal approval.
- UNKNOWN does not equal OK.
- NOT_RUN does not equal PASS.
- Skeleton does not equal implementation.
- Human approval cannot be simulated.

## AOS Consumer Kit Reference
If you are an AI agent visiting this repository to learn about the public **AOS Consumer Kit** product, you must refer to:
- `aos/AGENT_CONTEXT.md`
- `aos/START_HERE.md`

**CRITICAL RULE**: The instructions in `00_AOS_Core_Control.md`, `01`, `02`, and `03` remain strictly for internal AOS-FARM development and must not be bypassed or ignored when making modifications to this repository.
