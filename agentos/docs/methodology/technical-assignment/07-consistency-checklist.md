# 07 — Consistency Checklist

**Document status:** ACTIVE_MANUAL_CHECKLIST  
**Scope:** ручная проверка согласованности до появления validator  
**Validator available:** false  
**Execution authorized:** false  

---

## 1. Назначение

Этот checklist является ручным binding-механизмом пакета.

Он проверяет, что:

- `01-human-methodology.md` и `02-agent-contract.md` не разошлись;
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
| Bridge output остаётся candidate input only | PASS / FAIL / UNKNOWN |
| Task Brief material from bridge remains candidate-only | PASS / FAIL / UNKNOWN |
| Open questions remain UNKNOWN / HUMAN_REVIEW_REQUIRED | PASS / FAIL / UNKNOWN |
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

## 5. Session Entry Checklist

- Any non-empty user message starts the session.
- Explicit start word is not required.
- Agent detects language or asks for it.
- Agent greets user before intake.
- Agent presents only two initial routes: Interview and Existing Spec Review.
- User-facing EXPRESS route is not presented.
- User-facing FULL route is not presented.
- If Interview is selected, agent offers Problem Interview first.
- Problem Interview offer explains why it matters.
- Problem Interview offer has exactly two options: start or skip and return later.
- Skipped Problem Interview is recorded as SKIPPED_BY_USER.
- Skipped Problem Interview is not marked completed.
- Skipped Problem Interview cannot produce HIGH problem evidence.
- User can return to skipped sections later.

---

## 6. Skip / Return Checklist

- User may skip any intake section.
- Every skip must be recorded.
- Skipped sections are not completed.
- Skipped sections are not PASS.
- Skipped sections are visible in PROJECT_SPEC.draft.md.
- User may return to skipped sections later.
- Return updates section status.
- Return triggers confidence recalculation.
- Blocking skip in FULL blocks FULL continuation.
- Blocking skip in FULL blocks PROJECT_SPEC.draft.md.
- EXPRESS may continue with warnings after skip.
- EXISTING_SPEC_REVIEW may record missing sections as gaps.

---

## 7. Interview Depth and Method Checklist

- Agent asks one primary question per turn.
- Agent does not dump long questionnaires.
- Interview depth scales automatically.
- Adaptive Elicitation Method Selector exists.
- Each interview method has a separate runbook file.
- Method selection is not PASS.
- Method selection is not approval.
- Runbook completion is not PASS.
- Runbook completion is not approval.
- Entity-Process Traversal is used for data/process depth.
- Traversal coverage is not PASS.
- Traversal coverage is not approval.
- PROJECT_SPEC.draft.md exposes Interview Entry Status.
- PROJECT_SPEC.draft.md exposes Method Selection Status.
- PROJECT_SPEC.draft.md exposes Interview Depth Status.
- PROJECT_SPEC.draft.md exposes Entity-Process Traversal Summary.
- PROJECT_SPEC.draft.md exposes Skipped / Deferred Sections.
- PROJECT_SPEC.draft.md exposes Return Points.
- Interview includes mini-summary after every 5–7 questions.
- Mini-summary includes collected facts, assumptions, UNKNOWN, next block, and user confirmation/correction.
- Fatigue signals are tracked.
- If fatigue is detected, agent offers pause or summary.
- Entity-Process Traversal distinguishes CORE_ENTITY from REFERENCE_ENTITY.
- Full traversal is not run on every minor/reference entity.
- Core/risk entities receive full traversal.
- Reference entities may receive lightweight traversal.
- User-mentioned solution anchors are recorded as USER_MENTIONED_HINT.
- User-mentioned numbers are not treated as acceptance criteria.
- User-mentioned technologies are not treated as architecture decisions.
- Five Whys contains anti-anchor prompts.
- Method switch includes what user said, why route changes, and what next method collects.
- PROJECT_SPEC.draft.md exposes Mini-Summary Log.
- PROJECT_SPEC.draft.md exposes Entity Classification.
- PROJECT_SPEC.draft.md exposes Anchor Register.
- PROJECT_SPEC.draft.md exposes Not Discussed But Possibly Relevant.
- PROJECT_SPEC.draft.md exposes Developer Warnings.
- Structural UNKNOWN is visible.
- Method completion is not treated as execution readiness.
- All runbooks completed is not treated as approval.
- Edge Case Elicitation section exists.
- Exception / Anomaly questions are present.
- Hardest case question is present.
- End-of-period / peak-load questions are present.
- Hidden approval flow questions are present.
- Contradiction Probing Protocol exists.
- Contradictions affecting scope/safety/access/data trigger Human review.
- Contradiction is not treated as user error by default.
- Scenario Walkthrough includes exception/anomaly flow.
- Negative Requirements includes never-do questions.
- Five Whys includes grey-zone usage rule.
- Observation Evidence Boundary exists.
- Observation evidence is not treated as approval.
- Screenshot or walkthrough is not treated as production data authorization.
- PROJECT_SPEC.draft.md exposes Exception and Anomaly Register.
- PROJECT_SPEC.draft.md exposes Contradiction Register.
- PROJECT_SPEC.draft.md exposes Observation Evidence Register.
- PROJECT_SPEC.draft.md exposes Hidden Approval Flow Register.
- LOW_CONFIDENCE_ANSWER is not promoted to requirement.
- DEPTH_PROBING_REQUIRED is not treated as PASS.

---

## 8. Final Checklist Status

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
