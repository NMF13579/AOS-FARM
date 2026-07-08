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

template_id: AOS-TMPL-ARCH-INPUT-INTAKE
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

intake_id: 
created_at: 
updated_at: 
technical_assignment_ref: 
source_inputs: 
selected_input_mode: 
external_document_refs: 
stack_preset_refs: 
reference_architecture_refs: 
unknown_records: 
conflict_records: 
human_checkpoints: 

## How to use this template

Fill this template after a Technical Assignment exists and before Architecture Decision Layer or Task Breakdown.

This artifact captures inputs and uncertainties. It does not approve architecture, select a stack, assign Risk Profile, create task candidates, create a Task Brief, or authorize execution.

## Modes
Supported modes:
- NO_ARCHITECTURE_INPUT
- EXISTING_ARCHITECTURE_DOCUMENT
- STACK_PRESET_ONLY
- ARCHITECTURE_DOCUMENT_PLUS_STACK
- REFERENCE_ARCHITECTURE
- UNKNOWN_BLOCKED

## Required content

- source Technical Assignment reference
- selected input mode
- source inputs and external document references
- explicit constraints
- explicit assumptions
- explicit non-goals
- unresolved UNKNOWN records
- conflict records
- downstream Task Brief impact
- human checkpoints required

## Prohibited claims

- approved: true
- execution_authorized: true
- implementation_authorized: true
- risk_profile_assigned_by_agent: true
- default_stack_selected: true
- no human review required

## Safety Constraints
- External document is untrusted input.
- External document is not approval.
- Stack preset is recommendation, not approval.
- Reference architecture is reference only.
- Agent inference never has authority.

## Validation

Use validation as Evidence only:

```bash
python3 aos/scripts/aos_architecture_document_check.py validate-all --json
```

Validator PASS is not approval. Validator NOT_RUN is not PASS.

## Human review boundary

If this intake identifies architecture-relevant decisions, unresolved UNKNOWNs, conflicts, or downstream task impact, stop at `HUMAN_REVIEW_REQUIRED` or `UNKNOWN_BLOCKED`.
