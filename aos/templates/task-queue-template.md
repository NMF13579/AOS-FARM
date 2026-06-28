# Manual Task Queue (Projection / Compatibility View)

> [!WARNING]
> **PROJECTION ONLY**: This Markdown table format is a human-readable projection and compatibility view. The **canonical model** is the YAML Task Registry / Queue located in `aos/templates/tasks/task-registry-entry-template.md` and `aos/templates/tasks/task-queue-template.md`.
>
> **CRITICAL INVARIANTS**:
> - Queue position is NOT approval.
> - `show-current` is NOT execution.
> - `show-next` is NOT execution.

*Note: This is a markdown-first, manual tracking queue, not an automated runner queue.*

**Priority Model (Proposal Only):**
- **P0:** Blocking / safety / critical dependency
- **P1:** High-value or required next step
- **P2:** Useful but not blocking
- **P3:** Optional or later
*Priority ≠ approval. Task queue position ≠ execution authorization.*

## Task Queue Items

| Task ID | Task Title | Source TA Section | Task Status | Priority | Dependency Status | Proposed Risk | Human Risk | Batch Eligibility | Review Requirement | Execution Auth Status | Validation Status | Evidence Status | Stale/Recheck | Next Action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TASK-001 | [Title] | [Section] | DRAFT | P1 | CLEAR | LOW | PENDING | YES | REQUIRED | UNAUTHORIZED | PENDING | PENDING | OK | Wait for Review |

## Lifecycle States
Valid `Task Status` values:
- `DRAFT`
- `READY_FOR_REVIEW`
- `NEEDS_REVISION`
- `REJECTED`
- `BLOCKED`
- `READY_FOR_EXECUTION_AUTHORIZATION`
- `APPROVED_FOR_EXECUTION`
- `EXECUTED`
- `VERIFIED`

## Queue Insights (To answer user questions)
- **What should I do next?** Check tasks marked `READY_FOR_REVIEW` or `READY_FOR_EXECUTION_AUTHORIZATION`.
- **Which task is blocked?** Tasks with Dependency Status `BLOCKED` or Status `BLOCKED`.
- **Which task needs my review?** Tasks with `DRAFT` or `READY_FOR_REVIEW`.
- **Which task is ready for execution authorization?** Tasks where Human Risk is assigned and status is `READY_FOR_EXECUTION_AUTHORIZATION`.
- **Which tasks can be batched?** Tasks with Batch Eligibility `YES` that share dependencies.
- **Which tasks must be executed separately?** Tasks with Batch Eligibility `NO`.

**Safety Invariant Reminder:**
- **READY_FOR_EXECUTION_AUTHORIZATION ≠ APPROVED_FOR_EXECUTION.**
