# Stack Preset Registry

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

Stack presets are recommendations.
Stack presets are not approval.
Stack presets are not execution authorization.
Stack presets are not commit authorization.
Stack presets are not push authorization.

document_id: AOS-ARCH-STACK-PRESET-REGISTRY
status: DRAFT
safety_class: PROTECTED_PRODUCT_CONTROL
changes_require_checkpoint: true
approval_authority: none
execution_authority: none
commit_authority: none
push_authority: none
release_authority: none

## Stack Preset Fields

- **id**: Unique identifier for the stack preset.
- **name**: Human-readable name.
- **status**: Current status of the stack preset (e.g., PROPOSED).
- **applies_when**: Conditions under which the stack applies.
- **included_components**: Key technologies or tools included.
- **excluded_components**: Key technologies explicitly avoided.
- **rules**: Specific architectural rules for this stack.
- **forbidden_assumptions**: Assumptions that are prohibited.
- **version**: Preset version.
- **source_reference_note**: Reference or rationale.
- **human_review_required**: Whether human review is required.

## Stack Preset Seed Entries

### STACK-PRESET-001 local-markdown-cli
- id: STACK-PRESET-001
- name: local-markdown-cli
- status: PROPOSED
- applies_when: Building local CLI documentation tools
- included_components: Markdown, CLI tools
- excluded_components: Web server, Database
- rules: Markdown as Single Source of Truth
- forbidden_assumptions: Requires online connectivity
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### STACK-PRESET-002 python-cli-tool
- id: STACK-PRESET-002
- name: python-cli-tool
- status: PROPOSED
- applies_when: Building Python CLI apps
- included_components: Python, Click/Typer
- excluded_components: Node.js, Frontend framework
- rules: Use virtual environments
- forbidden_assumptions: System python dependencies
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### STACK-PRESET-003 static-docs-site
- id: STACK-PRESET-003
- name: static-docs-site
- status: PROPOSED
- applies_when: Creating documentation sites
- included_components: SSG (e.g., MkDocs, Docusaurus)
- excluded_components: Dynamic backend
- rules: Build to static HTML
- forbidden_assumptions: Database access at runtime
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### STACK-PRESET-004 nextjs-supabase-saas
- id: STACK-PRESET-004
- name: nextjs-supabase-saas
- status: PROPOSED
- applies_when: Full-stack SaaS
- included_components: Next.js, Supabase, Tailwind
- excluded_components: Custom authentication server
- rules: Leverage Supabase RLS
- forbidden_assumptions: Direct DB connection from client
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### STACK-PRESET-005 fastapi-postgres-api
- id: STACK-PRESET-005
- name: fastapi-postgres-api
- status: PROPOSED
- applies_when: Python REST API
- included_components: FastAPI, PostgreSQL, SQLAlchemy
- excluded_components: NoSQL
- rules: Async request handling
- forbidden_assumptions: Blocking DB calls are safe
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### STACK-PRESET-006 telegram-bot
- id: STACK-PRESET-006
- name: telegram-bot
- status: PROPOSED
- applies_when: Telegram integrations
- included_components: Telegram Bot API, Node/Python
- excluded_components: Web UI
- rules: Handle webhooks or polling safely
- forbidden_assumptions: Perfect message delivery
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true

### STACK-PRESET-007 electron-local-app
- id: STACK-PRESET-007
- name: electron-local-app
- status: PROPOSED
- applies_when: Cross-platform desktop apps
- included_components: Electron, React/Vue
- excluded_components: Native mobile compilation
- rules: Isolate main and renderer processes
- forbidden_assumptions: Node integration in renderer is safe
- version: 1.0.0-seed
- source_reference_note: AOS MVP
- human_review_required: true
