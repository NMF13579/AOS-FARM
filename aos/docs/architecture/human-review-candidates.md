# Human Review Candidates

This document lists candidates for human review.
It is not approval.
It does not authorize execution, commit, push, release, or canonical promotion.
Human approval cannot be simulated.

human-review-candidates.md is a required pre-condition for AOS-FARM.620.
AOS-FARM.620 must not start protected/canonical promotion review unless human-review-candidates.md exists and lists unresolved review questions.
This pre-condition does not authorize AOS-FARM.620 to start.
Starting AOS-FARM.620 still requires explicit human authorization.

## ARCH-CANDIDATE-001 — Markdown-first Source of Truth
- **candidate_id**: ARCH-CANDIDATE-001
- **title**: Markdown-first Source of Truth
- **linked_adr**: aos/docs/architecture/decisions/ADR-0001-markdown-first-source-of-truth.md
- **current_status**: HUMAN_REVIEW_REQUIRED
- **approval_status**: NOT_APPROVED
- **why_review_needed**: To confirm the baseline definition of Source of Truth.
- **known_unknowns**: None
- **risk_profile_suggestion**: HIGH_RISK_PROTECTED
- **review_question_for_human**: Should Markdown-first remain the default Source of Truth model for AOS-FARM?
- **approval_boundary**: NOT_APPROVED. PASS ≠ approval.
- **next_possible_stage**: AOS-FARM.620

## ARCH-CANDIDATE-002 — Validator before canonical promotion
- **candidate_id**: ARCH-CANDIDATE-002
- **title**: Validator before canonical promotion
- **linked_adr**: aos/docs/architecture/decisions/ADR-0002-validator-before-canonical-promotion.md
- **current_status**: HUMAN_REVIEW_REQUIRED
- **approval_status**: NOT_APPROVED
- **why_review_needed**: To confirm validation prerequisites for promotion.
- **known_unknowns**: None
- **risk_profile_suggestion**: HIGH_RISK_PROTECTED
- **review_question_for_human**: Should validator PASS be required before any future protected/canonical promotion checkpoint?
- **approval_boundary**: NOT_APPROVED. Validator PASS ≠ approval.
- **next_possible_stage**: AOS-FARM.620

## ARCH-CANDIDATE-003 — Manual queue over autonomous runner
- **candidate_id**: ARCH-CANDIDATE-003
- **title**: Manual queue over autonomous runner
- **linked_adr**: aos/docs/architecture/decisions/ADR-0003-manual-queue-over-autonomous-runner.md
- **current_status**: HUMAN_REVIEW_REQUIRED
- **approval_status**: NOT_APPROVED
- **why_review_needed**: To confirm execution and queue safety model.
- **known_unknowns**: None
- **risk_profile_suggestion**: HIGH_RISK_PROTECTED
- **review_question_for_human**: Should autonomous runner behavior remain out of the default first-start workflow?
- **approval_boundary**: NOT_APPROVED. Queue readiness ≠ execution authorization.
- **next_possible_stage**: AOS-FARM.620

## ARCH-CANDIDATE-004 — Safe installer boundary
- **candidate_id**: ARCH-CANDIDATE-004
- **title**: Safe installer boundary
- **linked_adr**: aos/docs/architecture/decisions/ADR-0004-safe-installer-boundary.md
- **current_status**: HUMAN_REVIEW_REQUIRED
- **approval_status**: NOT_APPROVED
- **why_review_needed**: To confirm installer safety behaviors and limits.
- **known_unknowns**: None
- **risk_profile_suggestion**: HIGH_RISK_PROTECTED
- **review_question_for_human**: Should install/apply behavior remain gated and conflict-aware before any broader automation?
- **approval_boundary**: NOT_APPROVED. Install dry-run PASS ≠ apply authorization.
- **next_possible_stage**: AOS-FARM.620

## ARCH-CANDIDATE-005 — Stack selection requires human review
- **candidate_id**: ARCH-CANDIDATE-005
- **title**: Stack selection requires human review
- **linked_adr**: aos/docs/architecture/decisions/ADR-0005-stack-selection-requires-human-review.md
- **current_status**: HUMAN_REVIEW_REQUIRED
- **approval_status**: NOT_APPROVED
- **why_review_needed**: To ensure explicit user consent for tech stacks.
- **known_unknowns**: None
- **risk_profile_suggestion**: HIGH_RISK_PROTECTED
- **review_question_for_human**: Should stack presets be introduced as PROPOSED candidates in a later dedicated stage?
- **approval_boundary**: NOT_APPROVED. Stack recommendation ≠ approval.
- **next_possible_stage**: AOS-FARM.620

## ARCH-CANDIDATE-006 — Architecture anti-pattern catalog promotion review
- **candidate_id**: ARCH-CANDIDATE-006
- **title**: Architecture anti-pattern catalog promotion review
- **linked_adr**: aos/docs/architecture/architecture-anti-pattern-catalog.md
- **current_status**: HUMAN_REVIEW_REQUIRED
- **approval_status**: NOT_APPROVED
- **why_review_needed**: To review the anti-pattern catalog when generated.
- **known_unknowns**: Content of catalog
- **risk_profile_suggestion**: HIGH_RISK_PROTECTED
- **review_question_for_human**: Should the future anti-pattern catalog be canonical?
- **approval_boundary**: NOT_APPROVED.
- **next_possible_stage**: AOS-FARM.620

## ARCH-CANDIDATE-007 — Architecture knowledge source register future use
- **candidate_id**: ARCH-CANDIDATE-007
- **title**: Architecture knowledge source register future use
- **linked_adr**: aos/docs/architecture/architecture-knowledge-source-register.md
- **current_status**: HUMAN_REVIEW_REQUIRED
- **approval_status**: NOT_APPROVED
- **why_review_needed**: To review the knowledge source register when generated.
- **known_unknowns**: Content of register
- **risk_profile_suggestion**: HIGH_RISK_PROTECTED
- **review_question_for_human**: Should the future knowledge source register be canonical?
- **approval_boundary**: NOT_APPROVED.
- **next_possible_stage**: AOS-FARM.620
