# Technical Assignment Methodology Package

Пакет документов для AOS-FARM / AgentOS workflow по созданию технического задания агентом.

Целевой путь в репозитории:

```text
agentos/docs/methodology/technical-assignment/
```

## Состав core-пакета

- `00-overview-and-routing.md` — обзор пакета и стартовый routing.
- `01-human-methodology.md` — человекочитаемая методология.
- `02-agent-contract.md` — machine-readable контракт агента в Markdown.
- `03-data-discovery-and-access.md` — сбор данных, потоки информации, роли и доступы.
- `04-draft-artifact-templates.md` — шаблоны draft artifacts.
- `05-safety-gates-and-statuses.md` — safety gates, статусы и fail-closed правила.
- `06-domain-extension-interface.md` — интерфейс отраслевых extensions.
- `07-consistency-checklist.md` — ручная проверка согласованности до появления validator.
- `08-interview-depth-loop-and-entity-process-traversal.md` — правила глубины интервью и Entity-Process Traversal.
- `09-adaptive-elicitation-method-selector.md` — логика выбора метода интервью на основе ответов.
- `10-ta-intake-to-documentation-assembly-bridge.md` — bridge contract от TA intake drafts к Documentation Assembly candidate inputs.

## Runbooks

- `runbooks/` — модульные методики интервью (Five Whys, JTBD, Scenario Walkthrough и др.). Эти runbooks являются вспомогательными инструментами для интервью и не дают разрешения на реализацию.

## Domain extensions

- `extensions/medical-intake-extension.md` — медицина / healthcare.
- `extensions/construction-intake-extension.md` — строительство.
- `extensions/education-intake-extension.md` — образование.
- `extensions/domain-extension-template.md` — шаблон нового отраслевого extension.

## Граница полномочий

Пакет разрешает только сбор входных данных и создание draft-документов.

Он не разрешает implementation, execution, commit, push, deploy, release, production use, stack selection, Risk Profile assignment, final database schema или lifecycle promotion.

Bridge output из этого пакета является только candidate input для Documentation Assembly Pipeline. Он не является approval, execution authorization, final Task Brief или lifecycle promotion.
