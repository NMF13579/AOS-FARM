# AOS-FARM Runtime Contracts

This document establishes the canonical contracts for Execution Packages, Sessions, Concurrency, and Recovery within the AOS-FARM architecture.

## 1. Execution Package Authority
- **package_request_creator**: Execution Agent
- **package_request_validator**: Control Plane
- **authoritative_package_issuer**: Control Plane
- **package_signer**: Signing Authority
- **package_revocation_authority**: Control Plane / Human Owner
- **package_activation_authority**: Control Plane
- **package_consumption_authority**: Control Plane / Trusted Runner
- **execution_agent_authority**: Cannot issue authoritative packages or sign packages.

## 2. Execution Package Schema
The authoritative Execution Package defines the exact boundary and policy of a granted session.
Missing required fields, unknown values, or conflicting authorization fields result in a `UNKNOWN_BLOCKED` or `BLOCKED` status. A package must bind uniquely to one repository, baseline, and authorization.

**Fields**:
- `schema_version`, `package_id`, `package_revision`
- `task_id`, `task_version`, `authorization_id`, `authorization_version`, `authorization_witness_digest`
- `repository_id`, `repository_root_identity`, `remote_identity`, `branch`, `baseline_head`, `baseline_state_digest`
- `platform_profile`, `execution_environment_id`, `execution_mode`, `risk_profile`, `lifecycle_state`
- `execution_authorized`, `policy_version`, `policy_digest`, `protected_path_registry_version`, `protected_path_registry_digest`
- `allowed_operations`, `allowed_paths`, `read_only_paths`, `forbidden_paths`, `required_checks`, `optional_checks`
- `shell_policy`, `editor_policy`, `patch_policy`, `filesystem_policy`, `local_git_policy`, `remote_git_policy`, `network_policy`, `dependency_policy`
- `create_authorized`, `update_authorized`, `delete_authorized`, `rename_authorized`, `move_authorized`, `chmod_authorized`, `symlink_authorized`
- `stage_authorized`, `commit_authorized`, `push_authorized`, `merge_authorized`, `tag_authorized`, `release_authorized`
- `issued_at`, `not_before`, `expires_at`, `trusted_time_reference`
- `nonce`, `single_use`, `maximum_sessions`, `resume_allowed`
- `issuer`, `issuer_authority`, `issuer_domain`
- `package_digest_algorithm`, `package_digest`
- `signature_algorithm`, `issuer_key_id`, `package_signature`
- `verification_key_reference`, `revocation_reference`, `capability_state_reference`

## 3. Canonical Serialization
- **format**: JSON
- **encoding**: UTF-8
- **unicode_normalization**: NFC
- **field_ordering**: Alphabetical sorting by key
- **duplicate_key_behavior**: REJECT
- **unknown_field_behavior**: REJECT
- **timestamp_format**: ISO 8601 UTC (e.g., `YYYY-MM-DDTHH:MM:SSZ`)
- **path_format**: Strict forward slash (`/`), no trailing slash, relative to repository root
- **newline_rule**: LF (`\n`) only
- **integer_format**: Base 10, no leading zeros
- **boolean_format**: `true` / `false`
- **null_policy**: Exclude null fields (do not serialize keys with null values)
- **array_ordering**: Preserve original order unless specified as a set
- **set_ordering**: Lexicographically sorted arrays
- **canonical_bytes_definition**: The raw byte sequence of the canonical JSON string.

## 4. Repository and Baseline Binding
- **repository_id**: Unique UUID or URI.
- **remote_identity**: Normalized HTTPS/SSH URL.
- **baseline_head**: Git commit SHA-1.
- **baseline_state_digest**: Hash of the current worktree state (tracked and explicitly allowed untracked files).
If `HEAD` drifts or the baseline digest mismatches, the runner evaluates to `BLOCKED_BASELINE_MISMATCH`.

## 5. Integrity and Authenticity Levels
- **UNBOUND**: No binding. Claim: `NO_INTEGRITY_CLAIM`
- **DIGEST_BOUND**: Contains canonical digest. Detects changes but lacks authenticity.
- **SIGNED_SAME_TRUST_DOMAIN**: Signed, but private key is in the same OS identity as the Agent/Runner. Vulnerable to same-user bypass.
- **SIGNED_SEPARATE_KEY_CUSTODY**: Key is isolated. Strong authenticity.
- **EXTERNALLY_ATTESTED**: Execution verified by an external trust domain.

**Stage Requirements**:
- AOS-FARM.677 and .678 require minimum `DIGEST_BOUND`.
- Target Production requires `SIGNED_SEPARATE_KEY_CUSTODY`.

## 6. Package Issuer Contract
- **execution_domain**: Control Plane (Separate from Agent)
- **callable_by_agent**: Yes (API only)
- **writable_by_agent**: false
- **failure_behavior**: Fail-closed (denies package issuance). Cannot create human approvals or expand scope.

## 7. Signing Authority Direction
- **private_key_location_direction**: Secure Enclave / KMS.
- **private_key_readable_by_agent/runner**: false.
- **signing_request_validation**: Required. Must bind to authorization witness and package digest.

## 8. Key Custody Options
- **REPOSITORY_FILE_KEY**: REJECTED (Agent access risk: CRITICAL).
- **SAME_USER_LOCAL_KEY_STORE**: ACCEPTED FOR MVP (Agent access risk: PRESENT). Max authenticity: `SIGNED_SAME_TRUST_DOMAIN`.
- **SEPARATE_OS_IDENTITY_KEY_STORE**: TARGET FOR LOCAL (Agent access risk: REDUCED).
- **REMOTE_SIGNING_SERVICE**: TARGET FOR PRODUCTION.

## 9. Verification Key Protection
- **registry_authority**: Control Plane
- **writable_by_agent/runner**: false
- **unknown_key_behavior**: UNKNOWN_BLOCKED
- **revoked_key_behavior**: BLOCKED

## 10. Trusted Time
- **agent_controls_clock**: false
- **unknown_time_behavior**: UNKNOWN_BLOCKED
- Clock rollback must be detected and decreases claim trust. Expiration relies on monotonic, external wall-clocks where possible.

## 11. Capability Lifecycle
- **States**: `ISSUED` → `ACTIVATION_PENDING` → `ACTIVATED` → `CONSUMED` (Terminal).
- **Alternative Terminals**: `EXPIRED`, `REVOKED`, `REJECTED`, `COMPROMISED`, `RECOVERY_REQUIRED`.
- Agent cannot reset capability state.

## 12. Nonce and Replay Protection
- **nonce_generator_authority**: Control Plane / Issuer
- **nonce_reuse_behavior**: `REPLAY_ATTEMPT` (Fail-closed)
- Nonce must bind to package digest and authorization ID. Single-use capability requires an atomic state store.

## 13. Session Identity Contract
- `task_id` → `authorization_id` → `package_id` → `authorization_lineage` → `root_session_id` → `session_id` → `operation_id`
- Session Admission requires validation of package schema, digest, baseline, lock availability, and lineage.

## 14. Authorization Lineage and Violations
- **terminal violation**: `EXECUTION_LINEAGE_BLOCKED`. Cannot be cleared by retry. Requires human checkpoint.
- **non-terminal violation**: `HUMAN_REVIEW_REQUIRED` after remediation.
- Violations are permanent records and carry over between sessions in the same lineage.

## 15. Workspace Concurrency
- **mutating_sessions_allowed**: 1
- **repository_lock_required**: true
- Lock binds to session ID and baseline.
- **unexpected external mutation**: `BLOCKED_CONCURRENT_MUTATION`.

## 16. Pre-Mutation Revalidation
Before any privileged mutation, the system must verify:
`session_active`, `package_valid`, `package_not_expired/revoked`, `capability_active`, `workspace_lock_valid`, `baseline_unchanged`.
Unknown check result → `UNKNOWN_BLOCKED`.

## 17. Crash Recovery and Partial Operations
- Crash before activation: Recoverable, start new session.
- Crash during mutation: `RECOVERY_REQUIRED` (Partial state).
- Partial State Detection: Requires before/after state digests.
- Unknown operation outcome blocks the session and requires workspace reconciliation.

## 18. Fail-Closed Defaults
- `unknown_schema`, `unknown_key`, `unknown_time`, `unknown_baseline`, `unknown_operation_outcome` → `UNKNOWN_BLOCKED`.
- `concurrent_mutating_sessions`, `direct_signing_by_agent` → `FORBIDDEN`.
