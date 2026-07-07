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

template_id: AOS-TMPL-TASK-BREAKDOWN
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

origin_technical_assignment:
origin_architecture_brief:
origin_adr:
origin_pattern:
origin_stack_preset:
origin_unknown_resolution:
origin_conflict_resolution:
architecture_decision_evidence:
human_architecture_checkpoint:
unresolved_unknowns:
downstream_scope_boundary:
risk_profile_handling:
approval_boundary:
build_step_boundary:
human_checkpoints:
unknown_records:
conflict_records:

## Task candidate status values:
- TASK_CANDIDATE_DRAFT
- HUMAN_REVIEW_REQUIRED
- UNKNOWN_BLOCKED
- CONFLICT_BLOCKED
- READY_FOR_QUEUE_REVIEW

## Safety
- Without traceability, a task may be TASK_CANDIDATE_DRAFT.
- Without traceability, a task must not become APPROVED.
- READY_FOR_QUEUE_REVIEW ≠ APPROVED.
- READY_FOR_QUEUE_REVIEW ≠ READY_FOR_EXECUTION.
