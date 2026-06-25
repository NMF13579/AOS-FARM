# Controlled Task Workflow

AOS execution follows a deterministic loop to ensure safety and traceability.

## 1. Preparation
- The human or agent prepares a task brief or authorization package.
- A human checkpoint is created.

## 2. Authorization
- The human reviews the checkpoint, assigns the Risk Profile, and marks it APPROVED.

## 3. Execution
- The agent runs a preflight check (git status, branch sync).
- The agent executes the task strictly within the authorized boundaries.
- The agent produces an execution report.

## 4. Verification
- A post-execution verification task confirms that only authorized files were modified.
