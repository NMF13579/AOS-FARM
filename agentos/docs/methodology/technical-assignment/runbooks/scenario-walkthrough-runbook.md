# Scenario Walkthrough

**Status:** DRAFT_METHOD  
**Runtime implementation:** not authorized  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## Purpose

Walk through a real or representative scenario step by step to reveal hidden workflow details, edge cases, and error states.

## When To Use

User describes real workflow, legacy process, or current workaround.

## When Not To Use

Purely greenfield ideas without analogous real-world operations.

## User-Facing Explanation

"Давайте пошагово разберем один реальный случай из вашей практики, чтобы увидеть скрытые детали и ошибки."

## One-Question-at-a-Time Flow

Agent asks for a last real case prompt. Then walks through the step-by-step flow. One question per turn.

## Required Questions

Last real case prompt.
Actor/action/data/result structure for each step.
Error states and onboarding signals.

## Follow-Up Triggers

Missing steps, skipped data inputs, unclear actor actions.

## Completion Criteria

Scenario is fully mapped from start to result including error states.

## Output Fields

- scenario_name
- actors
- steps
- data_used
- decisions
- failures
- edge_cases
- acceptance_candidates

## Skip / Return Behavior

User may skip and return later. Skip is recorded.

## Safety Boundaries

Runbook completion ≠ PASS.
Runbook completion ≠ approval.
Runbook output ≠ execution authorization.
User answer ≠ approval.
Human approval cannot be simulated.

## Final Rule

This runbook does not authorize execution or approval.
