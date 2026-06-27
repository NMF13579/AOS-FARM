# Task Quality Check Package Contract

## Source of Truth
* The Markdown and YAML files in the repository representing the Acceptance Criteria, Evidence Matrix, and Checkpoints are the definitive Source of Truth.
* The JSON Package is a derived input artifact only, generated or written for the read-only checker.

## Checker Output Constraints
* Output is Evidence and validation signal only.
* The package and the checker must NOT:
  * Approve the task.
  * Complete the task.
  * Authorize commit.
  * Authorize push.
  * Mutate lifecycle.
  * Start the next task.
