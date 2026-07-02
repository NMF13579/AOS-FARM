# Human Checkpoint Package Template

> **GUIDANCE BOUNDARY:**
> This document is a template for human checkpoint packages.
> It is guidance and navigation only.
> Canonical governance remains in `00_AOS_Core_Control.md`,
> `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and
> `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
> This template does not grant approval, execution permission, commit permission,
> push permission, merge permission, release permission, or lifecycle mutation
> permission.

---

> **MANDATORY BOUNDARY:**
> Human checkpoint must be explicit.
> Silence is not approval.
> A report is not approval.
> Evidence is not approval.
> PASS is not approval.
> CI PASS is not approval.
> Only an explicit human decision in this checkpoint constitutes authorization.

---

## Instructions for Use

Copy this template, fill in all fields, and have the human owner complete the
**Human Decision** section. All default values for authorization fields are
`false`. They must be explicitly changed to `true` by the human owner only.

Do not alter the default values below without human instruction.

---

```markdown
# Human Checkpoint Package

## Checkpoint ID

<!-- Example: AOS-FARM-571-EXEC-AUTH-001 -->
checkpoint_id: 

## Task / Stage

<!-- Example: AOS-FARM.571 Stage 3 — Documentation Implementation -->
task_or_stage: 

## Repository

repository: NMF13579/AOS-FARM

## Branch

branch: 

## Requested Decision

<!-- What specific action is the human being asked to authorize? -->
<!-- Be precise: "authorize execution of Stage 3 scoped file creation" -->
requested_decision: 

---

## Risk Profile Assignment

<!-- Human must assign this. Agent may only propose. -->
proposed_by_agent: 
assigned_by_human: 
assignment_evidence: 
<!-- Enter the exact instruction or approved classifier output that assigns the profile. -->

---

## Scope

<!-- Describe the exact scope of the authorized action. -->
<!-- List specific files, directories, or operations. -->
scope: 

---

## Allowed Files

<!-- List every file path that may be created or modified. -->
allowed_files:
  - 

---

## Forbidden Files

<!-- List every file that must NOT be touched. -->
forbidden_files:
  - 00_AOS_Core_Control.md
  - 01_AOS_Assembly_Pipelines_and_Build_Roadmap.md
  - 02_AOS_Governance_Control_Module_and_Safety_Rules.md
  <!-- Add any additional forbidden files below -->

---

## Allowed Actions

<!-- List every action the agent is permitted to take. -->
allowed_actions:
  - 

---

## Forbidden Actions

<!-- List every action the agent must not take. -->
forbidden_actions:
  - commit
  - push
  - merge
  - release
  - lifecycle mutation
  - scope expansion
  - protected/canonical file changes
  <!-- Add any additional forbidden actions below -->

---

## Authorization Decisions

<!-- DEFAULT: All authorizations are FALSE. -->
<!-- Human must change to true explicitly and sign below. -->

execution_authorized: false
commit_authorized: false
push_authorized: false
merge_authorized: false
release_authorized: false
approval_granted: false

---

## Evidence Reviewed

<!-- List the Evidence artifacts reviewed before making this decision. -->
evidence_reviewed:
  - 

---

## Unknowns

<!-- List any unknowns that remain before this checkpoint. -->
<!-- If unknowns exist, do not authorize until resolved. -->
unknowns:
  - 

---

## Not-Run Items

<!-- List validation steps that were not run. -->
<!-- NOT_RUN is not PASS. -->
not_run_items:
  - 

---

## Expiration / One-Time Boundary

<!-- This checkpoint is valid for one specific action only. -->
<!-- It expires after the authorized action is completed or rejected. -->
<!-- It does not authorize future actions of the same type. -->
expiration: one-time-use
valid_for: 
<!-- Example: "Stage 3 scoped file creation on branch build/aos-farm-571-..." -->

---

## Human Decision

<!-- HUMAN: Complete this section. Agent must not fill in this section. -->

human_name: 
decision_date: 
decision: 
<!-- Options: AUTHORIZED / REJECTED / DEFERRED / HUMAN_REVIEW_REQUIRED -->

<!-- If AUTHORIZED, change the relevant authorization fields above to true. -->
<!-- If REJECTED, state reason below. -->
<!-- If DEFERRED, state what is needed before a decision can be made. -->

rejection_reason: 
deferral_condition: 
notes: 

<!-- Signature / confirmation that this is a real human decision: -->
human_signature_or_confirmation: 
```

---

## Boundary Reminder

```text
Silence is not approval.
A report is not approval.
Evidence is not approval.
PASS is not approval.
CI PASS is not approval.
Human checkpoint must be explicit and scoped.
This checkpoint authorizes only the specific action stated above.
Commit authorization does not authorize push.
Push authorization does not authorize merge or release.
```

---

*This template is guidance only. It does not grant execution, commit, push,
merge, release, or approval permission. Canonical governance in 00/01/02
always takes precedence.*
