# AOS-FARM Runtime Trust Architecture

This document defines the canonical runtime trust boundaries, authority separation models, and execution plane restrictions for the AOS-FARM architecture. It relies on the findings from Prompt 1 (`aos/reports/runtime/aos-farm-676-current-control-gap-and-threat-audit.md`) as the factual baseline for existing gaps.

## 1. Authority Separation Model

### 1.1 Policy Authority
- **authoritative_for**: runtime policy, channel policy, path policy, operation policy, platform-profile policy
- **execution_domain**: Control Plane storage / Codebase (`00`, `01`, `02`)
- **writable_by_agent**: false (agent must not modify policy files without explicit authorization)
- **readable_by_agent**: true
- **update_authority**: Human Owner
- **integrity_protection**: Pre-action Write Guard / Protected Path Registry
- **compromise_effect**: Agent could rewrite rules to bypass all restrictions

### 1.2 Authorization Authority
- **authoritative_for**: human authorization witness, authorization scope, authorization expiration, authorization revocation
- **execution_domain**: External/Human interaction channel (e.g., chat/prompt UI)
- **human_identity_binding**: IDE login / Cryptographic signature (future)
- **writable_by_agent**: false (agent narrative is not a witness)
- **update_authority**: Human Owner
- **integrity_protection**: Cryptographic verification or immutable ledger
- **compromise_effect**: Agent can forge approvals, executing protected mutations

### 1.3 Control Plane
- **authoritative_for**: runtime decision, package issuance request, policy evaluation, capability state, session admission, violation continuation decision
- **execution_domain**: SEPARATE_EXECUTION_DOMAIN or at minimum SEPARATE_OS_IDENTITY (target)
- **writable_by_agent**: false
- **writable_by_runner**: false
- **integrity_protection**: OS Sandbox / Container boundary
- **compromise_effect**: Total bypassing of runtime policies and false PASS claims

### 1.4 Package Issuer
- **authoritative_for**: authoritative Execution Package creation, canonical package serialization request, package identifier issuance
- **execution_domain**: Control Plane
- **writable_by_agent**: false (Agent only provides draft/request; Issuer serializes the authoritative package)
- **package_input_validation**: Yes
- **compromise_effect**: Malicious execution package could be signed and executed

### 1.5 Signing Authority
- **authoritative_for**: package signature
- **execution_domain**: Secure Enclave / Key Management System (Directional)
- **private_key_location**: Isolated from Execution Plane
- **private_key_access**: Control Plane (via restricted API)
- **agent_access**: None
- **runner_access**: None
- **package_validation_before_signing**: Yes
- **compromise_effect**: Complete spoofing of authoritative packages

### 1.6 Verification Authority
- **authoritative_for**: technical runtime verification, Evidence reconciliation, claim verification
- **execution_domain**: SEPARATE_EXECUTION_DOMAIN (Independent from Agent)
- **writable_by_agent**: false
- **writable_by_runner**: false
- **authoritative_input**: Runner Ledger (immutable)
- **integrity_protection**: OS/Platform isolation
- **compromise_effect**: Acceptance of forged execution evidence

### 1.7 External Witness
- **authoritative_for**: external checkpoint, ledger witness, optional platform attestation
- **execution_domain**: Remote service / Immutable log
- **current_availability**: None (Gap)
- **agent_access**: None
- **runner_access**: Append-only / Read
- **compromise_effect**: Replay attacks and session truncation become viable

## 2. Trust Concentration

**trust_concentration_id**: TC_LOCAL_BROKER_MVP
- **combined_authorities**: Control Plane, Package Issuer, Verification Authority
- **shared_process**: Optional (Same python process for validation scripts)
- **shared_os_identity**: True (Agent and Validators run as same user)
- **shared_storage**: Workspace
- **shared_keys**: None yet (Keys not implemented)
- **reason**: MVP deployment simplicity, immediate IDE compatibility
- **initial_mvp_benefit**: Rapid iteration without OS-level configuration
- **security_cost**: Agent can directly modify the Control Plane code before it executes
- **compromise_blast_radius**: High (Agent can bypass all local controls)
- **claim_ceiling_effect**: Caps effective claim at POST_ACTION_DETECTION / BLOCKED_BY_REPO_RUNNER
- **required_future_separation_stage**: Move to OS sandbox or container.

## 3. Human Boundary

- **Human ↔ Authorization Authority**: Human provides identity and intent via chat UI. Decision scope, timestamp, and witness must be securely logged. Agent cannot create or modify this witness. Ambiguous auth → DENY.
- **Human ↔ Control Plane**: Control Plane relies on the Authorization Authority for decisions.
- **Human ↔ Architecture Decision Package**: Approval requires human explicitly marking ACCEPT.
- **Human ↔ Commit/Push Boundary**: Separate authorizations. Execution auth does not equal commit auth.

## 4. Control Plane Trust Model

- **role**: Mediates all high-privilege operations and policy evaluations.
- **execution_domain**: Target is SEPARATE_EXECUTION_DOMAIN.
- **process_model**: Separate daemon or isolated container.
- **callable_by_agent**: Yes, via strictly typed API.
- **writable_by_agent**: false.
- **compromise_effect**: Total loss of control.
- **initial_claim**: POLICY_ONLY / POST_ACTION_DETECTION (Due to TC_LOCAL_BROKER_MVP).
- **target_claim**: BLOCKED_BY_OS_OR_SANDBOX / BLOCKED_BY_PLATFORM.

## 5. Execution Plane Restrictions

The Execution Plane is where the Agent operates.
- **agent_location**: User OS / IDE Terminal
- **available_read_channels**: Workspace files, public network
- **available_mutation_channels**: Through Runner only (in ENFORCED_MODE)
- **forbidden_authorities**: The Execution Plane CANNOT expand scope, assign Risk Profile, create human approval, change lifecycle, issue authoritative packages, access signing keys, modify verification keys, or alter violation history.

## 6. Verification Independence

- **verification_level**: SEPARATE_OS_IDENTITY_VERIFICATION (Target)
- **execution_domain**: Target relies on OS or container isolation.
- **agent_can_modify_verifier**: false
- **runner_can_modify_verifier**: false
- **authoritative_input_source**: Immutable Runner Ledger
- **maximum_claim**: BLOCKED_BY_OS_OR_SANDBOX
- **initial_suitability**: Low (Requires complex setup). MVP will use SAME_PROCESS_VERIFICATION (Claim ceiling: POST_ACTION_DETECTION).

## 7. Trusted Runner Models

### 7.1 Same-Process Wrapper
- **isolation**: NONE
- **runner_model_claim_ceiling**: PARTIAL_BLOCKING
- **strong_isolation_claim**: FORBIDDEN

### 7.2 Separate Local Broker Under Same OS User
- **isolation**: PROCESS_BOUNDARY
- **os_user_separation**: false
- **runner_model_claim_ceiling**: BLOCKED_BY_REPO_RUNNER
- **strong_isolation_claim**: FORBIDDEN

### 7.3 Separate OS Identity Broker / Sandbox / Container
- **isolation**: OS_IDENTITY_BOUNDARY / PLATFORM_BOUNDARY
- **runner_model_claim_ceiling**: BLOCKED_BY_OS_OR_SANDBOX / BLOCKED_BY_PLATFORM

## 8. Runtime Mode Architecture

### 8.1 OBSERVE_MODE
- **direct_shell_may_exist**: true
- **direct_editor_write_may_exist**: true
- **direct_patch_may_exist**: true
- **direct_filesystem_mutation_may_exist**: true
- **direct_local_git_may_exist**: true
- **runner_observes_known_operations_only**: true
- **reconciliation_required**: true
- **physical_prevention_claim**: FORBIDDEN
- **maximum_claim**: ADVISORY_VALIDATOR / POST_ACTION_DETECTION

### 8.2 ENFORCED_MODE
- **direct_mutable_shell_available**: false
- **direct_editor_write_available**: false
- **direct_patch_api_available**: false
- **direct_filesystem_mutation_api_available**: false
- **direct_unauthorized_local_git_available**: false
- **all_mutations_runner_mediated**: true
- **typed_operations_required**: true
- **workspace_lock_required**: true
- **unknown_channel_behavior**: UNKNOWN_BLOCKED
- **bypass_indication_behavior**: BLOCKED
- **maximum_claim**: BLOCKED_BY_REPO_RUNNER / BLOCKED_BY_OS_OR_SANDBOX / BLOCKED_BY_PLATFORM

## 9. Channel Control Architecture
- **Command Channel**: IDE native `run_command`. Must be mediated by a Command Guard for ENFORCED_MODE.
- **Editor/Patch/Filesystem API Channel**: IDE native tools. Must be replaced by API calls to the Runner for ENFORCED_MODE.
- **Git Channel**: Must be intercepted by local hooks or isolated keys.
