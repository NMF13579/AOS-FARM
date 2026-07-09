# Evidence Review: [Task Name]

## Review Scope
- **Controlled Task Brief Reviewed:** [Path or ID]
- **Execution Report Reviewed:** [Path or ID]
- **Controlled Execution Evidence Report Reviewed:** [Path based on aos/templates/reports/controlled-execution-evidence-report-template.md]
- **Human Execution Authorization Reviewed:** [Path or ID]

## Claimed Evidence
- **Changed Files:** [List]
- **Validation Output:** [Logs / commands / screenshots / links]
- **Diff Evidence:** [Summary]
- **Other Evidence:** [Any additional artifacts]

## Validation Result Separation
- **PASS Items:** [What was actually validated successfully]
- **NOT_RUN Items:** [What was not run]
- **UNKNOWN Items:** [What is still unknown]

## Authorization Boundary Review
- **Stayed inside authorized scope?** [Yes / No / UNKNOWN]
- **Any forbidden actions observed?** [No / Yes - explain]
- **Any scope expansion requested?** [No / Yes - explain]

## Unresolved Questions
- [List any open questions or blockers]

## Decision Needed

Human decision required: [yes/no/unknown]

Decision options:
1. Accept Evidence as sufficient for this scoped stage.
2. Request additional verification.
3. Reject result and reopen the task.
4. Block due to UNKNOWN, missing Evidence, or scope issue.

This decision block does not grant:
1. Release authorization.
2. Merge authorization.
3. Push authorization.
4. General approval outside the stated scope.
5. Lifecycle mutation unless explicitly authorized elsewhere.

## Boundary Reminder
- **Evidence Review is not commit approval.**
- **Evidence Review is not push approval.**
- **PASS is not approval.**
- **Use the controlled execution evidence report template before requesting commit authorization.**

## Next Safe Step
- Prepare commit authorization only if the human approves this review.
