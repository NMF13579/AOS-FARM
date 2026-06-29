# Design Conflict Clarification

**What conflicts:** The requirement to generate a handoff prompt for an unapproved task vs. the validator's strict gate requirements for `READY_FOR_HANDOFF`.
**Which sources conflict:** The Dogfood task execution corridor (which tests generating a handoff prompt before human review) vs. `aos/scripts/aos_task_document_check.py` (which blocks `READY_FOR_HANDOFF` if `approval_status: NOT_APPROVED`).
**Exact conflicting statements:**
- Dogfood requirement: "The task file must include at minimum: `approval_status: NOT_APPROVED`... Generate handoff prompt."
- Validator code: `elif approval == "NOT_APPROVED": reasons_human.append("approval_status is NOT_APPROVED")` leading to `HUMAN_REVIEW_REQUIRED`, which fails the handoff generation: `if status != "READY_FOR_HANDOFF": print(f"FAIL: Task readiness is {status}. Must be READY_FOR_HANDOFF.")`.
**Affected decision:** Ability to generate handoff prompts and pass result-review for tasks that are intentionally unapproved (e.g., in a pre-approval execution mode).
**Risk:** Modifying the task to `APPROVED` or some other value to bypass the validator would simulate human approval, violating the core safety invariants.
**Required human decision:** Decide whether the handoff prompt should be generated for `HUMAN_REVIEW_REQUIRED` tasks, or whether the dogfood corridor should test a different state.
**Temporary safe status:** `BLOCKED_DESIGN_CONFLICT`
