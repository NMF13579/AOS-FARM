# Entity-Process Traversal

**Status:** DRAFT_METHOD  
**Runtime implementation:** not authorized  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## Purpose

Traverse entities, CRUD operations, lifecycle states, events, failure modes, access, audit, and Human review points.

## When To Use

Many entities, roles, permissions, lifecycle states, or data flows.

## When Not To Use

Single simple entity with no states or strict permissions.

## User-Facing Explanation

"Давайте пройдемся по жизненному циклу каждой важной сущности в системе, от ее создания до архивации."

## One-Question-at-a-Time Flow

Agent traverses step by step through the entity lifecycle and properties. One question per turn.

## Required Questions

Entity identification.
CRUD (Create, Read, Update, Delete).
Lifecycle.
Events.
Failure modes.
Relations.
Access / permissions.
Audit.
Human review points.

## Follow-Up Triggers

Missing lifecycle states, missing actors for CRUD.

## Completion Criteria

Core entity matrix is populated.

## Output Fields

- entity_name
- created_by
- read_by
- updated_by
- deleted_or_archived_by
- lifecycle_states
- transitions
- events
- failure_modes
- related_entities
- access_roles
- audit_required
- human_review_required

## Skip / Return Behavior

User may skip and return later. Skip is recorded.

## Safety Boundaries

Entity-Process Traversal ≠ architecture decision.
CRUD Matrix ≠ database schema.
Lifecycle Model ≠ implementation.
Aggregate Candidate ≠ final DDD aggregate.
Event list ≠ event-driven architecture approval.
Traversal coverage ≠ PASS.
Traversal coverage ≠ approval.
Runbook completion ≠ PASS.
Runbook completion ≠ approval.
Runbook output ≠ execution authorization.
User answer ≠ approval.
Human approval cannot be simulated.

## Core Entity Detection

```yaml
entity_classes:
  - CORE_ENTITY
  - SUPPORTING_ENTITY
  - REFERENCE_ENTITY
  - AUDIT_ENTITY
  - EXTERNAL_ENTITY
```

```yaml
core_entity_detection:
  entity_is_core_if:
    - referenced_by_two_or_more_entities
    - participates_in_financial_operation
    - participates_in_medical_operation
    - participates_in_access_critical_operation
    - has_sensitive_data
    - has_complex_lifecycle
    - has_audit_or_approval_requirement
    - is_required_for_primary_user_outcome

  full_traversal_required_for:
    - CORE_ENTITY
    - high_impact_entity
    - sensitive_data_entity
    - entity_with_complex_lifecycle
    - entity_with_permissions
    - entity_with_audit_or_approval_requirement

  lightweight_traversal_allowed_for:
    - REFERENCE_ENTITY
    - static_dictionary
    - low_risk_lookup_table
    - display_only_entity

  agent_must_not_run_full_traversal_on_every_minor_entity: true
```

Examples:
```text
Платёж → full traversal.
Пользователь → full traversal.
Медицинская запись → full traversal.
Справочник городов → lightweight traversal.
Справочник статусов → lightweight traversal, unless it controls lifecycle logic.
```

Invariants:
```text
Reference entity ≠ core entity.
Lookup table ≠ full traversal target by default.
Full traversal only for core/risk entities.
Lightweight traversal ≠ omission.
Entity classification ≠ database schema.
```

## Final Rule

This runbook does not authorize execution or approval.

