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

template_id: AOS-TMPL-ARCH-BRIEF
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

architecture_brief_id: 
created_at: 
updated_at: 
supersedes: 
superseded_by: 
source_inputs: 
technical_assignment_ref: 
accepted_adr_refs: 
pattern_refs: 
stack_preset_refs: 
unknown_records: 
conflict_records: 
human_checkpoints: 

## How to use this template

Use this template after Architecture Input Intake to draft candidate architecture evidence for human review.

This artifact may summarize selected and rejected candidate options, but it must not approve architecture, assign Risk Profile, authorize implementation, or create an executable Task Brief.

## Required content

- decision question
- source Technical Assignment reference
- source Architecture Input Intake reference
- selected option candidates
- rejected option candidates
- assumptions
- constraints
- tradeoffs
- risks
- unresolved UNKNOWN records
- conflict records
- downstream Task Brief impact
- validation command/output reference
- human review questions
- human checkpoints required

## Prohibited claims

- approved: true
- approval_status: APPROVED
- status: READY_FOR_EXECUTION
- execution_authorized: true
- implementation_authorized: true
- release_authorized: true
- risk_profile_assigned_by_agent: true
- validator PASS means approval
- no human review required

## Allowed Statuses
- DRAFT
- HUMAN_REVIEW_REQUIRED
- READY_FOR_TASK_BREAKDOWN
- CONFLICT_BLOCKED
- UNKNOWN_BLOCKED
- REJECTED
- SUPERSEDED

## Safety
- READY_FOR_TASK_BREAKDOWN ≠ APPROVED
- READY_FOR_TASK_BREAKDOWN ≠ READY_FOR_EXECUTION
- Architecture Brief does not authorize execution.
- Architecture Brief does not authorize commit.
- Architecture Brief does not authorize push.
- Architecture Brief does not authorize release.

## Validation

Use validation as Evidence only:

```bash
python3 aos/scripts/aos_architecture_document_check.py brief --file <path>
```

Validator PASS is not approval. Validator PASS does not authorize Task Brief execution.
