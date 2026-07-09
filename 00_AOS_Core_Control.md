00 — AOS Core Control

Статус

document_type: core_control
project: AOS-FARM
status: canonical_project_control_source
source_pack_role: core_required
language: ru
version: v5.4-final-min-clarified
pack_date: "2026-06-28"
owner: human / NMF13579
authorized_to_modify: human only

Назначение

Этот документ — главный canonical project control source для нового ChatGPT Project.

Он определяет:

project control
source precedence
build strategy
architecture/skeleton authority
layer model
source of truth rules
documentation strategy
legacy boundary
medical boundary

AOS-FARM — это Markdown-first система управления AI-разработкой. (AOS-1, AgentOS и AgentOS Next в старой документации — это historical/reference naming, которое не используется как активное без явного human approval). Она помогает безопасно пройти путь:

идея
→ документация
→ задача
→ кодовое изменение
→ Evidence
→ human review
→ human approval / rejection

Цель AOS-FARM — не дать AI-разработке создавать ложную уверенность: ложный PASS, скрытую мутацию lifecycle, подмену approval или симуляцию решения человека.

Граница Project Instructions

В Project Instructions нужно вставлять только:

PROJECT_SYSTEM_PROMPT_RU.txt

Нельзя вставлять туда полный текст всех sources. Иначе появится второй Source of Truth.

Required Sources

В Sources обязательно загрузить:

00_AOS_Core_Control.md
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
02_AOS_Governance_Control_Module_and_Safety_Rules.md

Optional:

03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
04_AOS_Model_Routing_and_Task_Decomposition_Research.md

Optional sources are reference/research only.

They do not grant:

roadmap authority
implementation permission
execution permission
approval authority
Risk Profile assignment
lifecycle mutation
Source of Truth promotion
protected/canonical change authorization

Если required project sources не загружены или недоступны, агент обязан сказать это явно.

Без required sources нельзя принимать решения по:

architecture
roadmap
approval
lifecycle
protected/canonical files
destructive operations
Source of Truth
execution authority
merge/release decisions

Default:

UNKNOWN_BLOCKED

или:

HUMAN_REVIEW_REQUIRED

Source Precedence

Общий порядок:

00_AOS_Core_Control.md
>
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
>
02_AOS_Governance_Control_Module_and_Safety_Rules.md
>
03_AOS_Future_and_Legacy_Reference_OPTIONAL.md
>
04_AOS_Model_Routing_and_Task_Decomposition_Research.md

Но есть domain-specific authority:

00_AOS_Core_Control.md = highest authority for all project control and safety invariants.
01_AOS_Assembly_Pipelines_and_Build_Roadmap.md = authority for Documentation Assembly Pipeline, Code Assembly Pipeline, Build Step roadmap and daily workflow.
02_AOS_Governance_Control_Module_and_Safety_Rules.md = authority for safety, Risk Profiles, gates, approval boundary, lifecycle boundary, protected/canonical rules, destructive operations, UNKNOWN, NOT_RUN, PASS/Evidence/approval semantics.
03_AOS_Future_and_Legacy_Reference_OPTIONAL.md = optional reference only.
04_AOS_Model_Routing_and_Task_Decomposition_Research.md = optional research/reference only; no active roadmap, implementation, execution, approval, Risk Profile, lifecycle or Source of Truth authority.

Если 01 и 02 конфликтуют по safety/control-семантике, 02 побеждает, если 00 явно не говорит иначе.

Если конфликт затрагивает approval, lifecycle, protected/canonical files, destructive operations, Source of Truth, execution authority, merge/release decisions или roadmap authority, безопасное поведение:

HUMAN_REVIEW_REQUIRED

или:

UNKNOWN_BLOCKED

Source Conflict Clarification Artifact

Если найден конфликт между sources, нужно создать или предложить conflict clarification artifact.

Он должен указать:

what conflicts
which sources conflict
exact conflicting statements
affected decision
risk
required human decision
temporary safe status

Пока конфликт не resolved by human:

HUMAN_REVIEW_REQUIRED

или:

UNKNOWN_BLOCKED

Repository Baseline

Репозиторий:

NMF13579/AOS-FARM

Модель веток:

main = стабильная / публичная / default branch
dev = active controlled integration baseline
build/ = recommended branch pattern for controlled implementation stages

dev считается active controlled integration baseline.

Новую работу нельзя случайно вести прямо в dev.

Human Availability Rule

Если required human review, approval, checkpoint или Risk Profile assignment недоступны:

status: BLOCKED

или:

status: HUMAN_REVIEW_REQUIRED

Агент не продолжает через предположение.

Агент не заменяет недоступного человека своим решением.

Active Build Strategy

Активная стратегия:

Documentation Assembly Pipeline first
→ Code Assembly Pipeline
→ Minimal Safety Floor always-on
→ Governance / Control Module progressive

Критическая поправка:

Minimal Safety Floor is not a late phase.
Minimal Safety Floor is always-on from day one.

Это означает:

1. Сначала собираем поток документации: idea → brief → spec → task → evidence → review.
2. Потом добавляем поток сборки кода: task → scoped code change → diff → checks → evidence.
3. Minimal Safety Floor действует с первого дня для документации и кода.
4. Governance / Control Module добавляется как отдельный усиливающий модуль.
5. Runtime Enforcement, Registry/Drift, RAG-light, SaaS и Domain Modules добавляются позже.

Strategy Lock

documentation_assembly_pipeline_first: true
code_assembly_pipeline_second: true
minimal_safety_floor_always_on: true
governance_control_module_progressive: true
runtime_enforcement_later: true
architecture_retained: true
target_skeleton_retained: true
dev_baseline_preserved: true
main_as_stable_default_branch: true
new_implementation_branch_recommended: build/
old_milestone_heavy_plan_retained: false
full_documentation_rewrite_required: false
full_repo_cleanup_required_before_new_strategy: false
skeleton_is_not_implementation: true
pass_is_not_approval: true
evidence_is_not_approval: true
ci_pass_is_not_approval: true
human_approval_required_for_protected_changes: true

Numbering Authority

Старая Stage-нумерация — это legacy/reference planning history.

Новая активная нумерация сборки:

Build Step 0
Build Step 1
Build Step 2
...

Старые Stage/milestone-документы не дают:

implementation permission
execution permission
lifecycle mutation
protected changes
next-stage start
approval

Главные инварианты

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

## Кратчайший безопасный путь

Планирование в AOS-FARM по умолчанию должно начинаться с поиска кратчайшего безопасного пути.

Кратчайший безопасный путь означает:

```text
минимальный набор безопасных действий, который закрывает активный блокер без нарушения protected invariants.
```

Агент не должен по умолчанию выбирать самый длинный или самый бюрократический control path, если более короткий путь безопасно закрывает проблему.

Перед предложением этапа, плана, implementation, audit, cleanup, commit, push или merge агент обязан сначала ответить:

```text
Какой кратчайший безопасный путь закрывает активный блокер?
```

Кратчайший безопасный путь разрешён только если одновременно верно:

```text
активный блокер ясен;
scope узкий;
ownership ясен;
изменение локальное и ограниченное;
protected/canonical files не меняются без checkpoint;
approval/lifecycle semantics не мутируют;
destructive operations не требуются или явно авторизованы;
UNKNOWN разрешён или fail-closed;
validation может доказать closure.
```

Кратчайший безопасный путь не ослабляет Minimal Safety Floor.

Он не может обходить:

```text
PASS ≠ approval;
Evidence ≠ approval;
CI PASS ≠ approval;
validator PASS ≠ approval;
UNKNOWN ≠ OK;
NOT_RUN ≠ PASS;
Human approval cannot be simulated;
Scope must not expand without explicit human permission;
Protected/canonical changes require human checkpoint;
Destructive operations are forbidden by default;
Commit authorization ≠ push authorization;
Push authorization ≠ release authorization.
```

Если кратчайший безопасный путь неясен, безопасное состояние:

```text
HUMAN_REVIEW_REQUIRED
```

или:

```text
UNKNOWN_BLOCKED
```

## Ручное сжатие пути человеком

Human может явно сжать предложенный агентом путь.

Примеры допустимого human intent:

```text
сжать путь;
объединить audit + fix + validation;
один этап;
один commit и push;
кратчайший безопасный путь;
не создавать отдельный design-stage.
```

Ручное сжатие пути человеком означает:

```text
агент обязан убрать лишние промежуточные этапы и предложить минимальный безопасный executable plan.
```

Ручное сжатие пути человеком не даёт:

```text
approval;
release authorization;
Risk Profile assignment;
lifecycle mutation;
protected/canonical change permission;
destructive operation permission;
scope expansion;
merge authorization;
push authorization.
```

Сжатие меняет длину процесса, а не safety authority.

Если human просит сжать путь, но такое сжатие пересекает protected boundary, агент обязан сказать это явно и вернуть:

```text
HUMAN_REVIEW_REQUIRED
```

или:

```text
UNKNOWN_BLOCKED
```

## Порядок планирования по умолчанию

Порядок планирования по умолчанию:

```text
1. Определить активный блокер.
2. Найти кратчайший безопасный путь.
3. Проверить, разрешено ли сжатие.
4. Переходить к полному control path только если это действительно требуется.
5. Сохранить все safety invariants.
6. Остановиться на human authorization boundaries.
```

Полный control path требуется только если:

```text
ownership неясен;
Source of Truth files меняются без checkpoint;
approval/lifecycle semantics затрагиваются;
protected/canonical files затрагиваются;
destructive operations вовлечены;
Risk Profile assignment требуется;
UNKNOWN остаётся неразрешённым;
изменение может создать false PASS или false approval;
scope может расшириться;
merge/release authority вовлечена.
```


Source of Truth

Markdown/YAML = Source of Truth.
JSON/generated/index/cache = только derived/navigation artifacts.
SQLite/cache = optional local runtime/cache, никогда не Source of Truth.
Reports/Evidence = фактические записи, не approval.
Human checkpoint/approval witness = только scoped human authorization.

Если generated/cache/index конфликтует с canonical Markdown/YAML, побеждает canonical source.

Если source state неизвестен — fail-closed.

fail-closed означает:

- явно сообщить о блокировке;
- не делать commit;
- не продолжать execution;
- не infer approval;
- не infer PASS;
- ждать human input или required evidence.

Architecture and Skeleton Authority

Canonical architecture and skeleton documents live in the repository.

ChatGPT Project Sources provide only a short orientation layer.

If this source pack conflicts with repository architecture/skeleton files, repository canonical files win, unless the conflict concerns safety invariants. In safety conflicts, fail-closed and require human review.

The source pack must not duplicate the full architecture.

If exact canonical paths are unknown:

canonical_architecture_path: unknown
canonical_skeleton_path: unknown
status: HUMAN_REVIEW_REQUIRED

If repository access is unavailable:

status: UNKNOWN_BLOCKED

Do not guess canonical file paths.

Product Identity

AOS-FARM — это:

governance layer
documentation-to-code assembly system
task/spec/Evidence/review/approval lifecycle system
controlled AI-development workflow
Markdown/YAML-first project operating system
safety boundary between agent claims and human decisions

AOS-FARM не является:

autonomous coding agent
заменой human approval
медицинской системой
SaaS сам по себе
CI system сам по себе
generic RAG database
multi-agent framework first

Product Folder Boundaries

Следующие границы структуры проекта строго определены:

Product folder AOS = /aos/
/aos/root/AGENTS.md = template for target project root AGENTS.md
Root 00/01/02 = AOS-FARM development canonical sources, not consumer runtime prerequisites.
agentos/ = internal/reference layer, not consumer first-start path.
legacy AgentOS = must not be imported into AOS-FARM and may be used only as reference.

Local Temporary Workspace Boundary

AOS-FARM repo and target projects use root-level /.aos-tmp/ for temporary command outputs, scratch logs, and local disposable intermediate files.

The /.aos-tmp/ directory is:

local-only
ignored by git
disposable
not Source of Truth
not Evidence storage
not approval storage
not checkpoint storage
not canonical documentation storage

Evidence, reports, approvals, checkpoints, protected/canonical files, and lifecycle artifacts must never be stored in /.aos-tmp/.

Temporary command outputs must not be written into repo root or inside /aos/.

Layer Model

Documentation Assembly Pipeline = собирает документационный flow.
Code Assembly Pipeline = собирает scoped code change flow.
Minimal Safety Floor = не даёт documentation/code flow врать.
Governance / Control Module = добавляет progressive governance.
Runtime Enforcement = позже физически блокирует forbidden actions.
SaaS = UX/commercial wrapper, позже.
Domain Modules = domain extensions, позже.

Критическое правило:

Documentation pipeline can be built first.
Code pipeline can be built second.
Minimal Safety Floor is mandatory from day one.
Governance / Control Module is progressive and may be implemented after Assembly MVP.
Runtime Enforcement is later.

Skeleton Interpretation

Skeleton — это target structure, а не claim о готовности реализации.

Target skeleton ≠ implementation readiness.
Skeleton is not runtime.
Skeleton is not validation.
Skeleton is not approval.

Active-now Areas

Эти зоны могут быть relevant для первичной сборки, если они есть в репозитории:

docs/
templates/
reports/

Active-now не означает, что они полностью реализованы.

Planned-later Areas

Не включать в immediate implementation scope без явной human authorization:

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

Documentation Strategy

Не переписывать всю документацию.

Использовать controlled documentation reset:

Keep baseline.
Create thin active control layer.
Defer future layers.
Do not mass-rewrite old reports.

Запрещено по default:

mass rewrite
bulk delete
move/rename/archive
hidden cleanup
compress protected/canonical docs
rewrite old evidence
rewrite reports to fit new strategy
replace architecture without decision record

Legacy Boundary

Old AgentOS / AOS-1 / AgentOS Next = historical/reference naming.
AOS-FARM = active target.

Старые материалы не дают:

active roadmap
active Source of Truth
implementation permission
execution permission
approval
lifecycle mutation
protected change authorization
required milestone chain

Medical Boundary

AOS-FARM core не является медицинской системой.

Если задача затрагивает:

clinical decisions
patient data
diagnosis
treatment
triage
medical recommendations
regulated health workflows
clinical decision support

то её нельзя считать обычной LOW_RISK_FAST.

Medical-domain work требует отдельной архитектуры для:

privacy
compliance
clinical safety
audit
data retention/deletion
liability
access control

AI-generated medical decision не является approval.

Роль ассистента

AI assistant может:

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

AI assistant не должен:

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

Финальная граница

Этот документ задаёт core governance и project control.

Он не является approval.

Он не авторизует execution.

Он не авторизует protected/canonical changes.

Он не авторизует destructive operations.

Он не запускает следующий Build Step автоматически.