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

template_id: AOS-TMPL-MINI-ADR
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

adr_id: 
title: 
decided_by: 
decided_at: 
task_context: 
technical_assignment_ref: 
architecture_brief_ref: 
related_patterns: 
related_unknowns: 
related_conflicts: 
supersedes: 
superseded_by: 
human_checkpoints: 

## Allowed Statuses
- PROPOSED
- HUMAN_REVIEW_REQUIRED
- ACCEPTED_BY_HUMAN
- REJECTED
- SUPERSEDED
- UNKNOWN_BLOCKED
- CONFLICT_BLOCKED

## Safety
- ACCEPTED_BY_HUMAN in ADR ≠ execution_authorized
- ACCEPTED_BY_HUMAN in ADR ≠ commit_authorized
- ACCEPTED_BY_HUMAN in ADR ≠ push_authorized
- ACCEPTED_BY_HUMAN in ADR ≠ release_authorized
