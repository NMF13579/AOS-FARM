# AOS-FARM.609 — AOS-FARM.610+ Task Candidates

Task Candidate ≠ approved task.
Task Candidate ≠ execution authorization.
Task Candidate ≠ roadmap mutation.

## candidate_id: AOS-FARM.610
title: Unify Derived Lifecycle State Engine
problem: Queue helper, dashboard, validator, and lifecycle reconciliation have diverged and can produce different answers about the active next task.
goal: Build one read-only lifecycle state engine and make queue/dashboard/review tools consume the same derived-state logic.
scope: `aos/scripts/` lifecycle/queue/dashboard consumers, read-only docs updates, tests, fixtures.
allowed_changes:
- read-only lifecycle state helper
- queue/dashboard integration changes
- tests and fixtures
- docs describing derived-state boundaries
forbidden_changes:
- no auto-authorization
- no automatic task promotion
- no commit/push/release logic changes
- no protected/canonical root source changes without separate checkpoint
risk_profile_proposal: HIGH_RISK_PROTECTED
human_checkpoint_required: yes
validation:
- lifecycle state consistency tests
- queue next/read-only tests
- dashboard parity checks
- fail-closed checks for DONE/BLOCKED tasks
expected_artifacts:
- implementation report
- validation report
- review package
depends_on: none
priority: CRITICAL

## candidate_id: AOS-FARM.611
title: Review Package Assembler for Commit and Push Gates
problem: Commit and push reviews repeat the same git, diff, and validation evidence manually across multiple reports.
goal: Create a read-only assembler that builds exact evidence bundles for human commit/push reviews without authorizing anything.
scope: `aos_review_package.py` or adjacent script, docs, tests, fixtures.
allowed_changes:
- review package assembler logic
- docs for human-facing package usage
- tests proving no authority fields are elevated
forbidden_changes:
- no authorization automation
- no staging/commit/push execution
- no lifecycle mutation
risk_profile_proposal: MEDIUM_RISK_GUIDED
human_checkpoint_required: yes
validation:
- exact file-set capture tests
- exact ref/divergence capture tests
- no-approval boundary tests
expected_artifacts:
- execution report
- validation output
- review package example
depends_on: none
priority: IMPORTANT

## candidate_id: AOS-FARM.612
title: Lifecycle Legend and Status Language Compression
problem: `READY_FOR_EXECUTION`, `READY_FOR_HANDOFF`, `READY_FOR_HUMAN_REVIEW`, closure review, and acceptance review are hard to parse without internal context.
goal: Publish one compact lifecycle legend and normalize report wording around it.
scope: docs and report templates only.
allowed_changes:
- docs
- report templates
- glossary/legend assets
forbidden_changes:
- no validator semantics change
- no task mutation
- no queue mutation
risk_profile_proposal: MEDIUM_RISK_GUIDED
human_checkpoint_required: yes
validation:
- wording scan for forbidden approval implications
- template consistency review
expected_artifacts:
- legend doc
- template update report
- before/after terminology comparison
depends_on: none
priority: IMPORTANT

## candidate_id: AOS-FARM.613
title: Queue Consistency Guardrails Before Commit Review
problem: Placeholder or impossible queue metadata survived until late closure and required follow-on remediation in `564` and `565`.
goal: Add early read-only queue consistency guardrails so impossible combinations are surfaced before package commit review.
scope: queue/task validation logic, fixtures, tests, docs.
allowed_changes:
- validator rules
- tests and fixtures
- docs for queue field semantics
forbidden_changes:
- no auto-repair of tasks
- no queue mutation side effects
- no approval automation
risk_profile_proposal: HIGH_RISK_PROTECTED
human_checkpoint_required: yes
validation:
- negative fixtures for duplicate positions and DONE-as-next
- read-only validator tests
- fail-closed output verification
expected_artifacts:
- implementation report
- validation report
- review package
depends_on: AOS-FARM.610
priority: IMPORTANT

## candidate_id: AOS-FARM.614
title: Missing Stage Artifact and Duplicate Prompt Detector
problem: Full lifecycle audits are expensive because missing stages and repeated boilerplate are discovered manually.
goal: Add a read-only analyzer that reports missing lifecycle artifacts and duplicated prompt/report segments.
scope: analysis script, tests, docs, optional fixtures.
allowed_changes:
- read-only analyzer
- tests
- docs
forbidden_changes:
- no authority mutation
- no report rewriting
- no commit/push automation
risk_profile_proposal: MEDIUM_RISK_GUIDED
human_checkpoint_required: yes
validation:
- fixture chains with missing stages
- duplication detection fixtures
- false-positive review
expected_artifacts:
- analyzer report
- validation results
- task examples
depends_on: AOS-FARM.611
priority: NICE_TO_HAVE

## candidate_id: AOS-FARM.615
title: Human Authorization Witness Schema Unification
problem: Human decisions are recorded inconsistently across reports, embedded text, and checkpoint-like sections.
goal: Define and adopt one stable witness format for execution, commit, and push authorization records.
scope: docs, templates, maybe helper validation, but not automatic authorization.
allowed_changes:
- templates
- docs
- optional read-only schema validation
forbidden_changes:
- no agent-side authorization
- no automatic Risk Profile assignment
- no lifecycle backfill without separate approval
risk_profile_proposal: HIGH_RISK_PROTECTED
human_checkpoint_required: yes
validation:
- witness schema examples
- boundary wording checks
- compatibility review against existing reports
expected_artifacts:
- witness schema draft
- migration guidance
- review package
depends_on: none
priority: CRITICAL
