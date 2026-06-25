# Task Breakdown Template

## 1. Technical Assignment Source Metadata
- **TA File:** [File path or reference]
- **TA Version/Date:** [Date or SHA]
- **TA Completeness Status:** [e.g., Fully Bounded, Has Ambiguities]

## 2. Unresolved UNKNOWN List
- List any ambiguities, missing information, or requirements that prevent safe decomposition.

## 3. Extracted Work Item Inventory & Task Drafts
| Task ID | Task Title | Description |
|---|---|---|
| TASK-001 | ... | ... |

## 4. Task-to-TA Traceability Matrix
This matrix answers: Which TA section justifies this task? Which task has no clear TA source? Which TA requirement has no task yet? Which task is blocked by missing information?
| Task ID | Source TA Section | Traceability Status |
|---|---|---|
| TASK-001 | Section 2.1 | Traced |

## 5. Dependency Map & Priority Proposal
| Task ID | Depends On | Priority Proposal (P0-P3) | Batch Plan (Can be grouped?) |
|---|---|---|---|
| TASK-001 | None | P1 | Yes, with TASK-002 |

## 6. Risk, Validation & Evidence Expectations
| Task ID | Risk Profile Proposal | Validation Expectations (Checks/Commands) | Evidence Expectations (Outputs/Diffs) |
|---|---|---|---|
| TASK-001 | MEDIUM_RISK_GUIDED | Run unit tests for component | Test output logs |

## 7. Stale-Task Detection
- **Last TA Review:** [Date]
- **Status:** [Are these tasks still aligned with the latest TA?]

## 8. Human Review Decision
- [ ] Needs Review
- [ ] Approved for Queue
- [ ] Rejected

## Final Boundary Rule
- **READY_FOR_EXECUTION_AUTHORIZATION ≠ APPROVED_FOR_EXECUTION.**
- **Task queue inclusion ≠ approval.**
- **Priority ≠ approval.**
- **Validation plan ≠ validation PASS.**
- **Evidence requirements ≠ collected Evidence.**
- **Risk Profile proposal ≠ human-assigned Risk Profile.**
- **Task draft ≠ approved task.**
