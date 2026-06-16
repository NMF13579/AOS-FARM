# Why-How Laddering

**Status:** DRAFT_METHOD  
**Runtime implementation:** not authorized  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## Purpose

Move between abstract goals and concrete actions to find the correct requirement level.

## When To Use

Abstract goal needs concrete implementation level.

## When Not To Use

When requirements are already at the exact target level.

## User-Facing Explanation

"У нас есть абстрактная цель. Давайте разберем, как именно мы будем её достигать, чтобы найти точный уровень требований."

## One-Question-at-a-Time Flow

Agent asks questions to move up (WHY) or down (HOW) the ladder. One question per turn.

## Required Questions

WHY direction questions.
HOW direction questions.
Target middle level questions.

## Follow-Up Triggers

Answers that are too abstract or too granular (implementation details).

## Completion Criteria

Target middle requirement level is reached.

## Output Fields

- abstract_goal
- concrete_actions
- selected_requirement_level
- implementation_hints
- unknowns

## Skip / Return Behavior

User may skip and return later. Skip is recorded.

## Safety Boundaries

Implementation detail is not architecture approval.
Runbook completion ≠ PASS.
Runbook completion ≠ approval.
Runbook output ≠ execution authorization.
User answer ≠ approval.
Human approval cannot be simulated.

## Final Rule

This runbook does not authorize execution or approval.
