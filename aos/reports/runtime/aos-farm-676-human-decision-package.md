# AOS-FARM.676 Human Decision Package

This package consolidates all explicitly required human decisions from the Runtime Trust Architecture phase (AOS-FARM.676). Without a designated Human Owner reviewing and establishing authority, these decisions remain `PENDING HUMAN INPUT` and fail-closed defaults will block progressive implementation.

## Category 1: Blockers for AOS-FARM.677
The following decisions must be resolved before the foundation implementation (AOS-FARM.677) can be authorized.

- **decision_id**: DEC_RISK_PROFILE
  - **question**: Will the architecture implementation be assigned the `HIGH_RISK_PROTECTED` Risk Profile?
  - **recommended_option**: Yes.
  - **human_decision_status**: PENDING HUMAN INPUT

- **decision_id**: DEC_AOS_FARM_677_SCOPE
  - **question**: Is the proposed DIGEST_BOUND schema scope for AOS-FARM.677 accepted?
  - **recommended_option**: Yes, restricting early claims to `POLICY_ONLY`.
  - **human_decision_status**: PENDING HUMAN INPUT

- **decision_id**: DEC_INITIAL_ENV
  - **question**: Which environment serves as the MVP execution environment?
  - **recommended_option**: Local IDE (macOS/Linux) in OBSERVE_MODE.
  - **human_decision_status**: PENDING HUMAN INPUT

- **decision_id**: DEC_PKG_INTEGRITY_677
  - **question**: Will `DIGEST_BOUND` be the required minimum integrity for AOS-FARM.677?
  - **recommended_option**: Yes.
  - **human_decision_status**: PENDING HUMAN INPUT

## Category 2: Defarrable Decisions (Post-677)
The following decisions can be deferred to stages AOS-FARM.678 through AOS-FARM.682 without blocking the basic foundation setup.

- **decision_id**: DEC_MACOS_TARGET_ISOLATION
  - **deferrable_until**: AOS-FARM.682
  - **question**: Target isolation for macOS: native separate OS users or VM/Container (Docker/OrbStack)?
  - **temporary_default**: LOCAL_BROKER_PROCESS (OBSERVE_MODE)
  - **human_decision_status**: PENDING HUMAN INPUT

- **decision_id**: DEC_RAW_SHELL_POLICY
  - **deferrable_until**: AOS-FARM.680
  - **question**: Final policy for raw shell utilization?
  - **temporary_default**: FORBIDDEN in ENFORCED_MODE.
  - **human_decision_status**: PENDING HUMAN INPUT

- **decision_id**: DEC_PKG_AUTH_WRITE
  - **deferrable_until**: AOS-FARM.682
  - **question**: What is the package authenticity minimum for write enforcement in target production?
  - **temporary_default**: SIGNED_SEPARATE_KEY_CUSTODY.
  - **human_decision_status**: PENDING HUMAN INPUT

- **decision_id**: DEC_TARGET_SIGNING_AUTHORITY
  - **deferrable_until**: AOS-FARM.682
  - **question**: What is the target signing authority domain?
  - **temporary_default**: REMOTE_SIGNING_SERVICE
  - **human_decision_status**: PENDING HUMAN INPUT

- **decision_id**: DEC_COMMIT_PUSH_GATE
  - **deferrable_until**: AOS-FARM.681
  - **question**: What is the minimum authorization gate for local commits and remote pushes?
  - **temporary_default**: Commit verified by operation contract; Push requires distinct authorization.
  - **human_decision_status**: PENDING HUMAN INPUT

*(Note: The agent is forbidden from signing or authorizing these decisions itself. They remain pending.)*
