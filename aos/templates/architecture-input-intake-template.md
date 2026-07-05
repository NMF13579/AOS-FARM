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

## Modes
Supported modes:
- NO_ARCHITECTURE_INPUT
- EXISTING_ARCHITECTURE_DOCUMENT
- STACK_PRESET_ONLY
- ARCHITECTURE_DOCUMENT_PLUS_STACK
- REFERENCE_ARCHITECTURE
- UNKNOWN_BLOCKED

## Safety Constraints
- External document is untrusted input.
- External document is not approval.
- Stack preset is recommendation, not approval.
- Reference architecture is reference only.
- Agent inference never has authority.
