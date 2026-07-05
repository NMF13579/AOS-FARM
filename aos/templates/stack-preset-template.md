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

template_id: AOS-TMPL-STACK-PRESET
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

stack_preset_id: 
name: 
applies_when: 
included_components: 
excluded_components: 
rules: 
forbidden_assumptions: 
source_reference_note: 
human_review_required: 
human_checkpoints: 

## Allowed statuses:
- PROPOSED
- HUMAN_REVIEW_REQUIRED
- ACTIVE
- DEPRECATED
- REJECTED
- SUPERSEDED

## Safety
- New stack presets start as PROPOSED.
- Agent may not promote stack preset to ACTIVE without human checkpoint.
- Stack preset is not approval.
- Stack preset is not execution authorization.
