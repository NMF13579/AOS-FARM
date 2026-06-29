---
example_only: true
authoritative: false
---
> [!WARNING]
> This is an example document only. It is non-authoritative and does not represent actual execution history or approval.

# Negative Force Push Claimed Checkpoint Fixture

checkpoint_type: push_authorization
push_authorized: true
human_decision_required: false
force_push_authorized: true
tag_push_authorized: false
merge_authorized: false
release_authorized: false
next_task_authorized: false
push_performed: false

Why blocked:
- force_push_authorized must be false.
