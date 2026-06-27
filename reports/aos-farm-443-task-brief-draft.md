task_id: AOS-FARM.443
title: Task Quality Acceptance Gate MVP
status: DRAFT
risk_profile_required: true
recommended_risk_profile: HIGH_RISK_PROTECTED
risk_profile_assigned_by_human: false
execution_authorized: false
implementation_started: false
commit_authorized: false
push_authorized: false

# Task objective
Implement Task Quality Acceptance Gate MVP so that after every completed task the user can understand whether the task actually fulfilled the function it was created for.

# Required user-facing result
The system must show:
* what the task was supposed to do;
* which Acceptance Criteria were declared;
* which criteria were verified;
* which Evidence supports each criterion;
* what is PASS / PASS_WITH_WARNINGS / BLOCKED / NOT_ENOUGH_EVIDENCE;
* what remains UNKNOWN / NOT_RUN;
* known limits;
* required human decision: ACCEPT_RESULT / NEEDS_CHANGES / REJECT_RESULT.

# Allowed implementation paths after future execution authorization only
* aos/docs/workflow/task-quality-acceptance-gate.md
* aos/docs/workflow/task-quality-check-package-contract.md
* aos/templates/tasks/task-quality-acceptance-criteria-template.md
* aos/templates/tasks/task-quality-evidence-matrix-template.md
* aos/templates/tasks/user-facing-acceptance-summary-template.md
* aos/templates/tasks/human-result-acceptance-checkpoint-template.md
* aos/templates/tasks/task-quality-check-package-template.md
* aos/schemas/task-quality-check-package.schema.json
* aos/tools/optional/task_quality_checker.py
* aos/scripts/aos_task_quality.py
* tests/task_quality/**
* tests/fixtures/task_quality/**
* aos/reports/examples/task-quality/**
* reports/aos-farm-443-*.md
* reports/aos-farm-443-*.json
* reports/human-checkpoints/aos-farm-443-*.md

# Forbidden paths
* 00_AOS_Core_Control.md
* 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
* 02_AOS_Governance_Control_Module_and_Safety_Rules.md
* 03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
* agentos/**
* .github/**
* release/**

# Forbidden behavior
* no runner;
* no auto-execution;
* no auto-approval;
* no lifecycle mutation;
* no release;
* no production readiness claim;
* no merge;
* no force push;
* no tag push;
* no destructive cleanup;
* no SQLite implementation;
* no RAG-light implementation;
* no protected/canonical changes;
* no commit without human commit authorization;
* no push without human push authorization.

# Implementation sequence after future authorization
* 443.4 Task Quality Gate Architecture Doc
* 443.5 Templates
* 443.6 Package Contract / Optional Schema
* 443.7 Read-only Checker MVP
* 443.8 Fixtures
* 443.9 Tests
* 443.10 Dogfood on AOS-FARM.442
* 443.11 Task Registry / Queue Integration Note
* 443.12 Final Review
* 443.13 Commit Authorization Package
* 443.14 Human Commit Authorization
* 443.15 Commit Execution
* 443.16 Push Authorization Package
* 443.17 Human Push Authorization
* 443.18 Push Execution
* 443.19 Remote Baseline Closure
* 443.20 Stage Closure Summary

# Boundary
* Task Quality PASS is not approval.
* Task Quality PASS is not task completion.
* Task Quality PASS is not commit authorization.
* Task Quality PASS is not push authorization.
* Evidence is not approval.
* Human review remains required.
