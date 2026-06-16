# Adaptive Elicitation Method Selector

**Status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT  
**Scope:** method selection logic  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## 1. Purpose

This file defines how the agent selects an interview methodology based on user signals.
User selects the entry route.
The methodology selects the depth.
The agent proposes the interview method.
The user may accept, skip, or return later.

## 2. Adaptive Elicitation Router

```yaml
adaptive_elicitation_router:
  input:
    - user_answer
    - current_route
    - current_section
    - detected_signals
    - skipped_sections
    - unknowns
    - risk_flags

  output:
    - proposed_method
    - reason
    - confidence
    - user_confirmation_required
    - allowed_next_actions
```

## 3. Method Selection Confidence

```yaml
method_selection_confidence:
  HIGH: clear_signal
  MEDIUM: likely_signal
  LOW: ambiguous_signal

  if_LOW:
    action: parking_lot_candidate
    user_confirmation_required: false
    continue_base_intake: true
```

## 4. Selector Table

| Signal | Recommended Method | Runbook |
|---|---|---|
| unclear problem or vague vision | Five Whys | runbooks/five-whys-runbook.md |
| solution named without problem, such as CRM or tracker | JTBD | runbooks/jtbd-runbook.md |
| abstract goal needs concrete implementation level | Why-How Laddering | runbooks/why-how-laddering-runbook.md |
| user describes real workflow, legacy process, or current workaround | Scenario Walkthrough | runbooks/scenario-walkthrough-runbook.md |
| sensitive data, fear, security, privacy, SLA, compliance, high impact | Negative Requirements | runbooks/negative-requirements-runbook.md |
| MVP, tight deadline, prioritization pressure | Kano Prioritization | runbooks/kano-prioritization-runbook.md |
| many entities, roles, permissions, lifecycle states, or data flows | Entity-Process Traversal | runbooks/entity-process-traversal-runbook.md |

## 5. Conflict Handling

```yaml
method_conflict_handling:
  if_multiple_HIGH_confidence_methods:
    agent_must_explain_detected_signals: true
    agent_must_recommend_order: true
    user_confirmation_required: true

  if_methods_conflict:
    agent_must_not_choose_silently: true
    agent_must_present_tradeoff: true
    user_confirmation_required: true

  if_signal_is_ambiguous:
    record_as_parking_lot_candidate: true
    continue_base_intake: true
```

## 6. Safety Invariants

```text
Method selection ≠ approval.
Method selection ≠ PASS.
Runbook completion ≠ approval.
Runbook completion ≠ PASS.
Method confidence ≠ Evidence.
User confirmation of method ≠ implementation approval.
Runbook is an interview aid, not Source of Truth above canonical AOS sources.
```

## 7. Relationship to Rules

- Relationship to one-question-at-a-time applies to all methods.
- Relationship to Skip / Return Protocol applies to all methods.

## 8. Anti-Anchoring Control

```yaml
anchoring_effect_control:
  trigger:
    - user_names_specific_technology_first
    - user_names_specific_number_first
    - user_names_specific_solution_first
    - user_declares_architecture_before_problem
    - user_says_we_need_exact_feature_before_problem_is_clear

  agent_must:
    - record_as_user_mentioned_hint
    - not_treat_as_requirement
    - not_treat_as_acceptance_criterion
    - not_treat_as_architecture_decision
    - ask_problem_reframing_question

  anchor_statuses:
    - USER_MENTIONED_HINT
    - UNVALIDATED_ANCHOR
    - CANDIDATE_REQUIREMENT
    - NEEDS_HUMAN_REVIEW
```

Examples:
```text
Оставим пока в стороне “100 полей”. Что случится в реальной работе, если этих данных вообще не будет?
```

```text
Пока не фиксирую CRM как требование. Сначала уточню: какую проблему должна решить эта система?
```

Invariants:
```text
Initial solution anchor ≠ requirement.
Initial number anchor ≠ acceptance criterion.
Initial technology anchor ≠ architecture decision.
User-mentioned architecture ≠ approved architecture.
User-mentioned feature ≠ approved scope.
```

## 9. Method Switch Explanation

```yaml
method_switch_explanation:
  required_before_switch: true
  abrupt_switch_forbidden: true

  must_include:
    - what_user_said
    - why_it_changes_interview_route
    - what_next_method_will_collect
    - user_choice_to_switch_or_continue
```

User-facing example:
```text
Вы упомянули внешних пользователей — это меняет требования к доступу. Я предлагаю один блок вопросов об этом, чтобы разработчик понимал, кто что может видеть и менять. Переключиться сейчас или сначала завершить текущий блок?
```

Rule:
```yaml
method_switch_confirmation:
  required_for_mid_session_switch: true
  not_required_for_next_question_inside_current_method: true
```

## 10. Final Rule

This document does not authorize code implementation, runtime method selection, probing engine implementation, validator implementation, execution, commit, push, deploy, release, production use, or approval simulation.

