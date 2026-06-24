# AOS-FARM.268 — Fix Batch Candidate Plan

## Batch 1 — Non-Destructive Onboarding Polish
**Scope:** Consolidate `docs/user-guide/agent-tutor-mode.md` and `docs/user-guide/bootstrap-agent-workflow.md` to remove overlap and improve onboarding clarity.
**Risk Profile:** `MEDIUM_RISK_GUIDED`
**Requirements:** Merge overlapping definitions safely. Do not delete canonical guides without explicit permission; if one must be removed, it moves to Batch 3.

## Batch 2 — Protected / Canonical Update Candidates
**Scope:** Update the "Active-now Areas" section in `00_AOS_Core_Control.md` to accurately reflect the Core Working Version layout (`docs/`, `reports/`, `templates/`, etc.) instead of the legacy `agentos/` paths.
**Risk Profile:** `HIGH_RISK_PROTECTED`
**Requirements:** Requires separate Human Checkpoint before modifying `00_AOS_Core_Control.md`.

## Batch 3 — Duplicate Template Cleanup Candidates
**Scope:** Delete all duplicate template files (identified by `* 2.md`) located in the `templates/` directory.
**Risk Profile:** `DESTRUCTIVE_OR_CANONICAL`
**Requirements:** Requires strict destructive Human Checkpoint and git execution. Must be executed separately from protected source changes.

## Batch 4 — Deferred / No-Action Items
**Scope:** No items from the AOS-FARM.267 report are currently deferred. All three findings are actionable and categorized into Batches 1, 2, and 3.

## Batch Isolation Rules
- Batch 1 (Polish) must not modify `00_AOS_Core_Control.md` or delete files.
- Batch 2 (Protected) must strictly target only the "Active-now Areas" list inside `00_AOS_Core_Control.md`.
- Batch 3 (Destructive) must solely target `* 2.md` files in `templates/`.
- Mixing Batches during execution is strictly forbidden. Each batch represents a distinct execution stage with its own Risk Profile and Checkpoint loop.

## Proposed Human Review Questions
- Which batch should we start executing first? (Recommendation: Start with Batch 2 to fix the core source, followed by Batch 1, then Batch 3).
- For Batch 3, do you prefer `git rm` (deletion) or moving the duplicates to an archive folder?

## What Must Not Be Mixed
Do not mix the destructive cleanup (Batch 3) with the protected canonical updates (Batch 2). They must be executed in separate branch loops and checked by independent Human Checkpoints.
