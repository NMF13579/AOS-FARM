# AOS-FARM.283 — First Template Dogfood Verification + README Onboarding Gap Plan

## Final Status
DRAFT_FOR_HUMAN_REVIEW

## AOS-FARM.282 Dogfood Verification
- **Status:** AOS_FARM_282_FIRST_TEMPLATE_DOGFOOD_EXECUTED_WITH_WARNINGS
- **Created Artifacts:**
  - `reports/dogfood/first-template/simple-notes-bootstrap-checklist.md`
  - `reports/dogfood/first-template/simple-notes-agent-tutor-session.md`
  - `reports/dogfood/first-template/simple-notes-first-task-brief.md`
  - `reports/dogfood/first-template/simple-notes-manual-task-queue-entry.md`
  - `reports/dogfood/first-template/simple-notes-handoff-package.md`
  - `reports/dogfood/first-template/simple-notes-verification-boundary-check.md`
  - `reports/aos-farm-282-first-template-dogfood-execution-report.md`
- **Usability Result:** The conceptual workflow is logical and safe. A non-programmer can safely navigate from task formulation to verification boundaries. However, initial access is currently obstructed.

## Exact README Blocker
The `README.md` file contains the following instruction:
`python3 agentos/agentos.py start`
This script (`agentos/agentos.py`) was removed/migrated in previous cleanups.

## Why this is an Onboarding Blocker
A vibe-coder or non-programmer relies on literal copy-paste instructions to bootstrap their environment. Encountering a "file not found" error on step 1 completely halts their progress and breaks trust in the template.

## Is First-User Path Usable Now?
Conceptually yes, but practically **no**, until the `README.md` entrypoint is updated to point to the current normalized documentation structure in `docs/user-guide/`.

## Recommendation
Authorize `AOS-FARM.284` to specifically fix the `README.md` to point to the correct workflow documents.

---

## Scope / Risk Plan for AOS-FARM.284

### Target File
- `README.md`

### Allowed Future Scope (AOS-FARM.284)
- Remove/replace the stale `python3 agentos/agentos.py start` instruction.
- Point the user to `docs/user-guide/README.md`.
- Point the user to `docs/user-guide/bootstrap-agent-workflow.md`.
- Point the user to Agent Tutor Mode (`docs/user-guide/agent-tutor-mode.md`).
- Clarify that PASS, CI, and Evidence do not constitute production/release approval.

### Forbidden Future Scope (AOS-FARM.284)
- No runner creation.
- No `agentos/agentos.py` restoration.
- No `00`, `01`, `02` canonical document edits.
- No templates cleanup (Batch 3 must wait).
- No release/production claims.

## Risk Profile
- `agent_proposed_risk_profile`: MEDIUM_RISK_GUIDED
- `human_assignment_required`: true
