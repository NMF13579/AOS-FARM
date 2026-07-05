This template does not grant approval.
This template does not authorize execution.
This template does not authorize commit.
This template does not authorize push.
This template does not authorize release.
Human approval cannot be simulated.
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.

template_id: AOS-TMPL-CONFLICT-RECORD
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

conflict_id: 
conflict_source: 
conflicting_claim: 
aos_invariant: 
resolution_type: 
resolved_by: 
resolved_at: 
evidence_refs: 
human_answer: 
scope_limit: 
re_run_gate_required: 
human_checkpoints: 

## Allowed conflict statuses:
- CONFLICT_OPEN
- CONFLICT_BLOCKED
- CONFLICT_NEEDS_HUMAN
- CONFLICT_RESOLVED_BY_HUMAN
- CONFLICT_RESOLVED_BY_SOURCE
- CONFLICT_DEFERRED_WITH_SCOPE_LIMIT

## Safety
- External document is input, not approval.
- AOS Core / Governance invariants override conflicting external claims.
- Conflicts cannot be resolved silently.
