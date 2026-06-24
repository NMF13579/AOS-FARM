---
version: draft-1
status: quickstart checklist template
last_reviewed: 2026-06-24
lifecycle: "Template/reference. Use a fresh copy or embed checklist answers into the task report for each real task. This file is not approval and does not authorize execution, commit, push, release, or production use."
source_priority_note: "If this checklist conflicts with canonical sources 00/01/02, the canonical sources win."
---

# Quickstart First Task Checklist

## 1. Before starting
- [ ] Task is bounded and fits "small first task" criteria.
- [ ] Required files to modify/create are explicitly listed.
- [ ] Task Brief is prepared and approved by a human.
- [ ] Risk Profile is assigned by a human, not the agent.

## 2. Before execution
- [ ] Agent has read canonical sources 00, 01, and 02.
- [ ] Agent understands that `PASS ≠ approval`.
- [ ] Agent understands that `UNKNOWN ≠ OK` and `NOT_RUN ≠ PASS`.
- [ ] Agent has generated a DRAFT execution plan (if required by Risk Profile).
- [ ] Human has explicitly authorized execution.

## 3. During execution
- [ ] Agent strictly modified only allowed files.
- [ ] No protected/canonical files (00, 01, 02) were modified.
- [ ] No autonomous runner behavior was initiated.
- [ ] No destructive operations were performed.
- [ ] Implementation report was generated.
- [ ] Verification report was generated.

## 4. Before commit
- [ ] Commit Authorization Package is generated.
- [ ] Human Commit Authorization Checkpoint is created in DRAFT status.
- [ ] Evidence is collected (Note: Evidence is NOT approval).
- [ ] Human has explicitly updated Checkpoint to `APPROVED_FOR_COMMIT`.

## 5. Before push
- [ ] Push Authorization Package is generated.
- [ ] Human Push Authorization Checkpoint is created in DRAFT status.
- [ ] Human has explicitly updated Checkpoint to `APPROVED_FOR_PUSH`.

## 6. Stop conditions (Fail-Closed)
Stop immediately if:
- [ ] Agent attempts to self-approve.
- [ ] Agent attempts to change 00, 01, or 02 without explicit protected authorization.
- [ ] Agent attempts to commit, push, or release autonomously.
- [ ] Production use is claimed.
- [ ] GitHub release is attempted.
- [ ] Unclear instructions cause ambiguity (`HUMAN_REVIEW_REQUIRED`).

## 7. Human approvals required
- [ ] Execution Authorization (Human)
- [ ] Commit Authorization (Human)
- [ ] Push Authorization (Human)
*(Note: Human approval cannot be simulated)*

## 8. Evidence to collect
- [ ] Implementation Report
- [ ] Verification Report
- [ ] Commit/Push Packages

## 9. Checklist lifecycle
- This file is a template/reference.
- It may be copied for a specific task or used as a checklist inside a Task Brief/report.
- A checked item is Evidence, not approval.
- The checklist does not replace Human Checkpoint.
- The checklist does not authorize execution, commit, push, release, protected/canonical changes, or production use.
- If the checklist becomes outdated, stop and request `HUMAN_REVIEW_REQUIRED`.
