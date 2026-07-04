# AOS-FARM.611 — Task Candidates
## 1. Scope
These are task candidates only.
They are not approved tasks.
They are not execution authorization.
They do not mutate roadmap.

## 2. Candidates

### Candidate 1: Lifecycle UX Helper Polish and Local Trace Boundary
```yaml
candidate_id: AOS-FARM.612
title: Lifecycle UX Helper Polish and Local Trace Boundary
problem: UX friction with untracked file diffs and shallow handoff summaries; need a safe place for local trace logs without bleeding into repository Evidence.
scope: Polish `aos_review_package.py` to handle untracked files in diffs, polish `aos_handoff_summary.py` to accept context args, and formalize `/.aos-tmp/logs/` boundary handling.
out_of_scope: Full log-rotation backend, auto-approvals, database creation, release automation, RAG vector stores.
risk_profile_recommendation: MEDIUM_RISK_GUIDED
requires_human_decision: true
expected_artifacts: Updated python scripts, /.aos-tmp/ trace boundary docs, updated prompt templates.
why_now: The helpers are actively being dogfooded; fixing the remaining friction makes the toolset polished enough for main branch promotion.
```

## 3. Recommended Candidate Selection
select_candidate_for_612
