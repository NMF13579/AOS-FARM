# JTBD

**Status:** DRAFT_METHOD  
**Runtime implementation:** not authorized  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## Purpose

Reframe solution-shaped requests into jobs, situations, motivations, and expected outcomes.

## When To Use

Solution named without problem, such as CRM or tracker.

## When Not To Use

When the problem and motivations are clearly stated, rather than just a solution.

## User-Facing Explanation

"Давайте отойдём от конкретного решения (например, CRM) и опишем саму работу (Job), которую система должна выполнить для пользователя."

## One-Question-at-a-Time Flow

Agent probes for situation, motivation, outcome, and role-specific jobs. One question per turn.

## Required Questions

JTBD formula:
- when;
- I want;
- so that;
Questions regarding pain, gain, comfort, anxiety, and role-specific jobs.

## Follow-Up Triggers

Missing motivation, missing specific outcome.

## Completion Criteria

JTBD formula is fully constructed with pains and gains.

## Output Fields

- role
- situation
- motivation
- expected_outcome
- pain
- gain
- anxiety
- negative_constraints_candidates

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
