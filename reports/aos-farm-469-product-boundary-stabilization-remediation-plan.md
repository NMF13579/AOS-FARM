# AOS-FARM.469 — Product Boundary Stabilization and Clean Embed Remediation Plan

## 1. Baseline
- origin/main SHA: 9fc5c78abaf13ed328b190a8a38dbdec78b8fa97
- origin/dev SHA: d1144379990acc70bd3198aa31efbc92fc4ebf38
- branch relation: 0 90 (main...dev)
- local status: dev branch, with dirty working tree (untracked reports and test scripts)
- mode: STRICT READ-ONLY PLANNING

## 2. Executive summary
- AOS PACKAGE CLEAN EMBED STATUS before remediation: FAIL
- MERGE TECHNICAL READINESS: NO
- MERGE GOVERNANCE DECISION: REQUIRES_HUMAN_DECISION
- main conclusion: The `/aos/` boundary contains significant internal reference leakage, developer-only artifacts posing as consumer examples, and skeleton placeholders. The package must be sanitized, rewritten to consumer-facing language, and disconnected from internal `agentos/` paths before it can be cleanly embedded into target repositories.

## 3. Confirmed blockers
[CLASSIFICATION] [CRITICAL] [origin/dev] [/aos/]
Finding: The /aos/ folder is not yet clean embed ready.
Evidence: 
- command: `git grep -n -E 'agentos/|AOS-FARM'`
- observed: Multiple internal development paths referenced in consumer-facing documents.
Impact: Agents embedding this package will attempt to read non-existent internal paths in the target repository.
Recommendation: Execute full path-level remediation as planned below.
Required decision: ACCEPT

[CLASSIFICATION] [HIGH] [origin/dev] [aos/prompts/problem-intake.md]
Finding: Intake prompt references root 00/01/02 and agentos/docs/.
Evidence: 
- command: `git grep -n -E '00_AOS|agentos/' origin/dev -- aos/prompts/problem-intake.md`
- observed: Direct imports of `agentos/docs/methodology/...`
Impact: Agent failure when run in consumer repository without AOS-FARM root sources.
Recommendation: Split internal and consumer prompts or rewrite to rely solely on `/aos/` documents.
Required decision: ACCEPT

[CLASSIFICATION] [HIGH] [origin/dev] [llms.txt]
Finding: llms.txt is stale and points agents to `./agentos/`.
Evidence: 
- command: `git show origin/dev:llms.txt`
- observed: Contains references to `AgentOS` and `agentos/`.
Impact: Misguides consumer agents at the entry point.
Recommendation: Rewrite to point to `/aos/START_HERE.md` and consumer context.
Required decision: ACCEPT

[CLASSIFICATION] [MEDIUM] [origin/dev] [aos/tools/optional/problem-intake-runner/problem_intake_runner.py]
Finding: Python runner defaults output to `agentos/reports/problem-intake`.
Evidence: 
- command: `git grep 'output-root' origin/dev -- aos/tools/`
- observed: `default="agentos/reports/problem-intake"`
Impact: Creates internal folders in consumer repos.
Recommendation: Change default to `.aos-tmp/problem-intake/`.
Required decision: ACCEPT

[CLASSIFICATION] [MEDIUM] [origin/dev] [aos/docs/ and root]
Finding: Several package-facing docs are skeletons.
Evidence: 
- command: `git ls-tree -r --format='%(objectsize) %(path)' origin/dev -- aos/ | awk '$1 == 752'`
- observed: 24+ identical 752-byte skeleton files.
Impact: Incomplete consumer guidance.
Recommendation: Rewrite or remove skeleton files.
Required decision: ACCEPT

[CLASSIFICATION] [MEDIUM] [origin/dev] [aos/reports/examples/]
Finding: Examples contain AOS-FARM-specific task IDs and root references.
Evidence: 
- command: `git grep 'AOS-FARM.438' origin/dev -- aos/reports/examples/`
- observed: Hardcoded internal execution evidence.
Impact: Confuses consumers with irrelevant history.
Recommendation: Sanitize to generic `TASK-001` or move to `tests/fixtures/`.
Required decision: ACCEPT

[CLASSIFICATION] [LOW] [origin/dev] [aos/tools/README.md]
Finding: README understates Python helpers and write capabilities.
Evidence: 
- observed: Lacks disclosure of file mutation (`output_path.write_text`).
Impact: Violates safe read-only expectations.
Recommendation: Explicitly document write-capable artifacts in tools README.
Required decision: ACCEPT

[CLASSIFICATION] [HIGH] [origin/dev] [aos/schemas/task-quality-check-package.schema.json]
Finding: Safety invariant implemented as free boolean.
Evidence: 
- observed: `task_quality_pass_is_not_human_result_acceptance` is mutable.
Impact: Allows bypassing human acceptance gate.
Recommendation: Harden schema to require `const: true`.
Required decision: ACCEPT

[CLASSIFICATION] [CRITICAL] [origin/dev] [Root Files]
Finding: Broad protected/public drift from origin/main.
Evidence: 
- command: `git diff origin/main...origin/dev`
- observed: Changes in 00, 01, 02.
Impact: Unverified control module drift.
Recommendation: Do not merge. Separate product remediation from root drift.
Required decision: REQUIRES_HUMAN_DECISION

## 4. Product boundary model
| PATH | Current role | Desired role | Problem | Recommended action | Risk | Human checkpoint required? |
|---|---|---|---|---|---|---|
| `llms.txt` | LEGACY_REFERENCE_ONLY | TARGET_ROOT_TEMPLATE | Points to agentos | REWRITE_REQUIRED | HIGH | Yes |
| `README.md` | ROOT_DEVELOPMENT_ONLY | ROOT_DEVELOPMENT_ONLY | Mixed context | REWRITE_REQUIRED | MED | No |
| `AGENTS.md` | TARGET_ROOT_TEMPLATE | TARGET_ROOT_TEMPLATE | Contains AOS-FARM constraints | REWRITE_REQUIRED | HIGH | Yes |
| `aos/START_HERE.md` | CONSUMER_PACKAGE_REQUIRED | CONSUMER_PACKAGE_REQUIRED | Excludes agentos incorrectly | REWRITE_REQUIRED | MED | No |
| `aos/AGENT_CONTEXT.md` | CONSUMER_PACKAGE_REQUIRED | CONSUMER_PACKAGE_REQUIRED | Mentions internal vectors | REWRITE_REQUIRED | MED | No |
| `aos/prompts/problem-intake.md` | ROOT_DEVELOPMENT_ONLY | CONSUMER_PACKAGE_REQUIRED | Imports internal methods | SPLIT_INTERNAL_AND_CONSUMER_PROMPTS | HIGH | Yes |
| `aos/tools/optional/problem-intake-runner/problem_intake_runner.py` | OPTIONAL_HELPER_TOOLING | OPTIONAL_HELPER_TOOLING | Writes to agentos/ | REWRITE_REQUIRED | MED | No |
| `aos/schemas/task-quality-check-package.schema.json` | CONSUMER_PACKAGE_REQUIRED | CONSUMER_PACKAGE_REQUIRED | Boolean safety invariant | REWRITE_REQUIRED | HIGH | Yes |
| `aos/reports/examples/` | DEV_ONLY_EVIDENCE | DEV_ONLY_FIXTURE | Has real AOS-FARM history | MOVE_CANDIDATE | LOW | No |

## 5. Internal/reference leakage map
[CLASSIFICATION] [HIGH] [origin/dev] [llms.txt]
Finding: Internal reference in `llms.txt`.
Evidence: 
- observed: Mentions `AgentOS` and `agentos/`.
Impact: Misdirects consumer agent.
Recommendation: REWRITE_TO_AOS_PATH
Required decision: ACCEPT

[CLASSIFICATION] [HIGH] [origin/dev] [aos/prompts/problem-intake.md]
Finding: Internal method leakage.
Evidence: 
- observed: Imports `agentos/docs/methodology/technical-assignment/00-overview-and-routing.md`
Impact: Agent failure on external repo.
Recommendation: REWRITE_TO_AOS_PATH
Required decision: ACCEPT

[CLASSIFICATION] [HIGH] [origin/dev] [aos/docs/methodology/technical-assignment/README.md]
Finding: Directory leakage.
Evidence: 
- observed: Refers to `agentos/docs/methodology/technical-assignment/`
Impact: Documentation inconsistency.
Recommendation: REWRITE_TO_AOS_PATH
Required decision: ACCEPT

## 6. llms.txt remediation requirements
[CLASSIFICATION] [HIGH] [origin/dev] [llms.txt]
Finding: Entry prompt for agents is not configured for consumer package.
Evidence: 
- observed: Refers to legacy AgentOS structure.
Impact: Immediate failure upon consumer onboarding.
Recommendation: Rewrite `llms.txt` to enforce:
1. AOS consumer package is located in `./aos/`.
2. Start with `./aos/START_HERE.md`.
3. Agent context is `./aos/AGENT_CONTEXT.md`.
4. Root 00/01/02 are AOS-FARM development canonical sources, not consumer runtime prerequisites.
5. PASS/Evidence/CI PASS are not approval.
6. UNKNOWN/NOT_RUN are not PASS.
7. Human approval cannot be simulated.
Required decision: ACCEPT

## 7. Consumer prompts remediation requirements
[CLASSIFICATION] [HIGH] [origin/dev] [aos/prompts/problem-intake.md]
Finding: The prompt is strongly coupled to AOS-FARM internal runbooks.
Evidence: 
- observed: Mentions `00_AOS_Core_Control.md` and `agentos/docs/methodology/technical-assignment/runbooks/jtbd-runbook.md`.
Impact: Not consumer-safe.
Recommendation: SPLIT_INTERNAL_AND_CONSUMER_PROMPTS. Create a generic consumer version inside `/aos/` that relies only on provided `/aos/` templates and drops dependencies on `00/01/02` and `agentos`.
Required decision: REQUIRES_HUMAN_DECISION

## 8. Optional tooling remediation requirements
[CLASSIFICATION] [MEDIUM] [origin/dev] [aos/tools/optional/problem-intake-runner/problem_intake_runner.py]
Finding: Hardcoded output directory outside of `/aos/`.
Evidence: 
- observed: `default="agentos/reports/problem-intake"`
Impact: Pollutes target repo with non-standard folders.
Recommendation: The default output path should be `.aos-tmp/problem-intake/`. This avoids polluting the consumer's permanent workspace with temporary drafts, clearly separating generated artifacts from tracked code until explicitly moved.
Required decision: ACCEPT

## 9. Skeleton rewrite plan
[CLASSIFICATION] [MEDIUM] [origin/dev] [Multiple Files]
Finding: Placeholder files block a clean embed.
Evidence: 
- observed: Identical 752-byte files containing exclusions boilerplates.
Impact: Bloat and unclear instructions.
Recommendation: 
- `aos/SELF_TEST.md`: REWRITE_REQUIRED
- `aos/MANIFEST.md`: REWRITE_REQUIRED
- `aos/VERSION.md`: REWRITE_REQUIRED
- `aos/COMPATIBILITY.md`: REWRITE_REQUIRED
- `aos/CHANGELOG.md`: REWRITE_REQUIRED
- `aos/UNINSTALL.md`: REWRITE_REQUIRED
- `aos/REMOVAL_CHECKLIST.md`: REWRITE_REQUIRED
Required decision: ACCEPT

## 10. Product metadata docs rewrite requirements
[CLASSIFICATION] [MEDIUM] [origin/dev] [aos/ Metadata Docs]
Finding: Metadata files require explicit semantic rules.
Recommendation:
- **SELF_TEST.md**: manual-first checklist unless runnable automation exists; concrete expected results; NOT_RUN ≠ PASS; PASS ≠ approval.
- **MANIFEST.md**: truthful file/folder manifest; required/optional; consumer/dev-only status.
- **VERSION.md**: package version, branch/SHA policy, release status, not approval.
- **COMPATIBILITY.md**: supported target repo assumptions, required tools, optional tools, unsupported cases.
- **CHANGELOG.md**: truth-bearing product changes, no fake release maturity.
- **UNINSTALL.md / REMOVAL_CHECKLIST.md**: manual review first, no destructive default, reversible where possible, human approval required.
Required decision: ACCEPT

## 11. Reports/examples classification
[CLASSIFICATION] [LOW] [origin/dev] [aos/reports/examples/]
Finding: Example files contain internal execution history.
Evidence: 
- observed: Tasks named `AOS-FARM.438` and references to specific checkpoints.
Impact: Misleading to external users.
Recommendation: Move internal dev evidence to `tests/fixtures/`. Rewrite remaining examples into generic `USER_GENERIC_EXAMPLE` inside `aos/examples/` with generic task IDs.
Required decision: ACCEPT

## 12. Schema hardening plan
[CLASSIFICATION] [HIGH] [origin/dev] [aos/schemas/task-quality-check-package.schema.json]
Finding: Safety boolean is left as free variable.
Evidence: 
- observed: `task_quality_pass_is_not_human_result_acceptance` lacks const definition.
Impact: Could be set to false by agent.
Recommendation: Convert invariant boolean fields to `const: true`. Leave state boolean fields as boolean.
Required decision: ACCEPT

## 13. Main/dev protected drift decision map
[CLASSIFICATION] [CRITICAL] [origin/dev] [Root Control Files]
Finding: Protected drift detected.
Evidence: 
- observed: Changes in `00_AOS_Core_Control.md`, `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`, `02_AOS_Governance_Control_Module_and_Safety_Rules.md`.
Impact: Cannot be automatically approved during package cleanup.
Recommendation: Do not approve any protected/canonical drift. Isolate remediation strictly to the `/aos/` directory and root template entrypoints (`llms.txt`, `AGENTS.md`). Exclude root governance files from 469 implementation.
Required decision: REQUIRES_HUMAN_DECISION

## 14. Allowed files for next implementation stage
- `aos/**`
- `llms.txt`
- `AGENTS.md`
- `README.md` (only to fix internal boundary references)

## 15. Forbidden files for next implementation stage
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`
- `constitution.md`
- `.github/**`
- Root `docs/` and `specs/`

## 16. Human checkpoints required
- Approval of split strategy for `aos/prompts/problem-intake.md`.
- Acceptance of `llms.txt` rewrite pointing to `/aos/`.
- Final review of hardened JSON schemas.

## 17. Risks
- Splitting the intake prompt may break internal AOS-FARM dev workflow if the generic prompt loses critical context.
- Moving examples to `tests/fixtures/` might break existing test scripts that hardcode the path.

## 18. Validation plan for next stage
- Dry-run consumer embed by copying `/aos/` to an empty repository.
- Verify `llms.txt` cleanly redirects to `/aos/START_HERE.md`.
- Run JSON schema validations against strict mock data.

## 19. Recommended next stage
AOS-FARM.470 — Product Boundary Stabilization Implementation

## 20. Single next step
AOS PACKAGE CLEAN EMBED STATUS before remediation: FAIL
MERGE TECHNICAL READINESS: NO
MERGE GOVERNANCE DECISION: REQUIRES_HUMAN_DECISION
NEXT STAGE: AOS-FARM.470 — Product Boundary Stabilization Implementation
