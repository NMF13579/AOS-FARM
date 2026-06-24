# AOS-FARM.219 — Scope / Risk Plan for Core User Workflow Docs + Agent Tutor Mode MVP

## State Verification
- **Required Sources**: Read and verified (`00`, `01`, `02`).
- **Git State**:
  - Branch: `build/core-user-workflow-agent-tutor-mvp`
  - HEAD: `ff79709f4ad7da0f0affefb0038e508d95bbf949`
  - origin/dev: `ff79709f4ad7da0f0affefb0038e508d95bbf949`
  - origin/dev...HEAD divergence: `0 0`
- **Local Uncommitted Evidence Artifacts**: Multiple old uncommitted check/closure reports exist in the tree. These evidence-tail artifacts do not block continuation unless explicitly requested by a human.

## Stage Goal
Create user-facing workflow documentation and define Agent Tutor Mode as a chat-based helper layer. The goal is to provide non-programmers/vibe-coders with clear guidance and an explanatory interface (Agent Tutor) to navigate the AOS-FARM project structure.

## Authorized Scope
Allowed Implementation Outputs:
- **Docs**:
  - `docs/user-guide/README.md`
  - `docs/user-guide/non-programmer-workflow.md`
  - `docs/user-guide/agent-controller-workflow.md`
  - `docs/user-guide/commit-push-approval-workflow.md`
  - `docs/user-guide/agent-tutor-mode.md`
- **Templates**:
  - `templates/new-project-start-template.md`
  - `templates/agent-tutor-session-template.md`
  - `templates/agent-tutor-question-routing-template.md`
- **Reports/Checkpoints**:
  - AOS-FARM.221, 222, 223, 225 reports and their respective human checkpoints.

## Core Safety Boundary
Agent Tutor Mode is an explanatory interface over project documents.
- Agent Tutor is **NOT** a Source of Truth.
- Agent Tutor is **NOT** an approval authority.
- Agent Tutor must preserve all governance invariants (UNKNOWN stays UNKNOWN, PASS ≠ approval).

## Forbidden Scope
- RAG implementation / SQLite / retrieval engines / chat engines.
- Automatic repo scanners / question-answering systems.
- Modifying protected/canonical sources (`00`, `01`, `02`).
- Modifying approval semantics or Source of Truth rules.
- CI / runtime / validator implementations.

## Proposed Risk Profile
**MEDIUM_RISK_GUIDED**
Reason: The stage only creates documentation and templates. It does not modify runtime code, canonical rules, or CI infrastructure. However, because it describes governance semantics, Human execution authorization with explicit Risk Profile assignment is strictly required before any implementation begins.
