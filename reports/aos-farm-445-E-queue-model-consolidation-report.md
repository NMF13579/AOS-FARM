# AOS-FARM.445.E Queue Model Consolidation Report

## Task Context
AOS-FARM.445.E — Queue Model Consolidation
Authorized Risk Profile: HIGH_RISK_PROTECTED

## Objective
Consolidate the Task Queue and Registry models by explicitly defining the YAML format as the canonical Source of Truth and marking the legacy Markdown table format as a human-readable projection. Reinforce boundaries against auto-execution via the queue.

## Prompt and Documentation Updates
- `aos/prompts/task-brief-builder.md`: Updated to instruct the AI to build task queues using the **canonical YAML task queue format**, noting that the markdown table is a projection only. Reasserted that queue position is not approval.
- `aos/docs/workflow/task-registry-and-queue.md`: Added core principles explicitly stating the canonical YAML model vs. the projection model. Asserted invariants:
  - `queue_position_is_not_approval`
  - `show_next_is_not_execution`
  - `show_current_is_not_execution`

## Template Adjustments
- `aos/templates/task-queue-template.md`: Added a `> [!WARNING]` header explicitly marking the file as a `PROJECTION ONLY` compatibility view, and pointing to the canonical YAML structure.
- `aos/templates/tasks/task-registry-entry-template.md` & `aos/templates/tasks/task-queue-template.md`: Added hard rules asserting that queue position is not approval and selection (show-current/show-next) is not execution.

## Validator and CLI Hardening
- `aos/scripts/aos_tasks.py`: Updated the JSON outputs for `show-current` and `show-next` commands to explicitly inject these invariants into the output map:
  ```json
  "invariants": {
      "queue_position_is_not_approval": true,
      "show_next_is_not_execution": true,
      "show_current_is_not_execution": true
  }
  ```

## Testing & Fixtures
Ran `python3 -m unittest discover -s tests/task_registry` successfully.
All CLI tests run predictably returning stable output statuses and accurately emitting the required invariants.

## Execution Constraints Verification
- [x] Canonical files were not modified.
- [x] Task Quality files were not modified.
- [x] Human Result Acceptance files were not modified.
- [x] Consumer docs were not modified.
- [x] No runner, auto-execution, auto-approval, SQLite, or RAG-light introduced.
- [x] No destructive cleanup was performed.
- [x] No commit, push, merge, or release was executed.
- [x] 445.F was not started.

## Status
Current Status: `HUMAN_REVIEW_REQUIRED`
