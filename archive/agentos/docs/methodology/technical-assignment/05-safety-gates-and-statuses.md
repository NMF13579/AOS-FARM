# 05 — Safety Gates и статусы

**Document status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT  
**Scope:** safety gates and status semantics for technical assignment intake  
**Execution authorized:** false  

---

## 1. Core Invariants

```text
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
Human approval cannot be simulated.
Skeleton ≠ implementation.
Scope must not expand without explicit human permission.
Protected/canonical changes require Human checkpoint.
Destructive operations are forbidden by default.
```

---

## 2. Default Status

```yaml
approval_status: NOT_APPROVED
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
commit_authorized: false
push_authorized: false
deploy_authorized: false
production_use_authorized: false
```

---

## 3. Запрещённые status promotions

Агент не должен выдавать:

```text
APPROVED
READY_FOR_EXECUTION
EXECUTION_AUTHORIZED
STACK_SELECTED
STACK_APPROVED
FINAL_ARCHITECTURE
FINAL_DATABASE_SCHEMA
IMPLEMENTATION_CHOICE
```

Эта методология не даёт такого authorization.

---

## 4. Critical Failures

Critical failures сами по себе блокируют spec finalization.

```yaml
critical_failures:
  - missing_data_inventory
  - missing_sensitive_data_check
  - missing_information_flow
  - missing_access_permissions_for_multi_user_or_sensitive_project
  - missing_negative_constraints_for_sensitive_project
  - missing_human_in_the_loop_for_high_impact_action
  - missing_acceptance_criteria
  - unresolved_contradiction_affecting_scope
  - stack_selected_without_human_review
  - final_database_schema_created_inside_tz
  - execution_authorized_inside_tz
  - approved_status_assigned_by_agent
  - intake_started_before_route_selection
  - language_unclear_but_not_asked
  - removed_express_route_still_presented
  - removed_full_route_still_presented
  - problem_interview_skipped_but_marked_completed
  - problem_interview_skipped_but_evidence_marked_high
  - skipped_section_marked_completed
  - skipped_section_hidden_from_draft
  - confidence_increased_from_skipped_section
  - section_completed_from_short_answer
  - generic_answer_marked_completed
  - keyword_match_treated_as_completion
  - traversal_coverage_treated_as_PASS
  - method_selection_treated_as_APPROVAL
  - runbook_completion_treated_as_PASS
  - runbook_completion_treated_as_APPROVAL
  - project_spec_generated_before_blocking_gate_pass
  - initial_solution_anchor_treated_as_requirement
  - initial_number_anchor_treated_as_acceptance_criterion
  - user_mentioned_technology_treated_as_architecture_decision
  - all_methods_completed_treated_as_execution_ready
  - structural_unknown_hidden_from_project_spec
  - skipped_negative_requirements_treated_as_safety_clearance
  - full_traversal_run_on_all_minor_reference_entities
  - core_entity_not_detected_for_sensitive_or_high_impact_data
  - method_switch_without_explanation
  - long_interview_without_mini_summary
  - fatigue_signals_detected_but_no_pause_or_summary_offered
  - contradiction_affecting_scope_safety_access_or_data_hidden
  - unresolved_contradiction_treated_as_ready_for_execution
  - exception_case_treated_as_approved_requirement
  - observation_evidence_treated_as_approval
  - unredacted_sensitive_observation_requested
  - hidden_approval_flow_treated_as_approved_access_model
  - low_confidence_answer_promoted_to_requirement
  - five_whys_forced_mechanically_despite_fatigue_signal
```

Policy:

```yaml
if_any_critical_failure: BLOCKED_FOR_SPEC_FINALIZATION
ready_for_execution: false
execution_authorized: false

fail_closed_result:
  ready_for_execution: false
  execution_authorized: false
  approval_status: NOT_APPROVED
```

---

## 5. Medical и High-Impact Gate

Если проект влияет на пациентов, деньги, юридический статус, personal data, external users или safety-critical operations:

- sensitive data check обязателен;
- Human-in-the-loop по умолчанию обязателен;
- Access / Permissions обязателен;
- audit trail обязателен;
- compliance review обязателен;
- autonomous high-impact decision-making запрещён без Human review.

---

## 6. Final Rule

Safety gates не дают approval на implementation.

Они только предотвращают unsafe draft finalization.

---

## 7. Workflow Statuses

```text
SELECTED_BY_USER
SKIPPED_BY_USER
DEFERRED_BY_USER
BLOCKED_BY_USER_DECISION
RETURNED_TO_SECTION
COMPLETED_LATER
UPDATED_AFTER_SKIP
PARKING_LOT_CANDIDATE
PARTIAL_ANSWER
NEEDS_FOLLOW_UP
UNKNOWN_PRESENT
BLOCKED_FOR_SECTION_COMPLETION
LIGHT
MEDIUM
DEEP
HIGH_RISK
DRAFT_WITH_WARNINGS
USER_MENTIONED_HINT
UNVALIDATED_ANCHOR
CANDIDATE_REQUIREMENT
STRUCTURAL_UNKNOWN
FALSE_COMPLETENESS_RISK
FATIGUE_SIGNAL_DETECTED
MINI_SUMMARY_REQUIRED
CORE_ENTITY
SUPPORTING_ENTITY
REFERENCE_ENTITY
AUDIT_ENTITY
EXTERNAL_ENTITY
LIGHTWEIGHT_TRAVERSAL
FULL_TRAVERSAL
EXCEPTION_CASE_FOUND
ANOMALY_FOUND
HARDEST_CASE_CAPTURED
END_OF_PERIOD_CASE_FOUND
PEAK_LOAD_CASE_FOUND
CONTRADICTION_FOUND
CONTRADICTION_UNRESOLVED
CONTRADICTION_RESOLVED
CONTRADICTION_SCOPE_BLOCKING
CONTRADICTION_SAFETY_BLOCKING
OBSERVATION_EVIDENCE_RECORDED
OBSERVATION_REDACTION_REQUIRED
HIDDEN_APPROVAL_FLOW_FOUND
LOW_CONFIDENCE_ANSWER
DEPTH_PROBING_REQUIRED
```

```text
SKIPPED_BY_USER ≠ COMPLETED.
SKIPPED_BY_USER ≠ PASS.
SKIPPED_BY_USER ≠ approval.
DEFERRED_BY_USER ≠ OK.
COMPLETED_LATER ≠ approval.
UPDATED_AFTER_SKIP ≠ approval.
PARTIAL_ANSWER ≠ COMPLETED.
NEEDS_FOLLOW_UP ≠ PASS.
UNKNOWN_PRESENT ≠ OK.
Short answer ≠ completion.
Generic answer ≠ completion.
Traversal coverage ≠ PASS.
Traversal coverage ≠ approval.
Method selection ≠ PASS.
Method selection ≠ approval.
Method confidence ≠ Evidence.
Runbook completion ≠ PASS.
Runbook completion ≠ approval.
USER_MENTIONED_HINT ≠ requirement.
UNVALIDATED_ANCHOR ≠ acceptance criterion.
CANDIDATE_REQUIREMENT ≠ approved requirement.
STRUCTURAL_UNKNOWN ≠ OK.
FALSE_COMPLETENESS_RISK ≠ PASS.
MINI_SUMMARY_REQUIRED ≠ completion.
CORE_ENTITY classification ≠ database schema.
LIGHTWEIGHT_TRAVERSAL ≠ omission.
FULL_TRAVERSAL ≠ implementation authorization.
EXCEPTION_CASE_FOUND ≠ approved requirement.
ANOMALY_FOUND ≠ implementation instruction.
HARDEST_CASE_CAPTURED ≠ execution readiness.
CONTRADICTION_FOUND ≠ user error.
CONTRADICTION_UNRESOLVED ≠ ready for execution.
CONTRADICTION_RESOLVED ≠ approval.
OBSERVATION_EVIDENCE_RECORDED ≠ approval.
OBSERVATION_REDACTION_REQUIRED ≠ OK.
HIDDEN_APPROVAL_FLOW_FOUND ≠ approved access model.
LOW_CONFIDENCE_ANSWER ≠ requirement.
DEPTH_PROBING_REQUIRED ≠ PASS.
```

If a blocking section is skipped in FULL mode, the agent must not continue as FULL and must not generate PROJECT_SPEC.draft.md until the section is completed or mode is changed.

The agent must not start intake before language and mode routing are complete.
