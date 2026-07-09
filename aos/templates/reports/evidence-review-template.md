# Evidence Review: [Task Name]

## Human Review Package Contract

This package is a decision-support artifact for one scoped human review.

It provides:

1. Task summary.
2. Scope summary.
3. Evidence summary.
4. Validation summary.
5. UNKNOWN / NOT_RUN summary.
6. Risk / escalation summary.
7. Current scoped decision options.
8. Authorization boundary.

This package does not provide:

1. Automatic approval.
2. Execution authorization.
3. Commit authorization.
4. Push authorization.
5. Merge authorization.
6. Release authorization.
7. Lifecycle mutation.
8. Protected/canonical change authorization.

PASS is not approval.
Evidence is not approval.
CI PASS is not approval.

## Reviewer Summary

In plain language:

1. What happened?
   - [Summary of what was done]
2. What Evidence supports it?
   - [Summary of evidence]
3. What is still UNKNOWN?
   - [Summary of unknowns]
4. What was NOT_RUN?
   - [Summary of not run checks]
5. What decision is being asked from the human?
   - [Summary of decision]
6. What this decision will not authorize?
   - [Summary of what is not authorized]

## Review Scope

- **Controlled Task Brief Reviewed:** [Path or ID]
- **Execution Report Reviewed:** [Path or ID]
- **Controlled Execution Evidence Report Reviewed:** [Path]
- **Human Execution Authorization Reviewed:** [Path or ID]

## Evidence Sufficiency Matrix

| Claim | Evidence source | Verification method | Status | Reviewer confidence | Gaps | Required next action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Scope claim | [source] | [method] | [status] | [confidence] | [gaps] | [action] |
| Changed files claim | [source] | [method] | [status] | [confidence] | [gaps] | [action] |
| Validation claim | [source] | [method] | [status] | [confidence] | [gaps] | [action] |
| NOT_RUN / UNKNOWN claim | [source] | [method] | [status] | [confidence] | [gaps] | [action] |
| Authorization boundary claim | [source] | [method] | [status] | [confidence] | [gaps] | [action] |

*(Allowed status values: PASS, FAIL, NOT_RUN, UNKNOWN, BLOCKED, HUMAN_REVIEW_REQUIRED, NOT_APPLICABLE)*

## Boundary Checklist

- [ ] 1. PASS was not treated as approval.
- [ ] 2. Evidence was not treated as approval.
- [ ] 3. CI PASS was not treated as approval.
- [ ] 4. UNKNOWN was not treated as OK.
- [ ] 5. NOT_RUN was not treated as PASS.
- [ ] 6. No human approval was simulated.
- [ ] 7. No Risk Profile was self-assigned by agent.
- [ ] 8. No protected/canonical file was changed without checkpoint.
- [ ] 9. No destructive operation was performed.
- [ ] 10. Commit authorization was separated from push authorization.
- [ ] 11. Push authorization was separated from merge authorization.
- [ ] 12. Push authorization was separated from release authorization.
- [ ] 13. Merge authorization was separated from release authorization.
- [ ] 14. Merge authorization was not treated as dev push authorization.
- [ ] 15. Feature branch push authorization was not treated as dev push authorization.
- [ ] 16. Dev push authorization used separate exact phrase.
- [ ] 17. Combined local integration + remote write command was not used.
- [ ] 18. Post-merge local verification was performed before dev push.
- [ ] 19. Accepted violation state was not used as authorization precedent.
- [ ] 20. Merge type was explicit or defaulted to --ff-only.
- [ ] 21. Lifecycle transition was not implied by Evidence.
- [ ] 22. Scope did not expand silently.
- [ ] 23. /.aos-tmp/ was not used as Source of Truth.

## Risk Profile and Escalation

Risk Profile:

1. Assigned by human: yes/no/unknown
2. Assignment Evidence: [explicit human Evidence or none]
3. Proposed by agent: yes/no
4. Proposed value: [if any]
5. Human assignment required: yes/no/unknown

Escalation triggers:

- [ ] 1. Protected/canonical file touched.
- [ ] 2. Lifecycle transition requested.
- [ ] 3. Destructive operation requested.
- [ ] 4. Risk Profile missing where required.
- [ ] 5. Evidence missing for a claim.
- [ ] 6. Required check NOT_RUN.
- [ ] 7. UNKNOWN affects decision.
- [ ] 8. Scope changed from original task.
- [ ] 9. Merge/release boundary reached.
- [ ] 10. Human reviewer unavailable.

*(If any trigger is checked, final review outcome must not be APPROVED)*

## Current Scoped Decision

Human decision required: yes/no/unknown

Current decision type:
[Select ONE]
- [ ] 1. Evidence sufficiency review.
- [ ] 2. Additional Evidence required.
- [ ] 3. Remediation required.
- [ ] 4. Scope correction required.
- [ ] 5. Escalation required.
- [ ] 6. Defer decision.

Decision options:
[Select ONE]
- [ ] 1. Accept Evidence as sufficient for this scoped review only.
- [ ] 2. Request additional Evidence.
- [ ] 3. Request remediation.
- [ ] 4. Reject the package.
- [ ] 5. Block due to UNKNOWN.
- [ ] 6. Block due to NOT_RUN required checks.
- [ ] 7. Escalate to protected/canonical review.
- [ ] 8. Escalate to human Risk Profile assignment.
- [ ] 9. Defer decision.

This decision does not imply:
1. Execution authorization.
2. Commit authorization.
3. Push authorization.
4. Merge authorization.
5. Release authorization.
6. Lifecycle transition.
7. Approval outside the stated scope.

## Boundaries Not Granted By This Review

This review does not grant:

1. Execution authorization.
2. Commit authorization.
3. Push authorization.
4. Merge authorization.
5. Release authorization.
6. Deployment authorization.
7. Lifecycle transition.
8. Protected/canonical file change authorization.
9. Risk Profile assignment unless explicit human assignment Evidence is present.
10. General approval outside the stated scope.

Required boundary phrases remain separate (do not bundle):
1. AOS COMMIT OK <task-id>
2. AOS PUSH OK <task-id>
3. AOS MERGE TO DEV OK <task-id>
4. AOS MERGE TO MAIN OK <task-id>
5. AOS RELEASE OK <task-id>

## Template-Local Review Outcome

These labels are template-local only.
They are not lifecycle states, validator statuses, or approval statuses.

outcome_label: [Select from: HUMAN_REVIEW_REQUIRED, HUMAN_REVIEW_REQUIRED_EVIDENCE_SUFFICIENCY_NOTED, REMEDIATION_REQUIRED, ADDITIONAL_EVIDENCE_REQUIRED, BLOCKED_UNKNOWN, BLOCKED_NOT_RUN_REQUIRED_CHECKS, BLOCKED_SCOPE_DEVIATION, BLOCKED_PROTECTED_CANONICAL_REVIEW_REQUIRED, BLOCKED_RISK_PROFILE_REVIEW_REQUIRED]
