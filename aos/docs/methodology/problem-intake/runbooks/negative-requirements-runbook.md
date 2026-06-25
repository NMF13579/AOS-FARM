# Negative Requirements

**Status:** DRAFT_METHOD  
**Runtime implementation:** not authorized  
**Execution authorized:** false  
**Approval status:** NOT_APPROVED  

## Purpose

Identify what the system must not do, who must not access data, what failures matter, and which safety/privacy/SLA constraints apply.

## When To Use

Sensitive data, fear, security, privacy, SLA, compliance, high impact context.

## When Not To Use

When there are strictly no risks or standard non-sensitive tools are discussed.

## User-Facing Explanation

"Чтобы избежать критических ошибок, давайте опишем сценарии того, чего система делать категорически не должна."

## One-Question-at-a-Time Flow

Agent asks negative constraints sequentially. One question per turn.

## Required Questions

Anti-goals.
Forbidden actions.
Forbidden access.
Sensitive data.
Unavailable system scenario.
Compromised system scenario.
High-impact risk.

## Follow-Up Triggers

Vague constraints like "system must be secure" without specific boundaries.

## Completion Criteria

Major forbidden paths, boundaries, and failure thresholds are documented.

## Output Fields

- anti_goals
- forbidden_actions
- forbidden_access
- sensitive_data_flags
- sla_candidates
- privacy_constraints
- human_review_required

## Hard Constraints and Never-Do Questions

Примеры обязательных вопросов:
- Что система никогда не должна делать?
- Какие действия она должна выполнять только после вашего подтверждения?
- Кому система никогда не должна показывать эти данные?
- Какая ошибка будет самой опасной?
- Что нельзя автоматизировать полностью?
- Что должно остаться под Human review?
- Кто ещё должен это одобрить?

```yaml
hard_constraints_output_fields:
  - never_do_actions
  - forbidden_access
  - human_review_required_actions
  - dangerous_error_modes
  - non_automatable_steps
  - hidden_approvers
  - compliance_or_policy_constraints
```

Invariants:
```text
Never-do answer ≠ final security policy.
Hidden approver mention ≠ approved approval flow.
Human review required ≠ execution approval.
```

## Skip / Return Behavior

User may skip and return later. Skip is recorded.

## Safety Boundaries

Runbook completion ≠ PASS.
Runbook completion ≠ approval.
Runbook output ≠ execution authorization.
User answer ≠ approval.
Human approval cannot be simulated.

## Final Rule

This runbook does not authorize execution or approval.
