# Human Approval Boundary Template

> **Внимание для пользователя (Attention):** 
> Этот шаблон — ЧЕРНОВИК (DRAFT). Наличие этого файла **не означает одобрения** (Evidence ≠ approval).
> Агент обязан остановиться (Stop here) и ждать вашего явного решения.
> Human Authorization required.

This template records a checkpoint boundary. It does not create human approval by itself.

## 1. Checkpoint Identity
- Checkpoint ID: 

## 2. Proposed Action
- Action: 

## 3. Required Human Decision
- Decision: 

## 4. Agent Preparation Boundary
- Agent has prepared the artifacts but not executed unauthorized actions.

## 5. Human Authorization Block

```yaml
checkpoint_status: PENDING_HUMAN_REVIEW
human_approval_recorded: false
human_decision: PENDING
execution_authorized: false
commit_authorized: false
push_authorized: false
release_authorized: false
production_use_authorized: false
human_signature: PENDING
```

## 6. Explicitly Unauthorized Actions
- List of explicitly unauthorized actions.

## 7. Final Status
- Status: 
