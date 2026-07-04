# AOS-FARM.609 — Automation Opportunities

This document classifies automation candidates only.
It is not approval and does not authorize any implementation.

## Summary

Safe automation is available mainly in evidence collection and package assembly.
Human checkpoints must remain for Risk Profile assignment, scope expansion, execution authorization, commit authorization, push authorization, merge, release, and protected/canonical changes.

## Automation Table

| Candidate | Classification | Why safe/unsafe | Required Evidence | Human checkpoint needed? | Suggested task |
|---|---|---|---|---|---|
| Baseline collection | SAFE_AUTOMATION | Pure read-only git/env capture. | branch, HEAD, remote refs, working tree, recent log | No | Add `aos_baseline_collect.py` |
| Branch/HEAD/origin state check | SAFE_AUTOMATION | Deterministic read-only git queries. | exact SHA and divergence output | No | Fold into shared baseline collector |
| Working tree check | SAFE_AUTOMATION | Read-only status and diff summary only. | `git status`, `git diff --stat`, tracked/untracked split | No | Add tracked-scope and untracked-scope views |
| Changed file list | SAFE_AUTOMATION | Read-only diff enumeration. | exact sorted file list | No | Reuse in review package assembler |
| Diff scope check | SAFE_AUTOMATION | Safe if it only compares against allowed scope and never stages. | expected vs actual file-set diff | No | Add exact candidate-set comparator |
| Queue status check | HUMAN_CHECKPOINT_REQUIRED | Read-only status collection is safe, but acting on "next task" is not. | queue list, queue next, lifecycle reconciler output | Yes for any downstream decision | Route through shared lifecycle state engine |
| Validation output collection | SAFE_AUTOMATION | Running read-only validators is safe if they do not mutate files. | raw validator output, NOT_RUN list, blocked list | No | Central validation capture helper |
| Remote closure verification | SAFE_AUTOMATION | Read-only ref equality and ls-remote checks are deterministic. | local SHA, remote SHA, divergence counts, ls-remote | No | Add one closure verifier |
| Lifecycle map assembly | HUMAN_CHECKPOINT_REQUIRED | Safe to draft automatically, but inferred mapping can be wrong without review. | artifact chain, task chain, commit chain | Yes | Build draft-only lifecycle mapper |
| Final review package assembly | SAFE_AUTOMATION | Safe if package generation is read-only and contains no authorization fields. | exact refs, file set, validation results, unknowns | No | Extend `aos_review_package.py` |
| Missing report detection | SAFE_AUTOMATION | Pure consistency scan. | expected stage list vs actual artifacts | No | Add lifecycle completeness checker |
| Duplicated prompt segment detection | SAFE_AUTOMATION | Static analysis only. | repeated text blocks, repeated command bundles | No | Add prompt/report duplication scanner |
| Risk Profile assignment | HUMAN_CHECKPOINT_REQUIRED | Explicitly reserved to human or approved deterministic classifier. | task scope, constraints, proposed profile | Yes | Recommendation-only helper at most |
| Scope expansion | HUMAN_CHECKPOINT_REQUIRED | Unsafe to automate because it changes allowed work. | exact requested expansion, files, reasons | Yes | No automation beyond warning |
| Execution authorization | HUMAN_CHECKPOINT_REQUIRED | Core boundary. | task, risk profile, allowed files, stop conditions | Yes | No automation beyond package prep |
| Commit authorization | HUMAN_CHECKPOINT_REQUIRED | Core git authority boundary. | candidate file set, validation, clean working tree | Yes | No automation beyond package prep |
| Push authorization | HUMAN_CHECKPOINT_REQUIRED | Core remote authority boundary. | exact commit SHA, target ref, divergence proof | Yes | No automation beyond package prep |
| Protected/canonical changes | UNSAFE_AUTOMATION | Must fail closed without human checkpoint. | explicit human checkpoint plus exact scope | Yes | Reject automatic path |
| Lifecycle mutation | UNSAFE_AUTOMATION | Can silently create false state. | explicit human approval and auditable diff | Yes | Reject automatic path |
| Acceptance/rejection of final result | UNSAFE_AUTOMATION | Decision boundary belongs to human. | review package and evidence | Yes | Reject automatic path |
| Merge/release authorization | UNSAFE_AUTOMATION | High-stakes authority boundary. | exact merge/release package | Yes | Reject automatic path |
| Cross-report response counting | UNKNOWN_BLOCKED | Repo does not preserve full conversation transcripts for exact counts. | full prompt/response logs | Maybe | Only possible with external session logs |

## Human Checkpoints That Must Remain

- Risk Profile assignment
- scope expansion
- execution authorization
- commit authorization
- push authorization
- protected/canonical changes
- lifecycle mutation
- acceptance or rejection of final result
- merge authorization
- release authorization

## Suggested Implementation Shape

- One shared read-only lifecycle state module used by queue, dashboard, and review tools.
- One baseline collector that prints exact git and environment proof blocks.
- One review package assembler that captures refs, changed files, validator output, and unknowns, but never claims approval.
- One remote closure verifier that proves local and remote equality after authorized push.
- One completeness checker that flags missing stage artifacts and duplicated review text.

## Required Guardrails

- Generated packages must set all authorization booleans to false by default.
- Automation may propose, summarize, or collect evidence, but must never mutate approval state.
- Any automation output that infers lifecycle steps must mark inferred items explicitly.
- Any report generator must preserve `NOT_RUN` and `UNKNOWN` as distinct from PASS.
- No tool may treat queue-next, dashboard-next, validation PASS, or evidence presence as execution authorization.
