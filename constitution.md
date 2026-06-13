# Constitution

# Конституция AOS Farm

```yaml
document_type: project_constitution
project: aos-farm
related_project: AOS-1 / AgentOS Next
status: DRAFT_HUMAN_REVIEW_REQUIRED
owner: human
approval_authority: human_only
agent_may_modify_without_explicit_permission: false
canonical_aos_source_of_truth: false
created_for: isolated_spec_kit_sandbox
```

## 1. Назначение

`aos-farm` — это изолированный тестовый репозиторий на базе Spec Kit для сборки, проверки и уточнения конвейера AOS-1 до переноса решений в основной проект.

`aos-farm` нужен для безопасной отработки:

```text
Documentation Assembly Pipeline
Code Assembly Pipeline
Governance / Control Module
Evidence flow
human review flow
approval / rejection boundary
```

Главная цель `aos-farm` — снизить риск ложной уверенности при AI-assisted разработке.

Проект должен предотвращать:

```text
fake PASS
fake approval
скрытую lifecycle mutation
скрытое расширение scope
непроверенные protected/canonical изменения
destructive operations по умолчанию
превращение agent-generated artifacts в решения человека
```

## 2. Статус этой конституции

Эта конституция управляет только sandbox-репозиторием `aos-farm`.

Она не управляет основным репозиторием AOS-1.

Она не заменяет required AOS-1 sources.

Она не становится вторым Source of Truth для AOS-1.

Если эта конституция конфликтует с required AOS-1 sources, побеждают required AOS-1 sources.

Если корректная интерпретация неизвестна, результат:

```text
UNKNOWN_BLOCKED
```

## 3. Source Precedence

Порядок authority:

```text
1. 00_AOS_Core_Control.md
2. 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
3. 02_AOS_Governance_Control_Module_and_Safety_Rules.md
4. Эта constitution aos-farm
5. Target state documents внутри aos-farm
6. Reference documents внутри aos-farm
7. Spec Kit defaults
8. Optional references
9. Agent-generated notes
```

`00_AOS_Core_Control.md` имеет высший приоритет для:

```text
project control
Source of Truth
skeleton authority
documentation strategy
legacy boundary
core invariants
```

`01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` имеет authority для:

```text
Documentation Assembly Pipeline
Code Assembly Pipeline
Build Step roadmap
daily workflow
role matrix
first dogfood flow
```

`02_AOS_Governance_Control_Module_and_Safety_Rules.md` имеет authority для:

```text
safety
Risk Profiles
Control Gates
approval boundary
lifecycle boundary
protected/canonical rules
destructive operations
UNKNOWN
NOT_RUN
PASS / Evidence / approval semantics
```

Если `01` и `02` конфликтуют по safety/control-семантике, побеждает `02`, если `00` явно не говорит иначе.

## 4. Идентичность проекта

AOS-1 / AgentOS Next — это Markdown-first governance system для AI-assisted software development.

Базовый путь работы:

```text
идея
→ документация
→ задача
→ scoped execution
→ Evidence
→ human review
→ approval / rejection
```

Система должна помогать не программисту, vibe coder и владельцу проекта работать с AI-агентами без слепого доверия к agent claims.

Система должна считать документацию, границы задачи, Evidence и human checkpoints полноценными частями разработки.

## 5. Граница sandbox

`aos-farm` — это farm/sandbox, не production.

`aos-farm` можно использовать для проверки:

```text
структуры
workflow
templates
task briefs
target state documents
controlled assembly logic
agent instructions
Evidence reports
review packages
```

`aos-farm` нельзя использовать для скрытого изменения canonical AOS-1 sources.

Разрешено внутри `aos-farm` после явного approval человека:

```text
1. Создавать sandbox documents.
2. Создавать target state documents.
3. Создавать test specifications.
4. Создавать execution packages для sandbox tasks.
5. Создавать Evidence reports для sandbox tasks.
6. Сравнивать sandbox behavior с required AOS-1 sources.
7. Готовить human review packages.
```

Запрещено без явного approval человека:

```text
1. Изменять canonical AOS-1 repository.
2. Считать sandbox output canonical.
3. Считать sandbox PASS approval.
4. Считать sandbox Evidence approval.
5. Push, merge, release или publish как canonical.
6. Изменять protected/canonical files.
7. Выполнять destructive operations.
8. Расширять scope.
9. Назначать LOW_RISK_FAST автоматически.
10. Автоматически запускать следующий lifecycle stage.
```

## 6. Spec Kit Boundary

Spec Kit используется только как scaffold и workflow substrate.

Spec Kit не является Source of Truth для AOS-1.

Spec Kit generated artifacts являются drafts до human review.

Spec Kit может помогать структурировать:

```text
constitution
specification
planning
tasks
implementation packages
```

Spec Kit не может переопределять AOS-1 governance.

Запрещено без явного approval человека:

```text
1. Автоматически заполнять эту constitution как final.
2. Считать generated specs утверждёнными.
3. Считать generated tasks исполнимыми без review.
4. Запускать implementation из generated tasks без approval.
5. Считать Spec Kit validation human approval.
6. Считать Spec Kit project structure canonical AOS-1 architecture.
```

## 7. Minimal Safety Floor

Minimal Safety Floor активен с первого дня.

Всегда действуют инварианты:

```text
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
Metrics ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.
BLOCKED ≠ PASS.
Human approval cannot be simulated.
Skeleton ≠ implementation.
Scope must not expand without explicit human permission.
Readiness ≠ execution permission.
Report ≠ lifecycle mutation.
Task completion ≠ approval.
```

Любой документ, отчёт, task brief, Spec Kit output или agent response, который нарушает эти инварианты, считается недействительным для принятия решений.

## 8. Approval Boundary

Только человек может дать approval.

Агент может:

```text
1. Подготовить draft.
2. Подготовить Evidence.
3. Подготовить review package.
4. Предложить Risk Profile.
5. Указать blockers.
6. Указать UNKNOWN.
7. Указать NOT_RUN.
8. Указать, что требуется human review.
```

Агент не может:

```text
1. Симулировать approval человека.
2. Назначать финальный approval.
3. Утверждать protected/canonical changes.
4. Самостоятельно назначать LOW_RISK_FAST.
5. Переводить lifecycle state без explicit human approval.
6. Объявлять готовность к production.
7. Объявлять release.
8. Объявлять merge-approved.
```

Формула:

```text
Agent report is claim.
Agent-written trace is claim.
Runner artifact is Evidence.
Human approval remains above every PASS.
```

## 9. Evidence Boundary

Evidence — это доказательный материал, а не approval.

Evidence может включать:

```text
command output
validation report
file inventory
diff summary
test output
logs
checksums
source availability report
review matrix
```

Evidence не может означать:

```text
approval
merge permission
release permission
lifecycle mutation
scope expansion
protected/canonical permission
```

Если Evidence отсутствует:

```text
Evidence status = NOT_RUN or MISSING
NOT_RUN ≠ PASS
MISSING ≠ PASS
```

Если Evidence неполное:

```text
Evidence status = INCOMPLETE
INCOMPLETE ≠ PASS
```

Если Evidence противоречит claim агента:

```text
claim_status = BLOCKED
human_review_required = true
```

## 10. UNKNOWN и NOT_RUN

`UNKNOWN` не является допустимым положительным состоянием.

Если критически важная информация неизвестна, задача должна быть заблокирована или передана на human review.

Правила:

```text
UNKNOWN ≠ OK
UNKNOWN ≠ PASS
UNKNOWN ≠ approval
UNKNOWN → UNKNOWN_BLOCKED
```

`NOT_RUN` означает, что проверка не выполнялась.

Правила:

```text
NOT_RUN ≠ PASS
NOT_RUN ≠ Evidence
NOT_RUN ≠ approval
NOT_RUN → BLOCKED unless explicitly allowed as non-blocking informational field
```

Нельзя заменять `UNKNOWN` или `NOT_RUN` предположением агента.

## 11. Scope Control

Каждая task должна иметь явный scope.

Scope должен включать:

```text
allowed files
forbidden files
allowed operations
forbidden operations
expected outputs
validation requirements
non-goals
final report requirements
```

Scope не может расширяться автоматически.

Если агент обнаруживает полезную дополнительную работу, он должен зафиксировать её как:

```text
candidate_follow_up
human_review_required: true
not_executed: true
```

Агент не должен выполнять такую работу без explicit human permission.

## 12. Protected / Canonical Boundary

Protected/canonical files требуют human checkpoint.

К protected/canonical зонам относятся:

```text
required AOS-1 sources
constitution
governance contracts
approval rules
lifecycle rules
validation authority
Risk Profile rules
Source of Truth declarations
canonical templates
canonical schemas
canonical validators
release/merge rules
```

Protected/canonical changes требуют:

```text
1. Явного указания exact path.
2. Обоснования.
3. Risk Profile.
4. Human checkpoint.
5. Evidence.
6. Final human approval.
```

Без этих условий статус:

```text
HUMAN_REVIEW_REQUIRED
```

или

```text
BLOCKED
```

## 13. Destructive Operations

Destructive operations запрещены по умолчанию.

К destructive operations относятся:

```text
delete
move
rename
archive
compress
overwrite
history rewrite
force push
cleanup
mass formatting
bulk rewrite
schema replacement
validator weakening
```

Destructive operations разрешены только при наличии:

```text
explicit human approval
exact scope
rollback plan
pre-change Evidence
post-change Evidence
validation
human checkpoint
```

Если хотя бы одно условие отсутствует:

```text
destructive_operation_status: BLOCKED
```

## 14. Skeleton Boundary

Skeleton не является implementation.

Skeleton может включать:

```text
folders
empty files
placeholder documents
templates
schemas draft
task brief draft
target state outline
reference index
```

Skeleton не может заявлять:

```text
feature implemented
pipeline implemented
validator implemented
governance enforced
runtime enforced
production ready
approved
```

Любой skeleton artifact должен явно указывать:

```text
skeleton_status: draft_or_placeholder
implementation_status: not_implemented
approval_status: not_approved
```

## 15. Documentation Assembly Pipeline

Documentation Assembly Pipeline должен собирать смысловую структуру AOS-1 перед code execution.

Он должен поддерживать:

```text
source intake
source precedence
project skeleton
target state
feature specification
task decomposition
review package
Evidence report
human decision boundary
```

Documentation Assembly Pipeline не должен:

```text
1. Автоматически создавать approval.
2. Подменять human review.
3. Запускать Code Assembly Pipeline без gate.
4. Изменять lifecycle без approval.
5. Считать документацию implementation.
```

## 16. Code Assembly Pipeline

Code Assembly Pipeline может начинаться только после достаточной документационной подготовки и human approval.

Он должен быть связан с:

```text
approved task brief
exact scope
allowed paths
forbidden paths
Risk Profile
validation plan
Evidence requirements
rollback or recovery expectations
```

Code Assembly Pipeline не должен запускаться из `aos-farm` автоматически.

`aos-farm` может моделировать Code Assembly Pipeline, но не должен выдавать simulation за production implementation.

## 17. Governance / Control Module

Governance / Control Module — активный термин для слоя safety/control.

Старый термин Protective Pipeline является legacy reference only.

Governance / Control Module должен обеспечивать:

```text
scope control
approval boundary
Evidence boundary
UNKNOWN handling
NOT_RUN handling
Risk Profile handling
protected/canonical checks
destructive operation blocking
lifecycle mutation blocking
false PASS resistance
```

Governance / Control Module не должен становиться автономным approval system.

Его результат:

```text
Evidence
status
blocker
warning
human_review_required
```

но не:

```text
human approval
```

## 18. Risk Profile Rules

Risk Profile должен быть определён до execution.

Агент может предложить Risk Profile, но не может сам назначить `LOW_RISK_FAST`.

Если Risk Profile неизвестен:

```text
risk_profile_status: UNKNOWN_BLOCKED
execution_allowed: false
```

Если задача касается protected/canonical files:

```text
risk_profile_minimum: HIGH_RISK_PROTECTED
human_checkpoint_required: true
```

Если задача включает destructive operations:

```text
risk_profile_minimum: DESTRUCTIVE_OR_CANONICAL
human_checkpoint_required: true
rollback_required: true
```

Если задача является sandbox-only и documentation-only:

```text
suggested_risk_profile: MEDIUM_RISK_GUIDED
```

Окончательное назначение Risk Profile делает человек.

## 19. Lifecycle Boundary

Lifecycle state не может меняться автоматически.

К lifecycle mutation относятся:

```text
DRAFT → READY_FOR_EXECUTION
READY_FOR_EXECUTION → APPROVED
APPROVED → EXECUTED
EXECUTED → COMPLETE
COMPLETE → RELEASED
BLOCKED → READY
REJECTED → READY
```

Агент не может выполнять lifecycle mutation без explicit human approval.

Readiness report не является lifecycle mutation.

Completion review не является approval.

PASS не является lifecycle mutation.

## 20. Agent Operating Rules

Агент в `aos-farm` должен:

```text
1. Читать required sources перед архитектурными решениями.
2. Указывать недоступные required sources.
3. Работать fail-closed.
4. Явно отделять claim от Evidence.
5. Явно отделять PASS от approval.
6. Явно отделять draft от approved.
7. Явно отделять skeleton от implementation.
8. Указывать UNKNOWN.
9. Указывать NOT_RUN.
10. Останавливать выполнение при human approval boundary.
```

Агент не должен:

```text
1. Симулировать human approval.
2. Скрывать UNKNOWN.
3. Скрывать NOT_RUN.
4. Расширять scope.
5. Изменять protected/canonical files без checkpoint.
6. Выполнять destructive operations без approval.
7. Запускать implementation без approval.
8. Делать commit/push/merge/release без approval.
9. Создавать production claims из sandbox artifacts.
10. Подменять AOS-1 required sources Spec Kit defaults.
```

## 21. Reports and Evidence

Каждая значимая задача должна завершаться report.

Report должен включать:

```yaml
task_id: value
scope_status: value
risk_profile: value_or_unknown
human_approval_required: true_or_false
human_approval_received: true_or_false
files_created: list
files_modified: list
files_deleted: list
commands_run: list
validation_status: value
not_run_items: list
unknowns: list
blockers: list
evidence_paths: list
approval_claimed_by_agent: false
lifecycle_mutation_claimed_by_agent: false
final_status: value
```

Если validation не запускалась:

```yaml
validation_status: NOT_RUN
not_run_is_pass: false
```

Если Evidence отсутствует:

```yaml
evidence_status: MISSING
evidence_is_approval: false
```

## 22. Target State Rule

Target state documents описывают желаемое состояние.

Target state не является implementation.

Target state не является approval.

Target state не является permission to execute.

Target state documents должны явно отделять:

```text
desired structure
current state
known gaps
unknowns
blockers
required human decisions
```

Если current state неизвестен:

```text
current_state: UNKNOWN
status: UNKNOWN_BLOCKED
```

## 23. Reference Rule

Reference documents внутри `aos-farm` являются навигационными.

Они не являются canonical source.

Reference documents должны указывать:

```text
reference_only: true
canonical_authority: external_required_aos_sources
```

Optional references могут использоваться только для контекста.

Optional references не могут:

```text
1. Переопределять required sources.
2. Создавать roadmap authority.
3. Создавать execution permission.
4. Создавать approval.
5. Разрешать protected/canonical changes.
```

## 24. Human Review Rule

Human review требуется для:

```text
constitution approval
Risk Profile assignment
execution authorization
protected/canonical changes
destructive operations
remote repository creation
commit approval
push approval
merge approval
release approval
lifecycle mutation
scope expansion
```

Если человек недоступен, статус:

```text
HUMAN_REVIEW_REQUIRED
```

или

```text
BLOCKED
```

Агент не может заменить человека.

## 25. Final Status Semantics

Разрешённые статусы для sandbox setup и planning tasks:

```text
DRAFT
READY_FOR_HUMAN_REVIEW
HUMAN_REVIEW_REQUIRED
READY_FOR_EXECUTION_AFTER_HUMAN_APPROVAL
BLOCKED
UNKNOWN_BLOCKED
REJECTED
```

Запрещённые agent-assigned статусы:

```text
APPROVED
HUMAN_APPROVED
MERGE_APPROVED
RELEASE_APPROVED
PRODUCTION_READY
CANONICAL_COMPLETE
```

Агент может использовать `APPROVED` только если он цитирует уже существующее explicit human approval и указывает Evidence этого approval.

## 26. Commit / Push / Remote Boundary

Без отдельного approval человека запрещено:

```text
git commit
git push
remote repository creation
pull request creation
merge
release
tag creation
branch protection changes
workflow activation
required checks activation
```

Если человек разрешил local-only setup, это не означает разрешение на remote operations.

Если человек разрешил file creation, это не означает разрешение на commit.

Если человек разрешил commit, это не означает разрешение на push.

Если человек разрешил push, это не означает разрешение на merge.

## 27. Project Success Definition

`aos-farm` успешен, если он помогает безопасно собрать и проверить AOS-1 conveyor without false approval.

Успех означает:

```text
clear source precedence
clear sandbox boundary
clear target state
clear task decomposition
clear Evidence flow
clear human review points
clear approval boundary
clear lifecycle boundary
clear blocked states
clear UNKNOWN handling
```

Успех не означает:

```text
autonomous implementation
automatic approval
automatic lifecycle mutation
production readiness
canonical replacement
```

## 28. Constitution Change Rule

Эта constitution может изменяться только через human-approved change.

Каждое изменение constitution должно иметь:

```text
reason
exact changed sections
risk assessment
human review
approval evidence
change date
```

Агент не может самостоятельно обновлять constitution.

Если constitution требует изменения, агент должен создать:

```text
constitution_change_candidate
human_review_required: true
not_applied: true
```

## 29. Current Constitutional Status

```yaml
constitution_status: DRAFT_HUMAN_REVIEW_REQUIRED
human_approved: false
agent_generated: true
canonical_for_aos_1: false
canonical_for_aos_farm_after_human_approval: pending
implementation_authorized_by_this_document: false
execution_authorized_by_this_document: false
lifecycle_mutation_authorized_by_this_document: false
```

## 30. Final Constitutional Rule

This constitution is not approval.

This constitution is not Evidence.

This constitution is not implementation.

This constitution does not authorize execution.

This constitution does not authorize lifecycle mutation.

This constitution does not authorize protected/canonical changes.

This constitution does not authorize destructive operations.

PASS ≠ approval.

Evidence ≠ approval.

CI PASS ≠ approval.

UNKNOWN ≠ OK.

NOT_RUN ≠ PASS.

Human approval cannot be simulated.

Skeleton ≠ implementation.

Scope must not expand without explicit human permission.

Minimal Safety Floor is always-on.
