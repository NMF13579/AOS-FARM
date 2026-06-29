---
task_id: AOS-FARM.463
title: Full Manual Handoff Corridor Dogfood
type: feature
template_level: S
status: DRAFT
queue_mode: AUTO
queue_position: null
queue_status: BACKLOG
queue_priority: NORMAL
risk_profile: HIGH_RISK_PROTECTED
risk_assigned_by: none
approval_status: NOT_APPROVED
commit_authorized: false
push_authorized: false
release_authorized: false
required_final_state: READY_FOR_HUMAN_REVIEW
human_checkpoint_required: true
validator_status: NOT_RUN
evidence_status: NOT_RUN
log_uri: ".aos-tmp/tasks/AOS-FARM.463/agent-actions.log"
log_status: NOT_STARTED
owner: human
created_at: 2026-06-29
updated_at: 2026-06-29
---

## Задача
Implement dogfooding task for the progressive task document format.
* Scope: Prove the existing manual handoff corridor works end-to-end without creating a runner.

## Out of scope
* Non-goals: Do not create or modify runner, execution bridge, automatic approval, auto lifecycle transition, auto commit, auto push, auto release, SQLite, RAG-light, generated registry as Source of Truth, generated queue as Source of Truth, generated cache as Source of Truth, protected/canonical documentation. Do not mix PASS/Evidence/approval/READY_FOR_EXECUTION/commit authorization/push authorization/release authorization.
* Allowed files: tasks/**, reports/aos-farm-463-full-manual-handoff-corridor-dogfood-report.md, tests/fixtures/**
* Forbidden files: 00_AOS_Core_Control.md, 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md, 02_AOS_Governance_Control_Module_and_Safety_Rules.md, .github/workflows/**, aos/SELF_TEST.md, protected/canonical documentation, /.aos-tmp/ (except as local disposable scratch), generated registry, generated queue, generated cache.
* Stop Condition: Stop after producing the implementation report and validation evidence. Stop at `READY_FOR_HUMAN_REVIEW` or `BLOCKED`.

## Done когда
* Readiness criteria: Python check command for task readiness passes.
* Handoff boundary: Handoff prompt is generated and checked for boundary violations. Handoff prompt is not approval.
* Result report boundary: Scoped work must be reported in `reports/aos-farm-463-full-manual-handoff-corridor-dogfood-report.md`. Handoff result is not approval.
* Human review boundary: Task must stop at `READY_FOR_HUMAN_REVIEW` prior to human approval.
* Commit boundary: Commit authorization is not granted. Task must stop before commit.
* Push boundary: Push authorization is not granted. Task must stop before push.

## История
2026-06-29 - Task drafted

## Evidence
NOT_RUN

## ⛔ Решение
<!-- Только human. Агент не редактирует существующее human decision. -->
**Статус:** PENDING  
**Дата:**  
**Решение:**  
**Комментарий:**  
