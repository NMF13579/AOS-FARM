# Task Brief: Build Step 11

## Mode

MEDIUM_RISK_GUIDED (Определено в Roadmap)

## Repository

AOS-FARM

## Branch

main (или текущая ветка)

## Risk Profile Assignment

- proposed_by_agent: MEDIUM_RISK_GUIDED
- assigned_by_human: [Ожидает подтверждения]
- assignment_evidence: Требуется утверждение вместе с запуском этого шага.

## Context

Валидатор написан, но он запускается только вручную. В будущем нам понадобится полноценный автоматический контроль исполнения (Runtime Enforcement), чтобы физически блокировать недопустимые команды и запись в файлы. На 11-м шаге мы должны спланировать это внедрение.

## Goal

Спланировать future Runtime Enforcement без внедрения раньше времени.

## Scope

Создать документ `agentos/docs/runtime-enforcement-plan.md`, в котором спланировать:
- command allowlist
- write allowlist
- protected path guard
- commit/push guard
- audit log

Создать `Execution Report` и `Evidence Report` по шагу 11.

## Rules

- No runtime implementation! Только план. 

## Allowed Changes

- `agentos/tasks/build-step-11.md` (этот файл)
- `agentos/docs/runtime-enforcement-plan.md`
- `agentos/reports/build-step-11/execution-report.md`
- `agentos/reports/build-step-11/evidence-report.md`

## Forbidden Changes

- Любое изменение файлов конфигурации GitHub Actions, git hooks, Makefile или других исполняемых элементов системы.

## Validation

- validator_status: NOT_RUN
- Ручная проверка документа человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
