# Architecture Anti-Pattern Catalog

Architecture Anti-Pattern Catalog is not approval.
Architecture Anti-Pattern Catalog is not canonical policy.
Architecture Anti-Pattern Catalog does not authorize execution.
Architecture Anti-Pattern Catalog does not authorize commit.
Architecture Anti-Pattern Catalog does not authorize push.
Architecture Anti-Pattern Catalog does not authorize release.
Architecture Anti-Pattern Catalog does not authorize canonical promotion.
Human approval is required before any anti-pattern entry becomes protected/canonical policy.
Architecture Anti-Pattern Catalog ≠ canonical policy.
Anti-pattern entry ≠ protected/canonical rule.
Human approval cannot be simulated.

### ARCH-ANTI-001 — PASS as approval
anti_pattern_id: ARCH-ANTI-001
title: PASS as approval
bad_behavior: Treating validator PASS as human approval.
why_it_is_risky: It bypasses the approval boundary and may promote unreviewed architecture decisions.
blocked_by: AOS governance invariants and validator safety checks.
correct_behavior: PASS only means validation succeeded; human approval is still required.
related_adr: ADR-0002-validator-before-canonical-promotion
related_human_review_candidate: ARCH-CANDIDATE-002
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-002 — Evidence as approval
anti_pattern_id: ARCH-ANTI-002
title: Evidence as approval
bad_behavior: Treating generated evidence files as human approval.
why_it_is_risky: Artifact existence does not guarantee correctness or human consent.
blocked_by: Core control rules.
correct_behavior: Evidence requires explicit human verification and approval.
related_adr: ADR-0001-markdown-first-source-of-truth
related_human_review_candidate: ARCH-CANDIDATE-001
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-003 — CI PASS as approval
anti_pattern_id: ARCH-ANTI-003
title: CI PASS as approval
bad_behavior: Assuming CI success grants execution or commit authority.
why_it_is_risky: CI only checks mechanical correctness, not architectural intent.
blocked_by: Governance rules blocking implicit authorization.
correct_behavior: CI PASS is a prerequisite, not an approval.
related_adr: ADR-0002-validator-before-canonical-promotion
related_human_review_candidate: ARCH-CANDIDATE-002
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-004 — NOT_RUN as PASS
anti_pattern_id: ARCH-ANTI-004
title: NOT_RUN as PASS
bad_behavior: Treating un-run validation checks as successful passes.
why_it_is_risky: Hides fatal errors or untested boundaries.
blocked_by: Validator gate enforcing explicit PASS.
correct_behavior: Validation must be explicitly run and return 0.
related_adr: ADR-0002-validator-before-canonical-promotion
related_human_review_candidate: ARCH-CANDIDATE-002
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-005 — UNKNOWN as OK
anti_pattern_id: ARCH-ANTI-005
title: UNKNOWN as OK
bad_behavior: Proceeding when a state or boundary is UNKNOWN.
why_it_is_risky: Leads to undefined behavior and potential safety violations.
blocked_by: System rules defining UNKNOWN ≠ OK.
correct_behavior: UNKNOWN states must be resolved explicitly.
related_adr: ADR-0002-validator-before-canonical-promotion
related_human_review_candidate: ARCH-CANDIDATE-002
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-006 — Silent stack selection
anti_pattern_id: ARCH-ANTI-006
title: Silent stack selection
bad_behavior: Choosing and implementing a stack without explicit human review.
why_it_is_risky: Traps the project in unwanted technical debt or unapproved architecture.
blocked_by: Stack review gating.
correct_behavior: Present stack options to human for review.
related_adr: ADR-0005-stack-selection-requires-human-review
related_human_review_candidate: ARCH-CANDIDATE-005
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-007 — ADR as execution authority
anti_pattern_id: ARCH-ANTI-007
title: ADR as execution authority
bad_behavior: Treating an ADR document as permission to start execution.
why_it_is_risky: ADRs are design decisions, not execution orders.
blocked_by: ADR templates denying execution authority.
correct_behavior: Execution requires explicit READY_FOR_EXECUTION tasks.
related_adr: ADR-0005-stack-selection-requires-human-review
related_human_review_candidate: ARCH-CANDIDATE-005
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-008 — ACTIVE registry without checkpoint
anti_pattern_id: ARCH-ANTI-008
title: ACTIVE registry without checkpoint
bad_behavior: Setting registry items to ACTIVE without human review checkpoints.
why_it_is_risky: Bypasses the architecture promotion process.
blocked_by: Future architecture validator checks on registry statuses.
correct_behavior: PROPOSED items require human checkpoint to become ACTIVE.
related_adr: ADR-0005-stack-selection-requires-human-review
related_human_review_candidate: ARCH-CANDIDATE-005
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-009 — Canonical promotion before validator
anti_pattern_id: ARCH-ANTI-009
title: Canonical promotion before validator
bad_behavior: Promoting a document to canonical before it passes structural validation.
why_it_is_risky: Introduces malformed data into the core truth.
blocked_by: Validation prerequisites for promotion.
correct_behavior: Validate first, promote second.
related_adr: ADR-0002-validator-before-canonical-promotion
related_human_review_candidate: ARCH-CANDIDATE-002
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-010 — Autonomous runner by default
anti_pattern_id: ARCH-ANTI-010
title: Autonomous runner by default
bad_behavior: Executing tasks automatically without manual queue progression.
why_it_is_risky: Loss of human oversight and failure isolation.
blocked_by: Queue design rules.
correct_behavior: Require manual triggers for task progression.
related_adr: ADR-0003-manual-queue-over-autonomous-runner
related_human_review_candidate: ARCH-CANDIDATE-003
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-011 — Installer overwrite
anti_pattern_id: ARCH-ANTI-011
title: Installer overwrite
bad_behavior: Silently overwriting existing user files during installation.
why_it_is_risky: Causes unrecoverable data loss in user projects.
blocked_by: Installer safe boundaries.
correct_behavior: Prompt or fail on existing files.
related_adr: ADR-0004-safe-installer-boundary
related_human_review_candidate: ARCH-CANDIDATE-004
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-012 — AGENTS.md auto-merge
anti_pattern_id: ARCH-ANTI-012
title: AGENTS.md auto-merge
bad_behavior: Automatically merging governance instructions without review.
why_it_is_risky: Overwrites project-specific agent rules.
blocked_by: Installer safe boundaries.
correct_behavior: Require manual merging for AGENTS.md.
related_adr: ADR-0004-safe-installer-boundary
related_human_review_candidate: ARCH-CANDIDATE-004
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-013 — Production RAG by default
anti_pattern_id: ARCH-ANTI-013
title: Production RAG by default
bad_behavior: Using complex or expensive RAG setups when a simple approach suffices.
why_it_is_risky: Premature scaling increases complexity and cost.
blocked_by: Architecture review processes.
correct_behavior: Justify RAG need through design discussion.
related_adr: ADR-0001-markdown-first-source-of-truth
related_human_review_candidate: ARCH-CANDIDATE-001
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-014 — Temp as Evidence
anti_pattern_id: ARCH-ANTI-014
title: Temp as Evidence
bad_behavior: Using temporary or derived files as formal architectural evidence.
why_it_is_risky: Temporary files lack permanence and traceability.
blocked_by: Truth location definitions.
correct_behavior: Store formal evidence in tracked markdown.
related_adr: ADR-0001-markdown-first-source-of-truth
related_human_review_candidate: ARCH-CANDIDATE-001
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-015 — Unstructured knowledge dump
anti_pattern_id: ARCH-ANTI-015
title: Unstructured knowledge dump
bad_behavior: Pasting large external documentation without synthesis.
why_it_is_risky: Degrades the context with noise and unverified information.
blocked_by: Knowledge register requirements.
correct_behavior: Synthesize only necessary context into the register.
related_adr: none
related_human_review_candidate: ARCH-CANDIDATE-007
status: PROPOSED
approval_status: NOT_APPROVED

### ARCH-ANTI-016 — Pattern without applicability context
anti_pattern_id: ARCH-ANTI-016
title: Pattern without applicability context
bad_behavior: Recommending a design pattern without explaining when NOT to use it.
why_it_is_risky: Leads to inappropriate usage of complex patterns.
blocked_by: Pattern registry schema.
correct_behavior: Require context and risks for all patterns.
related_adr: none
related_human_review_candidate: ARCH-CANDIDATE-006
status: PROPOSED
approval_status: NOT_APPROVED
