# Compact Safe Path Template

**Note:** This template does not override canonical governance sources. If this template conflicts with `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, then 00/01/02 win according to source precedence.

## 1. Header

- **task_id:** AOS-FARM.671
- **task_title:** Compact Safe Path Manual Real-Task Dogfood
- **mode:** Controlled dogfood / narrow implementation stage
- **requested_by:** Human Owner
- **date:** 2026-07-09
- **compact_path_variant:** Minimal Compact Path
- **current_boundary:** Pre-Execution
- **execution_authorized:** true
- **commit_authorized:** false
- **push_authorized:** false
- **merge_authorized:** false
- **release_authorized:** false

*Note: Compact Path selection is not approval. Missing human authorization must not be inferred. Authorization fields default to false.*

## 2. Compact Path Contract

- Compact Safe Path reduces ceremony only.
- Compact Safe Path does not reduce safety.
- Compact eligibility is not approval.
- Compact selection is not execution authorization.
- PASS is not approval.
- Evidence is not approval.
- CI PASS is not approval.
- UNKNOWN is not OK.
- NOT_RUN is not PASS.
- Every boundary remains separate.
- This template is not Source of Truth for governance.

## 3. Variant selection

Selectable variants:
- [x] **Minimal Compact Path**: Preferred only when safe.
- [ ] **Full Compact Path**: Used for borderline small tasks.

*Note: If either variant becomes unsafe, transition to full path. Variant selection is not approval.*

## 4. Friction budget

Target budget:
- One compact task card before execution authorization.
- One compact Evidence summary after execution.
- One human decision per boundary.
- No more than 5 required pre-execution fields.
- No more than 5 required post-execution Evidence bullets.
- No more than 1 current scoped decision at a time.
- Full path transition whenever this budget cannot be met safely.

*Note: Friction budget is target only. Friction budget cannot suppress Evidence, UNKNOWN, NOT_RUN, or required human review.*

## 5. Compact Task Card

1. **User request:** Manually dogfood the compact safe path on one realistic AOS-FARM task-like scenario.
2. **Plain-language goal:** Verify compact template is usable, preserves safety boundaries, doesn't imply approval, and can be checked by the standalone checker.
3. **Intended files or areas:** `tests/fixtures/compact_template_check/`; compact template and checker are inspection targets only unless a narrow defect is proven.
4. **Expected change type:** Minor documentation and fixture creation.
5. **Why compact path may apply:** The task is narrow, doesn't change core governance, and is a simple real-task dogfooding scenario.

## 6. Eligibility review

Checklist:
- [x] Single clear goal.
- [x] Small bounded scope.
- [x] User intent clear.
- [x] Files known or safely discoverable.
- [x] No protected/canonical file change.
- [x] No lifecycle semantics change.
- [x] No validator semantics change.
- [x] No runtime enforcement change.
- [x] No destructive operation.
- [x] No secrets or credentials.
- [x] No external deployment/release/production operation.
- [x] No architecture decision.
- [x] No Source of Truth rule change.
- [x] Required sources available.
- [x] No UNKNOWN affects safety.
- [x] Required checks can run or NOT_RUN can be explicitly surfaced.
- [x] Human boundary remains explicit.
- [x] Risk Profile does not require agent self-assignment.

- **eligible_for_compact_path:** yes
- **eligibility_review_status:** PASS
- **eligibility_reason:** The scope is strictly limited to dogfooding a narrow template with existing fixtures, no lifecycle changes.

*Note: `eligible_for_compact_path: yes` is not approval. `eligibility_review_status: PASS` is not approval. If eligibility is unknown, use HUMAN_REVIEW_REQUIRED or transition to full path.*

## 7. Exclusion review

Checklist:
- [ ] UNKNOWN affects safety.
- [ ] Required Evidence missing.
- [ ] Required checks NOT_RUN and needed for decision.
- [ ] Protected/canonical files involved.
- [ ] Lifecycle transition involved.
- [ ] Risk Profile assignment required but unavailable.
- [ ] Validator/governance semantics touched.
- [ ] Runtime enforcement touched.
- [ ] Destructive operation requested.
- [ ] Merge/release/deploy requested.
- [ ] Architecture decision required.
- [ ] Source of Truth rule changed.
- [ ] Scope expands.
- [ ] User request ambiguous.
- [ ] Human review unavailable where required.
- [ ] Agent would need to self-assign LOW_RISK_FAST.
- [ ] PASS would be treated as approval.
- [ ] Evidence would be treated as approval.
- [ ] NOT_RUN would be treated as PASS.
- [ ] UNKNOWN would be treated as OK.

- **active_exclusion_found:** no
- **exclusion_review_status:** PASS
- **exclusion_reason:** No active exclusions apply to this manual dogfood scenario.

*Note: Any active exclusion forces transition to full path or BLOCKED/HUMAN_REVIEW_REQUIRED. `active_exclusion_found: no` is not approval. `exclusion_review_status: PASS` is not approval.*

## 8. Scoped Change Plan

1. **Files expected to change:** `tests/fixtures/compact_template_check/aos_farm_671_compact_dogfood.md`
2. **Files explicitly out of scope:** `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
3. **Commands expected to run:** `python3 aos/scripts/aos_compact_template_check.py`
4. **Checks expected to run:** Template integrity check on this document.
5. **Safety boundary notes:** Commit and push remain completely separate boundaries.

*Note: Scope expansion must stop compact path. Unknown files must be surfaced. No protected/canonical file changes inside compact path unless explicitly escalated. No destructive operation.*

## 9. Pre-Execution Decision Prompt

- **current scoped decision requested:** Requesting execution authorization.
- **decision options:**
  1. Request clarification.
  2. Transition to full path.
  3. Authorize scoped execution if explicit human authorization exists.
  4. Block due to UNKNOWN.
  5. Block due to active exclusion.
  6. Defer decision.
- **explicit human phrase or Evidence, if existing phrase applies:** "Manually dogfood the compact safe path on one realistic AOS-FARM task-like scenario"
- **boundaries not granted:** Commit, Push, Merge, Release
- **execution_authorized:** true
- **commit_authorized:** false
- **push_authorized:** false
- **merge_authorized:** false
- **release_authorized:** false

## 10. Execution Authorization Boundary

- **execution_authorized:** true
- **explicit human phrase or Evidence:** Human owner requested AOS-FARM.671 manual dogfood execution.
- **authorization scope:** Creation of dogfood artifact and verification via checker.
- **what execution authorization does not grant:** Execution authorization does not grant commit, push, merge, release, or lifecycle transition.

## 11. Minimal Evidence Summary

1. **What changed:** Dogfood artifact created under tests/fixtures.
2. **Files changed:** `tests/fixtures/compact_template_check/aos_farm_671_compact_dogfood.md`
3. **Checks run:** `aos_compact_template_check.py` on the dogfood output.
4. **NOT_RUN / UNKNOWN:** None. Full validation executed and passed.
5. **Boundary status:** Execution completed; pending commit authorization.

*Note: Evidence may be short. Evidence cannot be absent. NOT_RUN must be explicit. UNKNOWN must be explicit. Evidence is not approval.*

## 12. Evidence Sufficiency Matrix

| Claim | Evidence source | Verification method | Status | Gaps | Required next action |
|---|---|---|---|---|---|
| Scope claim | Diff | Check for out-of-bounds | PASS | None | None |
| Changed files claim | Diff | File list check | PASS | None | None |
| Validation claim | Checker logs | Terminal output | PASS | None | None |
| NOT_RUN / UNKNOWN claim | Self-report | Status report | PASS | None | None |
| Authorization boundary claim | Template | Human confirmation | PASS | None | Wait for commit auth |

*Note: Matrix must stay compact. Matrix references Evidence; it must not duplicate raw logs. NOT_RUN cannot become PASS. UNKNOWN cannot become OK. PASS row does not imply approval.*

## 13. UNKNOWN / NOT_RUN Summary (including FAILED Validation)
1. **UNKNOWN items:** None.
2. **NOT_RUN checks:** None.
3. **Failed/BLOCKED checks:** None.
4. **Full validation status:** `aos_validate.py --json` executed and passed.
5. **Required next action:** Await explicit human commit authorization.
*Note: If UNKNOWN affects safety → transition to full path or BLOCKED. If a required check is NOT_RUN → transition to full path or HUMAN_REVIEW_REQUIRED. If a command was executed and returned non-zero, it must be classified as FAIL or BLOCKED, not NOT_RUN. UNKNOWN must not be hidden in raw logs. NOT_RUN must not be hidden in raw logs.*

## 14. Post-Execution Decision Prompt

- **current scoped decision requested:** Requesting commit authorization
- **decision options:**
  1. Request more Evidence.
  2. Request remediation.
  3. Transition to full path.
  4. Authorize commit with existing phrase.
  5. Defer decision.
  6. Block due to UNKNOWN.
  7. Block due to NOT_RUN.
  8. Block due to scope deviation.
- **explicit human phrase or Evidence, if existing phrase applies:** None yet.
- **boundaries not granted:** Push, Merge, Release
- **execution_authorized:** true
- **commit_authorized:** false
- **push_authorized:** false
- **merge_authorized:** false
- **release_authorized:** false

*Note: Commit authorization must be separate from push authorization. Do not request push authorization in the same decision block as commit authorization. Push authorization is displayed as a future boundary reminder only unless the current boundary is explicitly push.*

## 15. Future Boundary Reminder

- Execution authorization is separate.
- Commit authorization is separate.
- Push authorization is separate.
- Merge authorization is separate.
- Release authorization is separate.
- Commit authorization does not grant push.
- Push authorization does not grant merge.
- Push authorization does not grant release.
- Merge authorization does not grant release.
- Do not request push authorization in the same block as commit authorization.

## 16. General Boundary Reminder

- PASS ≠ approval.
- Evidence ≠ approval.
- CI PASS ≠ approval.
- Eligibility ≠ approval.
- Compact selection ≠ approval.
- Execution authorization ≠ commit authorization.
- Commit authorization ≠ push authorization.
- Push authorization ≠ merge authorization.
- Merge authorization ≠ release authorization.
- Release authorization is separate.
- Human approval cannot be simulated.
- Risk Profile cannot be self-assigned by agent.

## 17. Transition-to-Full-Path Trigger Summary

Transition triggers:
1. Eligibility fails.
2. Any exclusion is active.
3. Scope expands.
4. User intent changes.
5. Protected/canonical file appears.
6. Validator/governance/lifecycle/runtime semantics appear.
7. Required check fails.
8. Required check is NOT_RUN and needed.
9. UNKNOWN affects safety or decision.
10. Human approval boundary requires deeper review.
11. Risk Profile requires human assignment.
12. Evidence insufficient.
13. Agent uncertainty exists.
14. Friction budget cannot be met safely.

- **transition_required:** no
- **transition_reason:** Task successfully fit the minimal budget without safety violations.
- **recommended_next_path:** None.

*Note: If `transition_required` is unknown, treat as HUMAN_REVIEW_REQUIRED or BLOCKED.*

## 18. Risk Profile Handling
1. **agent_recommended_risk:** LOW_RISK_FAST
2. **human_assigned_risk:** none
3. **human_assignment_evidence:** none
4. **compact_path_allowed:** yes, only as scoped dogfood execution authorized by human task directive; not as Risk Profile assignment
5. **reason:** The task is narrow and non-destructive, but Risk Profile assignment remains a separate human boundary.
*Note: Agent may recommend Risk Profile. Agent must not assign Risk Profile. Human Risk Profile assignment cannot be inferred from task title, task mode, dogfood scope, checker PASS, Evidence, compact eligibility, or execution authorization. Missing required human Risk Profile assignment must be surfaced as HUMAN_REVIEW_REQUIRED or BLOCKED if such assignment is required for the next boundary.*

## 19. Template-Local Notes

- This template does not create lifecycle states.
- This template does not create validator statuses.
- This template does not create approval statuses.
- This template reuses existing AOS status vocabulary where possible.
- Any local labels are descriptive only unless future stage explicitly promotes them.
- This template is not Source of Truth for governance.
