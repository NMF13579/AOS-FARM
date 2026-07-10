# AOS-FARM Runtime Enforcement Roadmap

This document defines the implementation roadmap, dependencies, and claim progression for the AOS-FARM Runtime Trust Architecture (AOS-FARM.677 through AOS-FARM.683).

## Stage 1: AOS-FARM.677
**Goal**: Execution Package Integrity, Capability Lifecycle, and Session Binding Foundation
**Implementation Scope**:
- Package Schema definitions.
- Canonical serialization and digest bindings.
- Nonce and single-use validation constraints.
- Session Binding interfaces without physical enforcement.
**Maximum Allowed Claim**: `DIGEST_BOUND`, `POLICY_ONLY`
**Explicit Non-Goals**: No Write Guard, no Command Guard, no remote signing, no sandboxes.

## Stage 2: AOS-FARM.678
**Goal**: Trusted Read-Only Verification MVP
**Implementation Scope**:
- Basic Verifier interface implementation.
- Local tamper-evident ledger logic foundation.
- Verification dimensions (Session Binding, Package Authenticity).
**Maximum Allowed Claim**: `POST_ACTION_DETECTION`, `LOCAL_TAMPER_EVIDENT`

## Stage 3: AOS-FARM.679
**Goal**: Trusted Runner and Scoped Write Enforcement
**Implementation Scope**:
- Write Guard module.
- Path Resolution mechanisms.
- Runner Lifecycle initialization.
**Goal Constraint**: Must achieve `ENFORCED_MODE` in at least one explicitly supported environment (e.g., Linux User Namespaces) or block cleanly.
**Maximum Allowed Claim**: `BLOCKED_BY_REPO_RUNNER`

## Stage 4: AOS-FARM.680
**Goal**: Command, Process, Network, and Dependency Enforcement
**Implementation Scope**:
- Command Guard integration.
- Process tree and raw shell constraints.
- Network and Dependency policy module.

## Stage 5: AOS-FARM.681
**Goal**: Local and Remote Git Boundary Enforcement
**Implementation Scope**:
- Local staging and commit boundaries.
- Remote push authorization and ref binding.

## Stage 6: AOS-FARM.682
**Goal**: Platform Isolation, Authority Separation, Key Custody, and External Witness Decision
**Implementation Scope**:
- Finalizing strong separate key custody (e.g., Remote KMS/Hardware-backed key).
- Platform boundary hardening (macOS VMs, Linux Rootless Containers).
- External Witness selection and integration.
**Maximum Allowed Claim**: `SIGNED_SEPARATE_KEY_CUSTODY`, `EXTERNALLY_WITNESSED`

## Stage 7: AOS-FARM.683
**Goal**: End-to-End Bypass Resistance Dogfood
**Implementation Scope**:
- Execution of bypass fixtures specified in AOS-FARM.676.
- Demonstration of bypass resilience.
**Maximum Allowed Claim**: `PRODUCTION_READY` (Only after successful bypass tests).
