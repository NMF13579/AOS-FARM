# Token Budget and Model Routing Policy

## Purpose
To optimize API costs while preserving strict safety guarantees. Model tiering allows using smaller models for mechanical tasks while reserving expensive models for architecture, safety bounds, and protected modifications.

## Token / Session Continuity
Workflow must survive token context limits. The Controller must stop operations before the context limit is reached and emit a handoff artifact.

## Cost-Aware Model Tiering

### Cheap Model
- **Allowed Tasks:** `git status` summary, file existence checks, handoff generation, exact file list comparisons, simple report formatting, template filling, non-semantic markdown cleanup.
- **Forbidden Tasks:** Architecture decisions, Risk Profile downgrade, approval-boundary interpretation, protected/canonical decisions, runtime/validator/CI safety design, source precedence conflict resolution.

### Standard Model
- **Allowed Tasks:** Normal controlled execution, docs/templates creation, ordinary verification, next-task prompt generation, non-protected workflow documentation.

### Expensive Model
- **Required Tasks:** Architecture decisions, Deep Step Audit, safety semantics, protected/canonical changes, Governance/Control Module design, validator/runtime planning, source conflicts, suspected semantic drift.

## Continuity and Recovery Rules
1. **Stop Before Limit:** Do not start a commit or push operation if the session is unstable or near its token limit.
2. **Verification Recovery:** If files were changed but not verified before an interruption, the next task must be verification and recovery.
3. **Commit Recovery:** If staging happened but commit did not, the next task must inspect the cached diff and fail closed unless authorized.
4. **Push Recovery:** If a commit happened but push authorization was not prepared, the next task must prepare post-commit recovery.
5. **Closure Recovery:** If a push happened but a closure report was not created, the next task must be post-push closure recovery.
6. **Safety First:** Cost optimization must never weaken safety gates.
