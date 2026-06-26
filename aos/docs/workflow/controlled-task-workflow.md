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
- Guard PASS is not approval.

## 3. Execution
- After Human Execution Authorization, run Controlled Execution Guard `precheck`.
- The user gives the agent the copy-ready prompt in `aos/prompts/controlled-execution.md`.
- The agent verifies consumer/runtime workflow artifacts, branch state, repo state, human authorization, Risk Profile, and exact scope before editing files.
- The agent executes the task strictly within the authorized boundaries.
- After execution and before evidence review, run Controlled Execution Guard `scopecheck` against changed files.
- The agent produces an execution report with Evidence.

## 4. Verification
- Before finalizing Evidence Review, run Controlled Execution Guard `postcheck` against the Evidence or execution report.
- A post-execution verification task confirms that only authorized files were modified.
- A human reviews Evidence before any commit authorization is prepared.
- Commit and push remain separate human-authorized steps.
- Guard PASS does not authorize commit.
- Guard PASS does not authorize push.
- `BLOCKED`, `UNKNOWN_BLOCKED`, and `HUMAN_REVIEW_REQUIRED` mean stop and ask for human/project-owner review.

## Reference
For a non-programmer-friendly walkthrough, see `aos/docs/workflow/first-controlled-execution.md`.
