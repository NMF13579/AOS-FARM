# Task Quality Check Package Contract

## Source of Truth
* The Markdown and YAML files in the repository representing the Acceptance Criteria, Evidence Matrix, and Checkpoints are the definitive Source of Truth.
* The JSON Package is a derived input artifact only, generated or written for the read-only checker.

## Required Fields and Their Meanings
The Task Quality Check JSON package MUST contain the following required fields:

* `contract_version` (string): Version of the contract.
* `package_type` (string): Type of the package, e.g., "task_quality".
* `task_id` (string): Unique identifier for the task.
* `task_title` (string): Title of the task.
* `task_brief_path` (string): Path to the task brief.
* `acceptance_criteria_path` (string): Path to the acceptance criteria file.
* `evidence_matrix_path` (string): Path to the evidence matrix.
* `expected_artifacts` (array): List of artifacts expected to be delivered.
* `actual_artifacts` (array): List of artifacts actually delivered.
* `changed_files` (array): List of files changed during execution.
* `validation_outputs` (object): Map of validation names to their status (`PASS`, `NOT_RUN`, `UNKNOWN`, `BLOCKED`, etc.). Must include `forbidden_claims_present`.
* `known_limitations` (array): List of known limits or skipped items.
* `warnings` (array): Warnings encountered during execution.
* `blockers` (array): Issues that block the task completion.
* `human_review_required` (boolean): Flag explicitly stating if human review is required.
* `non_authority_boundary` (object): Explicit acknowledgement of safety boundaries (e.g., `task_quality_pass_is_not_human_result_acceptance`).
* `acceptance_criteria` (array): List of criteria objects with `id` and `required` flags.
* `evidence` (array): List of evidence objects mapping `criterion_id` to its `status`.

## Blocking Semantics
The checker implements strict fail-closed blocking logic:
* **Missing required fields:** BLOCKED.
* **Missing `non_authority_boundary`:** BLOCKED.
* **Required criteria without Evidence:** BLOCKED.
* **Required validation is `NOT_RUN`:** BLOCKED.
* **Required validation is `UNKNOWN`:** BLOCKED.
* **`forbidden_claims_present` is true:** BLOCKED.
* **`human_review_required` is false:** BLOCKED.

## Non-Authority Boundary
* Output is Evidence and validation signal only.
* **Task Quality PASS is not Human Result Acceptance.**
* **Task Quality result is not commit authorization.**
* **Task Quality result is not push authorization.**
* The package and the checker must NOT:
  * Approve the task.
  * Complete the task.
  * Authorize commit.
  * Authorize push.
  * Mutate lifecycle.
  * Start the next task.
