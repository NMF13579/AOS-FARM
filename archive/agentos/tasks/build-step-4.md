# Task Brief: Build Step 4

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

Мы заложили фундамент документации и базовые правила безопасности (Steps 1-3). Теперь нам нужно определить второй основной слой: Code Assembly Pipeline, который будет строить код внутри рамок, заданных Task Brief. Для начала нам нужен контракт.

## Goal

Определить, как Task Brief превращается в scoped code change (создать Code Assembly Pipeline Contract).

## Scope

Создание документа `agentos/docs/code-pipeline-contract.md`, который опишет:
- code execution package contract (как агент получает и выполняет код).
- diff/evidence expectations (какие доказательства кода требуются).
- allowed/forbidden change handling (поведение агента при выходе за рамки).
- manual review requirement.

Создание `Execution Report` и `Evidence Report` по шагу 4.

## Rules

- Должно соответствовать `Minimal Safety Floor`.
- Строгий запрет на автоматический мерж.

## Allowed Changes

- `agentos/tasks/build-step-4.md` (этот файл)
- `agentos/docs/code-pipeline-contract.md`
- `agentos/reports/build-step-4/execution-report.md`
- `agentos/reports/build-step-4/evidence-report.md`

## Forbidden Changes

- Модификация `minimal-safety-floor.md`.
- Создание скриптов автоматизации (это не runtime enforcement).

## Validation

- validator_status: NOT_RUN
- Ручная проверка контракта человеком.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
