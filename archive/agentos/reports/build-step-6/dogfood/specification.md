# Specification (Dogfood Trial)

## Метаданные

```yaml
document_type: specification
project: Dogfood Test
feature: Create Dogfood File
status: READY_FOR_REVIEW
```

## 1. Expected Behavior (Ожидаемое поведение)
В корне проекта (AOS-FARM) должен появиться файл с именем `.dogfood-test`. Файл может быть пустым или содержать тестовую строку "AOS-1 Dogfood Trial".

## 2. Технические рамки (Technical Scope)
- Затрагиваемые компоненты: файловая система (корень репозитория).

## 3. Data Flow / State
В репозиторий добавляется один новый untracked файл.

## 4. Критерии приемки (Acceptance Criteria)
- [ ] Файл `.dogfood-test` существует в корне.
- [ ] Конвейеры отработали без нарушения `Minimal Safety Floor`.

## Ограничение ответственности
Данная спецификация не разрешает выполнение.
