# Human Review Template

## Metadata

```yaml
task: [Task ID / Name]
reviewed_by: [Human Name / ID]
date: [Date]
decision: [APPROVED / REJECTED / CHANGES_REQUESTED]
```

## Review Checklist

- [ ] Scope соблюден? (Никаких скрытых изменений).
- [ ] Evidence Report присутствует и соответствует заявленному в Execution Report?
- [ ] Destructive/Canonical changes (если были) корректны?
- [ ] Валидаторы прошли успешно (если применимо)?

## Decision / Comments

[Комментарий ревьюера. Если APPROVED, указать явное разрешение на переход к следующему этапу или мерж. Если REJECTED, указать причины.]

## Signature

Одобрение данного документа является финальным `Human Approval` для связанного Task Brief.
