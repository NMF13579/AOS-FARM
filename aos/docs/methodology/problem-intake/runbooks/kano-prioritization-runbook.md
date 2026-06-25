# Kano Prioritization

**Status:** DRAFT_METHOD  
**Runtime implementation:** not authorized  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## Purpose

Classify requirements into Must-be, Performance, and Delighter categories for MVP slicing.

## When To Use

MVP, tight deadline, prioritization pressure.

## When Not To Use

When there are very few requirements or time/budget is unconstrained.

## User-Facing Explanation

"Давайте отделим то, без чего продукт вообще не сможет работать, от того, что можно добавить позже."

## One-Question-at-a-Time Flow

Agent asks functional and dysfunctional questions for candidate features. One question per turn.

## Required Questions

Functional question (how user feels if feature is present).
Dysfunctional question (how user feels if feature is missing).

## Follow-Up Triggers

Ambiguous answers that don't fit Kano classes.

## Completion Criteria

Target features are classified into MVP or backlog.

## Output Fields

- requirement
- kano_class
- mvp_candidate
- backlog_candidate
- priority_rationale
- human_decision_required

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
