# AOS-FARM.440 Dogfood Lessons Learned

source_task_id: AOS-FARM.439.P2
source_evidence: reports/aos-farm-439-p2-templates-examples-status-hardening-report.md
lesson_type: pipeline_hardening
problem_observed: AOS-FARM.439.P2 needed explicit template, example, and status-handling hardening so controlled execution guard outputs were easier to interpret without confusing PASS, Evidence, or validator output with approval.
what_worked:
- The P2 hardening report captured exact files changed, fixed gaps, validation commands, guard outcomes, NOT_RUN, UNKNOWN, BLOCKED, and remaining gaps.
- The P2 review report separated review PASS from commit authorization.
- The post-commit, push authorization, and remote closure reports preserved commit, push, merge, release, and next-task boundaries.
what_failed:
- No task-blocking failure remained in P2, but the evidence chain showed that follow-up learning is manual unless captured in explicit post-execution review artifacts.
what_was_manual:
- Human Risk Profile assignment.
- Human review and push decision boundaries.
- Interpreting the completed evidence into a backlog item and next task candidate.
what_was_ambiguous:
- Whether evidence-to-backlog outputs might be mistaken for execution authorization unless every artifact repeats the approval and authorization boundaries.
recommendation: Keep post-execution learning artifacts explicit, validate them with the optional Evidence-to-Backlog helper, and stop at human review before any next lifecycle transition.
requires_backlog_item: true
approval_claimed: false
status: DRAFT

## Approval Boundary
Lessons Learned ≠ approval.
This lesson does not authorize execution, commit, push, merge, release, Risk
Profile assignment, or next task start.
