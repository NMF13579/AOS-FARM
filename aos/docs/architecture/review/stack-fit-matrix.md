---
task_id: AOS-FARM.621
document_type: stack_fit_matrix
matrix_status: INCOMPLETE_WEIGHTS
approval_status: NOT_REQUESTED
human_weight_required: true
human_review_required: true
default_stack_selected: false
---

# Stack Fit Matrix

This matrix compares existing stack presets as candidate-only architecture evidence.
It does not select a default stack and does not authorize implementation.

## Stack candidates

| Stack preset | Candidate notes |
|---|---|
| STACK-PRESET-001 local-markdown-cli | Strong fit for local-first Markdown governance and low runtime authority. |
| STACK-PRESET-002 python-cli-tool | Strong fit for validator and tooling workflows; usability depends on CLI comfort. |
| STACK-PRESET-003 static-docs-site | Strong fit for read-only publication; limited for workflow mutation. |
| STACK-PRESET-004 nextjs-supabase-saas | Strong product surface potential; higher operational burden and external service dependency. |
| STACK-PRESET-005 fastapi-postgres-api | Strong integration potential; increases runtime authority and infrastructure scope. |
| STACK-PRESET-006 telegram-bot | Useful guided interaction surface; external platform dependency and command safety require review. |
| STACK-PRESET-007 electron-local-app | Strong non-programmer local UX potential; packaging and update complexity require review. |

## Criteria weights

| Criterion | Weight | Human weight required | Evidence source |
|---|---|---|---|
| Markdown-first compatibility | UNASSIGNED_BY_HUMAN | true | ADR-0001 |
| Validator-first lifecycle | UNASSIGNED_BY_HUMAN | true | ADR-0002 |
| Human-gated approval | UNASSIGNED_BY_HUMAN | true | ADR-0005 |
| Local-first operation | UNASSIGNED_BY_HUMAN | true | registry / project constraint |
| Non-programmer usability | UNASSIGNED_BY_HUMAN | true | project constraint |
| Safe installer boundary | UNASSIGNED_BY_HUMAN | true | ADR-0004 |
| Low operational burden | UNASSIGNED_BY_HUMAN | true | project constraint |
| Extensibility | UNASSIGNED_BY_HUMAN | true | registry |
| Fail-closed semantics | UNASSIGNED_BY_HUMAN | true | project constraint |
| Minimal runtime authority | UNASSIGNED_BY_HUMAN | true | ADR-0003 / project constraint |
| No autonomous runner by default | UNASSIGNED_BY_HUMAN | true | ADR-0003 |
| Product folder boundary preservation | UNASSIGNED_BY_HUMAN | true | project constraint |

## Candidate observations

| Criterion | local-markdown-cli | python-cli-tool | static-docs-site | nextjs-supabase-saas | fastapi-postgres-api | telegram-bot | electron-local-app |
|---|---|---|---|---|---|---|---|
| Markdown-first compatibility | High | High | High | Medium | Medium | Medium | High |
| Validator-first lifecycle | Medium | High | Medium | Medium | High | Medium | Medium |
| Human-gated approval | High | High | High | Medium | Medium | Medium | Medium |
| Local-first operation | High | High | Medium | Low | Medium | Low | High |
| Non-programmer usability | Medium | Medium | High | High | Low | High | High |
| Safe installer boundary | High | Medium | High | Medium | Medium | Medium | Medium |
| Low operational burden | High | High | High | Low | Medium | Medium | Medium |
| Extensibility | Medium | High | Medium | High | High | Medium | Medium |
| Fail-closed semantics | High | High | High | Medium | Medium | Medium | Medium |
| Minimal runtime authority | High | High | High | Low | Medium | Low | Medium |
| No autonomous runner by default | High | High | High | Medium | Medium | Medium | Medium |
| Product folder boundary preservation | High | High | High | Medium | Medium | Medium | Medium |

## Tradeoffs and rationale

- Local Markdown and Python CLI presets best preserve current AOS governance mechanics.
- Static docs are useful for review surfaces, but do not cover lifecycle mutation.
- SaaS, API, and bot candidates add collaboration or integration value while increasing external authority.
- Electron can improve local usability while adding packaging complexity.
- Human weighting is required before any stack decision can be promoted.
