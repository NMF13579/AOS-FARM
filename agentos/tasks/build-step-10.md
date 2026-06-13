# Task Brief: Build Step 10

## Mode

HIGH_RISK_PROTECTED (Определено в Roadmap)

## Repository

AOS-FARM

## Branch

main (или текущая ветка)

## Risk Profile Assignment

- proposed_by_agent: HIGH_RISK_PROTECTED
- assigned_by_human: [Ожидает подтверждения]
- assignment_evidence: Требуется утверждение вместе с запуском этого шага.

## Context

Мы зафиксировали правила для Thin Validator (Step 9). Теперь мы должны физически написать этот скрипт, чтобы конвейер мог автоматически блокировать нарушителей (включая агента, если он ошибется).

## Goal

Реализовать один быстрый validator для заданных deterministic checks.

## Scope

Создать исполняемый скрипт валидатора `agentos/scripts/thin-validator.sh` (или `.py`), который будет парсить Markdown/YAML файлы отчетов и задач и проверять их на соответствие `thin-validator-contract.md`.

Создать `Execution Report` и `Evidence Report` по шагу 10.

## Rules

- No broad script suite (только один скрипт).
- No auto-fix by default.
- Fail-closed semantics: если файл не удается прочитать, валидатор должен падать с ошибкой (exit code > 0).

## Allowed Changes

- `agentos/tasks/build-step-10.md` (этот файл)
- `agentos/scripts/thin-validator.sh` (или `.py`)
- `agentos/reports/build-step-10/execution-report.md`
- `agentos/reports/build-step-10/evidence-report.md`

## Forbidden Changes

- Автоматическое подключение скрипта к git pre-commit hooks (настраивается отдельно, если нужно).

## Validation

- validator_status: NOT_RUN (при самом создании)
- (По желанию) Можно запустить скрипт на файлах из догфуда (Step 6) для проверки.

## Expected Final Report

Execution Report с указанием статуса `READY_FOR_REVIEW`.
