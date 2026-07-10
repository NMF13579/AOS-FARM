# AOS-FARM Runtime Enforcement Contracts

This document establishes the architecture for Operation Guards, Runner Lifecycle, Ledger, Verification, and Bypass-Resistance.

## 1. Typed Operation Model
Operations are separated into discrete, typed requests to eliminate arbitrary capabilities.
**Minimal Operations**: `READ_FILE`, `LIST_DIRECTORY`, `SEARCH_TEXT`, `INSPECT_STATUS`, `INSPECT_DIFF`, `WRITE_FILE`, `CREATE_FILE`, `DELETE_FILE`, `RENAME_FILE`, `MOVE_FILE`, `CHANGE_MODE`, `CREATE_SYMLINK`, `RUN_SCOPED_TEST`, `RUN_REQUIRED_CHECK`, `RUN_UNIFIED_VALIDATOR`, `STAGE_SCOPED_FILES`, `CREATE_COMMIT`, `PUSH_AUTHORIZED_REF`.

### 1.1 Operation Classes
- READ_ONLY_OPERATION, WORKTREE_MUTATION, TEST_EXECUTION, VALIDATION_EXECUTION, LOCAL_GIT_MUTATION, REMOTE_GIT_MUTATION, NETWORK_OPERATION, DEPENDENCY_OPERATION, PLATFORM_OPERATION.
- *Rule*: Read permission does not imply write. Write does not imply delete. Dependency installation is a strictly privileged operation.

## 2. Operation Request and Authorization
An operation request binds to a session ID, package ID, and authorization ID. 
- Arbitrary bash commands are not typed operations.
- The control module verifies `session_active`, `package_valid`, `target_within_repository`, and `policy_unchanged` before generating an `ALLOW` or `DENY` decision.

## 3. Trusted Runner Lifecycle
- **States**: `RUNNER_UNINITIALIZED` → `RUNNER_STARTING` → `RUNNER_INTEGRITY_CHECK` → `RUNNER_READY` → `RUNNER_SESSION_BOUND` → `RUNNER_EXECUTING`.
- **Integrity Check**: Verifies executable identity, configuration digest, and verification-key digest.
- **Session Binding**: Binds strictly to a package digest, authorization ID, baseline, and workspace lock. Any mismatch results in `BLOCKED_SESSION_BINDING_MISMATCH`.

## 4. Command Guard
Controls process-tree execution, tracking executable identity and limits.
- **Executable Identity**: Must be resolved natively. Relying strictly on `$PATH` without trusted resolution lowers claims.
- **Raw Shell Policy**: Direct mutable shell in `ENFORCED_MODE` is `FORBIDDEN`. Pipes and redirects are categorized as potential write side-effects.
- **Environment**: Fixed/allowed variables only. Hidden credential forwarding is forbidden.
- **Structured Results**: Exit code 0 is insufficient. Valid structured output is required.

## 5. Write Guard
Regulates file system mutations through Path Resolution and Target Classification.
- **Path Resolution**: Absolute paths forbidden by default. Path traversal and symlink escapes are blocked. Case normalization depends on the platform.
- **Mutation Separation**: CREATE, UPDATE, DELETE, RENAME, MOVE, CHMOD, SYMLINK are isolated privileges.
- **Delete Policy**: Forbidden by default. Requires explicit target dependency impact review.

## 6. Protected Path Contract
Paths are classified into: CANONICAL, PROTECTED, APPROVAL_CONTROLLED, LIFECYCLE_CONTROLLED, EVIDENCE_CONTROLLED, RUNTIME_CONTROLLED, KEY_CONTROLLED, GENERATED, TEMPORARY, ORDINARY, UNKNOWN.
- `UNKNOWN` is never `ORDINARY`.
- `PROTECTED_REGISTRY_MISMATCH` blocks the session immediately.

## 7. Test Integrity
Changes to tests must be authorized. Reducing assertions, deleting negative fixtures, or changing test discovery limits the trust level of test execution Evidence.

## 8. Git Boundary Control
- **Local Git Control**: Arbitrary hooks, history rewrites, or `git reset --hard` are blocked. Commits require exact scoped staging and separate authorization.
- **Remote Git Boundary**: `PUSH_AUTHORIZED_REF` requires explicit remote and ref binding. Force pushing is forbidden.

## 9. Runner Ledger
- **Ledger Events**: Local append-only log tracking all runner decisions, intent, execution results, and capabilities.
- **Hash Chain**: Detects mutation, reordering, and truncation (when coupled with a checkpoint). It does not prevent wholesale replacement by the execution agent if the ledger is in the same trust domain.
- **Storage**: Must not reside strictly in `/.aos-tmp/`.

## 10. Verifier Contract
Evaluates the task dimensions (Session Binding, Package Authenticity, Scope Conformance, Runner Integrity).
- **Agent Claim Verification**: Matches agent-supplied assertions against trusted ledger outputs. Claims that contradict the ledger result in `CLAIM_CONTRADICTED`.
- **Verification Output**: PASS, FAIL, BLOCKED, HUMAN_REVIEW_REQUIRED, UNKNOWN_BLOCKED, NOT_RUN.

## 11. Violation Model
- **Terminal Violations**: POLICY_TAMPERING, RUNNER_TAMPERING, KEY_TAMPERING, PACKAGE_TAMPERING, PROTECTED_PATH_VIOLATION, REPLAY_ATTEMPT, BYPASS_ATTEMPT.
- Terminal violations permanently halt the session (`EXECUTION_LINEAGE_BLOCKED`) and require a human checkpoint to unblock. Ordinary retries cannot bypass a terminal violation.

## 12. Bypass-Resistance Specification
The implementation must pass future fixtures validating:
1. Write outside allowed paths.
2. Traversal and symlink escapes.
3. Raw shell redirect writes.
4. Old package and session replays.
5. Ledger deletion/truncation.
6. Execution outside strict baseline limits.
