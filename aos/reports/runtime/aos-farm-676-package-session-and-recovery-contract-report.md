# AOS-FARM.676 Prompt 3 — Package, Session, and Recovery Contract Report

## 1. Execution Record
This report summarizes the architectural recommendations and human decisions generated during Prompt 3 of the `AOS-FARM.676` task. The baseline and architectures defined in Prompt 1 and Prompt 2 were strictly utilized as factual inputs. No implementations, key generation, test changes, or lifecycle mutations were performed.

## 2. Recommendations

### Integrity and Authenticity Strategy
- **AOS-FARM.677 Target**: `DIGEST_BOUND`.
- **Target Production Profile**: `SIGNED_SEPARATE_KEY_CUSTODY`.
- **Key Custody**: `SAME_USER_LOCAL_KEY_STORE` is proposed for MVP only (caps authenticity at `SIGNED_SAME_TRUST_DOMAIN`). `SEPARATE_OS_IDENTITY_KEY_STORE` or `REMOTE_SIGNING_SERVICE` is recommended for target production.

### Session and Lineage Strategy
- **Concurrency**: `mutating_sessions_allowed: 1`. Strict workspace locking is required.
- **Violation Carry-over**: Violations are permanently recorded in the authorization lineage. Terminal violations block lineage execution and require explicit human checkpoint resolution.
- **Crash Recovery**: Unknown operation outcomes block the session and require physical workspace reconciliation. Automatic recovery is disabled for unknown states.

## 3. Human Decision Inventory

The following decisions are strictly required by a Human Owner. The Agent CANNOT authorize these. 

- **decision_id**: DEC_PKG_INTEGRITY_677
  - **question**: Will `DIGEST_BOUND` be the required package integrity minimum for AOS-FARM.677?
  - **recommended_option**: Yes.
  - **human_decision_status**: RECOMMENDATION_PROPOSED (DEFERRED_WITH_BLOCKING_EFFECT if implementation begins)
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_PKG_AUTH_WRITE
  - **question**: What is the package authenticity minimum for write enforcement in target production?
  - **recommended_option**: SIGNED_SEPARATE_KEY_CUSTODY.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_TARGET_SIGNING_AUTHORITY
  - **question**: What is the target signing authority domain?
  - **recommended_option**: REMOTE_SIGNING_SERVICE or Hardware-backed Key.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_TRUSTED_TIME
  - **question**: Will an external trusted time requirement be strictly enforced for capability expiration?
  - **recommended_option**: Yes (Wall-clock monotonic enforcement).
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_CONCURRENCY_POLICY
  - **question**: What is the policy for unexpected external human mutation during a session?
  - **recommended_option**: Immediate session block (`BLOCKED_CONCURRENT_MUTATION`).
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

- **decision_id**: DEC_CRASH_RECOVERY
  - **question**: What is the threshold for human review following a crash during mutation?
  - **recommended_option**: Required for any `UNKNOWN_OPERATION_OUTCOME`.
  - **human_decision_status**: RECOMMENDATION_PROPOSED
  - **human_decision**: [PENDING HUMAN INPUT]
  - **human_witness**: [PENDING]

*(Note: Without an explicit human witness, these remain `PENDING HUMAN INPUT` and fail-closed defaults apply.)*

## 4. Validation Results

- **Prompt 1 and Prompt 2 Inputs**: Located, read, and applied.
- **Baseline Integrity**: Retained and not materially stale. Source precedence strictly maintained.
- **Architectural Constraints**: `DIGEST_BOUND` and `SIGNED_SAME_TRUST_DOMAIN` were not falsely claimed as `SIGNED_SEPARATE_KEY_CUSTODY`.
- **Fail-closed Logic**: Unknown states, unexpected schemas, and concurrency issues consistently resolve to `UNKNOWN_BLOCKED` or `FORBIDDEN`.
- **Security Posture**: Agent execution has no authority to issue its own authoritative execution packages.
- **Implementation Constraint**: Keys were not generated. Protected files were not modified. `git commit` and `git push` were explicitly avoided.

## 5. Changed-File Inventory

- `[NEW] aos/docs/runtime/runtime-contracts.md`
- `[NEW] aos/reports/runtime/aos-farm-676-package-session-and-recovery-contract-report.md`

## 6. Prompt 4 Input Package

The contracts designed in this step define the schema and state transition rules. Prompt 4 will consume these contracts to design the Runner Lifecycle, Verifier, Local Ledger, and Operation Guard definitions.

**Execution of Prompt 4 is strictly DEFERRED pending human review.**
