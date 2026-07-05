# Pattern Registry

This document does not grant approval.
This document does not authorize execution.
This document does not authorize commit.
This document does not authorize push.
This document does not authorize release.
Human approval cannot be simulated.
PASS ≠ approval.
Evidence ≠ approval.
CI PASS ≠ approval.
UNKNOWN ≠ OK.
NOT_RUN ≠ PASS.

Initial pattern entries in this MVP are seed proposals.
They are usable for draft architecture reasoning only.
They are not canonical approvals.
They do not authorize execution.
They require human review before promotion to ACTIVE.
Agent-authored registry seed ≠ architecture authority.
Agent inference never has authority.

document_id: AOS-ARCH-PATTERN-REGISTRY
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

## Registry Entry Fields

- **id**: Unique identifier for the pattern.
- **name**: Human-readable name.
- **status**: Current status of the pattern (e.g., PROPOSED).
- **category**: The category this pattern belongs to.
- **applies_when**: Conditions under which the pattern applies.
- **rules**: Specific rules mandated by the pattern.
- **forbidden_assumptions**: Assumptions that are explicitly prohibited.
- **version**: Pattern version.
- **source_reference_note**: Reference to the origin or inspiration.
- **human_review_required**: Whether human review is required.

## AOS / Governance Seed Patterns

### AOS-PATTERN-001 Markdown-first Governance
- id: AOS-PATTERN-001
- name: Markdown-first Governance
- status: PROPOSED
- category: Governance
- applies_when: Always in AOS-FARM
- rules: All governance is codified in markdown
- forbidden_assumptions: Code overrides markdown
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-002 Human-Gated Pipeline
- id: AOS-PATTERN-002
- name: Human-Gated Pipeline
- status: PROPOSED
- category: Workflow
- applies_when: Executing execution or release pipelines
- rules: Explicit human approval required at gates
- forbidden_assumptions: Agent can auto-approve
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-003 Template + Validator
- id: AOS-PATTERN-003
- name: Template + Validator
- status: PROPOSED
- category: Tooling
- applies_when: Creating artifacts
- rules: Must use templates and pass validators
- forbidden_assumptions: Validators auto-approve
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-004 Candidate → Approved Queue
- id: AOS-PATTERN-004
- name: Candidate → Approved Queue
- status: PROPOSED
- category: Workflow
- applies_when: Task generation
- rules: Tasks start as candidates
- forbidden_assumptions: Tasks are auto-approved
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-005 Local Scratch Boundary
- id: AOS-PATTERN-005
- name: Local Scratch Boundary
- status: PROPOSED
- category: Folder Structure
- applies_when: Creating temporary files
- rules: Scratch files go to /.aos-tmp/
- forbidden_assumptions: Scratch files are Source of Truth
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-006 Product Folder Boundary
- id: AOS-PATTERN-006
- name: Product Folder Boundary
- status: PROPOSED
- category: Folder Structure
- applies_when: Organizing project files
- rules: Maintain /aos/, /project/ separation
- forbidden_assumptions: Consumer depends on root
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-007 Read-only Dashboard
- id: AOS-PATTERN-007
- name: Read-only Dashboard
- status: PROPOSED
- category: Tooling
- applies_when: Viewing project state
- rules: Dashboard cannot execute destructive commands
- forbidden_assumptions: Dashboard acts as terminal
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-008 Safe-Create Installer
- id: AOS-PATTERN-008
- name: Safe-Create Installer
- status: PROPOSED
- category: Tooling
- applies_when: Bootstrapping a project
- rules: Non-destructive apply logic only
- forbidden_assumptions: Installer can overwrite existing files without confirmation
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### AOS-PATTERN-009 Tutor-Guided Workflow
- id: AOS-PATTERN-009
- name: Tutor-Guided Workflow
- status: PROPOSED
- category: Workflow
- applies_when: First-time setup
- rules: Provide step-by-step guidance
- forbidden_assumptions: User knows architecture immediately
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

## General Architecture Seed Patterns

### ARCH-PATTERN-001 Layered Architecture
- id: ARCH-PATTERN-001
- name: Layered Architecture
- status: PROPOSED
- category: Architecture
- applies_when: Building traditional enterprise apps
- rules: Strict layer boundaries
- forbidden_assumptions: Layers can be bypassed freely
- version: 1.0.0-seed
- source_reference_note: Industry standard
- human_review_required: true

### ARCH-PATTERN-002 Modular Monolith
- id: ARCH-PATTERN-002
- name: Modular Monolith
- status: PROPOSED
- category: Architecture
- applies_when: Startups, medium-scale apps
- rules: Code boundaries replace physical boundaries
- forbidden_assumptions: Cannot scale
- version: 1.0.0-seed
- source_reference_note: Industry standard
- human_review_required: true

### ARCH-PATTERN-003 Event-Driven Architecture
- id: ARCH-PATTERN-003
- name: Event-Driven Architecture
- status: PROPOSED
- category: Architecture
- applies_when: Highly decoupled systems
- rules: Asynchronous message passing
- forbidden_assumptions: Strong consistency everywhere
- version: 1.0.0-seed
- source_reference_note: Industry standard
- human_review_required: true

### ARCH-PATTERN-004 Microservices
- id: ARCH-PATTERN-004
- name: Microservices
- status: PROPOSED
- category: Architecture
- applies_when: Large scale organizational structure
- rules: Independent deployability
- forbidden_assumptions: Free data sharing
- version: 1.0.0-seed
- source_reference_note: Industry standard
- human_review_required: true

### ARCH-PATTERN-005 Hexagonal / Ports and Adapters
- id: ARCH-PATTERN-005
- name: Hexagonal / Ports and Adapters
- status: PROPOSED
- category: Architecture
- applies_when: Domain-centric applications
- rules: Dependency inversion for external systems
- forbidden_assumptions: Domain logic depends on DB
- version: 1.0.0-seed
- source_reference_note: Industry standard
- human_review_required: true

### ARCH-PATTERN-006 CQRS
- id: ARCH-PATTERN-006
- name: CQRS
- status: PROPOSED
- category: Architecture
- applies_when: High read-write asymmetry
- rules: Separate read and write models
- forbidden_assumptions: Read model must be synchronous
- version: 1.0.0-seed
- source_reference_note: Industry standard
- human_review_required: true

### ARCH-PATTERN-007 Serverless
- id: ARCH-PATTERN-007
- name: Serverless
- status: PROPOSED
- category: Architecture
- applies_when: Cloud-native applications
- rules: Managed services and functions
- forbidden_assumptions: Infinite execution time
- version: 1.0.0-seed
- source_reference_note: Industry standard
- human_review_required: true
