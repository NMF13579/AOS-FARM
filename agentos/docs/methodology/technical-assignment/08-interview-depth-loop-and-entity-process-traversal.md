# Interview Depth Loop and Entity-Process Traversal

**Status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT  
**Scope:** interview depth, traversal, scaling  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## 1. Purpose

The purpose of interview depth is to ensure requirements are not just recorded, but analyzed for completeness, edge cases, risks, and lifecycle stages before being accepted into the draft.

## 2. Invariants

```text
PASS ≠ approval.
Evidence ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
SKIPPED_BY_USER ≠ COMPLETED.
SKIPPED_BY_USER ≠ PASS.
DEFERRED_BY_USER ≠ OK.
Short answer ≠ completion.
Generic answer ≠ completion.
User Vision ≠ Problem Evidence.
Keyword match ≠ completion.
Traversal coverage ≠ PASS.
Traversal coverage ≠ approval.
Human approval cannot be simulated.
```

Deep Interview = sequential depth, not questionnaire volume.

## 3. One-Question-at-a-Time Rule

```yaml
one_question_at_a_time:
  one_primary_question_per_turn: true
  wait_for_user_answer_before_next_question: true
  long_questionnaire_dump_forbidden: true
  multiple_independent_questions_per_turn_forbidden: true
```

Allowed exceptions:

```yaml
allowed_multi_option_turns:
  - language_selection
  - route_selection
  - problem_interview_offer
  - explicit_user_requested_full_question_list
```

## 4. Interview Depth Loop

```yaml
interview_depth_loop:
  after_each_user_answer:
    - classify_answer_depth
    - detect_missing_slots
    - detect_unknowns
    - detect_risks
    - detect_contradictions
    - detect_follow_up_need
    - update_section_status
    - decide_next_question_or_pause
```

## 5. Entity-Process Traversal

```text
Entity
→ Create
→ Read
→ Update
→ Delete / Archive
→ Lifecycle States
→ State Transitions
→ Events
→ Failure Modes
→ Relations
→ Access / Permissions
→ Audit
→ Human Review Points
```

## 6. Adaptive Internal Depth Scaling

```yaml
adaptive_depth_scaling:
  user_facing_express_mode: false
  internal_depth_scaling: true

  depth_levels:
    - LIGHT
    - MEDIUM
    - DEEP
    - HIGH_RISK

  scale_up_triggers:
    - sensitive_data_present
    - external_users_present
    - multi_tenant_present
    - ai_or_rag_present
    - medical_or_legal_or_financial_context
    - high_impact_actions_present
    - integrations_present
    - role_count_greater_than_2
    - entity_count_greater_than_2
    - lifecycle_complexity_present
    - unclear_problem_or_vision
```

If scale is unclear, default to MEDIUM.
If sensitive data, AI/RAG, multi-tenancy, medical, finance, legal, external users, or high-impact actions are present, minimum depth is HIGH_RISK.

## 7. Completion Gates

- Data Discovery completion gate
- Problem Interview completion gate
- Skip / Return integration

## 8. Future Probing Engine Boundary

```yaml
probing_engine_boundary:
  runtime_implementation_authorized: false
  advisory_only_if_implemented_later: true
  may_suggest_next_question: true
  may_detect_missing_slots: true
  may_detect_partial_answers: true
  may_detect_candidate_unknowns: true
  may_not_emit_PASS: true
  may_not_emit_APPROVED: true
  may_not_authorize_completion: true
  may_not_authorize_execution: true
  may_not_override_markdown_contract: true
  may_not_treat_keyword_match_as_completion: true
```

## 9. Required Draft Visibility

The draft must expose interview depth status, missing slots, and traversal coverage explicitly.

## 10. Critical Failures

```text
- section_completed_from_short_answer
- generic_answer_marked_completed
- keyword_match_treated_as_completion
- traversal_coverage_treated_as_PASS
```

## 11. Interview Fatigue Control

```yaml
interview_fatigue_control:
  agent_must_track_progress: true
  agent_must_show_periodic_mini_summaries: true
  agent_must_offer_pause_after_long_sequence: true
  agent_must_not_continue_deep_drill_indefinitely: true

  mini_summary_required_after_questions: 5_to_7

  mini_summary_must_include:
    - collected_facts
    - current_assumptions
    - current_UNKNOWN
    - next_reasonable_block
    - user_confirmation_or_correction

  fatigue_signals:
    - short_or_one_word_answers
    - user_says_later
    - user_says_tired
    - repeated_unknown
    - repeated_skip
    - declining_answer_quality

  if_fatigue_detected:
    agent_must:
      - summarize_collected_information
      - show_remaining_sections
      - offer_pause_or_continue
      - preserve_return_points
```

Пример для пользователя:
```text
Из того что вы рассказали: система работает с медицинскими данными, есть три роли, MVP нужен через 6 недель. Сейчас главный UNKNOWN — кто имеет право видеть и менять данные пациента. Это верно? Дальше уточню доступы.
```

## 12. Draft State Tracking

```text
PROJECT_SPEC.draft.md = working Source of Truth during intake.
JSON State, if introduced later = derived/cache only.
Hidden state ≠ Evidence.
Hidden state ≠ approval.
```

```yaml
draft_state_tracking:
  before_starting_new_method:
    agent_must_review_current_project_spec_draft: true

  after_each_phase:
    agent_must_update_visible_draft_sections:
      - collected_facts
      - assumptions
      - UNKNOWN
      - skipped_sections
      - return_points
      - selected_methods
      - developer_warnings

  json_state_authorized_now: false
  json_state_if_added_later: derived_only
  hidden_state_is_evidence: false
  hidden_state_is_approval: false
```

## 13. False Completeness Control

```yaml
false_completeness_control:
  end_of_session_gap_scan_required: true
  method_completion_is_not_total_completion: true
  all_runbooks_completed_is_not_execution_readiness: true

  agent_must_surface:
    - not_discussed_but_possibly_relevant
    - structural_UNKNOWN
    - hidden_domain_risks
    - assumptions_that_may_be_wrong
    - areas_requiring_human_review
```

Invariants:
```text
All methods completed ≠ execution-ready.
All questions answered ≠ approval.
No visible UNKNOWN ≠ no hidden risk.
Method coverage ≠ requirements completeness.
Interview completion ≠ implementation authorization.
```

## 14. Final Rule

This document does not authorize code implementation, runtime implementation, validators, CI workflows, execution, commit, push, deploy, release, production use, stack selection, Risk Profile assignment, final database schema, lifecycle promotion, or approval simulation.

