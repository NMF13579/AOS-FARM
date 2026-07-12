import argparse
import json
import sys
import unicodedata
from pathlib import Path


DEFAULT_ARCHITECTURE = Path("aos/docs/workflow/simple-control-surface.md")
DEFAULT_COMMANDS = Path("aos/config/simple-control-command-registry.yaml")
DEFAULT_LOCALES = Path("aos/config/simple-control-locale-registry.yaml")
DEFAULT_STATE_SCHEMA = Path("aos/schemas/simple-control-state.schema.json")
DEFAULT_WITNESS_SCHEMA = Path("aos/schemas/human-decision-witness.schema.json")

COMMAND_IDS = {
    "HELP",
    "LANGUAGE",
    "ANALYZE",
    "PLAN",
    "ACCEPT_SCOPE",
    "REVISE_SCOPE",
    "SELECT_RISK",
    "EXECUTE",
    "VALIDATE",
    "STATUS",
    "NEXT",
    "SHOW_DETAILS",
    "COMMIT",
    "PUSH",
    "INTEGRATE",
    "STOP",
    "PREPARE_CLOSURE",
}

OPERATION_CLASSES = {
    "PURE_READ",
    "TEMPORARY_LOCAL_ANALYSIS",
    "LOCAL_METADATA_WRITE",
    "TRACKED_WORKTREE_WRITE",
    "GIT_INDEX_WRITE",
    "GIT_OBJECT_WRITE",
    "REMOTE_WRITE",
    "INTEGRATION_WRITE",
    "CLOSURE_PREPARATION",
    "DECISION_RECORD_PREPARATION",
}

WRITE_RELATED_CLASSES = {
    "LOCAL_METADATA_WRITE",
    "TRACKED_WORKTREE_WRITE",
    "GIT_INDEX_WRITE",
    "GIT_OBJECT_WRITE",
    "REMOTE_WRITE",
    "INTEGRATION_WRITE",
    "CLOSURE_PREPARATION",
}

EFFECT_KEYS = {
    "tracked_worktree_write",
    "untracked_worktree_write",
    "canonical_artifact_write",
    "git_index_write",
    "git_object_write",
    "local_git_ref_write",
    "remote_ref_write",
    "external_system_write",
    "temp_write",
}

REQUIRED_COMMAND_FIELDS = {
    "command_id",
    "contract_version",
    "operation_class",
    "allowed_control_states",
    "required_roles",
    "required_Risk_Profile_status",
    "required_human_decisions",
    "preconditions",
    "grants",
    "non_grants",
    "effects",
    "success_control_state",
    "failure_control_state",
    "partial_failure_operation_state",
    "idempotency_required",
    "reconciliation_required",
    "available_in_contract_only_release",
    "availability",
    "implementation_status",
}

AUTHORIZATION_FLAGS = {
    "scope_confirmed_by_human",
    "Risk_Profile_assigned_by_human",
    "execution_authorized",
    "commit_authorized",
    "push_authorized",
    "integration_authorized",
    "release_authorized",
    "lifecycle_mutation_authorized",
}

DECISION_TYPES = {"scope", "risk", "execution", "EXECUTION_AUTHORIZATION", "PRODUCTION_EXECUTION_AUTHORIZATION", "COMMIT_AUTHORIZATION", "PUSH_AUTHORIZATION", "commit", "push", "integration", "lifecycle", "release"}
CLAIM_CEILING_FLAGS = {
    "approval_granted": False,
    "execution_authorized": False,
    "commit_authorized": False,
    "push_authorized": False,
    "integration_authorized": False,
    "platform_enforced": False,
    "runtime_implemented": False,
}

READ_ONLY_IMPLEMENTED_COMMANDS = {"HELP", "LANGUAGE"}
PLANNING_IMPLEMENTED_COMMANDS = {"ANALYZE", "PLAN", "REVISE_SCOPE"}
DECISION_PREPARATION_COMMANDS = {"ACCEPT_SCOPE", "SELECT_RISK"}
VALIDATION_IMPLEMENTED_COMMANDS = {"VALIDATE"}
DERIVED_READ_ONLY_COMMANDS = {"STATUS", "NEXT", "SHOW_DETAILS"}
EXECUTION_PREVIEW_COMMANDS = {"EXECUTE"}


def read_text(path, failures):
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as exc:
        failures.append(f"could not read {path}: {exc}")
        return None


def read_json_contract(path, failures):
    text = read_text(path, failures)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        failures.append(f"could not parse {path}: {exc}")
        return None


def add_check(checks, name, status, message):
    checks.append({"name": name, "status": status, "message": message})


def normalize_alias(alias):
    return unicodedata.normalize("NFC", alias).casefold()


def char_script(ch):
    if not ch.isalpha():
        return None
    name = unicodedata.name(ch, "")
    if name.startswith("LATIN "):
        return "LATIN"
    if name.startswith("CYRILLIC "):
        return "CYRILLIC"
    if name.startswith("GREEK "):
        return "GREEK"
    if name.startswith("HEBREW "):
        return "HEBREW"
    if name.startswith("ARABIC "):
        return "ARABIC"
    return "OTHER"


def has_mixed_script(alias):
    scripts = {script for ch in alias for script in [char_script(ch)] if script}
    return len(scripts) > 1


def has_invisible_or_control(alias):
    for ch in alias:
        code = ord(ch)
        category = unicodedata.category(ch)
        if category in {"Cc", "Cf", "Zl", "Zp"}:
            return True
        if 0xFE00 <= code <= 0xFE0F:
            return True
        if 0x200B <= code <= 0x200F:
            return True
        if 0x202A <= code <= 0x202E:
            return True
    return False


def check_architecture(path, failures, checks):
    text = read_text(path, failures)
    if text is None:
        return
    required = [
        "The Simple Control Surface is a user-facing adapter",
        "PASS is not approval",
        "Evidence is not approval",
        "CI PASS is not approval",
        "UNKNOWN is not OK",
        "NOT_RUN is not PASS",
        "Simple Control Surface | UI adapter | none",
        "## Input Processing Order",
        "## Documentation Route",
        "## Source Of Truth",
        "## Human Decision Model",
        "## Unicode Security",
        "## Execution Package Template Conflict",
        "must not report `APPROVED`, `EXECUTION_AUTHORIZED`, `COMMIT_AUTHORIZED`, `PUSH_AUTHORIZED`, or `INTEGRATION_AUTHORIZED`",
    ]
    for phrase in required:
        if phrase not in text:
            failures.append(f"architecture contract missing required phrase: {phrase}")
    if "Simple Control Surface | UI adapter | approval authority" in text:
        failures.append("Simple Control Surface must not be authority")
    add_check(checks, "Architecture Contract", "PASS" if not failures else "CHECKED", "architecture contract inspected")


def command_by_id(commands):
    return {cmd.get("command_id"): cmd for cmd in commands if isinstance(cmd, dict)}


def check_command_registry(data, failures, checks):
    if not isinstance(data, dict):
        failures.append("command registry must be an object")
        return {}
    commands = data.get("commands")
    if not isinstance(commands, list):
        failures.append("command registry commands must be a list")
        return {}

    seen = set()
    for cmd in commands:
        command_id = cmd.get("command_id") if isinstance(cmd, dict) else None
        if command_id in seen:
            failures.append(f"duplicate command_id: {command_id}")
        seen.add(command_id)
        if not isinstance(cmd, dict):
            failures.append("command entry must be object")
            continue
        for field in REQUIRED_COMMAND_FIELDS:
            if field not in cmd:
                failures.append(f"{command_id}: missing required field {field}")
        if cmd.get("contract_version") != 1 and "contract_version" in cmd:
            failures.append(f"{command_id}: contract_version must be 1")
        if cmd.get("operation_class") not in OPERATION_CLASSES:
            failures.append(f"{command_id}: invalid operation_class")
        implementation_status = cmd.get("implementation_status")
        if command_id in READ_ONLY_IMPLEMENTED_COMMANDS:
            if implementation_status not in {"NOT_IMPLEMENTED", "IMPLEMENTED_READ_ONLY"}:
                failures.append(f"{command_id}: implementation_status must be NOT_IMPLEMENTED or IMPLEMENTED_READ_ONLY")
            if implementation_status == "IMPLEMENTED_READ_ONLY":
                if cmd.get("operation_class") != "PURE_READ":
                    failures.append(f"{command_id}: IMPLEMENTED_READ_ONLY requires PURE_READ operation_class")
                if any(cmd.get("effects", {}).values()):
                    failures.append(f"{command_id}: IMPLEMENTED_READ_ONLY requires no write effects")
        elif implementation_status != "NOT_IMPLEMENTED":
            if command_id in PLANNING_IMPLEMENTED_COMMANDS and implementation_status == "IMPLEMENTED_PLANNING_ONLY":
                if cmd.get("operation_class") != "TEMPORARY_LOCAL_ANALYSIS":
                    failures.append(f"{command_id}: IMPLEMENTED_PLANNING_ONLY requires TEMPORARY_LOCAL_ANALYSIS")
                if any(cmd.get("effects", {}).values()):
                    failures.append(f"{command_id}: IMPLEMENTED_PLANNING_ONLY requires no write effects")
            elif command_id in DECISION_PREPARATION_COMMANDS and implementation_status == "IMPLEMENTED_DECISION_PREPARATION_ONLY":
                if cmd.get("operation_class") != "DECISION_RECORD_PREPARATION":
                    failures.append(f"{command_id}: IMPLEMENTED_DECISION_PREPARATION_ONLY requires DECISION_RECORD_PREPARATION")
                if any(cmd.get("effects", {}).values()):
                    failures.append(f"{command_id}: IMPLEMENTED_DECISION_PREPARATION_ONLY requires no write effects")
            elif command_id in VALIDATION_IMPLEMENTED_COMMANDS and implementation_status == "IMPLEMENTED_READ_ONLY_VALIDATION":
                if cmd.get("operation_class") != "TEMPORARY_LOCAL_ANALYSIS":
                    failures.append(f"{command_id}: IMPLEMENTED_READ_ONLY_VALIDATION requires TEMPORARY_LOCAL_ANALYSIS")
                if any(cmd.get("effects", {}).values()):
                    failures.append(f"{command_id}: IMPLEMENTED_READ_ONLY_VALIDATION requires no write effects")
            elif command_id in DERIVED_READ_ONLY_COMMANDS and implementation_status == "IMPLEMENTED_DERIVED_READ_ONLY":
                if cmd.get("operation_class") != "PURE_READ":
                    failures.append(f"{command_id}: IMPLEMENTED_DERIVED_READ_ONLY requires PURE_READ")
                if any(cmd.get("effects", {}).values()):
                    failures.append(f"{command_id}: IMPLEMENTED_DERIVED_READ_ONLY requires no write effects")
            elif command_id in EXECUTION_PREVIEW_COMMANDS and implementation_status == "IMPLEMENTED_ORCHESTRATION_PREVIEW_ONLY":
                if cmd.get("operation_class") != "DECISION_RECORD_PREPARATION":
                    failures.append(f"{command_id}: IMPLEMENTED_ORCHESTRATION_PREVIEW_ONLY requires DECISION_RECORD_PREPARATION")
                if "execution_authorization" not in cmd.get("required_human_decisions", []):
                    failures.append(f"write-related command {command_id} requires human decision")
                if any(cmd.get("effects", {}).values()):
                    failures.append(f"{command_id}: IMPLEMENTED_ORCHESTRATION_PREVIEW_ONLY requires no write effects")
                if cmd.get("production_execution_available") is not False:
                    failures.append(f"{command_id}: production execution must remain unavailable")
                if cmd.get("production_execution_reason_code") != "OPERATION_CONTROL_FOUNDATION_NOT_IMPLEMENTED":
                    failures.append(f"{command_id}: production execution reason code must be OPERATION_CONTROL_FOUNDATION_NOT_IMPLEMENTED")
            elif command_id in EXECUTION_PREVIEW_COMMANDS and implementation_status == "IMPLEMENTED_CONTROLLED_LOCAL_WRITE":
                if cmd.get("operation_class") != "TRACKED_WORKTREE_WRITE":
                    failures.append(f"{command_id}: IMPLEMENTED_CONTROLLED_LOCAL_WRITE requires TRACKED_WORKTREE_WRITE")
                decisions = set(cmd.get("required_human_decisions", []))
                if not {"execution_authorization", "production_execution_authorization"}.issubset(decisions):
                    failures.append(f"{command_id}: controlled write requires execution and production execution authorization")
                effects = cmd.get("effects", {})
                if not effects.get("tracked_worktree_write") or not effects.get("untracked_worktree_write") or not effects.get("temp_write"):
                    failures.append(f"{command_id}: controlled write must declare local worktree and temp effects")
                for forbidden in ["canonical_artifact_write", "git_index_write", "git_object_write", "local_git_ref_write", "remote_ref_write", "external_system_write"]:
                    if effects.get(forbidden):
                        failures.append(f"{command_id}: controlled write must not declare {forbidden}")
                non_grants = set(cmd.get("non_grants", []))
                for non_grant in ["protected_canonical_write", "destructive_operation", "commit", "push", "integration", "merge", "release", "lifecycle_mutation"]:
                    if non_grant not in non_grants:
                        failures.append(f"{command_id}: missing non-grant {non_grant}")
            elif command_id == "COMMIT" and implementation_status == "IMPLEMENTED_CONTROLLED_GIT_COMMIT":
                if cmd.get("operation_class") != "GIT_OBJECT_WRITE":
                    failures.append("COMMIT: controlled commit requires GIT_OBJECT_WRITE")
                if "commit_authorization" not in cmd.get("required_human_decisions", []):
                    failures.append("COMMIT: commit authorization is required")
                effects = cmd.get("effects", {})
                for required_effect in ["git_index_write", "git_object_write", "local_git_ref_write", "temp_write"]:
                    if effects.get(required_effect) is not True:
                        failures.append(f"COMMIT: missing required effect {required_effect}")
                for forbidden in ["tracked_worktree_write", "untracked_worktree_write", "canonical_artifact_write", "remote_ref_write", "external_system_write"]:
                    if effects.get(forbidden):
                        failures.append(f"COMMIT: forbidden effect {forbidden}")
                for non_grant in ["amend", "history_rewrite", "push", "integration", "merge", "release", "lifecycle_mutation"]:
                    if non_grant not in set(cmd.get("non_grants", [])):
                        failures.append(f"COMMIT: missing non-grant {non_grant}")
            elif command_id == "PUSH" and implementation_status == "IMPLEMENTED_CONTROLLED_BUILD_BRANCH_PUSH":
                if cmd.get("operation_class") != "REMOTE_WRITE":
                    failures.append("PUSH: controlled push requires REMOTE_WRITE")
                if "push_authorization" not in cmd.get("required_human_decisions", []):
                    failures.append("PUSH: push authorization is required")
                effects = cmd.get("effects", {})
                for required_effect in ["remote_ref_write", "external_system_write", "temp_write"]:
                    if effects.get(required_effect) is not True:
                        failures.append(f"PUSH: missing required effect {required_effect}")
                for forbidden in ["tracked_worktree_write", "untracked_worktree_write", "canonical_artifact_write", "git_index_write", "git_object_write", "local_git_ref_write"]:
                    if effects.get(forbidden):
                        failures.append(f"PUSH: forbidden effect {forbidden}")
                for non_grant in ["commit", "push_to_dev", "push_to_main", "force_push", "integration", "merge", "release", "branch_deletion", "lifecycle_mutation"]:
                    if non_grant not in set(cmd.get("non_grants", [])):
                        failures.append(f"PUSH: missing non-grant {non_grant}")
            else:
                failures.append(f"{command_id}: implementation_status must be NOT_IMPLEMENTED")

        effects = cmd.get("effects", {})
        if set(effects.keys()) != EFFECT_KEYS:
            failures.append(f"{command_id}: effects must declare exact required keys")
        for key, value in effects.items():
            if not isinstance(value, bool):
                failures.append(f"{command_id}: effect {key} must be boolean")

        op_class = cmd.get("operation_class")
        decisions = cmd.get("required_human_decisions", [])
        if op_class in WRITE_RELATED_CLASSES and not decisions:
            failures.append(f"write-related command {command_id} requires human decision")

        grants = set(cmd.get("grants", []))
        if command_id == "COMMIT" and "push" in grants:
            failures.append("COMMIT must not grant push")
        if command_id == "PUSH" and "integration" in grants:
            failures.append("PUSH must not grant integration")
        if command_id == "EXECUTE":
            preconditions = set(cmd.get("preconditions", []))
            if "controlled_execution_package_authorized_true" in preconditions and "execution_authorization" not in decisions:
                failures.append("authorized execution package requires Human Decision Witness")

        availability = cmd.get("availability", {})
        if command_id == "INTEGRATE" and data.get("integration_mechanism") == "UNKNOWN":
            if availability.get("available") is not False:
                failures.append("INTEGRATE must stay unavailable while integration_mechanism is UNKNOWN")

    missing_ids = COMMAND_IDS - seen
    extra_ids = seen - COMMAND_IDS
    if missing_ids:
        failures.append(f"missing command_id values: {sorted(missing_ids)}")
    if extra_ids:
        failures.append(f"unknown command_id values: {sorted(extra_ids)}")

    add_check(checks, "Command Registry", "PASS" if not failures else "CHECKED", "command registry inspected")
    return command_by_id(commands)


def check_locale_registry(data, commands, failures, checks):
    if not isinstance(data, dict):
        failures.append("locale registry must be an object")
        return
    if data.get("default_fallback") != "en":
        failures.append("default_fallback must be en")
    if "en" not in data.get("supported_locales", []):
        failures.append("English fallback locale must be supported")

    required_keys = set(data.get("required_explanation_keys", []))
    locales = data.get("locales", {})
    for locale in data.get("supported_locales", []):
        locale_payload = locales.get(locale)
        if not isinstance(locale_payload, dict):
            failures.append(f"missing locale payload: {locale}")
            continue
        explanation_keys = set(locale_payload.get("explanation_keys", {}).keys())
        missing = required_keys - explanation_keys
        if missing:
            failures.append(f"locale {locale} missing explanation keys: {sorted(missing)}")

        raw_alias_owner = {}
        normalized_owner = {}
        for command_id, entry in locale_payload.get("commands", {}).items():
            if command_id not in commands:
                failures.append(f"unknown command_id in locale {locale}: {command_id}")
            if "grants" in entry:
                failures.append("locale registry must not define grants")
            aliases = entry.get("aliases", [])
            if entry.get("primary_alias") not in aliases:
                failures.append(f"primary alias must be listed for {locale}/{command_id}")
            for alias in aliases:
                if alias in data.get("namespace_separators", []):
                    failures.append(f"alias collides with namespace separator: {alias}")
                if has_invisible_or_control(alias):
                    failures.append(f"invisible or control character in alias: {command_id}")
                if alias in raw_alias_owner and raw_alias_owner[alias] != command_id:
                    failures.append(f"duplicate alias in locale {locale}: {alias}")
                raw_alias_owner[alias] = command_id
                normalized = normalize_alias(alias)
                if normalized in normalized_owner and normalized_owner[normalized] != command_id:
                    failures.append(f"normalized alias collision in locale {locale}: {alias}")
                normalized_owner[normalized] = command_id
                op_class = commands.get(command_id, {}).get("operation_class")
                if op_class in WRITE_RELATED_CLASSES and has_mixed_script(alias):
                    failures.append(f"mixed-script alias for write-related command {command_id}")

        if locale != "en":
            en_commands = locales.get("en", {}).get("commands", {})
            for command_id, en_entry in en_commands.items():
                english_aliases = set(en_entry.get("aliases", []))
                locale_aliases = set(locale_payload.get("commands", {}).get(command_id, {}).get("aliases", []))
                if not english_aliases.intersection(locale_aliases):
                    failures.append(f"English fallback alias missing for {locale}/{command_id}")

    add_check(checks, "Locale Registry", "PASS" if not failures else "CHECKED", "locale registry inspected")


def nested_get(data, path):
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def check_state_schema(data, failures, checks):
    if not isinstance(data, dict):
        failures.append("state schema must be an object")
        return
    props = data.get("properties", {})
    if "status" in props:
        failures.append("untyped top-level status is forbidden")
    for namespace in ["lifecycle", "control", "operation", "validation", "authorization", "evidence", "approval"]:
        if namespace not in props:
            failures.append(f"state schema missing namespace {namespace}")

    auth_props = nested_get(data, ["properties", "authorization", "properties"]) or {}
    if "authorized" in auth_props:
        failures.append("generic authorized flag is forbidden")
    missing_flags = AUTHORIZATION_FLAGS - set(auth_props.keys())
    if missing_flags:
        failures.append(f"authorization flags missing: {sorted(missing_flags)}")

    approval_enum = nested_get(data, ["properties", "approval", "properties", "approval_status", "enum"]) or []
    if "PASS" in approval_enum:
        failures.append("PASS must not be an approval status")
    if "EVIDENCE" in approval_enum:
        failures.append("Evidence must not be an approval status")

    validation_props = nested_get(data, ["properties", "validation", "properties"]) or {}
    if validation_props.get("not_run_counts_as_pass", {}).get("const") is not False:
        failures.append("NOT_RUN must not count as PASS")
    if validation_props.get("unknown_counts_as_ok", {}).get("const") is not False:
        failures.append("UNKNOWN must not count as OK")
    if validation_props.get("pass_grants_approval", {}).get("const") is not False:
        failures.append("PASS must not grant approval")

    evidence_props = nested_get(data, ["properties", "evidence", "properties"]) or {}
    if evidence_props.get("evidence_is_approval", {}).get("const") is not False:
        failures.append("Evidence must not be approval")

    add_check(checks, "State Schema", "PASS" if not failures else "CHECKED", "state schema inspected")


def check_witness_schema(data, failures, checks):
    if not isinstance(data, dict):
        failures.append("human witness schema must be an object")
        return
    required = set(data.get("required", []))
    for field in [
        "decision_id",
        "decision_type",
        "actor_reference",
        "actor_role",
        "authentication_level",
        "decision_channel",
        "task_binding",
        "command_contract_binding",
        "repository_baseline_binding",
        "proposal_binding",
        "execution_request_binding",
        "candidate_binding",
        "operation_binding",
        "decision_value",
        "issued_at",
        "expires_at",
        "single_use",
        "consumed_at",
        "grants",
        "non_grants",
    ]:
        if field not in required:
            failures.append(f"{field} is required")

    decision_enum = set(nested_get(data, ["properties", "decision_type", "enum"]) or [])
    if decision_enum != DECISION_TYPES:
        failures.append("decision_type must stay separated")

    props = data.get("properties", {})
    if props.get("agent_generated_record_is_human_approval", {}).get("const") is not False:
        failures.append("agent-generated record cannot be human approval")
    if props.get("evidence_can_replace_witness", {}).get("const") is not False:
        failures.append("Evidence must not replace witness")
    if props.get("expired_decision_usable", {}).get("const") is not False:
        failures.append("expired decisions must not be usable")
    if props.get("consumed_single_use_decision_usable", {}).get("const") is not False:
        failures.append("consumed single-use decisions must not be reusable")

    add_check(checks, "Human Decision Witness Schema", "PASS" if not failures else "CHECKED", "human witness schema inspected")


def run(args):
    failures = []
    checks = []

    check_architecture(args.architecture_contract, failures, checks)
    command_data = read_json_contract(args.command_registry, failures)
    locale_data = read_json_contract(args.locale_registry, failures)
    state_data = read_json_contract(args.state_schema, failures)
    witness_data = read_json_contract(args.human_witness_schema, failures)

    commands = {}
    if command_data is not None:
        commands = check_command_registry(command_data, failures, checks)
    if locale_data is not None:
        check_locale_registry(locale_data, commands, failures, checks)
    if state_data is not None:
        check_state_schema(state_data, failures, checks)
    if witness_data is not None:
        check_witness_schema(witness_data, failures, checks)

    final_status = "CONTRACT_INVALID" if failures else "CONTRACT_VALID"
    result = {
        "final_status": final_status,
        "checks": checks,
        "failures": failures,
        **CLAIM_CEILING_FLAGS,
    }
    return result


def build_parser():
    parser = argparse.ArgumentParser(description="Validate the AOS Simple Control Surface contract artifacts.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    parser.add_argument("--architecture-contract", default=str(DEFAULT_ARCHITECTURE))
    parser.add_argument("--command-registry", default=str(DEFAULT_COMMANDS))
    parser.add_argument("--locale-registry", default=str(DEFAULT_LOCALES))
    parser.add_argument("--state-schema", default=str(DEFAULT_STATE_SCHEMA))
    parser.add_argument("--human-witness-schema", default=str(DEFAULT_WITNESS_SCHEMA))
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    result = run(args)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result["final_status"])
        for failure in result["failures"]:
            print(f"- {failure}")
    return 0 if result["final_status"] == "CONTRACT_VALID" else 1


if __name__ == "__main__":
    sys.exit(main())
