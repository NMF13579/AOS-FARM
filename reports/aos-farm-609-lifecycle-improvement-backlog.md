# AOS-FARM.609 — Lifecycle Improvement Backlog

Task Candidate is not an approved task.
This backlog is not execution authorization.
This backlog does not mutate roadmap or lifecycle state.

## Prioritized Findings

### CRITICAL

id: AOS-609-BL-001
title: Unify derived lifecycle state across queue, dashboard, validator, and review tools
impact: Removes conflicting "next task" answers and reduces false operator confidence.
safety_risk: High. Conflicting derived state can surface a `DONE` task as active.
suggested_next_action: Build one shared read-only lifecycle state engine and migrate queue/dashboard consumers onto it.
proposed_owner_layer: lifecycle
evidence: `AOS-FARM.565`, `AOS-FARM.607`

id: AOS-609-BL-002
title: Standardize human authorization witness format
impact: Makes execution, commit, and push decisions auditable with one stable shape.
safety_risk: High. Mixed formats increase ambiguity about what the human actually authorized.
suggested_next_action: Define one canonical witness schema for execution, commit, and push checkpoints.
proposed_owner_layer: docs
evidence: `AOS-FARM.511`, `AOS-FARM.543`, `AOS-FARM.545`

### IMPORTANT

id: AOS-609-BL-003
title: Auto-assemble review evidence bundles without auto-authorizing anything
impact: Cuts repeated manual assembly work for commit and push reviews.
safety_risk: Medium. Safer if bundle generation is read-only and never writes authorization fields.
suggested_next_action: Add a read-only review package assembler with exact file-set, ref-set, and validation capture.
proposed_owner_layer: scripts
evidence: `AOS-FARM.542`, `AOS-FARM.544`, `AOS-FARM.568`

id: AOS-609-BL-004
title: Collapse redundant remote closure reporting
impact: Reduces three near-duplicate post-push reviews to one required closure proof and one optional human review.
safety_risk: Low.
suggested_next_action: Keep exact remote verification, but merge `post-push`, `final closure`, and `acceptance-style` report templates where no new human decision exists.
proposed_owner_layer: docs
evidence: `AOS-FARM.546`, `AOS-FARM.547`, `AOS-FARM.548`

id: AOS-609-BL-005
title: Publish one lifecycle legend for status words and stage names
impact: Makes the system understandable without internal tribal knowledge.
safety_risk: Medium. Misread status words can be mistaken for permission.
suggested_next_action: Create a compact legend referenced by every review/report template.
proposed_owner_layer: docs
evidence: `AOS-FARM.507`, `AOS-FARM.541`, `AOS-FARM.548`, `AOS-FARM.607`

id: AOS-609-BL-006
title: Add queue field consistency guardrails earlier in the lifecycle
impact: Prevents later cleanup stages like `564` and `565`.
safety_risk: Medium.
suggested_next_action: Extend read-only validation to flag impossible queue combinations before they land in active package reviews.
proposed_owner_layer: validator
evidence: `AOS-FARM.541`, `AOS-FARM.564`, `AOS-FARM.565`

id: AOS-609-BL-007
title: Add package manifest linking task artifacts to commit payloads
impact: Makes later commit/push reviews easier to audit and compress.
safety_risk: Low to medium.
suggested_next_action: Generate one manifest listing source candidate, task, execution report, review reports, and final commit SHA.
proposed_owner_layer: queue
evidence: `AOS-FARM.505`, `AOS-FARM.509`, `AOS-FARM.542`

### NICE_TO_HAVE

id: AOS-609-BL-008
title: Rename acceptance-style reports to non-approval wording
impact: Reduces semantic confusion.
safety_risk: Medium.
suggested_next_action: Replace "acceptance review" wording where no explicit human approval exists.
proposed_owner_layer: docs
evidence: `AOS-FARM.548`

id: AOS-609-BL-009
title: Add duplicated prompt segment detection for review stages
impact: Identifies reusable prompt sections and review boilerplate.
safety_risk: Low.
suggested_next_action: Add a read-only analyzer over recent report chains and prompts.
proposed_owner_layer: scripts
evidence: repeated boundary blocks across `542` to `548`, `568`, `570`

id: AOS-609-BL-010
title: Add forbidden-placement scanner for reports/checkpoints in `.aos-tmp`
impact: Hardens Source-of-Truth boundaries.
safety_risk: Medium.
suggested_next_action: Add a read-only scanner and surface violations in validation output.
proposed_owner_layer: validator
evidence: `AOS-FARM.507`, `AOS-FARM.607`

### FUTURE

id: AOS-609-BL-011
title: Machine-readable lifecycle event ledger per package
impact: Makes reconstruction, dashboarding, and audits cheaper.
safety_risk: Medium if it becomes a shadow source of truth.
suggested_next_action: Design a minimal append-only event index with explicit source-of-truth rules.
proposed_owner_layer: lifecycle
evidence: full reconstruction required many reports

id: AOS-609-BL-012
title: Derived-state UI that reads the reconciler instead of re-implementing logic
impact: Better human usability.
safety_risk: Medium unless it is strictly read-only.
suggested_next_action: After unified lifecycle state exists, rebuild dashboard on top of it.
proposed_owner_layer: dashboard
evidence: `AOS-FARM.607`

### REJECTED_FOR_NOW

id: AOS-609-BL-013
title: Auto-assign Risk Profile from reports
impact: Would save human time.
safety_risk: High. Violates explicit human checkpoint boundary.
suggested_next_action: Do not implement. At most propose a recommendation-only helper later.
proposed_owner_layer: human workflow
evidence: `00`, `02`, and repeated task/report boundaries

id: AOS-609-BL-014
title: Auto-approve commit or push when validations pass
impact: High speed.
safety_risk: Critical. Directly violates AOS invariants.
suggested_next_action: Reject.
proposed_owner_layer: human workflow
evidence: all governing sources and all reviewed report chains

id: AOS-609-BL-015
title: Auto-promote Task Candidate to real task
impact: Shorter intake.
safety_risk: High. Blurs candidate, task, Risk Profile, and execution boundaries.
suggested_next_action: Reject for now.
proposed_owner_layer: queue
evidence: `AOS-FARM.505`, `AOS-FARM.507`, `AOS-FARM.509`
