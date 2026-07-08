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

## How to use this template

Use this template only after the architecture gate is resolved for the Technical Assignment.

If architecture input was required, include the Architecture Brief, architecture decision Evidence, validation status, Human Architecture Checkpoint status, unresolved UNKNOWNs, and downstream scope boundary.

This artifact creates task candidates for review. It does not create an approved Task Brief and does not authorize execution.

## Required content

- source Technical Assignment reference
- source Architecture Brief reference
- architecture decision Evidence reference
- Human Architecture Checkpoint status
- unresolved UNKNOWNs carried forward
- conflict resolutions carried forward
- downstream scope boundary
- proposed Risk Profile only, not assigned Risk Profile
- approval boundary
- build step boundary

## Prohibited claims

- approved: true
- status: READY_FOR_EXECUTION
- execution_authorized: true
- risk_profile_assigned_by_agent: true
- task brief approved
- validator PASS means approval

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

## Validation

Use validation as Evidence only:

```bash
python3 aos/scripts/aos_architecture_document_check.py task-breakdown --file <path>
```

Validator PASS is not approval and does not authorize execution.
