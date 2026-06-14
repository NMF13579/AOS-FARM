# Architect/Auditor Operating Mode

## 1. Purpose
Systemize Architect/Auditor Mode as repo-level operating policy to ensure self-verification and bounded self-correction occur before any finalization.

## 2. Authority and Source Precedence
- `00_AOS_Core_Control.md`
- `01_AOS_Assembly_Pipelines_and_Build_Roadmap.md`
- `02_AOS_Governance_Control_Module_and_Safety_Rules.md`

## 3. Operating Formula
- Architect logic is mandatory.
- Response/task mode is adaptive.
- Self-verification is mandatory before finalization.
- Bounded self-correction is allowed only inside exact allowed files and exact authorized scope.
- If correction requires scope expansion or approval simulation, fail closed.

## 4. Applicable Task Modes
Execution, remediation, implementation, contract/template creation, and final verification + authorization preparation tasks.

## 5. Mandatory Architect/Auditor Pass
Required before finalizing the task. It checks boundaries, completeness, and adherence to rules.

## 6. Required Self-Verification Checklist
Verification against all boundaries and task specifications.

## 7. Bounded Self-Correction Rules
Correction must remain strictly inside allowed files and scope.

## 8. Fail-Closed Rules
Fail closed if correction requires scope expansion, human simulation, or unauthorized operations (commit, push, staging, etc.).

## 9. Read-Only Verification Exception
Self-verification is mandatory, but self-correction is forbidden. The agent must detect and report only.

## 10. Human Checkpoint Exception
The agent may prepare or update only the explicitly allowed checkpoint file, without simulating human decisions.

## 11. Commit Execution Exception
Correction limited to staged-file verification. Do not amend after creation without explicit authorization.

## 12. Push Execution Exception
Correction limited to closure report consistency. Do not force push, tag push, or override git options unless authorized.

## 13. Protected/Canonical Boundary
Cannot be modified without explicit checkpoint.

## 14. Approval Boundary
Agent cannot simulate human approval.

## 15. Risk Profile Boundary
Agent cannot assign Risk Profile as human.

## 16. UNKNOWN / NOT_RUN Boundary
UNKNOWN is not OK. NOT_RUN is not PASS.

## 17. PASS / Evidence / CI PASS Boundary
PASS != approval. Evidence != approval. CI PASS != approval.

## 18. Forbidden Claims
PASS grants approval, Evidence grants approval, CI PASS grants approval, agent can simulate human approval, agent can assign Risk Profile as human, agent can assign LOW_RISK_FAST, UNKNOWN is OK, NOT_RUN is PASS, skeleton is implementation, task completion is approval.

## 19. Forbidden Operations
Scope expansion, unauthorized staging, commit, push, release, runtime/validator/CI modifications.

## 20. Final Report Requirements
Must reflect verified and corrected state accurately.

## 21. Relationship to Controller Loop
Integrates as the final verification step within the Controller's lifecycle.

## 22. Relationship to Governance / Control Module
Enforces the module's safety boundaries mechanically during tasks.

## 23. Relationship to Future Validator
Will transition from prompt-based to code-based execution blocking once validators are built.

## 24. Examples
If an allowed file has an omission, correct it. If an omission requires a new file, fail closed.

## 25. Final Invariants
- Architect logic is mandatory.
- Response/task mode is adaptive.
- Self-verification is mandatory before finalization.
- Bounded self-correction is allowed only inside exact allowed files and exact authorized scope.
- If correction requires scope expansion or approval simulation, fail closed.
