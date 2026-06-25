# Five Whys

**Status:** DRAFT_METHOD  
**Runtime implementation:** not authorized  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## Purpose

Find the root problem behind a vague request, symptom, or solution-shaped request.

## When To Use

Unclear problem or vague vision.

## When Not To Use

When the problem is well-defined and structurally validated.

## User-Facing Explanation

"Чтобы мы не решили ложную проблему, я задам несколько уточняющих вопросов «Почему?». Это поможет найти корневую причину."

## One-Question-at-a-Time Flow

Agent asks up to five sequential why questions. One question per turn.
Stop condition when root cause is clear.
Agent must not force exactly five questions if enough evidence is reached earlier.
A shallow answer requires follow-up.

## Required Questions

Why did this problem occur? / Why do you need this? (up to 5 levels deep)

## Follow-Up Triggers

Shallow answers, symptoms instead of causes.

## Completion Criteria

Root cause identified or user indicates limit of their knowledge.

## Output Fields

- initial_statement
- why_chain
- candidate_root_problem
- assumptions
- unknowns
- confidence

## Skip / Return Behavior

User may skip and return later. Skip is recorded.

## Safety Boundaries

Runbook completion ≠ PASS.
Runbook completion ≠ approval.
Runbook output ≠ execution authorization.
User answer ≠ approval.
Human approval cannot be simulated.

## Anti-Anchoring Questions

Five Whys must be used to reduce anchoring when the user starts with a solution, number, technology, feature list, or architecture claim.

```text
Оставим пока в стороне [solution/number/technology]. Что произойдёт в реальной работе, если этого не будет?
```

```text
Какая проблема останется нерешённой, если мы не сделаем [anchor]?
```

```text
Кто пострадает от отсутствия [anchor] и как именно?
```

```yaml
five_whys_anti_anchor_rule:
  if_user_starts_with_solution:
    agent_must_not_accept_solution_as_requirement: true
    agent_must_reframe_to_problem: true
    anchor_must_be_recorded_as_USER_MENTIONED_HINT: true
```

Invariants:
```text
Five Whys output ≠ approved requirement.
Root problem candidate ≠ approval.
Anchor reframing ≠ rejection of user idea.
```

## Five Whys for Grey Zones

Five Whys may be used for grey zones, manual workarounds, vague constraints, and unclear root causes.
The agent must not force exactly five why-questions.
The agent must stop earlier if sufficient evidence appears.

```yaml
five_whys_grey_zone_rule:
  use_when:
    - root_cause_unclear
    - manual_workaround_mentioned
    - generic_constraint_given
    - contradiction_requires_cause_clarification
    - exception_case_has_unclear_trigger

  stop_when:
    - root_cause_candidate_is_clear
    - user_fatigue_signal_detected
    - answer_quality_declines
    - user_requests_skip
    - sufficient_evidence_recorded

  must_not:
    - ask_why_mechanically
    - convert_root_cause_candidate_to_approved_requirement
    - assign_HIGH_confidence_without_evidence
```

Invariants:
```text
Root cause candidate ≠ approved requirement.
Five Whys completion ≠ PASS.
Grey zone explanation ≠ implementation authorization.
```

## Final Rule

This runbook does not authorize execution or approval.

