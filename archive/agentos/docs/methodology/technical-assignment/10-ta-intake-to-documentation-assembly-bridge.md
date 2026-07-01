# 10 - TA Intake to Documentation Assembly Bridge

**Document status:** ACTIVE_OPERATIONAL_METHOD_COMPONENT
**Scope:** bridge contract from Technical Assignment intake drafts to Documentation Assembly candidate inputs
**Approval authorized:** false
**Execution authorized:** false
**Implementation authorized:** false
**Commit authorized:** false
**Push authorized:** false
**Production use authorized:** false

---

## 1. Purpose

This document defines the safe handoff from Technical Assignment intake outputs to the AOS Documentation Assembly Pipeline.

It maps draft intake artifacts into candidate inputs for:

- Project Brief;
- Specification;
- Task Brief candidate material;
- Human Review Package.

The bridge exists to preserve traceability and safety. It does not finalize scope, approve requirements, authorize implementation, authorize execution, assign Risk Profile, or promote lifecycle status.

---

## 2. Inputs

Allowed bridge inputs:

```text
PROJECT_SPEC.draft.md
REQUIREMENTS.draft.md
problem-interview-report.md
requirements-checklist-draft.md
problem-intake-run-report.md
```

Input requirements:

- inputs must be produced by the Technical Assignment intake flow or supplied as explicitly reviewed drafts;
- missing sections must remain visible;
- assumptions must remain marked as assumptions;
- contradictions must remain visible;
- open questions must remain blocking unless resolved by explicit human decision;
- implementation hints must remain non-authoritative.

The bridge must not use unrelated dirty or untracked files as source material.

---

## 3. Outputs

Allowed bridge outputs are candidate inputs only:

```text
project_brief_candidate_input
specification_candidate_input
task_brief_candidate_input
human_review_package_input
```

Required output safety fields:

```yaml
bridge_output_status: CANDIDATE_INPUT_ONLY
approval_status: NOT_APPROVED
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
risk_profile_assigned_by_human: missing
task_brief_output_kind: CANDIDATE_ONLY
human_review_required: true
```

The bridge output must not be treated as:

- approval;
- execution authorization;
- implementation authorization;
- final Task Brief;
- final architecture decision;
- final database schema;
- stack approval;
- commit authorization;
- push authorization;
- release authorization;
- production-use authorization.

---

## 4. Artifact Mapping

### 4.1. PROJECT_SPEC.draft.md to Project Brief candidate input

Map these fields:

| PROJECT_SPEC.draft.md section | Project Brief candidate input |
|---|---|
| User Vision | Problem, goal, target user summary |
| Problem Evidence | Problem evidence and urgency |
| Optional Current Workflow | Current state / workflow context |
| Negative Constraints | Constraints and non-goals |
| MVP | Initial scope candidate |
| UNKNOWN / Open Questions | Assumptions and blocking questions |
| Human Decisions Required | Human Review Package input |

Rules:

- user vision remains a user-stated intent, not approved scope;
- problem evidence remains evidence, not approval;
- MVP remains candidate scope, not execution scope;
- assumptions must be marked as assumptions;
- unresolved questions must remain blocking.

### 4.2. PROJECT_SPEC.draft.md to Specification candidate input

Map these fields:

| PROJECT_SPEC.draft.md section | Specification candidate input |
|---|---|
| Requirements Draft | Expected behavior candidates |
| Data Discovery | Data flow / state candidates |
| Information Flow | Data flow / state candidates |
| Access / Permissions | Access and permission candidates |
| Acceptance Criteria | Acceptance criteria candidates |
| Contradictions | Open issues / blocked specification areas |
| Implementation Hints | Non-authoritative notes only |

Rules:

- Data Discovery must not become final database schema;
- implementation hints must not become architecture decisions;
- access notes must not become approved access model;
- contradictions must block finalization until human review.

### 4.3. REQUIREMENTS.draft.md to Task Brief candidate input

Map these fields:

| REQUIREMENTS.draft.md section | Task Brief candidate input |
|---|---|
| Functional Requirements | Candidate required behavior |
| Data Requirements | Candidate data handling scope |
| Access Requirements | Candidate access scope |
| Non-Functional Requirements | Candidate quality constraints |
| Constraints | Forbidden changes / non-goals candidates |
| Security / Privacy | Safety and review requirements |
| Acceptance Criteria | Validation candidates |
| Out of Scope | Forbidden changes candidates |

Rules:

- Task Brief material remains candidate-only;
- a separate scoped Task Brief is required before any implementation;
- exact allowed and forbidden files must be defined in the future Task Brief;
- Risk Profile must be assigned by human before execution;
- validation candidates do not become evidence until run and recorded.

### 4.4. Open questions to UNKNOWN / HUMAN_REVIEW_REQUIRED

Map every unresolved question, contradiction, missing data area, skipped safety area, or uncertain decision to one of:

```text
UNKNOWN
HUMAN_REVIEW_REQUIRED
UNKNOWN_BLOCKED
```

Rules:

- UNKNOWN is blocking;
- UNKNOWN must not be treated as OK;
- missing evidence must remain visible;
- skipped sections must remain visible;
- contradiction resolution requires explicit human decision or documented evidence.

### 4.5. Human decisions to Human Review Package input

Map these items into the Human Review Package input:

- Risk Profile assignment needed;
- scope decisions needed;
- unresolved contradictions;
- sensitive data decisions;
- access and permission decisions;
- implementation authorization needed;
- execution authorization needed;
- acceptance criteria confirmation needed;
- out-of-scope confirmation needed.

Rules:

- Human Review Package input is not human approval;
- human decisions must be recorded as pending until explicit human action;
- `risk_profile_assigned_by_human` remains `missing` unless a human checkpoint or approval witness assigns it;
- `execution_authorized` remains `false` unless a separate human checkpoint authorizes execution.

---

## 5. Bridge Checklist

Before any bridge output can be used as candidate input, verify:

| Check | Required result |
|---|---|
| Required intake artifacts are present or missing artifacts are listed | yes |
| Project Brief candidate input is traceable to intake sections | yes |
| Specification candidate input is traceable to intake sections | yes |
| Task Brief material is marked candidate-only | yes |
| UNKNOWN and HUMAN_REVIEW_REQUIRED items are visible | yes |
| Human decisions are listed as pending | yes |
| Approval is not declared | yes |
| Execution authorization is false | yes |
| Implementation authorization is false | yes |
| Risk Profile is not assigned by the agent | yes |

If any required result is missing:

```yaml
bridge_status: HUMAN_REVIEW_REQUIRED
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
```

---

## 6. Final Boundary

Bridge completion means only:

```yaml
bridge_status: CANDIDATE_INPUTS_PREPARED
ready_for_human_review: true
approval_status: NOT_APPROVED
ready_for_execution: false
execution_authorized: false
implementation_authorized: false
risk_profile_assigned_by_human: missing
```

Bridge completion does not authorize TA execution, code changes, commits, pushes, releases, production use, lifecycle promotion, protected changes, or destructive operations.
