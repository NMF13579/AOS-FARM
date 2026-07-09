# Compact Safe Path Template

**Note:** This template does not override canonical governance sources. If this template conflicts with `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, or `02_AOS_Governance_Control_Module_and_Safety_Rules.md`, then 00/01/02 win according to source precedence.

## 1. Header

- **task_id:** [Insert Task ID]
- **task_title:** [Insert Task Title]
- **mode:** [Insert Mode]
- **requested_by:** [Insert Requester]
- **date:** [Insert Date]
- **compact_path_variant:** [Minimal Compact Path | Full Compact Path]
- **current_boundary:** [Insert Current Boundary]
- **execution_authorized:** false
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
- [ ] **Minimal Compact Path**: Preferred only when safe.
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

1. **User request:** [Brief description of the request]
2. **Plain-language goal:** [What is the goal?]
3. **Intended files or areas:** [List of areas to touch]
4. **Expected change type:** [e.g., documentation, minor code fix]
5. **Why compact path may apply:** [Reason for compactness]

## 6. Eligibility review

Checklist:
- [ ] Single clear goal.
- [ ] Small bounded scope.
- [ ] User intent clear.
- [ ] Files known or safely discoverable.
- [ ] No protected/canonical file change.
- [ ] No lifecycle semantics change.
- [ ] No validator semantics change.
- [ ] No runtime enforcement change.
- [ ] No destructive operation.
- [ ] No secrets or credentials.
- [ ] No external deployment/release/production operation.
- [ ] No architecture decision.
- [ ] No Source of Truth rule change.
- [ ] Required sources available.
- [ ] No UNKNOWN affects safety.
- [ ] Required checks can run or NOT_RUN can be explicitly surfaced.
- [ ] Human boundary remains explicit.
- [ ] Risk Profile does not require agent self-assignment.

- **eligible_for_compact_path:** [yes | no | unknown]
- **eligibility_review_status:** [PASS | FAIL | UNKNOWN | HUMAN_REVIEW_REQUIRED]
- **eligibility_reason:** [Explanation]

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

- **active_exclusion_found:** [yes | no | unknown]
- **exclusion_review_status:** [PASS | FAIL | UNKNOWN | HUMAN_REVIEW_REQUIRED | BLOCKED]
- **exclusion_reason:** [Explanation]

*Note: Any active exclusion forces transition to full path or BLOCKED/HUMAN_REVIEW_REQUIRED. `active_exclusion_found: no` is not approval. `exclusion_review_status: PASS` is not approval.*

## 8. Scoped Change Plan

1. **Files expected to change:** [List files]
2. **Files explicitly out of scope:** [List files]
3. **Commands expected to run:** [List commands]
4. **Checks expected to run:** [List checks]
5. **Safety boundary notes:** [Notes]

*Note: Scope expansion must stop compact path. Unknown files must be surfaced. No protected/canonical file changes inside compact path unless explicitly escalated. No destructive operation.*

## 9. Pre-Execution Decision Prompt

- **current scoped decision requested:** [e.g., Requesting execution authorization]
- **decision options:**
  1. Request clarification.
  2. Transition to full path.
  3. Authorize scoped execution if explicit human authorization exists.
  4. Block due to UNKNOWN.
  5. Block due to active exclusion.
  6. Defer decision.
- **explicit human phrase or Evidence, if existing phrase applies:** [Quote phrase if available]
- **boundaries not granted:** [e.g., Commit, Push, Merge, Release]
- **execution_authorized:** [true | false]
- **commit_authorized:** [true | false]
- **push_authorized:** [true | false]
- **merge_authorized:** [true | false]
- **release_authorized:** [true | false]

## 10. Execution Authorization Boundary

- **execution_authorized:** false
- **explicit human phrase or Evidence:** [Blank by default]
- **authorization scope:** [Describe exact bounded scope authorized]
- **what execution authorization does not grant:** Execution authorization does not grant commit, push, merge, release, or lifecycle transition.

## 11. Minimal Evidence Summary

1. **What changed:** [Summary]
2. **Files changed:** [List]
3. **Checks run:** [List]
4. **NOT_RUN / UNKNOWN:** [List]
5. **Boundary status:** [Current authorization status]

*Note: Evidence may be short. Evidence cannot be absent. NOT_RUN must be explicit. UNKNOWN must be explicit. Evidence is not approval.*

## 12. Evidence Sufficiency Matrix

| Claim | Evidence source | Verification method | Status | Gaps | Required next action |
|---|---|---|---|---|---|
| Scope claim | [Logs/Diff] | [Method] | [Status] | [Gaps] | [Action] |
| Changed files claim | [Logs/Diff] | [Method] | [Status] | [Gaps] | [Action] |
| Validation claim | [Logs] | [Method] | [Status] | [Gaps] | [Action] |
| NOT_RUN / UNKNOWN claim | [Logs] | [Method] | [Status] | [Gaps] | [Action] |
| Authorization boundary claim | [Template/Phrase] | [Method] | [Status] | [Gaps] | [Action] |

*Note: Matrix must stay compact. Matrix references Evidence; it must not duplicate raw logs. NOT_RUN cannot become PASS. UNKNOWN cannot become OK. PASS row does not imply approval.*

## 13. UNKNOWN / NOT_RUN Summary

1. **UNKNOWN items:** [List]
2. **NOT_RUN checks:** [List]
3. **Whether any UNKNOWN affects safety:** [Yes/No]
4. **Whether any NOT_RUN check is required for decision:** [Yes/No]
5. **Required next action:** [Action]

*Note: If UNKNOWN affects safety → transition to full path or BLOCKED. If required check is NOT_RUN → transition to full path or HUMAN_REVIEW_REQUIRED. UNKNOWN must not be hidden in raw logs. NOT_RUN must not be hidden in raw logs.*

## 14. Post-Execution Decision Prompt

- **current scoped decision requested:** [e.g., Requesting commit authorization]
- **decision options:**
  1. Request more Evidence.
  2. Request remediation.
  3. Transition to full path.
  4. Authorize commit with existing phrase.
  5. Defer decision.
  6. Block due to UNKNOWN.
  7. Block due to NOT_RUN.
  8. Block due to scope deviation.
- **explicit human phrase or Evidence, if existing phrase applies:** [Quote]
- **boundaries not granted:** [e.g., Push, Merge, Release]
- **execution_authorized:** [true | false]
- **commit_authorized:** [true | false]
- **push_authorized:** [true | false]
- **merge_authorized:** [true | false]
- **release_authorized:** [true | false]

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
- Merge authorization is not dev push authorization.
- Dev push requires separate exact phrase: AOS PUSH DEV OK AOS-FARM.<ID>.
- Feature branch push authorization is not dev push authorization.
- Combined local integration + remote write command is forbidden.
- Post-merge local verification required before dev push.
- Accepted violation state is not authorization precedent.
- Merge type must be explicit or default --ff-only.
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

- **transition_required:** [yes | no | unknown]
- **transition_reason:** [Explanation]
- **recommended_next_path:** [Path]

*Note: If `transition_required` is unknown, treat as HUMAN_REVIEW_REQUIRED or BLOCKED.*

## 18. Risk Profile Handling

1. **agent_recommended_risk:** [Recommended Risk]
2. **human_assigned_risk:** [Assigned Risk]
3. **human_assignment_evidence:** [Evidence]
4. **compact_path_allowed:** [yes | no]
5. **reason:** [Reason]

*Note: Agent may recommend risk. Agent must not assign Risk Profile. Missing required human Risk Profile assignment → HUMAN_REVIEW_REQUIRED or BLOCKED. Compact path cannot bypass Risk Profile review.*

## 19. Template-Local Notes

- This template does not create lifecycle states.
- This template does not create validator statuses.
- This template does not create approval statuses.
- This template reuses existing AOS status vocabulary where possible.
- Any local labels are descriptive only unless future stage explicitly promotes them.
- This template is not Source of Truth for governance.
