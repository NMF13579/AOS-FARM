# AOS-FARM.435 — First Controlled Execution Bridge Verification / Dogfood

task_id: AOS-FARM.435
task_name: First Controlled Execution Bridge Verification / Dogfood
mode: verification_dogfood_report_only
risk_profile: MEDIUM_RISK_GUIDED
branch: build/first-controlled-execution-bridge-verification-dogfood
head: 414637b13f50a93d34228063b9b9385e886b2199
origin_dev: 414637b13f50a93d34228063b9b9385e886b2199
ahead_behind: 0 0
remote_baseline_safe_at_start: true
aos_farm_435_commit_performed: false
aos_farm_435_push_performed: false
final_status: AOS_FARM_435_FIRST_CONTROLLED_EXECUTION_BRIDGE_DOGFOOD_PASS_WITH_FINDINGS

## 1. Scope
Verify, by read-only dogfood walkthrough and report-only inspection, whether the AOS-FARM.434 first controlled execution bridge is understandable, safe, and usable as a first-time path for a non-programmer / vibe-coder user moving from `Controlled Task Brief` to Human Execution Authorization, Controlled Execution, Evidence Review, and separate commit/push gates.

## 2. Non-goals
- No implementation changes
- No remediation
- No edits under `aos/`
- No template changes
- No prompt changes
- No `AOS-FARM.436`
- No runner, automation, CI, Spec Kit, SQLite, RAG-light, vector DB, or release work
- No staging, commit, push, merge, cleanup, or destructive operations

## 3. Required Sources Verification
- `00_AOS_Core_Control.md`: present and readable
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`: present and readable
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`: present and readable
- Source precedence applied:
  1. `00_AOS_Core_Control.md`
  2. `02_AOS_Governance_Control_Module_and_Safety_Rules.md` for safety/control semantics
  3. `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md` for assembly/build workflow
  4. other repository files as supporting context only

## 4. Repository Baseline
- Working branch created and used: `build/first-controlled-execution-bridge-verification-dogfood`
- `HEAD`: `414637b13f50a93d34228063b9b9385e886b2199`
- `origin/dev`: `414637b13f50a93d34228063b9b9385e886b2199`
- `ahead/behind`: `0 0`
- Remote baseline safe at task start: `true`
- Pre-existing unrelated dirty worktree paths were observed, including many `D` paths under `agentos/reports/problem-intake/*` and multiple unrelated untracked `reports/*` and `reports/human-checkpoints/*` paths.
- Those paths were treated as out of scope, were not used as Source of Truth for AOS-FARM.435, and were not touched.

## 5. Best-Practice Criteria Applied
- User-needs-first
- Staged disclosure
- Contextual help at the decision boundary
- Visibility of current state and next safe step
- Error prevention against approval confusion and scope creep
- Hard gate verification for `Controlled Task Brief -> Human Execution Authorization -> Controlled Execution`

## 6. Inspected Files
- `aos/START_HERE.md`
- `aos/docs/workflow/first-session-guide.md`
- `aos/docs/workflow/controlled-task-workflow.md`
- `aos/docs/workflow/consumer-runtime-handoff.md`
- `aos/docs/workflow/first-controlled-execution.md`
- `aos/prompts/controlled-execution.md`
- `aos/templates/task-briefs/controlled-task-brief-template.md`
- `aos/templates/checkpoints/human-execution-authorization-template.md`
- `aos/templates/authorization/execution-authorization-package-template.md`
- `aos/templates/reports/execution-report-template.md`
- `aos/templates/reports/evidence-review-template.md`
- `aos/templates/reports/verification-report-template.md`
- `aos/templates/verification/post-execution-verification-template.md`
- `aos/templates/checkpoints/human-push-authorization-template.md`
- `reports/aos-farm-434-first-controlled-execution-bridge-mvp.md`
- Supporting history only: `reports/aos-farm-433-first-controlled-task-execution-flow-audit-and-design.md`

## 7. Dogfood Scenario
Synthetic user scenario applied:
- non-programmer / vibe-coder
- already completed Problem Intake, Technical Assignment, Task Queue, and Controlled Task Brief
- wants to authorize exactly one controlled task safely
- does not know Git internals, CI, runner, Spec Kit, SQLite, RAG, or internal AOS governance terminology
- needs clear answers for what to open, what to review, what to copy into agent chat, what the human must approve explicitly, what remains forbidden, what output to expect, when to stop with `BLOCKED`, and why commit/push still remain forbidden

No real execution, file mutation, runner, automation, or validator implementation was performed as part of this dogfood pass.

## 8. Dogfood Walkthrough Table
| Step | User action | File/template used | Expected user understanding | Safety boundary checked | Result: PASS / GAP / BLOCKED | Evidence |
|---|---|---|---|---|---|---|
| 1 | User starts from START_HERE | `aos/START_HERE.md` | There is a safe consumer path and Controlled Execution is Step 5, not the start | `Controlled Task Brief` still not approval | PASS | `START_HERE` Step 5 and invariant section |
| 2 | User opens first-session guidance | `aos/docs/workflow/first-session-guide.md` | The user must finish intake, TA, queue, and human review before execution | readiness and planning are not approval | PASS | Step 6 and approval clarification |
| 3 | User reaches Controlled Task Brief stage | `aos/templates/task-briefs/controlled-task-brief-template.md` | Brief must contain explicit scope, forbidden scope, validation, evidence target, and authorization reference | readiness != execution authorization | PASS | Execution Context, Scope & Boundaries, Final Boundary Rule |
| 4 | User opens first-controlled-execution guide | `aos/docs/workflow/first-controlled-execution.md` | This is the first-time bridge from brief to authorization to execution to evidence review | hard gate before execution | PASS | Purpose, When To Use, What You Need First |
| 5 | User reviews Controlled Task Brief | `aos/docs/workflow/first-controlled-execution.md` + brief template | User knows exactly what to inspect before approving anything | stop if scope/forbidden/match is ambiguous | PASS | Step 2 BLOCKED conditions |
| 6 | User assigns Risk Profile | `aos/docs/workflow/first-controlled-execution.md` + `aos/templates/checkpoints/human-execution-authorization-template.md` | Agent may propose, but human must assign one explicit Risk Profile | no agent self-assignment, especially `LOW_RISK_FAST` | PASS | Step 3, template checkbox list |
| 7 | User creates Human Execution Authorization | `aos/templates/checkpoints/human-execution-authorization-template.md` | Authorization is separate, brief-specific, and still does not authorize commit/push | execution approval separated from later gates | PASS | Boundary Reminder and Human Decision section |
| 8 | User copies Controlled Execution prompt | `aos/prompts/controlled-execution.md` | User knows exactly what to paste with the brief and authorization | prompt does not itself broaden authority | PASS | opening instructions and final paragraph |
| 9 | Agent preflight checks are reviewed | `aos/prompts/controlled-execution.md` | Agent must verify sources, branch/repo state, authorization, Risk Profile, allowed scope, forbidden scope | fail closed on missing preconditions | PASS | numbered preflight checks 1-6 |
| 10 | Agent execution boundaries are reviewed | `aos/prompts/controlled-execution.md` + `aos/docs/workflow/controlled-task-workflow.md` | Agent must stay inside exact scope and must not commit/push/merge/release | scope expansion and lifecycle mutation blocked | PASS | Hard rules and During execution bullets |
| 11 | Execution Report expectations are reviewed | `aos/templates/reports/execution-report-template.md` | User knows the expected output is an Execution Report plus evidence and separated validation statuses | execution claim != approval | PASS | Modified Files, Validation Results, Evidence, Boundary Verification |
| 12 | Evidence Review template is reviewed | `aos/templates/reports/evidence-review-template.md` | User knows how to review claimed evidence, PASS/NOT_RUN/UNKNOWN, and whether scope was respected | Evidence Review != commit/push approval | PASS | Validation Result Separation, Boundary Reminder, Next Safe Step |
| 13 | User sees commit is still not authorized | `aos/docs/workflow/first-controlled-execution.md` | Commit remains a later, separate human decision | execution authorization does not mutate lifecycle | PASS | What Is Still Not Authorized, Step 8 |
| 14 | User sees push is still not authorized | `aos/docs/workflow/first-controlled-execution.md` + `aos/templates/checkpoints/human-push-authorization-template.md` | Push is a later, separate human decision against explicit target branch | separate push checkpoint preserved | PASS | What Is Still Not Authorized, Push Authorization template |
| 15 | User sees when to stop with BLOCKED | `aos/docs/workflow/first-controlled-execution.md` + `aos/prompts/controlled-execution.md` | Missing source, missing approval, ambiguity, `UNKNOWN`, blocking `NOT_RUN`, or scope creep must stop the flow | fail-closed semantics stay visible | PASS | BLOCKED Conditions and prompt fail-closed rule |

## 9. User Path Verification
1. Can the user find the first controlled execution path from `START_HERE`?
   - Yes. `aos/START_HERE.md` now points directly to `aos/docs/workflow/first-controlled-execution.md`.
2. Can the user understand what to do after `Controlled Task Brief` exists?
   - Yes. `aos/docs/workflow/first-controlled-execution.md` gives a staged sequence from brief review to authorization to prompt handoff to evidence review.
3. Can the user find the new first Controlled Execution document?
   - Yes. It is linked from both `START_HERE` and `first-session-guide`.
4. Can the user find the Controlled Execution prompt?
   - Yes. Step 5 in `first-controlled-execution.md` points directly to `aos/prompts/controlled-execution.md`.
5. Can the user find the Evidence Review template?
   - Yes. Step 7 in `first-controlled-execution.md` names `aos/templates/reports/evidence-review-template.md`.
6. Can the user identify the next safe step after Evidence Review?
   - Yes. The current materials say commit authorization may be prepared only after human review of evidence.
7. Can the user tell when commit is still forbidden?
   - Yes. This remains explicit in `START_HERE`, `first-controlled-execution.md`, the prompt, the human execution authorization template, and the Evidence Review template.
8. Can the user tell when push is still forbidden?
   - Yes. This remains explicit in `first-controlled-execution.md`, the prompt, and the push authorization template.

Conclusion:
- The path is now assembled into a readable first-time bridge.
- A non-programmer still needs to read a few linked artifacts, but the path no longer depends on reconstructing the whole methodology stack.

## 10. Human Approval Boundary Verification
- `Controlled Task Brief != approval`: preserved and surfaced
- readiness != approval: preserved and surfaced
- Human Execution Authorization is required before execution: preserved and surfaced
- Evidence Review != commit approval: preserved and surfaced
- Commit authorization is separate: preserved and surfaced
- Push authorization is separate: preserved and surfaced
- Human approval cannot be simulated: preserved and surfaced

Assessment:
- PASS
- No inspected file weakened the approval boundary.

## 11. Risk Profile Boundary Verification
- Agent may propose Risk Profile: visible in canonical sources and consumer guidance
- Agent cannot assign Risk Profile: visible in `first-controlled-execution.md`, the controlled execution prompt, and the controlled task brief template
- Human must explicitly assign Risk Profile: visible in the first-execution guide and execution authorization template
- `LOW_RISK_FAST` cannot be self-assigned by the agent: explicitly stated in the guide and prompt
- Missing Risk Profile assignment -> `BLOCKED` / `HUMAN_REVIEW_REQUIRED`: functionally preserved by the first-execution guide and prompt

Assessment:
- PASS

## 12. Agent Boundary Verification
The Controlled Execution prompt requires the agent to:
- verify required sources
- verify branch and repo state
- verify Human Execution Authorization
- verify human-assigned Risk Profile
- verify allowed scope
- verify forbidden scope
- stop on missing source
- stop on missing approval
- stop on `UNKNOWN`
- stop on blocking `NOT_RUN`
- stop on ambiguity
- stop on scope expansion
- not commit
- not push
- return an Execution Report with Evidence

Assessment:
- PASS
- The first controlled execution guide and prompt now operationalize the previously fragmented boundary rules into one first-time handoff.

## 13. Evidence Review Boundary Verification
The Evidence Review template separates:
- claimed Evidence
- validation result
- `PASS`
- `NOT_RUN`
- `UNKNOWN`
- scope adherence
- human review decision
- commit approval boundary
- next safe step

Assessment:
- PASS
- The template clearly states that Evidence Review is not commit approval and not push approval.

## 14. Branch-Neutral Push Authorization Check
- Verified current wording: `origin/<target_branch>`
- Verified the template no longer hard-codes `origin/main`
- Verified push rules remain intact:
  - force push is not authorized by this template
  - tag push is not authorized by this template
  - release remains separate
  - target branch remains explicit
  - separate human decision remains required

Assessment:
- PASS

## 15. Scope Creep Check
Verified no AOS-FARM.434 first-execution materials introduced:
- runner as part of the default path
- automation
- SQLite
- RAG-light
- vector DB
- CI workflows
- Spec Kit execution
- production deployment
- release flow
- automatic approval
- automatic execution
- automatic commit
- automatic push
- background agent loop
- database-backed state

Notes:
- Optional runner references remain explicitly marked optional and non-authoritative.
- Consumer-to-runtime handoff keeps runtime/document pipeline references outside the default first-start bridge.

Assessment:
- PASS

## 16. Safety Invariant Verification
These invariants remain visible and preserved:
- `PASS != approval`
- `Evidence != approval`
- `CI PASS != approval`
- `UNKNOWN != OK`
- `NOT_RUN != PASS`
- Human approval cannot be simulated
- Skeleton != implementation
- Scope must not expand without explicit human permission
- Protected/canonical changes require human checkpoint
- Destructive operations are forbidden by default
- `Controlled Task Brief != execution approval`
- readiness != approval
- Human Execution Authorization is required before execution
- Commit authorization remains separate
- Push authorization remains separate

Assessment:
- PASS

## 17. Validation Results
- `git diff --check -- reports/aos-farm-435-first-controlled-execution-bridge-verification-dogfood.md`: PASS
- documented safe markdown validation command: `NOT_RUN`
- reason for `NOT_RUN`: no clearly documented repository command was found for markdown validation in the inspected first-path workflow materials; `aos/tools/dry-run-only/README.md` describes a dry-run-only area but does not document an executable validation command

## 18. Findings
### Finding 1
- severity: `NON_BLOCKING`
- title: Execution authorization templates remain thinner than the new walkthrough guide
- affected files:
  - `aos/templates/checkpoints/human-execution-authorization-template.md`
  - `aos/templates/authorization/execution-authorization-package-template.md`
- detail:
  - The first-time path now works because `aos/docs/workflow/first-controlled-execution.md` supplies the missing staged guidance.
  - However, the execution authorization templates themselves still do not reinforce `BLOCKED` triggers, expected evidence outputs, or the exact fail-closed handling for ambiguity/`UNKNOWN`/blocking `NOT_RUN`.
  - A user who jumps directly into the templates without the walkthrough guide may have less contextual help than ideal.

### Finding 2
- severity: `POLISH`
- title: Human execution authorization wording could be more exact for first-time users
- affected file:
  - `aos/templates/checkpoints/human-execution-authorization-template.md`
- detail:
  - `Requested Authorization: Approval to execute the implementation plan.` is workable, but `implementation plan` is broader than the actual boundary enforced elsewhere.
  - The surrounding materials are stricter and correctly brief-specific, so this is a wording polish issue rather than a safety failure.

## 19. Recommended Remediation, If Any
- No remediation is authorized inside AOS-FARM.435.
- If the human decides the findings are worth fixing now, create a bounded follow-up task to:
  - tighten execution authorization template language to match the exact brief-specific boundary already used in the guide
  - add slightly stronger fail-closed reminders inside the execution authorization templates themselves

## 20. Deferred Items
- Any template remediation or wording changes
- Any implementation or automation work
- Any lifecycle expansion into commit/push execution
- Any cleanup of unrelated dirty worktree paths
- Any AOS-FARM.436 creation

## 21. Final Decision
`AOS_FARM_435_FIRST_CONTROLLED_EXECUTION_BRIDGE_DOGFOOD_PASS_WITH_FINDINGS`

Decision basis:
- The first controlled execution bridge now works as a safe first-time user path for a non-programmer / vibe-coder.
- The gate `Controlled Task Brief -> Human Execution Authorization -> Controlled Execution` is preserved and visible.
- Evidence Review is clearly separated from commit and push approval.
- The remaining gaps are clarity/polish issues, not blockers and not safety boundary failures.

## 22. Next Safe Step
AOS-FARM.435 is ready for human review.

After human review:
- decide whether the documented findings warrant a bounded future remediation task
- if the report is accepted, prepare separate Human Commit Authorization for AOS-FARM.435
- after any authorized commit, push still requires separate Human Push Authorization
