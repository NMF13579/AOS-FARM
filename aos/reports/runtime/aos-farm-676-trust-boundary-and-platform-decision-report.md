# AOS-FARM.676 Prompt 2 — Trust Boundary and Platform Decision Report

## 1. Execution Record
This report summarizes the architectural recommendations and human decisions generated during Prompt 2 of the `AOS-FARM.676` task. The baseline and gaps identified in Prompt 1 (`aos/reports/runtime/aos-farm-676-current-control-gap-and-threat-audit.md`) were utilized as factual input. No implementations, sandbox configurations, or modifications to protected canonical rules were performed.

## 2. Recommendations

### Initial Architecture Recommendation
- **initial_execution_mode**: OBSERVE_MODE
- **macos_initial_runner_model**: LOCAL_BROKER_PROCESS
- **linux_initial_runner_model**: LOCAL_BROKER_PROCESS
- **editor_write_detection_fallback**:
  - **mechanism**: FILE_WATCHER_AND_RECONCILIATION
  - **claim**: POST_ACTION_DETECTION
  - **physical_prevention_claim**: FORBIDDEN
- **first_enforced_mode_requirement**: At least one explicitly supported environment must technically disable direct mutable shell, editor write, patch API, filesystem mutation API, and unauthorized local Git mutation so that all mutations pass through the trusted runner.

**Analysis**:
The proposal to start with a `LOCAL_BROKER_PROCESS` in `OBSERVE_MODE` is highly suitable for an initial MVP. It minimizes operational complexity and maintains high developer/IDE usability without requiring complex virtualization setup immediately.
- **Remaining Threats**: The Agent retains direct shell and editor access (same-user bypass). The Agent could subvert the Control Plane or bypass the broker entirely.
- **Uncontrolled Channels**: Shell, Editor API, Filesystem API, Local Git.
- **Allowed Claims**: Maximum claim is `POST_ACTION_DETECTION`. Claims of strong isolation or physical prevention are strictly forbidden.
- **First ENFORCED_MODE Environment**: Linux (via rootless container or user namespaces) is recommended to be the first environment to achieve `ENFORCED_MODE` due to native namespace support being easier to secure than macOS native constraints.
- **Human Decisions Required**: The acceptance of the residual same-user bypass risk for the MVP phase requires human approval.

### Target Architecture Recommendation
- **platform**: Linux (Primary Enforced Target) / macOS (via Virtualization)
- **recommended_target_execution_mode**: ENFORCED_MODE
- **recommended_target_runner_model**: SEPARATE_EXECUTION_DOMAIN
- **recommended_target_isolation_level**: PLATFORM_BOUNDARY
- **recommended_agent_identity**: Unprivileged IDE user / Inner Container
- **recommended_runner_identity**: Outer Container / Remote Control Plane
- **recommended_control_plane_domain**: SEPARATE_EXECUTION_DOMAIN
- **recommended_policy_authority_domain**: Read-only mount enforced by the platform
- **recommended_signing_authority_direction**: Remote Secure Enclave or isolated KMS
- **recommended_verifier_domain**: SEPARATE_EXECUTION_DOMAIN
- **recommended_claim_ceiling**: BLOCKED_BY_PLATFORM

## 3. Human Decision Inventory

The following decisions are strictly required by a Human Owner. The Agent CANNOT authorize these.

- **decision_id**: DEC_RISK_PROFILE
  - **question**: Will the architecture implementation be assigned the `HIGH_RISK_PROTECTED` Risk Profile?
  - **recommended_option**: Yes.
  - **human_decision_status**: DEFERRED_WITH_BLOCKING_EFFECT
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_INITIAL_ENV
  - **question**: Which environment will serve as the initial supported execution environment?
  - **recommended_option**: Local IDE (macOS/Linux) in OBSERVE_MODE.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_FIRST_ENFORCED_ENV
  - **question**: Which environment will be the first to transition to ENFORCED_MODE?
  - **recommended_option**: Linux via Rootless Container.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_RESIDUAL_RISK_MVP
  - **question**: Does the organization accept the same-user bypass residual risk for the LOCAL_BROKER_PROCESS MVP?
  - **recommended_option**: Accept temporarily, capped at POST_ACTION_DETECTION claim.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_MACOS_TARGET_ISOLATION
  - **question**: Should macOS target isolation rely on native separate OS users or a VM-based container (e.g. Docker/OrbStack)?
  - **recommended_option**: VM-based container for standard developer experience.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_SHELL_POLICY
  - **question**: Should the direct shell be FORBIDDEN, READ_ONLY, or AVAILABLE_OBSERVE_MODE_ONLY during MVP?
  - **recommended_option**: AVAILABLE_OBSERVE_MODE_ONLY.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

## 4. Validation Results

- Prompt 1 artifact was located and read successfully.
- Baseline remains identical and is not materially stale.
- Required sources (00, 01, 02) were evaluated and source precedence maintained.
- Authority separations have been mapped and defined.
- Trust Concentration (TC_LOCAL_BROKER_MVP) explicitly documented.
- No protected/canonical files or validators were changed.
- No execution sandbox or implementation logic was executed.
- No commit or push was performed.

## 5. Changed-File Inventory

- `[NEW] aos/docs/runtime/runtime-trust-architecture.md`
- `[NEW] aos/docs/runtime/platform-control-profiles.md`
- `[NEW] aos/reports/runtime/aos-farm-676-trust-boundary-and-platform-decision-report.md`

## 6. Prompt 3 Input Package

The artifacts generated in this stage serve as the architectural contract for Prompt 3:
1. `runtime-trust-architecture.md` defines the boundaries and limitations.
2. `platform-control-profiles.md` defines the macOS/Linux realities.
3. The `Human Decision Inventory` must be resolved by the human owner.

**Execution of Prompt 3 is strictly DEFERRED pending human review of these outputs.**
