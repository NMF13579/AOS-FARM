# 02 — AOS Governance Control Module and Safety Rules

## Статус

```yaml
document_type: governance_control_module_and_safety_rules
project: AOS-FARM
status: active_safety_and_control_rules
source_pack_role: core_required
language: ru
version: v5.4-final-min
pack_date: "2026-06-10"
owner: human / NMF13579
authorized_to_modify: human only
```

## Назначение

Этот документ определяет:

```text
Minimal Safety Floor
Governance / Control Module
Risk Profiles
Risk Matrix
Control Gates
CI/CD Boundary
UNKNOWN_BLOCKED handling
Task Writing rules
Task Brief example
```

Для safety/control semantics этот документ имеет authority над `01`, если `00` явно не говорит иначе.

Governance / Control Module не собирает проект.

Governance / Control Module проверяет, блокирует и отделяет claims от decisions.

## Главная формула

```text
Documentation Assembly Pipeline defines scope.
Code Assembly Pipeline builds within scope.
Minimal Safety Floor prevents lying from day one.
Governance / Control Module adds progressive governance.
Runtime Enforcement physically blocks forbidden actions later.
```

## Product Folder Boundaries

Следующие границы структуры проекта строго определены:

```text
Product folder AOS = /aos/
/aos/root/AGENTS.md = template for target project root AGENTS.md
Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites.
agentos/ = internal/reference layer, not consumer first-start path.
legacy AgentOS = must not be imported into AOS-FARM and may be used only as reference.
```

## Local Temporary Workspace Boundary

AOS-FARM repo and target projects use root-level `/.aos-tmp/` for temporary command outputs, scratch logs, and local disposable intermediate files.

The `/.aos-tmp/` directory is:
* local-only
* ignored by git
* disposable
* not Source of Truth
* not Evidence storage
* not approval storage
* not checkpoint storage
* not canonical documentation storage

Evidence, reports, approvals, checkpoints, protected/canonical files, and lifecycle artifacts must never be stored in `/.aos-tmp/`.
Temporary command outputs must not be written into repo root or inside `/aos/`.

If an agent finds Evidence, approval records, checkpoints, lifecycle decisions, Risk Profile assignments, protected/canonical files, or Source of Truth artifacts in `/.aos-tmp/`, the safe state is:

```text
HUMAN_REVIEW_REQUIRED
```

или:

```text
UNKNOWN_BLOCKED
```

## Minimal Safety Floor

Minimal Safety Floor обязателен с первого дня, даже если полноценный Governance / Control Module ещё не реализован.

Всегда активные инварианты:

```text
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Metrics ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
BLOCKED ≠ PASS.
Human approval cannot be simulated.
Skeleton is not implementation.
Scope must not expand without explicit human permission.
```

## Запрещено с первого дня

```text
fake human approval
auto-approval
auto-completion
auto-merge
auto-commit
hidden execution
hidden lifecycle mutation
protected/canonical change without checkpoint
destructive operation by default
scope expansion without explicit human permission
treating missing Evidence as acceptable
treating unknown state as OK
treating NOT_RUN as PASS
agent self-assignment of LOW_RISK_FAST
```

## Required Failure Semantics

```yaml
unknown_result: BLOCKED
unknown_scope: BLOCKED
unknown_file_change: BLOCKED
unknown_flow_class: BLOCKED
missing_evidence: BLOCKED
validation_not_run: NOT_RUN
not_run_is_pass: false
warning_is_clean_pass: false
human_unavailable_for_required_decision: BLOCKED
```

## Governance / Control Module

Governance / Control Module — это progressive governance module.

Он добавляет проверки поверх Documentation Assembly Pipeline и Code Assembly Pipeline:

```text
Risk Profile control
Scope Gate
Evidence Gate
Human Review Gate
False PASS Gate
Lifecycle Mutation Gate
Protected/Canonical Gate
CI/CD Boundary
UNKNOWN_BLOCKED escalation
```

Governance / Control Module не должен:

```text
approve
заменять human decision
сам мутировать lifecycle
автоматически запускать следующий Build Step
расширять scope
скрыто включать/отключать gates
```

## Approval Boundary

Только человек может approve:

```text
final result
protected/canonical change
destructive operation
release
merge
lifecycle mutation requiring approval
scope expansion
next-stage transition
```

AI может рекомендовать review.

AI может подготовить Evidence.

AI не может approve.

Если required human approval недоступен:

```text
BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

## Evidence Boundary

Evidence может включать:

```text
git diff
validation output
test output
command logs
changed file list
not-run list
unknowns
blockers
```

Evidence не может писать:

```text
approved: true
```

если этот approval отдельно не предоставлен через human checkpoint/approval witness.

## CI/CD Boundary

AI может создать draft:

```text
CI config
workflow
validator
quality gate
branch protection proposal
```

AI не может без explicit human approval:

```text
enable required check
disable check
weaken validator
change branch protection
change approval semantics
change PASS semantics
claim CI PASS as approval
```

Любое изменение required checks, branch protection, validator behavior или approval semantics требует:

```text
minimum Risk Profile: HIGH_RISK_PROTECTED
human checkpoint: required
```

## Risk Profile Assignment Rule

Risk/control profile назначается только человеком или явно реализованным deterministic classifier, который был approved by human.

Пока такого classifier нет, агент может только предложить profile.

Агент не должен сам назначать:

```text
LOW_RISK_FAST
```

Если profile assignment отсутствует, неоднозначен или спорный, default:

```text
UNKNOWN_BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

Если human недоступен для required Risk Profile assignment:

```text
BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

## Core Risk Rule

```text
UNKNOWN cannot be LOW.
```

Если risk нельзя классифицировать, задача не может идти как fast/advisory.

## Non-Canonical Draft Definition

`Non-canonical draft` — это черновик, который одновременно выполняет все условия:

```text
- находится в явно разрешённой draft/sandbox зоне;
- не объявлен Source of Truth;
- не является protected/canonical file;
- не меняет roadmap, architecture, lifecycle, approval, validator, CI/CD или runtime semantics;
- не используется как required input для execution или approval;
- имеет явный статус draft/non-canonical;
- может быть изменён без изменения project authority.
```

Агент не может сам объявить произвольный файл `non-canonical`.

Если файл не имеет явного draft/non-canonical статуса, считать его неясным:

```text
UNKNOWN_BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

## Risk Profiles

## LOW_RISK_FAST

Используется только если human явно назначил этот Risk Profile.

Фраза «простая идея», «черновик», «заметка» или «non-canonical draft» не является автоматическим разрешением на LOW_RISK_FAST.

Разрешено:

```text
писать черновики
делать заметки
предлагать структуру
создавать non-canonical drafts
готовить feature parking notes
готовить task drafts без execution
```

Запрещено:

```text
approve
менять lifecycle
трогать protected/canonical files
delete/move/rename/archive
commit/merge/release
включать/отключать validators или CI gates
```

## MEDIUM_RISK_GUIDED

Используется для:

```text
Documentation Assembly Pipeline changes
Code Assembly Pipeline contract drafts
lifecycle-adjacent templates
Evidence templates
validation contract drafts
roadmap draft changes
module boundary drafts
non-runtime schema drafts
```

Обязательно:

```text
explicit scope
allowed changes
forbidden changes
Evidence/report
validation notes
human review before acceptance
```

## HIGH_RISK_PROTECTED

Используется для:

```text
approval semantics
PASS semantics
Evidence semantics
lifecycle mutation
protected/canonical files
validators
runtime enforcement
Source of Truth policy
security/privacy-sensitive behavior
branch/merge/release rules
Governance / Control Module authority
```

Обязательно:

```text
full strict task brief
human checkpoint
negative checks
fail-closed semantics
explicit final boundary
no automatic next-stage start
```

## DESTRUCTIVE_OR_CANONICAL

Используется для:

```text
delete
move
rename
archive
cleanup
compression
protected/canonical rewrite
bulk documentation rewrite
force-push/history rewrite
merge/release
```

Default:

```text
BLOCKED
```

Чтобы продолжить, требуется:

```text
explicit human authorization
rollback plan
validation
diff review
```

## UNKNOWN_BLOCKED

Используется когда:

```text
scope is unclear
target files unknown
risk unknown
branch state unknown
Source of Truth conflict exists
Evidence missing
validation state unknown
human decision unavailable
```

Default:

```text
BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

Никогда:

```text
LOW_RISK_FAST
```

## Матрица: тип задачи → минимальный Risk Profile

| Тип задачи | Минимальный Risk Profile | Кто назначает |
|---|---|---|
| Черновик заметки / non-canonical draft | LOW_RISK_FAST | Human |
| Feature Parking note | LOW_RISK_FAST | Human |
| Project Brief / Spec draft | LOW_RISK_FAST или MEDIUM_RISK_GUIDED | Human |
| Task draft | LOW_RISK_FAST или MEDIUM_RISK_GUIDED | Human |
| Documentation Assembly Pipeline doc | MEDIUM_RISK_GUIDED | Human |
| Code Assembly Pipeline contract | MEDIUM_RISK_GUIDED | Human |
| Execution/Evidence report draft | MEDIUM_RISK_GUIDED | Human |
| Изменение lifecycle template | MEDIUM_RISK_GUIDED | Human |
| Изменение Evidence template | MEDIUM_RISK_GUIDED | Human |
| Изменение roadmap / Strategy Lock | HIGH_RISK_PROTECTED | Human |
| Изменение architecture authority | HIGH_RISK_PROTECTED | Human |
| Validator / approval / PASS logic | HIGH_RISK_PROTECTED | Human |
| Governance / Control Module authority | HIGH_RISK_PROTECTED | Human |
| Runtime enforcement | HIGH_RISK_PROTECTED | Human |
| CI required checks / branch protection | HIGH_RISK_PROTECTED | Human + checkpoint |
| Protected/canonical file change | HIGH_RISK_PROTECTED | Human + checkpoint |
| Medical-domain task with clinical/patient data | HIGH_RISK_PROTECTED | Human + domain checkpoint |
| Cleanup / delete / move / rename / archive | DESTRUCTIVE_OR_CANONICAL | Human + separate checkpoint |
| Непонятный scope / unknown risk | UNKNOWN_BLOCKED | Default |

## Control Gates

## Scope Gate

Проверяет:

```text
clear scope exists
allowed changes are explicit
forbidden changes are explicit
no hidden scope expansion
```

Если scope unknown:

```text
UNKNOWN_BLOCKED
```

## Evidence Gate

Проверяет:

```text
required Evidence exists
not-run items are disclosed
validation outputs are recorded
agent claims are separated from proof
```

Missing Evidence:

```text
BLOCKED
```

## False PASS Gate

Проверяет:

```text
PASS is not approval
Evidence is not approval
CI PASS is not approval
NOT_RUN is not PASS
UNKNOWN is not OK
```

Violation:

```text
BLOCKED
```

## Human Review Gate

Проверяет:

```text
human review is required where decision is needed
AI did not simulate approval
review is scoped
```

Missing required human review:

```text
HUMAN_REVIEW_REQUIRED
```

If human is unavailable:

```text
BLOCKED
```

## Lifecycle Mutation Gate

Проверяет:

```text
no lifecycle mutation without explicit rule
no lifecycle mutation without required human checkpoint
readiness did not start next Build Step
```

Violation:

```text
BLOCKED
```

## Protected/Canonical Gate

Проверяет:

```text
protected/canonical files are identified
human checkpoint exists when required
agent did not self-authorize protected change
```

Unknown protected status:

```text
UNKNOWN_BLOCKED
```

## UNKNOWN_BLOCKED Escalation Rule

Чтобы вывести ситуацию из `UNKNOWN_BLOCKED`, нужно создать или предложить clarification/report artifact в явно разрешённом месте.

Допустимые места, если они существуют и разрешены текущим task scope:

```text
drafts/
agentos/reports/
```

Если эти пути отсутствуют, неизвестны или не входят в allowed changes, не создавать файл автоматически. Вместо этого предложить artifact content в final report.

Clarification artifact должен указать:

```text
what is unknown
why it blocks
what evidence is missing
who can resolve it
what exact decision is needed
whether protected/canonical/destructive scope is involved
```

Агент не может resolve UNKNOWN через предположение.

Человек может resolve UNKNOWN только explicit scoped decision.

Если после clarification остаётся unknown, статус остаётся:

```text
UNKNOWN_BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

## Task Writer Role

При создании AOS-1 task brief действовать только как task writer.

Можно:

```text
draft task briefs
propose a safe control profile
define scope
define allowed changes
define forbidden changes
define validation
define expected final report
identify risks and blockers
```

Нельзя:

```text
approve the task
simulate human checkpoint
authorize execution
activate sandbox/write mode by yourself
start the next task or stage
create lifecycle mutation
claim PASS as approval
expand scope beyond the user request
self-assign LOW_RISK_FAST
```

## Preferred Task Brief Format

```markdown
# Task ID / Name

## Mode

[SAFE_TASK_DRAFT / LOW_RISK_FAST / MEDIUM_RISK_GUIDED / HIGH_RISK_PROTECTED / DESTRUCTIVE_OR_CANONICAL / UNKNOWN_BLOCKED]

## Repository

[repo]

## Branch

[branch]

## Risk Profile Assignment

- proposed_by_agent: [profile or none]
- assigned_by_human: [profile or missing]
- assignment_evidence: [exact user instruction or approved deterministic classifier output]

## Context

[why this task exists]

## Goal

[one clear goal]

## Scope

[in-scope work only]

## Rules

[mandatory rules]

## Allowed Changes

[exact files/paths or artifact types]

## Forbidden Changes

[what must not be changed]

## Required Behavior / Content

[required output details]

## Non-Goals

[explicitly out of scope]

## Validation

[commands/checks/review requirements]

## Expected Final Report

[what final report must include]

## Final Boundary Rule

[no approval, no lifecycle mutation, no next-stage start unless explicitly authorized]
```

## Финальная граница

Minimal Safety Floor не optional.

Governance / Control Module снижает риск, но не заменяет human approval.

Task drafts не дают execution permission.

Этот документ не даёт approval authority.

Этот документ не авторизует lifecycle mutation.

Этот документ не авторизует protected/canonical changes.

Этот документ не авторизует destructive operations.

Этот документ не авторизует commit, merge, release или next-stage start.
