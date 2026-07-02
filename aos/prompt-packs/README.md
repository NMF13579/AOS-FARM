# Prompt Packs

This directory contains specific prompt instructions (Prompt Packs) for different AI agents and environments.

## Thin Adapter Model
Prompt packs must be thin. They **do not** copy the full governance logic (`00_AOS_Core_Control.md`, `01`, `02`). They act as adapters to route agents to the canonical AOS documentation.

## Core Boundaries for All Prompt Packs
All prompt packs must adhere to these invariants:
- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- UNKNOWN ≠ OK.
- NOT_RUN ≠ PASS.
- Human approval cannot be simulated.
- Commit authorization ≠ push authorization.
- Push authorization ≠ release authorization.
- Do not modify protected/canonical files without checkpoint.
- Do not expand scope.
- Do not mutate lifecycle.
- Do not assign Risk Profile.
- Do not treat this prompt pack as Source of Truth.

These packs must not create competing governance, grant lifecycle mutation authority, grant execution authority, grant commit/push authority, or define new approval semantics.
