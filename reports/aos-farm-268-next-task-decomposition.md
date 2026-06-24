# AOS-FARM.268 — Next Task Decomposition

## Recommended Next Path
Execute Batch 2 (Protected Updates) to fix the canonical source `00`, followed by Batch 1 (Onboarding Polish), and finally Batch 3 (Destructive Cleanup). Since Batch 2 and 3 involve protected and destructive actions, they cannot be mixed and require independent Human Checkpoints.

## Proposed Task Chain

**AOS-FARM.269 — Human Review: Select Fix Batch**
- Human selects which batch to execute first (Batch 2 recommended).

**Chain A: Protected Updates (Batch 2)**
- `AOS-FARM.270` — Protected Source Execution Prep & Human Checkpoint
- `AOS-FARM.271` — Controlled Execution: Protected Canonical Update
- `AOS-FARM.272` — Verification & Commit/Push Authorization
- `AOS-FARM.273` — Push & Remote Closure

**Chain B: Non-Destructive Polish (Batch 1)**
- `AOS-FARM.274` — Controlled Execution: Non-Destructive Onboarding Polish Batch
- `AOS-FARM.275` — Post-Execution Verification
- `AOS-FARM.276` — Commit/Push Authorization & Closure

**Chain C: Destructive Cleanup (Batch 3)**
- `AOS-FARM.277` — Destructive Cleanup Scope Lock
- `AOS-FARM.278` — Human Destructive Checkpoint
- `AOS-FARM.279` — Controlled Cleanup Execution
- `AOS-FARM.280` — Cleanup Verification & Commit/Push Closure

## Candidate Task Briefs
- **Batch 2 Task:** "Update `00_AOS_Core_Control.md` Active Areas to reflect root layout. Do not alter safety invariants."
- **Batch 1 Task:** "Consolidate Tutor guides (`agent-tutor-mode.md` and `bootstrap-agent-workflow.md`). Create unified workflow document."
- **Batch 3 Task:** "Execute `git rm` on all duplicate templates matching `* 2.md` in `templates/`."

## Human Checkpoints Required
- `HIGH_RISK_PROTECTED` execution checkpoint for Batch 2 execution.
- `DESTRUCTIVE_OR_CANONICAL` execution checkpoint for Batch 3 execution.
- Standard Commit/Push checkpoints required for the closure of each respective chain.

## Commit / Push Boundary
Each batch will have its own independent Commit and Push authorization to prevent mixing safe documentation polish with destructive actions in the remote history.

## Release Boundary
Completion of Batch 2 and 3 is recommended before labeling the repository as "Public Release Ready", though they do not strictly block the current "Release Candidate" baseline.

## Final Recommendation
Start with `AOS-FARM.269` to explicitly select the first batch to execute.
