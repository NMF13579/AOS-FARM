# Simple Control Surface Contract

Status: canonical architecture contract for AOS-FARM.681.2.

This document defines the Simple Control Surface authority boundary. As of AOS-FARM.681.3 it also recognizes a minimal read-only CLI adapter for `/`, `HELP`, and `LANGUAGE`. That adapter is not task execution runtime, not a write-command runtime, not a TUI, not a UI authority, and not a platform write guard.

## Purpose

The Simple Control Surface is a user-facing adapter that helps a non-technical user describe intent, see an explained plan, distinguish required and optional actions, and request separate human decisions. It does not own approval, lifecycle mutation, direct execution, commit, push, integration, merge, release, or Risk Profile assignment.

PASS is not approval. Evidence is not approval. CI PASS is not approval. UNKNOWN is not OK. NOT_RUN is not PASS. Validator output is not human approval.

## Component Ownership

| Component | Owner | Authority | Forbidden responsibility |
|---|---|---|---|
| Simple Control Surface | UI adapter | none | approval, lifecycle, direct execution |
| Documentation Route | Documentation Assembly Pipeline | task formation | execution |
| Command Registry | Governance / Control Module | command semantics | UI localization |
| Locale Registry | UI adapter + Governance validation | aliases/text | grants |
| Code Assembly Pipeline | Code Assembly Pipeline | scoped changes | approval |
| Governance gates | Governance / Control Module | allow/block | human decision |
| Human decision | human | scoped authorization | technical PASS |
| Git platform | repository platform | physical Git effect | scope formation |

The Governance / Control Module does not replace the Documentation Assembly Pipeline. The UI adapter does not become authority. Validators do not create approval.

## Authority Boundaries

Root `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, and `02_AOS_Governance_Control_Module_and_Safety_Rules.md` remain the controlling AOS-FARM development sources. Product folder AOS remains `/aos/`. Root 00/01/02 are not consumer runtime prerequisites. AgentOS and legacy AgentOS names are reference only and are not imported into AOS-FARM.

The Simple Control Surface may display or explain decisions, but it must not create a human approval or claim that local validation proves identity.

## Input Processing Order

```text
Raw Input
-> Unicode Security Filter
-> Namespace Resolver
-> Locale Resolver
-> Intent / Command Resolver
-> Canonical Command Registry
-> Command Contract Loader
-> Operation Classification
-> Required Gates
-> Preview
-> Human Decision
-> Execution Adapter
```

For a free-form task:

```text
Intent Resolver
-> Documentation Assembly Pipeline
-> Documentation Route
-> Explained Scope Proposal
```

## Documentation Route

| Route | Use | Required output | Unknown behavior |
|---|---|---|---|
| NARROW_LOCAL_TASK | narrow local change with clear ownership | compressed route may be proposed | CONTROL_UNKNOWN_BLOCKED |
| FEATURE_OR_BEHAVIOR_CHANGE | user-visible feature or behavior | Project Brief and Specification | CONTROL_UNKNOWN_BLOCKED |
| ARCHITECTURE_OR_CONTROL_CHANGE | authority, control, lifecycle, validator, Source of Truth, or safety behavior | Architecture Decision | CONTROL_UNKNOWN_BLOCKED |

Compressed routing is process compression only. It does not grant execution authorization, Risk Profile assignment, commit, push, integration, release, lifecycle mutation, or protected/canonical mutation.

## Source Of Truth

Canonical Markdown/YAML is authority for this contract. Schemas validate representations. UI state is derived. JSON runtime state is derived. Cache and generated views are derived. Evidence is a factual record, not approval. Operation records are factual records, not approval. Human decision witnesses are separate scoped records. `/.aos-tmp/` is not Source of Truth, not Evidence storage, not approval storage, and not checkpoint storage.

If generated state conflicts with canonical Markdown/YAML, canonical Markdown/YAML wins. If authority is unknown, the control state is `CONTROL_UNKNOWN_BLOCKED`.

## Human Decision Model

The following decisions are separate:

| Decision | Separate from |
|---|---|
| scope confirmation | execution authorization |
| Risk Profile assignment | scope confirmation and execution |
| execution authorization | commit authorization |
| commit authorization | push authorization |
| push authorization | integration authorization |
| integration or merge authorization | release authorization |
| lifecycle authorization | technical validation |
| release authorization | integration success |

Scope confirmation is not execution authorization. Execution authorization is not commit authorization. Commit authorization is not push authorization. Push authorization is not integration authorization. Integration authorization is not release authorization.

## Trust Ceiling

A local human decision witness can record binding, claimed actor, claimed role, channel, and timestamps. It does not necessarily prove identity, does not necessarily have an independent trust domain, and must not be described as externally authenticated approval unless an external authentication mechanism exists and is separately approved.

## State Namespaces

Inter-module contracts must use typed namespaces:

```yaml
lifecycle:
  status: <canonical-lifecycle-value>
control:
  state: <CONTROL_*>
operation:
  state: <OPERATION_*>
validation:
  status: <PASS|FAIL|NOT_RUN|UNKNOWN>
```

Untyped cross-module `status` fields are forbidden. Approval, Evidence, validation, control, operation, lifecycle, and authorization flags remain separate.

## Effect Model

Every command must declare:

```yaml
effects:
  tracked_worktree_write: false
  untracked_worktree_write: false
  canonical_artifact_write: false
  git_index_write: false
  git_object_write: false
  local_git_ref_write: false
  remote_ref_write: false
  external_system_write: false
  temp_write: false
```

The contract can describe future effects. It does not perform them.

## Unicode Security

Aliases use Unicode normalization form `NFC` through the standard library. The contract does not claim full confusable protection because the standard library does not provide complete UTS 39 confusable detection.

Command aliases must reject bidi controls, zero-width characters, invisible separators, control characters, and unexpected variation selectors. Write-related aliases must reject mixed-script aliases. Read-only fuzzy suggestions may be displayed in a future adapter, but automatic execution is forbidden. Write-related commands require exact registered aliases and fuzzy matching is forbidden.

## Minimal Safety Floor

The user cannot remove these controls from the plan:

Scope Gate, Risk Profile Gate, Evidence Gate, False PASS Gate, Protected/Canonical Gate, Lifecycle Mutation Gate, UNKNOWN handling, NOT_RUN disclosure, required validation, reconciliation, and fresh repository check.

## Execution Package Template Conflict

`aos/templates/execution-packages/executor-handoff-package-template.yaml` is recognized as the neutral pre-authorization handoff template.

`aos/templates/execution-packages/controlled-execution-package-template.yaml` is post-authorization only. Its authorization fields must not be treated as automatically created human decisions. Future package generation must receive authorization binding from a separate Human Decision Witness. This contract does not modify either template.

## Validation

`aos/scripts/aos_simple_control_contract_check.py` validates contract integrity only. It may report `CONTRACT_VALID`, `CONTRACT_INVALID`, or `UNKNOWN_BLOCKED`. It must not report `APPROVED`, `EXECUTION_AUTHORIZED`, `COMMIT_AUTHORIZED`, `PUSH_AUTHORIZED`, or `INTEGRATION_AUTHORIZED`.

## Non-Goals

This task does not implement CLI, TUI, UI, runtime execution, shell execution, write commands, commit orchestration, push orchestration, integration, merge, release, lifecycle mutation, platform-enforced write blocking, external authentication, operation ledger runtime, or GitHub branch protection.

## Future Implementation Slices

Future slices may add a read-only menu foundation, locale rendering, command discovery, preview views, operation records, runtime adapters, or platform guards only after separate scope confirmation, Risk Profile assignment, and execution authorization. The `INTEGRATE` command remains blocked while `integration_mechanism: UNKNOWN`.

## AOS-FARM.681.3 Read-Only Adapter Contract

`aos/scripts/aos_control_surface.py` is a read-only CLI adapter. It may load the canonical command registry and locale registry, normalize input with Unicode NFC, reject unsafe Unicode controls, resolve `/`, `/help`, `/помощь`, `/language`, `/язык`, `/aos help`, and `/aos помощь`, render the registry menu, and show registry metadata through `--details`.

It must not execute shell commands, use subprocess, create files, write settings, write cache, create operation records, stage, commit, push, fetch, integrate, merge, mutate lifecycle, create a human witness, assign Risk Profile, or claim platform enforcement.

Stable exit codes:

| Code | Meaning |
|---:|---|
| 0 | read-only command completed |
| 2 | invalid CLI usage |
| 3 | Unicode or ambiguity blocked |
| 4 | known command unavailable |
| 5 | registry or contract invalid |
| 6 | unknown command |

Exit code 0 is not approval. Command request is not authorization.

## AOS-FARM.681.4 Planning Foundation Contract

`aos/runtime/simple_control_planning.py` implements deterministic planning and decision-preparation helpers only. It may create User Intent Records, validate read-only Analysis Packages, render Explained Scope Proposals, revise proposals, prepare Scope Confirmation Record candidates, recommend Risk Profile, and prepare Risk Profile Assignment Record candidates.

This planning foundation is not a semantic analysis engine. If an Analysis Package is absent, analysis status remains `NOT_RUN`, control state remains `CONTROL_ANALYZING`, and the runtime must not invent repository findings.

Implemented planning commands:

| Command | Status | Boundary |
|---|---|---|
| ANALYZE | IMPLEMENTED_PLANNING_ONLY | creates intent record and validates optional analysis package |
| PLAN | IMPLEMENTED_PLANNING_ONLY | renders proposal from valid analysis package |
| ACCEPT_SCOPE | IMPLEMENTED_DECISION_PREPARATION_ONLY | emits scope confirmation candidate to stdout only |
| REVISE_SCOPE | IMPLEMENTED_PLANNING_ONLY | emits revised proposal to stdout only |
| SELECT_RISK | IMPLEMENTED_DECISION_PREPARATION_ONLY | emits recommendation or Risk Profile assignment candidate to stdout only |

Decision-preparation output is not persisted, not externally authenticated, not approval, and not execution authorization. Scope confirmation is not Risk Profile assignment. Risk Profile assignment is not execution authorization.

## AOS-FARM.681.5 Read-Only Validation And Derived Status Contract

`aos/runtime/simple_control_status.py` validates structured planning bundles and derives advisory control state. It validates User Intent, Analysis Package, Explained Scope Proposal, Scope Confirmation, and Risk Profile Assignment records by binding and completeness.

It does not observe Git state, run user tests, execute validators on behalf of the user task, create Evidence, persist status, create human witnesses, approve results, authorize execution, or mutate lifecycle.

`VALIDATE` means validation of the provided structured artifact bundle only. A validation `PASS` means contract integrity for the bundle; it is not approval, execution authorization, Code Assembly Pipeline readiness, or platform enforcement. `STATUS`, `NEXT`, and `SHOW_DETAILS` render derived read-only views from the same bundle. They are advisory outputs, not Sources of Truth.

The allowed 681.5 derived states are limited to `CONTROL_ANALYZING`, `CONTROL_ANALYZED`, `CONTROL_SCOPE_CONFIRMATION_REQUIRED`, `CONTROL_RISK_SELECTION_REQUIRED`, `CONTROL_EXECUTION_AUTHORIZATION_REQUIRED`, `CONTROL_BLOCKED`, and `CONTROL_UNKNOWN_BLOCKED`. This slice must not derive `CONTROL_READY_FOR_EXECUTION`, `CONTROL_EXECUTING`, `CONTROL_CHANGES_PREPARED`, `CONTROL_READY_TO_COMMIT`, `CONTROL_COMMITTED`, `CONTROL_PUSHED`, or `CONTROL_INTEGRATED`.

`NEXT` recommends only the next command label. At `CONTROL_EXECUTION_AUTHORIZATION_REQUIRED`, it may show `EXECUTE` as the next required command, but the recommendation itself does not execute anything and does not grant authorization.

## AOS-FARM.681.6 Execution Orchestration Foundation Contract

`aos/runtime/simple_control_execution.py` implements the Simple Control Surface execution control plane for preview and package preparation only. It validates a ready planning bundle, exact execution request, execution authorization witness, read-only repository observation, scoped planned actions, and binding chain.

`EXECUTE` in this slice prepares an execution preview and Execution Package. It does not apply planned actions, change product files, run user tests, run arbitrary validators, write Git metadata, create commits, push, integrate, mutate lifecycle, persist operation records, or claim platform enforcement.

The Execution Authorization Witness grant is limited to `prepare_exact_execution_package`. It does not grant production file mutation, commit, push, integration, merge, release, or lifecycle mutation. The witness uses `LOCAL_DECLARED` authentication and is not externally authenticated approval.

The successful preview state is `CONTROL_READY_FOR_EXECUTION` with `OPERATION_PREVIEWED`. This means the exact package is ready for a future controlled executor after a separate Operation Control Foundation. It does not mean execution started. Production execution remains unavailable with `OPERATION_CONTROL_FOUNDATION_NOT_IMPLEMENTED`.

If a planned action is outside confirmed write scope, the orchestrator returns `CONTROL_SCOPE_EXPANSION_REQUIRED` and a Scope Expansion Proposal. It does not add the action automatically.

## AOS-FARM.681.7 Operation Control Foundation Contract

`aos/runtime/simple_control_operations.py` implements the local Operation Control Foundation and controlled local write backend for `CREATE_FILE` and `REPLACE_FILE`. It introduces an exact Operation ID, local operation record, atomic operation claim, single-use production witness consumption marker, preimage verification, postimage verification, idempotent completed-operation retry, and reconciliation results.

The operation store path is `/.aos-tmp/simple-control/operations/` with sibling `locks/` and `consumed/` directories under the operation repository root. This store is local-only, disposable, not Source of Truth, not Evidence, not approval, not a checkpoint, and not lifecycle authority.

The controlled backend must not be applied to the active AOS-FARM repository during AOS-FARM.681.7. Tests validate side effects only in `tempfile.TemporaryDirectory` sandboxes. The runtime blocks apply/reconcile mode when the current working directory is the active AOS-FARM checkout.

`EXECUTE` now has three contract modes:

| Mode | Effect | Boundary |
|---|---|---|
| preview | prepare preview and Execution Package | no production operation starts |
| apply | apply exact package once in an allowed sandbox | requires Operation ID and `PRODUCTION_EXECUTION_AUTHORIZATION` |
| reconcile-only | inspect target pre/postimage state | does not repeat side effects |

The Production Execution Authorization Witness grant is limited to `apply_exact_execution_package_once` for one Operation ID and one Execution Package binding. It does not grant protected/canonical write, destructive operation, commit, push, integration, merge, release, or lifecycle mutation. It uses `LOCAL_DECLARED` authentication and is not externally authenticated approval.

Supported file effects:

| Action | Supported | Notes |
|---|---:|---|
| CREATE_FILE | yes | exclusive creation, parent must already exist, postimage hash verified |
| REPLACE_FILE | yes | preimage hash required, same-directory temporary file, atomic `os.replace`, postimage hash verified |
| DELETE/MOVE/RENAME/CHMOD/SYMLINK/MKDIR/SHELL/Git operations | no | blocked by contract |

Single-file create/replace atomicity is implemented within filesystem limits. Multi-file transaction atomicity is not implemented. Rollback is not promised. Partial progress is tracked, and partial, blocked, or unknown results require reconciliation and human review before retry.

Successful controlled apply returns `CONTROL_CHANGES_PREPARED` with `OPERATION_COMPLETED`. It means local file changes were prepared in the allowed sandbox. It is not commit authorization, push authorization, integration authorization, release authorization, lifecycle mutation, approval, Evidence, or platform enforcement.

## AOS-FARM.681.8 Commit And Build-Branch Push Control Contract

`aos/runtime/simple_control_git.py` implements controlled Git commit and Build-branch push controls for isolated temporary Git repositories only. During AOS-FARM.681.8 it must not stage, commit, or push the active AOS-FARM candidate.

Commit flow:

```text
Candidate Manifest
-> Commit Request
-> Commit Preview
-> Commit Authorization Witness
-> exact git add -- <manifest paths>
-> staged tree verification
-> one ordinary commit
-> commit reconciliation
```

Push flow:

```text
Exact Commit
-> Push Request
-> remote baseline observation by git ls-remote --refs
-> Push Preview
-> Push Authorization Witness
-> git push --porcelain origin <exact-oid>:<exact-build-ref>
-> remote verification
-> push reconciliation
```

The commit witness grants only `stage_exact_candidate_manifest` and `create_one_ordinary_commit`. It does not grant push, integration, merge, release, lifecycle mutation, amend, history rewrite, or cleanup.

The push witness grants only `push_exact_commit_to_exact_build_ref`. It does not grant commit, push to dev, push to main, force push, tag push, integration, merge, release, branch deletion, or lifecycle mutation.

Build-branch push policy requires an exact `refs/heads/build/...` target ref and an exact source commit OID. Push to `dev`, push to `main`, wildcard refspecs, tag push, branch deletion, force push, fetch, merge, rebase, reset, clean, checkout, and switch are outside this contract.

Git operation records remain local disposable operation data under `.aos-tmp/simple-control/` inside the isolated test repository. They are not Source of Truth, Evidence, approval, or lifecycle authority.
