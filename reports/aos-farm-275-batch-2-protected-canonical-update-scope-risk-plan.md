# AOS-FARM.275 — Batch 2 Protected Canonical Update Scope/Risk Plan

## Exact Legacy Drift Finding
- Source: `00_AOS_Core_Control.md`
- Section: `## Active-now Areas` (Lines 411-428)
- Finding: The section incorrectly lists legacy `agentos/` paths (e.g., `agentos/architecture/`, `agentos/governance/`, `agentos/templates/`). In the active AOS-FARM template, the true active directories are standard root folders like `docs/`, `templates/`, `reports/`, etc.

## Why it is a Protected/Canonical Change
`00_AOS_Core_Control.md` is the highest canonical project control source (`document_type: core_control`). Under AOS-FARM governance rules, any modification to this file—even for documentation drift—is strictly regulated. It requires explicit human authorization under a `HIGH_RISK_PROTECTED` profile to ensure core governance rules are never accidentally mutated.

## Proposed Edit Scope (Minimal)
- Target File: `00_AOS_Core_Control.md`
- Candidate Section: `## Active-now Areas`
- Candidate Changes: Remove the legacy `agentos/*` paths and replace them with the correct active structure (e.g., `docs/`, `templates/`, `reports/`).

## Forbidden Changes (What cannot be changed)
- Do not change any other sections or rules within `00_AOS_Core_Control.md`.
- Do not mutate any governance rules, safety invariants, source precedence, or layer models.
- Do not edit `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
- Do not change any lifecycle, approval, or Source of Truth semantics.
- Do not delete templates or perform any destructive cleanup operations.

## Execution Requirements
- agent_proposed_risk_profile: HIGH_RISK_PROTECTED
- human_assignment_required: true
- execution_authorized_now: false
- commit_authorized_now: false
- push_authorized_now: false
- release_authorized_now: false
