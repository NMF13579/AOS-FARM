# Multi-Environment Agent Workflow

## Purpose
This document defines how the AOS-FARM workflow seamlessly operates across multiple execution environments (Antigravity, VS Code / Codex CLI, ChatGPT) without losing safety context or relying on fragile conversational memory.

## Supported Environments
- **Antigravity:** Native IDE agent environment.
- **VS Code / Codex CLI:** Local IDE environment for command-line and editor-based agents.
- **ChatGPT:** External environment for high-level architecture review, escalation, and debugging.

## Repo-Centered Source of Truth
The central principle of the multi-environment workflow is that **Agent memory is not the Source of Truth.** The Git repository, its tracked files, and the markdown reports/checkpoints dictate the state. Any agent dropped into the repository should be able to instantly understand the current phase.

## Protocol Rules
1. **Required Session Start Checks:**
   Agents must always verify `git status`, `HEAD`, `origin/dev`, and the existence of the three core control sources (`00`, `01`, `02`) at the start of any session.
2. **Missing Sources / Ambiguous Checkpoints:**
   If sources are missing or the state cannot be explicitly reconstructed, the agent must fail closed and report `BLOCKED`.
3. **Dirty Working Tree:**
   If a working tree has pending staged/modified files that lack a verified execution report, the next task MUST be verification and recovery. Duplicate commits or pushes must be strictly prevented.
4. **Environment Switching:**
   Switching environments does NOT change authorization state. A human checkpoint approved for Antigravity is valid for Codex CLI, provided the bounds are respected.
5. **Session Limit Handoff:**
   When an environment nears its token, usage, or time limits, the agent must emit a handoff template to capture the current state for the next session/environment to resume without context loss.
6. **Human Checkpoints:**
   Human checkpoints cannot be automated by any environment. The user acts as the sole authority.
