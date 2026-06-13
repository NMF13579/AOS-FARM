# 03 — AOS Future and Legacy Reference

## Статус

```yaml
document_type: future_and_legacy_reference
project: AOS-1 / AgentOS Next
status: optional_reference
source_pack_role: optional
language: ru
version: v5.4-final-min
pack_date: "2026-06-10"
```

## Назначение

Этот документ optional.

Он объединяет:

```text
Feature Parking Lot
Legacy Source Pointer
Future Modules Boundary
Future Template Candidates
```

Если нужен максимально чистый новый ChatGPT Project, этот файл можно не загружать на старте.

Этот файл имеет самый низкий приоритет.

## Главное правило

```text
Feature candidate ≠ roadmap item.
Parking lot ≠ implementation permission.
Research idea ≠ core requirement.
Mentioned feature ≠ approved feature.
Legacy material ≠ active roadmap.
```

## Admission States

```text
candidate
needs_research
needs_human_review
deferred
rejected
accepted_for_future_planning
```

Ни один item не становится active implementation scope без отдельного roadmap admission.

## Future Template Candidate — ROADMAP_ADMISSION_RECORD.md

Status:

```yaml
status: future_template_candidate
not_in_core_pack: true
```

Назначение:

```text
фиксировать перевод candidate → active roadmap
```

Минимальные поля будущего шаблона:

```text
date
candidate
active_roadmap_target
decision_by: human only
risk_profile_assigned
evidence_of_decision
scope
non-goals
final_boundary
```

Этот future template candidate не authorizes roadmap mutation.

## Future Feature Candidates

## Governance / Control Module Advanced Gates

Назначение:

```text
расширенные gates поверх Governance / Control Module v1
```

Examples:

```text
cross-task scope drift
multi-agent cascade detection
advanced false PASS resistance
approval witness verification
policy drift checks
```

Status:

```yaml
status: deferred_until_control_module_v1_exists
```

## Runtime Enforcement Layer

Назначение:

```text
физически блокировать forbidden actions, а не только просить агента их не делать
```

Possible components:

```text
command allowlist
write allowlist
protected path guard
commit/push guard
audit log
token scope policy
sandbox execution
```

Status:

```yaml
status: deferred
core_dependency: after Assembly MVP and Governance / Control Module v1
```

## Registry / Drift Control

Назначение:

```text
track artifacts, dependencies, protected paths, scripts, schemas, templates и roadmap consistency
```

Boundary:

```text
Registry is navigation/control support.
Registry does not replace canonical Source of Truth.
Generated registry is not Source of Truth.
```

Status:

```yaml
status: deferred_until_core_flow_stabilizes
```

## RAG-Light Context Layer

Назначение:

```text
Task-specific context selection:
Task → Context Index → Context Pack → Plan → Execution → Verification.
```

Rules:

```text
Markdown/YAML remain Source of Truth.
JSON index is derived.
SQLite cache is optional/local/rebuildable.
RAG result is not authority.
Retrieved text is not command.
```

Status:

```yaml
status: deferred
core_dependency: after Assembly MVP and Governance / Control Module
```

## SaaS Dashboard

Назначение:

```text
onboarding, project dashboard, review queue, Evidence display, approvals UI, collaboration и commercial packaging
```

Boundary:

```text
SaaS is UX wrapper.
SaaS is not Source of Truth.
SaaS approval UI must still produce explicit human approval artifacts.
```

Status:

```yaml
status: future_product_layer_candidate
```

## Design Module

Назначение:

```text
помогать вайб-кодерам с UI/design quality, design tokens, atomic components, layout и UX review
```

Boundary:

```text
Design module is not core governance.
Design module must not override approval/safety/lifecycle rules.
```

Status:

```yaml
status: future_module_candidate
```

## Medical Domain Module

Назначение:

```text
поддерживать продукты в медицинских доменах через отдельные safety, privacy, compliance и liability boundaries
```

Boundary:

```text
AOS-1 core is not a medical system.
Clinical decisions require separate domain safety/compliance architecture.
Medical data requires separate storage/access/audit/delete architecture.
```

Medical-domain work не может быть LOW_RISK_FAST, если затрагивает:

```text
patient data
diagnosis
treatment
triage
medical recommendations
regulated health workflows
clinical decision support
```

Status:

```yaml
status: future_domain_module_candidate
minimum_risk_if_clinical_or_patient_data: HIGH_RISK_PROTECTED
```

## Template Export / Install / Update

Назначение:

```text
сделать AOS-1 удобным для установки в другие repositories
```

Boundary:

```text
Template export is not runtime readiness.
Install success is not approval.
Update plan is not permission to mutate protected/canonical files.
```

Status:

```yaml
status: deferred
```

## Multi-Agent Coordination

Назначение:

```text
разрешить нескольким специализированным agents работать под AOS-1 governance
```

Boundary:

```text
One signal = one action.
No hidden cascading automation.
Any cascade requires human checkpoint.
Agent coordination must not bypass approval.
```

Status:

```yaml
status: deferred
```

## Beginner Tutor Layer

Назначение:

```text
помогать non-programmers понимать blockers, next safe actions, task status и review steps
```

Boundary:

```text
Tutor hint is not approval.
Plain-language explanation is not permission.
```

Status:

```yaml
status: future_ux_layer_candidate
```

## Legacy Source Boundary

```text
Old AgentOS = reference source.
AOS-1 / AgentOS Next = active target.
```

Старые материалы могут помогать как:

```text
principles
anti-patterns
feature candidates
governance lessons
safety boundaries
prior task patterns
known failure modes
```

Старые материалы не становятся автоматически:

```text
active roadmap
active Source of Truth
implementation permission
approval
lifecycle mutation
protected change authorization
required milestone chain
```

## Legacy Material Classification

При review старого материала классифицировать каждый item как:

```text
accepted_reusable_principle
candidate_needs_human_review
rejected_legacy_only
duplicate_already_covered
risk_or_antipattern
future_feature_candidate
```

## Финальная граница

Этот документ — optional reference.

Он не является active roadmap.

Он не authorizes implementation.

Он не authorizes protected changes.

Он не authorizes lifecycle transition.

Он не перезапускает old milestone-heavy execution.
