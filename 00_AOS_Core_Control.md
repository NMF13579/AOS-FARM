# 00 — AOS Core Control

## Статус

```yaml
document_type: core_control
project: AOS-1 / AgentOS Next
status: canonical_project_control_source
source_pack_role: core_required
language: ru
version: v5.4-final-min
pack_date: "2026-06-10"
owner: human / NMF13579
authorized_to_modify: human only
```

## Назначение

Этот документ — главный `canonical project control source` для нового ChatGPT Project.

Он определяет:

```text
project control
source precedence
build strategy
architecture/skeleton authority
layer model
source of truth rules
documentation strategy
legacy boundary
medical boundary
```

AOS-1 / AgentOS Next — это Markdown-first система управления AI-разработкой. Она помогает безопасно пройти путь:

```text
идея
→ документация
→ задача
→ кодовое изменение
→ Evidence
→ human review
→ human approval / rejection
```

Цель AOS-1 — не дать AI-разработке создавать ложную уверенность: ложный `PASS`, скрытую мутацию `lifecycle`, подмену `approval` или симуляцию решения человека.

## Граница Project Instructions

В Project Instructions нужно вставлять только:

```text
PROJECT_SYSTEM_PROMPT_RU.txt
```

Нельзя вставлять туда полный текст всех sources. Иначе появится второй `Source of Truth`.

## Required Sources

В Sources обязательно загрузить:

```text
00_AOS_Core_Control.md
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
02_AOS_Governance_Control_Module_and_Safety_Rules.md
```

Optional:

```text
03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
```

Если required project sources не загружены или недоступны, агент обязан сказать это явно.

Без required sources нельзя принимать решения по:

```text
architecture
roadmap
approval
lifecycle
protected/canonical files
destructive operations
Source of Truth
execution authority
merge/release decisions
```

Default:

```text
UNKNOWN_BLOCKED
```

или:

```text
HUMAN_REVIEW_REQUIRED
```

## Source Precedence

Общий порядок:

```text
00_AOS_Core_Control.md
>
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
>
02_AOS_Governance_Control_Module_and_Safety_Rules.md
>
03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
```

Но есть domain-specific authority:

```text
00_AOS_Core_Control.md = highest authority for all project control and safety invariants.
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md = authority for Documentation Assembly Pipeline, Code Assembly Pipeline, Build Step roadmap and daily workflow.
02_AOS_Governance_Control_Module_and_Safety_Rules.md = authority for safety, Risk Profiles, gates, approval boundary, lifecycle boundary, protected/canonical rules, destructive operations, UNKNOWN, NOT_RUN, PASS/Evidence/approval semantics.
03_AOS_Future_and_Legacy_Reference_OPTIONAL.md = reference only.
```

Если `01` и `02` конфликтуют по safety/control-семантике, `02` побеждает, если `00` явно не говорит иначе.

Если конфликт затрагивает `approval`, `lifecycle`, `protected/canonical files`, `destructive operations`, `Source of Truth`, `execution authority`, `merge/release decisions` или roadmap authority, безопасное поведение:

```text
HUMAN_REVIEW_REQUIRED
```

или:

```text
UNKNOWN_BLOCKED
```

## Source Conflict Clarification Artifact

Если найден конфликт между sources, нужно создать или предложить conflict clarification artifact.

Он должен указать:

```text
what conflicts
which sources conflict
exact conflicting statements
affected decision
risk
required human decision
temporary safe status
```

Пока конфликт не resolved by human:

```text
HUMAN_REVIEW_REQUIRED
```

или:

```text
UNKNOWN_BLOCKED
```

## Repository Baseline

Репозиторий:

```text
NMF13579/AOS-1
```

Модель веток:

```text
main = стабильная / публичная / default branch
dev = frozen skeleton/reference baseline
build/assembly-first = рекомендуемая новая ветка реализации
```

`dev` считается сохранённым `skeleton/reference baseline`.

Новую работу нельзя случайно вести прямо в `dev`.

## Human Availability Rule

Если required human review, approval, checkpoint или Risk Profile assignment недоступны:

```text
status: BLOCKED
```

или:

```text
status: HUMAN_REVIEW_REQUIRED
```

Агент не продолжает через предположение.

Агент не заменяет недоступного человека своим решением.

## Active Build Strategy

Активная стратегия:

```text
Documentation Assembly Pipeline first
→ Code Assembly Pipeline
→ Minimal Safety Floor always-on
→ Governance / Control Module progressive
```

Критическая поправка:

```text
Minimal Safety Floor is not a late phase.
Minimal Safety Floor is always-on from day one.
```

Это означает:

```text
1. Сначала собираем поток документации: idea → brief → spec → task → evidence → review.
2. Потом добавляем поток сборки кода: task → scoped code change → diff → checks → evidence.
3. Minimal Safety Floor действует с первого дня для документации и кода.
4. Governance / Control Module добавляется как отдельный усиливающий модуль.
5. Runtime Enforcement, Registry/Drift, RAG-light, SaaS и Domain Modules добавляются позже.
```

## Strategy Lock

```yaml
documentation_assembly_pipeline_first: true
code_assembly_pipeline_second: true
minimal_safety_floor_always_on: true
governance_control_module_progressive: true
runtime_enforcement_later: true

architecture_retained: true
target_skeleton_retained: true
dev_baseline_preserved: true
main_as_stable_default_branch: true
new_implementation_branch_recommended: build/assembly-first

old_milestone_heavy_plan_retained: false
full_documentation_rewrite_required: false
full_repo_cleanup_required_before_new_strategy: false

skeleton_is_not_implementation: true
pass_is_not_approval: true
evidence_is_not_approval: true
ci_pass_is_not_approval: true
human_approval_required_for_protected_changes: true
```

## Numbering Authority

Старая Stage-нумерация — это `legacy/reference planning history`.

Новая активная нумерация сборки:

```text
Build Step 0
Build Step 1
Build Step 2
...
```

Старые Stage/milestone-документы не дают:

```text
implementation permission
execution permission
lifecycle mutation
protected changes
next-stage start
approval
```

## Главные инварианты

```text
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Metrics ≠ approval.
Human approval cannot be simulated.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
BLOCKED ≠ PASS.
Skeleton ≠ implementation.
Readiness ≠ execution permission.
Report ≠ lifecycle mutation.
Task completion ≠ human approval.
Minimal Safety Floor is always-on.
```

## Source of Truth

```text
Markdown/YAML = Source of Truth.
JSON/generated/index/cache = только derived/navigation artifacts.
SQLite/cache = optional local runtime/cache, никогда не Source of Truth.
Reports/Evidence = фактические записи, не approval.
Human checkpoint/approval witness = только scoped human authorization.
```

Если `generated/cache/index` конфликтует с canonical Markdown/YAML, побеждает canonical source.

Если source state неизвестен — `fail-closed`.

`fail-closed` означает:

```text
- явно сообщить о блокировке;
- не делать commit;
- не продолжать execution;
- не infer approval;
- не infer PASS;
- ждать human input или required evidence.
```

## Architecture and Skeleton Authority

Canonical architecture and skeleton documents live in the repository.

ChatGPT Project Sources provide only a short orientation layer.

If this source pack conflicts with repository architecture/skeleton files, repository canonical files win, unless the conflict concerns safety invariants. In safety conflicts, fail-closed and require human review.

The source pack must not duplicate the full architecture.

If exact canonical paths are unknown:

```yaml
canonical_architecture_path: unknown
canonical_skeleton_path: unknown
status: HUMAN_REVIEW_REQUIRED
```

If repository access is unavailable:

```text
status: UNKNOWN_BLOCKED
```

Do not guess canonical file paths.

## Product Identity

AOS-1 — это:

```text
governance layer
documentation-to-code assembly system
task/spec/Evidence/review/approval lifecycle system
controlled AI-development workflow
Markdown/YAML-first project operating system
safety boundary between agent claims and human decisions
```

AOS-1 не является:

```text
autonomous coding agent
заменой human approval
медицинской системой
SaaS сам по себе
CI system сам по себе
generic RAG database
multi-agent framework first
```

## Layer Model

```text
Documentation Assembly Pipeline = собирает документационный flow.
Code Assembly Pipeline = собирает scoped code change flow.
Minimal Safety Floor = не даёт documentation/code flow врать.
Governance / Control Module = добавляет progressive governance.
Runtime Enforcement = позже физически блокирует forbidden actions.
SaaS = UX/commercial wrapper, позже.
Domain Modules = domain extensions, позже.
```

Критическое правило:

```text
Documentation pipeline can be built first.
Code pipeline can be built second.
Minimal Safety Floor is mandatory from day one.
Governance / Control Module is progressive and may be implemented after Assembly MVP.
Runtime Enforcement is later.
```

## Skeleton Interpretation

Skeleton — это `target structure`, а не claim о готовности реализации.

```text
Target skeleton ≠ implementation readiness.
Skeleton is not runtime.
Skeleton is not validation.
Skeleton is not approval.
```

## Active-now Areas

Эти зоны могут быть relevant для первичной сборки, если они есть в репозитории:

```text
agentos/architecture/
agentos/governance/
agentos/templates/
agentos/schemas/
agentos/pipelines/
agentos/state/
agentos/reports/
agentos/approvals/
agentos/scripts/
```

Active-now не означает, что они полностью реализованы.

## Planned-later Areas

Не включать в immediate implementation scope без явной human authorization:

```text
agentos/runtime/
agentos/context/
agentos/registry/
agentos/generated/
agentos/install/
agentos/modules/
agentos/tutor/
agentos/prompt-packs/
cross-repo behavior
template export
update/uninstall flows
RAG/SQLite cache
```

## Documentation Strategy

Не переписывать всю документацию.

Использовать controlled documentation reset:

```text
Keep baseline.
Create thin active control layer.
Defer future layers.
Do not mass-rewrite old reports.
```

Запрещено по default:

```text
mass rewrite
bulk delete
move/rename/archive
hidden cleanup
compress protected/canonical docs
rewrite old evidence
rewrite reports to fit new strategy
replace architecture without decision record
```

## Legacy Boundary

```text
Old AgentOS = reference source.
AOS-1 / AgentOS Next = active target.
```

Старые материалы не дают:

```text
active roadmap
active Source of Truth
implementation permission
approval
lifecycle mutation
protected change authorization
required milestone chain
```

## Medical Boundary

AOS-1 core не является медицинской системой.

Если задача затрагивает:

```text
clinical decisions
patient data
diagnosis
treatment
triage
medical recommendations
regulated health workflows
clinical decision support
```

то её нельзя считать обычной `LOW_RISK_FAST`.

Medical-domain work требует отдельной архитектуры для:

```text
privacy
compliance
clinical safety
audit
data retention/deletion
liability
access control
```

AI-generated medical decision не является approval.

## Роль ассистента

AI assistant может:

```text
анализировать architecture
писать drafts документов
писать task briefs
предлагать безопасные implementation plans
находить blockers
предлагать Risk Profile только как предложение
предлагать validation
готовить reports
помогать сжимать и прояснять documentation
писать drafts CI/workflow/validator configs
```

AI assistant не должен:

```text
approve результаты
симулировать human approval
создавать fake human checkpoints
сам назначать LOW_RISK_FAST
автоматически запускать следующий Build Step
авторизовать destructive operations
авторизовать protected/canonical changes
утверждать, что PASS = approval
утверждать, что Evidence = approval
утверждать, что CI PASS = approval
расширять scope без явной команды человека
делать commit, merge или release без явной human authorization
считать старые Stage/milestone документы active roadmap
включать, отключать, ослаблять или обходить CI/control gates без explicit human approval
```

## Финальная граница

Этот документ задаёт core governance и project control.

Он не является approval.

Он не авторизует execution.

Он не авторизует protected/canonical changes.

Он не авторизует destructive operations.

Он не запускает следующий Build Step автоматически.
