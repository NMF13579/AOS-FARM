# AOS-FARM.TA-09 Problem Intake Agent Prompt Commit Authorization Package

## Purpose

Prepare commit-only review for the updated `agentos/docs/prompts/problem-intake-agent.md` prompt, which aligns the agent behavior with the AOS-FARM TA-06/TA-07 adaptive technical assignment intake methodology.

## Scope Summary

- Prompt updated from legacy three-route entry to the current two-route system.
- Added Problem Interview Offer workflow.
- Integrated the Adaptive Elicitation Method Selector and Runbook references.
- Added controls for Interview Fatigue, Anti-Anchoring, Core Entity Filtering, and False Completeness.
- Integrated Developer Handoff protocol.

## Boundary

This package does not authorize commit by itself.
This package does not authorize push.
This package does not authorize combined commit+push.
Human Commit Authorization is required before commit.
Push authorization must be prepared only after commit SHA exists.

## Current Git State

- branch: dev
- HEAD: b8a03c1edf0375fc1b1cc89dcf8917a996fe579c
- origin/dev: b8a03c1edf0375fc1b1cc89dcf8917a996fe579c
- origin/dev...HEAD ahead/behind: 0 0

## Validation Evidence

```text
agentos/docs/prompts/problem-intake-agent.md:# AOS-FARM Prompt: Adaptive Technical Assignment Intake Agent
agentos/docs/prompts/problem-intake-agent.md:**Document status:** DRAFT_OPERATIONAL
agentos/docs/prompts/problem-intake-agent.md:5. present exactly two initial routes;
agentos/docs/prompts/problem-intake-agent.md:# 9. Problem Interview Offer
agentos/docs/prompts/problem-intake-agent.md:The agent must use the Adaptive Elicitation Method Selector.
agentos/docs/prompts/problem-intake-agent.md:method_routing_automation_boundary:
agentos/docs/prompts/problem-intake-agent.md:runbooks/five-whys-runbook.md
agentos/docs/prompts/problem-intake-agent.md:one_question_at_a_time_contract:
agentos/docs/prompts/problem-intake-agent.md:# 14. Interview Fatigue Control
agentos/docs/prompts/problem-intake-agent.md:# 15. Anti-Anchoring Control
agentos/docs/prompts/problem-intake-agent.md:# 16. Core Entity Detection and Traversal Depth
agentos/docs/prompts/problem-intake-agent.md:# 26. False Completeness Control
agentos/docs/prompts/problem-intake-agent.md:# 17. Draft State Tracking
agentos/docs/prompts/problem-intake-agent.md:→ Developer Handoff
agentos/docs/prompts/problem-intake-agent.md:Method selection ≠ approval.
agentos/docs/prompts/problem-intake-agent.md:Automatic method routing ≠ execution authorization.
```

## Candidate Commit Set

- agentos/docs/prompts/problem-intake-agent.md
- reports/aos-farm-ta-09-problem-intake-agent-commit-authorization-package.md
- reports/human-checkpoints/aos-farm-ta-09-problem-intake-agent-commit-authorization.md

## Out-of-Scope Local Files

- (various untracked legacy report files)

## Proposed Commit Message

docs: update problem intake agent prompt for adaptive TA methodology

## Explicit Non-Authorization

- commit_authorized_by_this_package: false
- push_authorized: false
- combined_commit_push_authorized: false
- release_authorized: false
- production_use_authorized: false
