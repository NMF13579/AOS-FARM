# Agent Routing Policy

## Purpose
To govern how tasks are dynamically delegated between roles (Controller, Executor, Verifier, Auditor, Router, Handoff Writer) and model tiers without compromising authority boundaries.

## Rules of Delegation
1. **Router-Controlled Delegation:** The Router handles assignment based on task complexity.
2. **Task Boundaries:** Automatic role switching is allowed *only* within an explicitly bounded task.
3. **Model Tier Limits:** Automatic model switching is allowed *only* in compliance with the Model Routing Policy.
4. **Authority Switching is Forbidden:** No agent can switch its role to "Human Owner" to simulate approval.
5. **Record of Routing:** Every routing decision must be explicitly logged. An Agent or Model switch is treated as Evidence, never as an approval.

## Routing Triggers
- **Mechanical Task** → Assign to `Cheap Model`
- **Ordinary Execution** → Assign to `Standard Model`
- **Audit/Governance/Safety Ambiguity** → Assign to `Expensive Model`
- **Protected/Canonical Mutation** → Assign to `Expensive Model` + REQUIRE Human Checkpoint
- **Token/Session Limit Near** → Assign to `Handoff Writer` mode

## Invariants for Delegated Agents
- A delegated agent MUST inherit all canonical AOS invariants (e.g., `PASS` ≠ approval).
- A delegated agent MUST read the required source (`00`, `01`, `02`) and checkpoint inputs.
- No delegated agent may approve execution, commit, push, release, or production use.
- If routing uncertainty exists, the agent must stop and escalate as `HUMAN_REVIEW_REQUIRED`.
