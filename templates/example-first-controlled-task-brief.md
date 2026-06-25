# Task Brief: Example First Controlled Task

> **Как использовать этот шаблон (How to use):** 
> 1. Скопируйте этот текст. 
> 2. Замените ID задачи и цель на свои. 
> 3. Передайте агенту как первую инструкцию.

**Task ID / Name**: AOS-FARM.EXAMPLE-01 — Add Documentation Note
**Mode**: Controlled documentation implementation + verification + DRAFT commit authorization preparation.
**Repository**: NMF13579/AOS-FARM
**Branch**: dev

## Context
This is an example brief demonstrating a safe, small, bounded task for a non-programmer interacting with the AOS-FARM system.

## Goal
Add a single explanatory note to a specific user guide document.

## Scope
Allowed to modify exactly one target documentation file and create the required reports/checkpoints.

## Rules
- You must read `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and `02_AOS_Governance_Control_Module_and_Safety_Rules.md` before proceeding.
- **PASS ≠ approval**
- **Evidence ≠ approval**
- **CI PASS ≠ approval**
- **UNKNOWN ≠ OK**
- **NOT_RUN ≠ PASS**
- **Human approval cannot be simulated.**

## Required Behavior
1. Verify the Git baseline.
2. Add the note to the document.
3. Run `git diff` to verify only the target file was changed.
4. Prepare the Evidence report and Verification report.
5. Prepare the DRAFT Human Commit Authorization checkpoint.
6. Stop and await human review.

## Non-Goals
- Do not refactor other documentation.
- Do not set up CI/CD workflows.
- Do not add autonomous runners.

## Validation
Run read-only `git status` and `git diff` to prove no protected/canonical files or workflow files were altered.

## Expected Final Report
Return a summary containing final status, files modified, validation results, and next safe step.

## Final Rule
This task may prepare a DRAFT commit authorization checkpoint, but it must not perform commit or push. Human Commit Authorization remains required before any commit.
