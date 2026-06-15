# 07 — Consistency Checklist

**Document status:** ACTIVE_MANUAL_CHECKLIST  
**Scope:** ручная проверка согласованности до появления validator  
**Validator available:** false  
**Execution authorized:** false  

---

## 1. Назначение

Этот checklist является ручным binding-механизмом пакета.

Он проверяет, что:

- `01-human-methodology.md` и `02-agent-contract.yaml` не разошлись;
- Domain Extensions не ослабляют core;
- draft artifacts не заявляют approval;
- execution authorization не создаётся.

---

## 2. 01 ↔ 02 Binding Checklist

| Check | Status |
|---|---|
| `methodology_id` совпадает в 01 и 02 | PASS / FAIL / UNKNOWN |
| 02 отмечен как machine-readable projection документа 01 | PASS / FAIL / UNKNOWN |
| 02 не добавляет permissions, отсутствующие в 01 | PASS / FAIL / UNKNOWN |
| 02 не ослабляет constraints из 01 | PASS / FAIL / UNKNOWN |
| 02 не override 01 | PASS / FAIL / UNKNOWN |
| Conflict policy = HUMAN_REVIEW_REQUIRED | PASS / FAIL / UNKNOWN |

Если любой пункт = `FAIL`:

```yaml
consistency_status: BLOCKED_FOR_HUMAN_REVIEW
execution_authorized: false
```

---

## 3. Core Safety Checklist

| Check | Status |
|---|---|
| `execution_authorized` всегда false | PASS / FAIL / UNKNOWN |
| `implementation_authorized` всегда false | PASS / FAIL / UNKNOWN |
| `commit_authorized` всегда false | PASS / FAIL / UNKNOWN |
| `push_authorized` всегда false | PASS / FAIL / UNKNOWN |
| `READY_FOR_EXECUTION` не является allowed output | PASS / FAIL / UNKNOWN |
| `APPROVED` не назначается агентом | PASS / FAIL / UNKNOWN |
| Data Discovery не становится final database schema | PASS / FAIL / UNKNOWN |
| Implementation Hints не становятся architecture decisions | PASS / FAIL / UNKNOWN |
| User Vision не становится approved requirement | PASS / FAIL / UNKNOWN |
| Current Workflow optional, а не mandatory | PASS / FAIL / UNKNOWN |
| Critical failures работают fail-closed | PASS / FAIL / UNKNOWN |

---

## 4. Domain Extension Checklist

| Check | Status |
|---|---|
| Extension содержит `may_override_core: false` | PASS / FAIL / UNKNOWN |
| Extension содержит `may_weaken_core: false` | PASS / FAIL / UNKNOWN |
| Extension не authorizes execution | PASS / FAIL / UNKNOWN |
| Extension не authorizes implementation | PASS / FAIL / UNKNOWN |
| Extension не select stack | PASS / FAIL / UNKNOWN |
| Extension не finalize database schema | PASS / FAIL / UNKNOWN |
| Extension добавляет только questions, constraints, data fields, gates или Human review requirements | PASS / FAIL / UNKNOWN |

Если любой пункт = `FAIL`:

```yaml
domain_extension_status: BLOCKED_FOR_HUMAN_REVIEW
execution_authorized: false
```

---

## 5. Final Checklist Status

Allowed outcomes:

```text
CONSISTENCY_PASS
CONSISTENCY_PASS_WITH_WARNINGS
CONSISTENCY_FAIL
CONSISTENCY_UNKNOWN_BLOCKED
```

Final rule:

```text
Consistency PASS не authorizes implementation, execution, commit, push, deploy или production use.
```
