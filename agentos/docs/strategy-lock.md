# Strategy Lock (Build Step 0)

## Статус

```yaml
document_type: strategy_lock
project: AOS-1 / AgentOS Next
status: active_baseline
source_pack_role: core_required
language: ru
owner: human
```

## Assembly-First Strategy

1. **Документация управляет Кодом:** Documentation Assembly Pipeline определяет рамки (scope, tasks). Code Assembly Pipeline выполняет работу строго внутри этих рамок.
2. **Minimal Safety Floor:** Защитные механизмы включены с нулевого дня (PASS ≠ approval, Evidence ≠ approval).
3. **Нет симуляции решений:** Агент не генерирует fake human approvals.
4. **Постепенное наращивание Governance:** Управление (gates, validators, runtime enforcement) вводится шаг за шагом, как независимый слой поверх сборки.

## Branch Strategy

- **main:** Защищенная ветка (Protected/Canonical). Любые изменения требуют Human Checkpoint и approval.
- **feature/*:** Ветки для выполнения изолированных Task Briefs. 
- **agentos/drafts/*:** Разрешенная зона для non-canonical черновиков. 

## Legacy Strategy (Reference Only)

Любые старые планы (old milestone-heavy plans), которые противоречат Assembly-First Strategy, признаются устаревшими (reference only). Они могут использоваться только для извлечения принципов или features candidates через `ROADMAP_ADMISSION_RECORD`, но не авторизуют execution.

## Baseline
С этого момента все дальнейшие шаги (Build Steps 1-12) используют данный документ в качестве базиса и не могут нарушать или обходить установленную стратегию.
