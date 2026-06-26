# Controlled Task Workflow

AOS execution follows a deterministic loop to ensure safety and traceability.

## 1. Preparation
- The human selects exactly one task from the queue.
- The human prepares or reviews the `Controlled Task Brief`.
- The human confirms allowed scope, forbidden scope, validation, and expected output.

## 2. Authorization
- The human assigns the Risk Profile.
- The human creates Human Execution Authorization for that exact brief.
- `Controlled Task Brief` is still not approval by itself.

## 3. Execution
- The user gives the agent the copy-ready prompt in `aos/prompts/controlled-execution.md`.
- The agent verifies required sources, branch state, repo state, human authorization, Risk Profile, and exact scope before editing files.
- The agent executes the task strictly within the authorized boundaries.
- The agent produces an execution report with Evidence.

## 4. Verification
- A post-execution verification task confirms that only authorized files were modified.
- A human reviews Evidence before any commit authorization is prepared.
- Commit and push remain separate human-authorized steps.

## Reference
For a non-programmer-friendly walkthrough, see `aos/docs/workflow/first-controlled-execution.md`.
