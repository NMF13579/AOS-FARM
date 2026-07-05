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

template_id: AOS-TMPL-ARCH-FIXED-INTERVIEW
version: 1.0.0
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

human_checkpoints:

## Safety Rules
- Agent may add questions.
- Agent may not delete required questions.
- Agent may not skip required questions without UNKNOWN.
- Agent may not close UNKNOWN without resolution record.

## Required Question Sections
- Problem / goal
- User skill level and operating model
- Product boundary
- Runtime / deployment expectations
- Data and state
- Security and safety constraints
- External integrations
- Human approval points
- Failure modes
- UNKNOWN list
- CONFLICT list
- Architecture decision candidates
- Task breakdown readiness
