# 02 — Agent Contract

**Document status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT  
**Contract format:** Markdown with embedded YAML contract  
**Methodology ID:** TECHNICAL_ASSIGNMENT_AGENT_WORKFLOW  
**Contract version:** 1.0  
**Derived from:** `01-human-methodology.md`  
**Validator available:** false  
**Implementation authorized:** false  
**Execution authorized:** false  

---

## 1. Назначение

Этот документ содержит machine-readable contract агента в формате Markdown.

Файл остаётся `.md`, чтобы:

- его было удобно читать человеку;
- его можно было редактировать как обычный документ;
- внутри можно было держать YAML-блоки;
- агент мог извлекать строгие rules из fenced blocks;
- пакет оставался Markdown-first.

Этот документ является machine-readable projection документа `01-human-methodology.md`.

Он не является самостоятельным Source of Truth и не может добавлять новые permissions.

---

## 2. Authority Model

```yaml
authority_model:
  contract_role: machine_readable_projection
  semantic_authority: "01-human-methodology.md"
  may_add_new_permissions: false
  may_weaken_human_methodology: false
  may_override_human_methodology: false
  if_conflict_with_human_methodology:
    status: HUMAN_REVIEW_REQUIRED
    execution_authorized: false
    agent_must_not_choose_interpretation: true
```

---

## 3. Source Precedence

```yaml
source_precedence:
  this_document: below_canonical_aos_control_sources
  higher_authority:
    - 00_AOS_Core_Control.md
    - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
    - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  if_conflict: canonical_sources_win
  this_document_may_override_canonical_sources: false
```

---

## 4. Default Status

```yaml
default_status:
  approval_status: NOT_APPROVED
  ready_for_execution: false
  execution_authorized: false
  implementation_authorized: false
  commit_authorized: false
  push_authorized: false
  deploy_authorized: false
  production_use_authorized: false
  stack_selected: false
  final_database_schema_created: false
  risk_profile_assigned: false
```

---

## 5. Allowed Actions

```yaml
allowed_actions:
  - select_intake_mode
  - accept_existing_specification
  - conduct_express_intake
  - conduct_full_intake
  - record_problem_interview_skip
  - collect_user_vision
  - collect_problem_evidence
  - collect_data_discovery
  - collect_information_flow
  - collect_access_permissions
  - collect_implementation_hints
  - collect_constraints
  - collect_negative_constraints
  - collect_acceptance_criteria
  - apply_domain_extension
  - create_project_spec_draft
  - create_requirements_draft
  - create_requirements_checklist_draft
  - create_problem_interview_report
  - recommend_handoff
  - list_human_decisions_required
```

---

## 6. Forbidden Actions

```yaml
forbidden_actions:
  - authorize_implementation
  - authorize_execution
  - create_execution_package
  - create_commit_authorization
  - create_push_authorization
  - authorize_deploy
  - authorize_production_use
  - select_stack
  - approve_stack
  - make_final_architecture_decision
  - create_final_database_schema
  - assign_risk_profile
  - assign_low_risk_fast
  - create_canonical_project_spec_md
  - set_approved_status_on_behalf_of_human
  - treat_user_vision_as_approved_requirement
  - treat_implementation_hint_as_architecture_decision
  - treat_data_discovery_as_final_database_schema
  - treat_problem_interview_skip_as_blocked
```

---

## 7. Intake Modes

```yaml
intake_modes:
  EXPRESS:
    purpose: lean_draft_for_small_project_or_aprobation
    allowed: true
    output: lean_project_spec_draft
    execution_authorized: false
    minimum_required_fields:
      - user_vision
      - goal
      - users
      - minimum_data_discovery
      - sensitive_data_status
      - key_data_create_read_update_context
      - mvp
      - negative_constraints
      - acceptance_signal
      - unknowns
      - final_status

  FULL:
    purpose: deep_intake_for_serious_or_risky_project
    allowed: true
    output: stronger_project_spec_draft
    execution_authorized: false
    minimum_required_fields:
      - user_vision
      - data_discovery
      - information_flow
      - access_permissions
      - constraints
      - negative_constraints
      - human_in_the_loop_points
      - sensitive_data_status
      - acceptance_criteria
      - mvp
      - unknowns
      - contradictions
      - human_decisions_required
      - final_status

  EXISTING_SPEC_REVIEW:
    purpose: structure_existing_user_material
    allowed: true
    output: structured_review_and_draft
    execution_authorized: false
    required_actions:
      - accept_user_native_language
      - extract_user_vision
      - extract_requirements
      - extract_data_discovery
      - extract_constraints
      - identify_unknowns
      - identify_contradictions
    forbidden_actions:
      - treat_existing_spec_as_approved
      - move_to_execution
```

---

## 8. Required Sections for `PROJECT_SPEC.draft.md`

```yaml
required_sections_for_project_spec_draft:
  - source_status
  - user_vision
  - data_discovery
  - information_flow
  - access_permissions
  - problem_evidence_if_applicable
  - optional_current_workflow_if_applicable
  - requirements_draft
  - implementation_hints
  - negative_constraints
  - acceptance_criteria
  - mvp
  - unknown_open_questions
  - contradictions
  - human_decisions_required
  - final_status
```

---

## 9. Data Discovery Contract

```yaml
data_discovery:
  required: true
  final_database_schema_allowed: false
  required_outputs:
    - data_inventory
    - sensitive_data_status
    - information_flow
    - access_permissions
    - audit_trail_need
  if_missing:
    status: BLOCKED_FOR_SPEC_FINALIZATION
    execution_authorized: false
```

---

## 10. Information Flow Contract

```yaml
information_flow:
  required: true
  default_human_review_needed_for_high_impact_actions: true
  if_missing:
    status: BLOCKED_FOR_SPEC_FINALIZATION
    execution_authorized: false
```

---

## 11. Access / Permissions Contract

```yaml
access_permissions:
  required_when:
    - multi_user_system
    - sensitive_data_present
    - external_users_present
    - role_based_access_needed
  if_required_and_missing:
    status: BLOCKED_FOR_SPEC_FINALIZATION
    execution_authorized: false
```

---

## 12. Implementation Hints Contract

```yaml
implementation_hints:
  allowed: true
  allowed_statuses:
    - USER_MENTIONED
    - AGENT_INFERENCE
    - CANDIDATE_REQUIREMENT
    - NOT_EVALUATED
    - NEEDS_HUMAN_REVIEW
  forbidden_statuses:
    - APPROVED_REQUIREMENT
    - SELECTED_STACK
    - FINAL_ARCHITECTURE
    - READY_FOR_EXECUTION
    - STACK_APPROVED
    - IMPLEMENTATION_CHOICE
```

---

## 13. Critical Failures

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

critical_failure_policy:
  if_any_critical_failure: BLOCKED_FOR_SPEC_FINALIZATION
  ready_for_execution: false
  execution_authorized: false
```

---

## 14. Domain Extension Policy

```yaml
domain_extension_policy:
  may_add_questions: true
  may_add_required_data_fields: true
  may_add_constraints: true
  may_add_safety_gates: true
  may_add_human_review_requirements: true

  may_override_core: false
  may_weaken_core: false
  may_authorize_execution: false
  may_authorize_implementation: false
  may_assign_risk_profile: false
  may_select_stack: false
  may_finalize_database_schema: false

  if_conflict_with_core:
    status: HUMAN_REVIEW_REQUIRED
    execution_authorized: false
```

---

## 15. Final Status Required Fields

```yaml
final_status_required_fields:
  - artifact_type
  - intake_depth
  - problem_interview_status
  - problem_evidence_level
  - data_discovery_depth
  - information_flow_status
  - access_permissions_status
  - requirements_confidence
  - unknown_count
  - contradiction_count
  - inference_count
  - implementation_hint_count
  - critical_failure_count
  - ready_for_requirements_review
  - ready_for_execution
  - approval_status
  - execution_authorized
  - implementation_authorized
  - commit_authorized
  - push_authorized
  - deploy_authorized
  - production_use_authorized
```

---

## 16. Final Rule

```yaml
final_rule:
  methodology_authorizes_only: technical_assignment_intake_and_draft_creation
  methodology_does_not_authorize:
    - implementation
    - execution
    - commit
    - push
    - deploy
    - release
    - production_use
    - stack_selection
    - risk_profile_assignment
    - final_database_schema
    - lifecycle_promotion
```
