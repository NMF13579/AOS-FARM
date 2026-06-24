# AOS-FARM.281 — First Template Dogfood Scope/Risk Plan

## Final Status
DRAFT_FOR_HUMAN_REVIEW

## Baseline
- branch: dev
- HEAD: f561509e3e9fee660c00064ebd89d083d01257ef
- origin/dev: f561509e3e9fee660c00064ebd89d083d01257ef
- ahead/behind: 0 0
- remote_baseline_closed: true

## Required Sources
- 00: Verified and compliant.
- 01: Verified and compliant.
- 02: Verified and compliant.

## Evidence-Tail Warning
AOS-FARM.280 closure report is local-only evidence-tail and should be included in a future commit candidate set.
Do not commit it in AOS-FARM.281.

## Dogfood Mode
dogfood_mode: simulated_local
external_repo_creation_authorized: false
github_repo_creation_authorized: false
github_push_authorized: false
release_authorized: false
production_use_authorized: false

## Dogfood Scenario
- project_name: Simple Notes App
- user_type: non-programmer / vibe-coder
- project_goal: create a tiny Markdown-first notes app project plan
- dogfood_goal: Test whether a user can follow AOS-FARM from first entry to first safe task handoff.
- excluded_scope: No production code, no real repo, no external deployment, no database, no RAG, no authentication, no payment, no release.

## First-User Journey Under Test
1. Where does a new user start? (`README.md` -> `docs/user-guide/bootstrap-agent-workflow.md`)
2. Which file tells them what to do first? (`README.md`)
3. How do they complete bootstrap? (Executing bootstrap tasks outlined in `docs/user-guide/bootstrap-agent-workflow.md`)
4. How do they invoke Agent Tutor? (Following `docs/user-guide/agent-tutor-mode.md`)
5. How is the first task created? (By agent tutor writing a task brief)
6. How is the first task placed into Manual Task Queue? (By moving/creating brief in `docs/task-queue/`)
7. How is handoff prepared for executor-agent? (Via `handoff-package.md`)
8. How is execution result supposed to be verified? (By independent verification boundaries)
9. Where is Human Commit Authorization required? (Before any `git commit` execution)
10. Where is Human Push Authorization required? (Before any `git push` execution)
11. What remains UNKNOWN? (How smoothly the agent handles the transition without full context)
12. What must not be automated? (Human authorizations, Risk Profile assignment)

## Expected AOS-FARM.282 Outputs
- `reports/dogfood/first-template/simple-notes-bootstrap-checklist.md`
- `reports/dogfood/first-template/simple-notes-agent-tutor-session.md`
- `reports/dogfood/first-template/simple-notes-first-task-brief.md`
- `reports/dogfood/first-template/simple-notes-manual-task-queue-entry.md`
- `reports/dogfood/first-template/simple-notes-handoff-package.md`
- `reports/dogfood/first-template/simple-notes-verification-boundary-check.md`
- `reports/aos-farm-282-first-template-dogfood-execution-report.md`

## Risk Profile
agent_proposed_risk_profile: MEDIUM_RISK_GUIDED
human_assignment_required: true

## Allowed Scope for AOS-FARM.282
- Creating simulated dogfood artifacts in `reports/dogfood/first-template/`.
- Generating an execution report.

## Forbidden Scope for AOS-FARM.282
- No real GitHub repo creation
- No external state
- No git commit or push
- No release/tag
- No production use
- No destructive cleanup
- No canonical source changes
- No template deletion/rename/move
- No approval simulation
- No autonomous execution

## Human Decisions Needed
- Assign Risk Profile in the checkpoint.
- Authorize execution of AOS-FARM.282.

## Open Questions / UNKNOWN
- Are there any specific validation scripts the Human wants to simulate running?

## Final Recommendation
Assign `MEDIUM_RISK_GUIDED` and approve `AOS-FARM.282` execution to proceed with simulated dogfooding.
