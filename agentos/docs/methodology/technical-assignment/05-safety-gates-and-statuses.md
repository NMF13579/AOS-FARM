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
```

Policy:

```yaml
if_any_critical_failure: BLOCKED_FOR_SPEC_FINALIZATION
ready_for_execution: false
execution_authorized: false
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

PASS по этому checklist не является approval.
