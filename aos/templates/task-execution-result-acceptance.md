# Task Execution Result Acceptance Package

## 1. Task Identity

- **Task ID**: [TASK_ID]
- **Schema version**: 1.0.0

## 2. Related Task Brief

- **Task brief path**: [PATH_TO_TASK_BRIEF]

## 3. Related Quality Package

- **Quality package path**: [PATH_TO_QUALITY_PACKAGE or N/A]

## 4. Related Forbidden Behavior Mapping

- **Forbidden behavior mapping path**: [PATH_TO_FORBIDDEN_BEHAVIOR_MAPPING or N/A]

## 5. Implementation Summary

[One or two sentences summarizing what was implemented. No claims of approval or correctness.]

## 6. Changed Files

| path | change_type | scope_status | human_review_required |
| :--- | :--- | :--- | :--- |
| `[file path]` | ADDED / MODIFIED / DELETED / RENAMED | IN_SCOPE / OUT_OF_SCOPE / UNKNOWN | true / false |

> OUT_OF_SCOPE or UNKNOWN changed files require `human_review_required: true` and are flagged for Human Review.

## 7. Validation Results

| name | command_or_check | status | evidence | human_review_required |
| :--- | :--- | :--- | :--- | :--- |
| [check name] | `[command]` | PASS / FAIL / NOT_RUN / UNKNOWN / BLOCKED / HUMAN_REVIEW_REQUIRED | [output or path] | true / false |

> NOT_RUN or UNKNOWN validation items must be disclosed here and in Section 9 / Section 10.

## 8. Evidence Items

| evidence_id | description | path_or_command |
| :--- | :--- | :--- |
| EV_001 | [description of evidence] | [path or command] |

## 9. NOT_RUN Items

Items intentionally skipped or not yet executed. Must be listed explicitly.

| item_id | reason |
| :--- | :--- |
| NR_001 | [reason this item was not run] |

> Empty list is allowed. Missing list is invalid.

## 10. UNKNOWN Items

Items whose status could not be determined. Each requires `human_review_required: true`.

| item_id | description | human_review_required |
| :--- | :--- | :--- |
| UNK_001 | [description of unknown] | true |

> Empty list is allowed. Missing list is invalid.
> UNKNOWN without human_review_required: true is blocked by validator.

## 11. Deviations from Scope

[List any out-of-scope changes, reasons, and required human review decisions. If none, state: none.]

## 12. Human Review Boundary

- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- Result acceptance validation is not approval.
- Human approval cannot be simulated.
- Human Review is required before any acceptance decision.
- This result package does not grant commit authorization.
- This result package does not grant push authorization.
- This result package does not grant merge authorization.
- This result package does not grant release authorization.

## 13. Approval Boundary

```yaml
pass_is_not_approval: true
evidence_is_not_approval: true
ci_pass_is_not_approval: true
result_acceptance_is_not_approval: true
human_review_required: true
validator_does_not_grant_approval: true
validator_does_not_grant_commit_authorization: true
validator_does_not_grant_push_authorization: true
validator_does_not_grant_merge_authorization: true
validator_does_not_grant_release_authorization: true
```

## 14. Final Result Status

```yaml
final_status: [READY_FOR_HUMAN_RESULT_REVIEW | HUMAN_REVIEW_REQUIRED | BLOCKED | UNKNOWN_BLOCKED | REJECTED_BY_VALIDATOR]
approval_granted: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
```

> Allowed statuses: READY_FOR_HUMAN_RESULT_REVIEW, HUMAN_REVIEW_REQUIRED, BLOCKED, UNKNOWN_BLOCKED, REJECTED_BY_VALIDATOR.
> APPROVED is never a valid final_status. Only a human can approve.
