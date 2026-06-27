---
task_id: AOS-FARM.444
title: Human Result Acceptance Loop MVP
status: DRAFT
recommended_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: false
execution_authorized: false
implementation_started: false
commit_authorized: false
push_authorized: false
---

# Task objective

Implement a minimal, explicit Human Result Acceptance Loop so that after a task is completed and Task Quality is evaluated, the user must make an explicit result decision: ACCEPT_RESULT, NEEDS_CHANGES, or REJECT_RESULT.

# Required user-facing result

The system must show:
1. What the task was supposed to do.
2. What was actually delivered.
3. What Task Quality status says.
4. Which Evidence exists.
5. What remains UNKNOWN / NOT_RUN / NOT_ENOUGH_EVIDENCE.
6. What human decision is required.
7. What each decision means.
8. What is forbidden to happen automatically.

# Allowed future implementation paths after explicit execution authorization only

aos/docs/workflow/human-result-acceptance-loop.md
aos/docs/workflow/human-result-acceptance-decision-contract.md
aos/templates/tasks/human-result-acceptance-decision-template.md
aos/templates/tasks/result-acceptance-follow-up-task-template.md
aos/templates/tasks/result-acceptance-user-summary-template.md
aos/schemas/human-result-acceptance-decision.schema.json
aos/tools/optional/human_result_acceptance_checker.py
aos/scripts/aos_result_acceptance.py
tests/result_acceptance/**
tests/fixtures/result_acceptance/**
reports/aos-farm-444-*.md
reports/aos-farm-444-*.json
reports/human-checkpoints/aos-farm-444-*.md

# Forbidden paths

00_AOS_Core_Control.md
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
02_AOS_Governance_Control_Module_and_Safety_Rules.md
03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
agentos/**
.github/**
release/**

# Forbidden behavior

no runner
no auto-execution
no auto-approval
no auto task closure
no auto next-task start
no lifecycle mutation
no commit authorization
no push authorization
no merge
no release
no tag push
no SQLite
no RAG-light
no protected/canonical source changes
