# Construction Intake Extension

**Domain:** construction  
**Extension status:** ACTIVE_DOMAIN_EXTENSION  
**Extends:** technical-assignment-agent-workflow  
**May override core:** false  
**May weaken core:** false  
**Execution authorized:** false  

---

## 1. Когда использовать

Использовать extension, если проект затрагивает:

- construction sites;
- contractors;
- materials;
- estimates;
- project documentation;
- permits;
- work stages;
- inspections;
- defects;
- schedules;
- safety incidents.

---

## 2. Серые зоны

Строительные проекты требуют внимания к:

- responsibility boundaries;
- contractors and subcontractors;
- safety;
- documentation;
- permits;
- estimates;
- material tracking;
- change orders;
- inspection records;
- photo evidence;
- deadlines and dependencies.

---

## 3. Domain-Specific Questions

1. Какой объект или project управляется?
2. Кто contractors и responsible parties?
3. Какие work stages есть?
4. Какая documentation обязательна?
5. Какие approvals нужны до начала работ?
6. Какие materials нужно отслеживать?
7. Какие defects или incidents нужно фиксировать?
8. Кто может approve completion?
9. Какие photos или documents должны быть приложены?
10. Какие actions должны логироваться?

---

## 4. Construction Data Discovery

Возможные data objects:

- Construction Project;
- Site;
- Contractor;
- Work Stage;
- Estimate;
- Material;
- Permit;
- Inspection;
- Defect;
- Photo Evidence;
- Act / Completion Record;
- Audit Log.

---

## 5. Access / Permissions

Типичные roles:

- Owner;
- Project Manager;
- Contractor;
- Subcontractor;
- Inspector;
- Accountant;
- Admin.

Sensitive actions:

- approving work completion;
- changing estimates;
- changing deadlines;
- deleting evidence;
- approving payment;
- modifying permits.

---

## 6. Negative Constraints

Система не должна:

- delete inspection evidence silently;
- allow unauthorized estimate changes;
- approve completion without authorized reviewer;
- hide defects;
- modify audit trail;
- treat contractor self-report as final approval.

---

## 7. Acceptance Criteria

Acceptance Criteria должны включать:

- stage status tracking;
- evidence attachment;
- approval trail;
- estimate change history;
- defect workflow;
- role-based access verification.

---

## 8. Human Decisions Required

- Кто approves work completion?
- Кто может modify estimates?
- Кто может close defects?
- Какая documentation обязательна?
- Какие actions require photo evidence?
- Какие events trigger notifications?

---

## 9. Final Status

```yaml
extension_applied: true
domain: construction
domain_review_required: true
safety_review_required: true
execution_authorized: false
```
