# Task Queue Template

```yaml
schema_version: 1
queue_revision: 2026-06-27-01
queue_items:
  - queue_item_id: AOS-FARM.QUEUE.2026-06-27-01.001
    queue_revision: 2026-06-27-01
    queue_order: "001"
    task_id: AOS-FARM.XXX
    status: QUEUED
    source_file: null
    source_commit: null
    source_hash: null
    indexed_at: null
```

## Template Rules
- Queue item ID is stable.
- Queue order is not identity.
- Queue order changes require new queue_revision.
- Queue may report current/next task.
- Queue must not approve, authorize, execute, commit, or push.
