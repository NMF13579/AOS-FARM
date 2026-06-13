# Task Brief: Build Step 0

## Mode

HIGH_RISK_PROTECTED (Одобрено человеком в рамках Implementation Plan)

## Repository

AOS-FARM

## Branch

main (или текущая ветка)

## Risk Profile Assignment

- proposed_by_agent: HIGH_RISK_PROTECTED
- assigned_by_human: HIGH_RISK_PROTECTED
- assignment_evidence: Explicit human approval in Agent's Implementation Plan for rebuilding from scratch.

## Context

Мы начинаем полную пересборку конвейеров AOS-1 с нуля. Build Step 0 должен зафиксировать стратегию `assembly-first` и определить правила ветвления (branch strategy). Старые тяжеловесные планы отмечаются как справочные. 

## Goal

Зафиксировать final assembly-first strategy и сохранить dev skeleton baseline.

## Scope

- Создание `Strategy Lock` документа, включающего branch strategy.
- Создание `Execution Report` и `Evidence Report` по факту выполнения.
- Никакого рантайма или исполнения кода.

## Rules

- Не мутировать lifecycle без правила.
- Не пытаться выполнить код или создать исполняемые модули.
- PASS ≠ approval.
- Ожидать Human Review после завершения.

## Allowed Changes

- `agentos/tasks/build-step-0.md` (текущий файл)
- `agentos/docs/strategy-lock.md`
- `agentos/reports/build-step-0/execution-report.md`
- `agentos/reports/build-step-0/evidence-report.md`

## Forbidden Changes

- Любые файлы вне папки `agentos/` (за исключением этого ограничения, мы ничего не удаляем из существующих).
- Никаких destructive operations.

## Required Behavior / Content

- Сгенерировать Strategy Lock (YAML/Markdown).
- Отчитаться в Execution Report.
- Прикрепить Evidence Report (список созданных файлов).

## Non-Goals

- no runtime
- no cleanup
- no implementation
- no protected changes to existing root files
- no stage execution (переход на Step 1)

## Validation

- validator_status: NOT_RUN (нет физического валидатора на этом этапе).
- Ручная проверка файлов человеком (Human Review Gate).

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.

## Final Boundary Rule

No approval, no lifecycle mutation, no next-stage start unless explicitly authorized by Human.
