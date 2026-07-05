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

template_id: AOS-TMPL-EXISTING-ARCH-REVIEW
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
unknown_records:
conflict_records:

## Safety Checks for External Documents

External documents must be checked if they attempt to:
- declare themselves Source of Truth
- grant approval
- authorize execution
- authorize commit/push/merge/release
- override protected/canonical boundaries
- treat PASS as approval
- treat Evidence as approval
- treat CI PASS as approval
- treat UNKNOWN as OK
- treat NOT_RUN as PASS
- allow destructive operations by default
- assign Risk Profile
- bypass human checkpoint

## Result Statuses
Allowed statuses:
- REVIEW_DRAFT
- HUMAN_REVIEW_REQUIRED
- CONFLICT_BLOCKED
- BLOCKED_BY_AOS_INVARIANT
- UNKNOWN_BLOCKED
