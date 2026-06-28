# Pipeline Hardening Backlog Item: AOS-FARM.448

**Source Task:** AOS-FARM.448
**Item Type:** Pipeline Hardening / Guard Rails

## Description
Based on the AOS-FARM.448 dogfood loop, the Controlled Execution Guard (`aos_controlled_execution_guard.py`) has strict dictionary parsing requirements for embedded YAML within Markdown files. The schema requirements should be formally documented in `aos/docs/workflow/first-controlled-execution.md` so that the agent can reliably generate the exact expected keys (`validation_results`, `human_review_required`, etc.) without failing the initial `postcheck` run.

## Proposed Implementation
- Extend `first-controlled-execution.md` with the explicit YAML snippet schema expected by the `postcheck` command.
- Add an explicit type check on `human_execution_authorization` schema in the doc to prevent missing keys (`authorized`, `authorized_by`).

*Note: Pipeline Hardening Backlog Item ≠ execution authorization.*
