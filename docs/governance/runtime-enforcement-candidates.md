# Runtime Enforcement Candidates

## 1. Command Allowlist
- **purpose**: Prevent execution of forbidden or highly destructive commands.
- **blocked_actions**: `rm -rf /`, `curl | bash` without approval.
- **required_inputs**: Executed command string.
- **required_outputs**: Block or Allow (0/1).
- **risk_profile_minimum**: HIGH_RISK_PROTECTED.
- **human_checkpoint_required**: true.
- **implementation_prerequisites**: Clear list of forbidden commands.
- **failure_mode**: Fail-closed (block all unknown).
- **unknown_behavior**: Blocked.
- **forbidden_claims**: "Command passed means approved."

## 2. Write Allowlist
- **purpose**: Restrict agent writing outside task scope.
- **blocked_actions**: Writing to any file not in `authorized_files`.
- **required_inputs**: File path, Checkpoint path.
- **required_outputs**: Block or Allow.
- **risk_profile_minimum**: HIGH_RISK_PROTECTED.
- **human_checkpoint_required**: true.
- **implementation_prerequisites**: Parsing of `authorized_files_if_approved`.
- **failure_mode**: Fail-closed.
- **unknown_behavior**: Blocked.
- **forbidden_claims**: "Can write because it's not protected."

## 3. Protected Path Guard
- **purpose**: Protect `00_AOS_Core_Control.md`, `01_*`, `02_*`.
- **blocked_actions**: Overwriting core control files.
- **required_inputs**: File path.
- **required_outputs**: Block or Allow.
- **risk_profile_minimum**: HIGH_RISK_PROTECTED.
- **human_checkpoint_required**: true.
- **implementation_prerequisites**: List of protected paths.
- **failure_mode**: Fail-closed.
- **unknown_behavior**: Blocked.
- **forbidden_claims**: "Agent updated rules automatically."

## 4. Commit/Push Guard
- **purpose**: Ensure Human Owner explicitly authorized commits/pushes.
- **blocked_actions**: `git commit`, `git push`.
- **required_inputs**: Checkpoint file status.
- **required_outputs**: Block or Allow.
- **risk_profile_minimum**: HIGH_RISK_PROTECTED.
- **human_checkpoint_required**: true.
- **implementation_prerequisites**: Git hooks (pre-commit, pre-push).
- **failure_mode**: Fail-closed.
- **unknown_behavior**: Blocked.
- **forbidden_claims**: "Auto-pushed because tests passed."

## 5. Audit Log
- **purpose**: Record all operations immutably.
- **blocked_actions**: Operations without logging.
- **required_inputs**: Command/File operation details.
- **required_outputs**: Log entry.
- **risk_profile_minimum**: STANDARD_RISK.
- **human_checkpoint_required**: false.
- **implementation_prerequisites**: Central log file.
- **failure_mode**: Fail-closed (if cannot log, abort).
- **unknown_behavior**: Log as UNKNOWN and block.
- **forbidden_claims**: "Log means approved."

## 6. Token Scope Policy
- **purpose**: Restrict LLM agent token permissions (e.g. read-only vs write).
- **blocked_actions**: API calls exceeding token scope.
- **required_inputs**: Token metadata.
- **required_outputs**: Access denied.
- **risk_profile_minimum**: HIGH_RISK_PROTECTED.
- **human_checkpoint_required**: true.
- **implementation_prerequisites**: Cloud/Local API layer config.
- **failure_mode**: Fail-closed.
- **unknown_behavior**: Deny.
- **forbidden_claims**: "Has write token means approved."

## 7. Sandbox Execution
- **purpose**: Isolate agent actions from host system.
- **blocked_actions**: Host system access.
- **required_inputs**: Execution context.
- **required_outputs**: Isolated env.
- **risk_profile_minimum**: HIGH_RISK_PROTECTED.
- **human_checkpoint_required**: true.
- **implementation_prerequisites**: Container or VM runtime.
- **failure_mode**: Fail-closed.
- **unknown_behavior**: Kill sandbox.
- **forbidden_claims**: "Sandbox means safe to auto-approve."
