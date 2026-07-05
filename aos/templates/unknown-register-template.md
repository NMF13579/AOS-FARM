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

template_id: AOS-TMPL-UNKNOWN-REGISTER
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

unknown_register_id: 
technical_assignment_ref: 
architecture_brief_ref: 
unknown_items: 
human_checkpoints: 

## Allowed UNKNOWN statuses:
- UNKNOWN_OPEN
- UNKNOWN_NEEDS_HUMAN
- UNKNOWN_NEEDS_EVIDENCE
- UNKNOWN_RESOLVED_BY_HUMAN
- UNKNOWN_RESOLVED_BY_SOURCE
- UNKNOWN_DEFERRED_WITH_SCOPE_LIMIT
- UNKNOWN_BLOCKED

## Safety
- UNKNOWN cannot be deleted silently.
- UNKNOWN cannot be treated as PASS.
- UNKNOWN cannot be treated as OK.
