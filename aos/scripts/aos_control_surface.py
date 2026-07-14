import argparse
import difflib
import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

SURFACE = "AOS_SIMPLE_CONTROL"
COMMAND_REGISTRY = Path("aos/config/simple-control-command-registry.yaml")
LOCALE_REGISTRY = Path("aos/config/simple-control-locale-registry.yaml")
READ_ONLY_IMPLEMENTED = {"HELP", "LANGUAGE", "STOP"}
PLANNING_IMPLEMENTED = {"ANALYZE", "PLAN", "ACCEPT_SCOPE", "REVISE_SCOPE", "SELECT_RISK"}
VALIDATION_IMPLEMENTED = {"VALIDATE", "STATUS", "NEXT", "SHOW_DETAILS"}
CLOSURE_IMPLEMENTED = {"PREPARE_CLOSURE"}
EXECUTION_IMPLEMENTED = {"EXECUTE"}
GIT_IMPLEMENTED = {"COMMIT", "PUSH"}
IMPLEMENTED_COMMANDS = READ_ONLY_IMPLEMENTED | PLANNING_IMPLEMENTED | VALIDATION_IMPLEMENTED | CLOSURE_IMPLEMENTED | EXECUTION_IMPLEMENTED | GIT_IMPLEMENTED
READ_ONLY_CLASSES = {"PURE_READ"}
PLANNING_CLASSES = {"TEMPORARY_LOCAL_ANALYSIS", "DECISION_RECORD_PREPARATION"}
VALIDATION_CLASSES = {"TEMPORARY_LOCAL_ANALYSIS", "PURE_READ"}
MAX_INLINE_JSON_BYTES = 65536
EXIT_OK = 0
EXIT_USAGE = 2
EXIT_UNICODE_BLOCKED = 3
EXIT_UNAVAILABLE = 4
EXIT_REGISTRY_INVALID = 5
EXIT_UNKNOWN = 6
EXIT_VALIDATION_FAILED = 7
EXIT_UNKNOWN_BLOCKED = 8


class RegistryError(Exception):
    pass


class InputBlocked(Exception):
    pass


def repo_root():
    return Path(__file__).resolve().parents[2]


def normalize_token(value):
    return unicodedata.normalize("NFC", value)


def load_json_file(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryError(f"registry file missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"registry file malformed: {path}: {exc}") from exc


def char_script(ch):
    if not ch.isalpha():
        return None
    name = unicodedata.name(ch, "")
    for prefix in ("LATIN", "CYRILLIC", "GREEK", "HEBREW", "ARABIC"):
        if name.startswith(prefix + " "):
            return prefix
    return "OTHER"


def has_mixed_script(value):
    scripts = {script for ch in value for script in [char_script(ch)] if script}
    return len(scripts) > 1


def has_blocked_character(value):
    for ch in value:
        code = ord(ch)
        category = unicodedata.category(ch)
        if ch in "\n\r\t":
            return True
        if category in {"Cc", "Cf", "Zl", "Zp"}:
            return True
        if 0xFE00 <= code <= 0xFE0F:
            return True
        if 0x200B <= code <= 0x200F:
            return True
        if 0x202A <= code <= 0x202E:
            return True
    return False


def unicode_security_filter(raw_input):
    if has_blocked_character(raw_input):
        raise InputBlocked("blocked Unicode control or invisible character")
    if "  " in raw_input:
        raise InputBlocked("ambiguous whitespace sequence")
    normalized = normalize_token(raw_input.strip())
    parts = normalized.split(" ")
    for part in parts:
        token = part[1:] if part.startswith("/") else part
        if token and has_mixed_script(token):
            raise InputBlocked("mixed-script input")
    return normalized


def command_records(command_registry):
    commands = command_registry.get("commands", [])
    return {command["command_id"]: command for command in commands}


def build_alias_index(command_registry, locale_registry):
    commands = command_records(command_registry)
    supported = locale_registry.get("supported_locales", [])
    if locale_registry.get("default_fallback") != "en" or "en" not in supported:
        raise RegistryError("missing English fallback")

    by_locale = {}
    global_aliases = {}
    for locale in supported:
        payload = locale_registry.get("locales", {}).get(locale)
        if not payload:
            raise RegistryError(f"locale missing: {locale}")
        seen = {}
        by_locale[locale] = {}
        for command_id, entry in payload.get("commands", {}).items():
            if command_id not in commands:
                raise RegistryError(f"unknown command ID in locale registry: {command_id}")
            if "grants" in entry:
                raise RegistryError("locale entry containing grants")
            for alias in entry.get("aliases", []):
                normalized = normalize_token(alias).casefold()
                if normalized in seen and seen[normalized] != command_id:
                    raise RegistryError("duplicate normalized alias")
                seen[normalized] = command_id
                by_locale[locale][normalized] = command_id
                global_aliases.setdefault(normalized, []).append((locale, command_id))

    for command_id, command in commands.items():
        status = command.get("implementation_status")
        effects = command.get("effects", {})
        if status == "IMPLEMENTED_READ_ONLY":
            if command_id not in READ_ONLY_IMPLEMENTED:
                raise RegistryError("implemented command outside read-only foundation")
            if command.get("operation_class") not in READ_ONLY_CLASSES:
                raise RegistryError("implemented command without PURE_READ operation class")
            if any(effects.values()):
                raise RegistryError("implemented command without PURE_READ-compatible effects")
        if status in {"IMPLEMENTED_PLANNING_ONLY", "IMPLEMENTED_DECISION_PREPARATION_ONLY"}:
            if command_id not in PLANNING_IMPLEMENTED:
                raise RegistryError("implemented planning command outside 681.4 scope")
            if command.get("operation_class") not in PLANNING_CLASSES:
                raise RegistryError("planning command must use planning operation class")
            if any(effects.values()):
                raise RegistryError("planning command effects must be read-only")
        if status in {"IMPLEMENTED_READ_ONLY_VALIDATION", "IMPLEMENTED_DERIVED_READ_ONLY"}:
            if command_id not in VALIDATION_IMPLEMENTED:
                raise RegistryError("implemented validation command outside 681.5 scope")
            if command.get("operation_class") not in VALIDATION_CLASSES:
                raise RegistryError("validation command must use read-only validation operation class")
            if any(effects.values()):
                raise RegistryError("validation command effects must be read-only")
        if status == "IMPLEMENTED_READ_ONLY_CLOSURE":
            if command_id not in CLOSURE_IMPLEMENTED:
                raise RegistryError("implemented closure command outside 684.1 scope")
            if command.get("operation_class") != "CLOSURE_PREPARATION":
                raise RegistryError("closure command must use CLOSURE_PREPARATION")
            if any(effects.values()):
                raise RegistryError("closure command effects must be read-only")
        if status == "IMPLEMENTED_ORCHESTRATION_PREVIEW_ONLY":
            if command_id not in EXECUTION_IMPLEMENTED:
                raise RegistryError("implemented execution preview command outside 681.6 scope")
            if command.get("operation_class") != "DECISION_RECORD_PREPARATION":
                raise RegistryError("execution preview command must use DECISION_RECORD_PREPARATION")
            if any(effects.values()):
                raise RegistryError("execution preview command effects must be read-only")
        if status == "IMPLEMENTED_CONTROLLED_LOCAL_WRITE":
            if command_id not in EXECUTION_IMPLEMENTED:
                raise RegistryError("implemented controlled write command outside 681.7 scope")
            if command.get("operation_class") != "TRACKED_WORKTREE_WRITE":
                raise RegistryError("controlled write command must use TRACKED_WORKTREE_WRITE")
            if not effects.get("tracked_worktree_write") or not effects.get("untracked_worktree_write") or not effects.get("temp_write"):
                raise RegistryError("controlled write command must declare local write and temp effects")
            forbidden_effects = {"canonical_artifact_write", "git_index_write", "git_object_write", "local_git_ref_write", "remote_ref_write", "external_system_write"}
            if any(effects.get(key) for key in forbidden_effects):
                raise RegistryError("controlled write command must not declare Git, canonical, or external effects")
        if status == "IMPLEMENTED_CONTROLLED_GIT_COMMIT":
            if command_id != "COMMIT":
                raise RegistryError("controlled Git commit status is only valid for COMMIT")
            if command.get("operation_class") != "GIT_OBJECT_WRITE":
                raise RegistryError("COMMIT must use GIT_OBJECT_WRITE")
            required = {"git_index_write", "git_object_write", "local_git_ref_write", "temp_write"}
            if not all(effects.get(key) for key in required):
                raise RegistryError("COMMIT must declare index, object, ref, and temp effects")
            forbidden = {"tracked_worktree_write", "untracked_worktree_write", "canonical_artifact_write", "remote_ref_write", "external_system_write"}
            if any(effects.get(key) for key in forbidden):
                raise RegistryError("COMMIT must not declare worktree, canonical, remote, or external effects")
        if status == "IMPLEMENTED_CONTROLLED_BUILD_BRANCH_PUSH":
            if command_id != "PUSH":
                raise RegistryError("controlled build-branch push status is only valid for PUSH")
            if command.get("operation_class") != "REMOTE_WRITE":
                raise RegistryError("PUSH must use REMOTE_WRITE")
            required = {"remote_ref_write", "external_system_write", "temp_write"}
            if not all(effects.get(key) for key in required):
                raise RegistryError("PUSH must declare remote, external, and temp effects")
            forbidden = {"tracked_worktree_write", "untracked_worktree_write", "canonical_artifact_write", "git_index_write", "git_object_write", "local_git_ref_write"}
            if any(effects.get(key) for key in forbidden):
                raise RegistryError("PUSH must not declare worktree, canonical, index, object, or local ref effects")
    return {"by_locale": by_locale, "global": global_aliases}


def load_registries(root=None):
    root = Path(root) if root else repo_root()
    command_registry = load_json_file(root / COMMAND_REGISTRY)
    locale_registry = load_json_file(root / LOCALE_REGISTRY)
    alias_index = build_alias_index(command_registry, locale_registry)
    return command_registry, locale_registry, alias_index


def parse_surface_input(raw_input):
    normalized = unicode_security_filter(raw_input)
    if normalized == "/":
        return normalized, None, "MENU"
    if not normalized.startswith("/"):
        raise InputBlocked("command must start with slash")
    body = normalized[1:]
    if body.startswith("aos "):
        body = body[4:]
    elif " " in body:
        raise InputBlocked("unsupported namespace")
    if not body:
        return normalized, None, "MENU"
    return normalized, body, None


def choose_locale(explicit_locale, token, locale_registry, alias_index):
    supported = locale_registry.get("supported_locales", [])
    if explicit_locale:
        if explicit_locale not in supported:
            raise RegistryError(f"unsupported locale: {explicit_locale}")
        return explicit_locale
    if token:
        normalized = normalize_token(token).casefold()
        matches = alias_index["global"].get(normalized, [])
        matched_locales = {locale for locale, _command_id in matches}
        if len(matched_locales) == 1:
            return next(iter(matched_locales))
    return locale_registry.get("default_fallback", "en")


def resolve_command(token, locale, alias_index):
    if token is None:
        return "MENU"
    normalized = normalize_token(token).casefold()
    locale_match = alias_index["by_locale"].get(locale, {}).get(normalized)
    if locale_match:
        return locale_match
    fallback = alias_index["by_locale"].get("en", {}).get(normalized)
    if fallback:
        return fallback
    return None


def command_locale_entry(command_id, locale, locale_registry):
    locales = locale_registry.get("locales", {})
    return (
        locales.get(locale, {}).get("commands", {}).get(command_id)
        or locales.get("en", {}).get("commands", {}).get(command_id)
        or {}
    )


def group_for(command):
    command_id = command["command_id"]
    if command_id in IMPLEMENTED_COMMANDS:
        return "RECOMMENDED"
    if command.get("required_human_decisions"):
        return "REQUIRES_SEPARATE_DECISION"
    if command.get("availability", {}).get("available"):
        return "AVAILABLE"
    return "UNAVAILABLE"


def declared_effects(command):
    return command.get("effects", {
        "tracked_worktree_write": False,
        "untracked_worktree_write": False,
        "canonical_artifact_write": False,
        "git_index_write": False,
        "git_object_write": False,
        "local_git_ref_write": False,
        "remote_ref_write": False,
        "external_system_write": False,
        "temp_write": False,
    })


def base_response(raw_input, normalized_input, locale):
    return {
        "surface": SURFACE,
        "locale": locale,
        "input": raw_input,
        "normalized_input": normalized_input,
        "resolved_command_id": None,
        "available": False,
        "reason_code": None,
        "operation_class": None,
        "operation_started": False,
        "authority": False,
        "grants": [],
        "non_grants": [],
        "effects": declared_effects({}),
        "risk_profile_assigned": False,
        "lifecycle_mutated": False,
        "platform_enforced": False,
        "result": {},
    }


def render_menu(command_registry, locale_registry, locale):
    commands = []
    for command in command_registry.get("commands", []):
        command_id = command["command_id"]
        entry = command_locale_entry(command_id, locale, locale_registry)
        availability = command.get("availability", {})
        commands.append({
            "group": group_for(command),
            "command_id": command_id,
            "label": entry.get("label", command_id),
            "primary_alias": entry.get("primary_alias"),
            "description": entry.get("description", ""),
            "available": availability.get("available", False),
            "reason_code": availability.get("reason_code"),
            "operation_class": command.get("operation_class"),
            "request_is_authorization": False,
        })
    return {
        "kind": "menu",
        "groups": ["RECOMMENDED", "AVAILABLE", "UNAVAILABLE", "REQUIRES_SEPARATE_DECISION"],
        "commands": commands,
        "boundary": "Command input is not authorization. PASS and Evidence are not approval.",
    }


def render_help(locale):
    return {
        "kind": "help",
        "groups": {
            "RECOMMENDED": "Suggested read-only commands.",
            "AVAILABLE": "Available read-only commands.",
            "UNAVAILABLE": "Commands present in the registry but not executable here.",
            "REQUIRES_SEPARATE_DECISION": "Commands that require a separate human decision before any future action.",
        },
        "available_means": "The read-only adapter can render the command response.",
        "unavailable_means": "The operation is not started and the reason code is shown.",
        "request_vs_authorization": "A command request is not human authorization.",
        "approval_boundary": "PASS, Evidence, and CI PASS are not approval.",
        "language_selection": "Use --locale en or --locale ru for the current invocation only.",
        "details": "Use --details with a command to show registry metadata.",
        "locale": locale,
    }


def render_language(locale, locale_registry):
    return {
        "kind": "language",
        "current_locale": locale,
        "supported_locales": locale_registry.get("supported_locales", []),
        "default_fallback": locale_registry.get("default_fallback"),
        "persistent_setting_created": False,
    }


def repository_binding():
    return {
        "repository": "NMF13579/AOS-FARM",
        "branch": "build/aos-farm-680-candidate-freeze",
        "head": "b1b9e7bd66db81598e1d02c0db9f4915d2b933af",
    }


def parse_json_arg(value, label):
    if not value:
        raise RegistryError(f"{label} is required")
    if len(value.encode("utf-8")) > MAX_INLINE_JSON_BYTES:
        raise RegistryError(f"{label} exceeds input size limit")
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise RegistryError(f"{label} is malformed JSON: {exc}") from exc


def parse_bundle_arg(args):
    if args.bundle_stdin:
        text = sys.stdin.read(MAX_INLINE_JSON_BYTES + 1)
        if len(text.encode("utf-8")) > MAX_INLINE_JSON_BYTES:
            raise RegistryError("bundle-stdin exceeds input size limit")
        return parse_json_arg(text, "bundle-stdin")
    return parse_json_arg(args.bundle_json, "bundle-json")


def parse_execution_request_arg(args):
    if args.execution_request_stdin:
        text = sys.stdin.read(MAX_INLINE_JSON_BYTES + 1)
        if len(text.encode("utf-8")) > MAX_INLINE_JSON_BYTES:
            raise RegistryError("execution-request-stdin exceeds input size limit")
        return parse_json_arg(text, "execution-request-stdin")
    return parse_json_arg(args.execution_request_json, "execution-request-json")


def parse_execution_package_arg(args):
    if args.execution_package_stdin:
        text = sys.stdin.read(MAX_INLINE_JSON_BYTES + 1)
        if len(text.encode("utf-8")) > MAX_INLINE_JSON_BYTES:
            raise RegistryError("execution-package-stdin exceeds input size limit")
        return parse_json_arg(text, "execution-package-stdin")
    return parse_json_arg(args.execution_package_json, "execution-package-json")


def parse_candidate_manifest_arg(args):
    if args.candidate_manifest_stdin:
        text = sys.stdin.read(MAX_INLINE_JSON_BYTES + 1)
        if len(text.encode("utf-8")) > MAX_INLINE_JSON_BYTES:
            raise RegistryError("candidate-manifest-stdin exceeds input size limit")
        return parse_json_arg(text, "candidate-manifest-stdin")
    return parse_json_arg(args.candidate_manifest_json, "candidate-manifest-json")


def parse_push_request_arg(args):
    if args.push_request_stdin:
        text = sys.stdin.read(MAX_INLINE_JSON_BYTES + 1)
        if len(text.encode("utf-8")) > MAX_INLINE_JSON_BYTES:
            raise RegistryError("push-request-stdin exceeds input size limit")
        return parse_json_arg(text, "push-request-stdin")
    return parse_json_arg(args.push_request_json, "push-request-json")


def parse_closure_input_arg(args):
    if args.closure_input != "-":
        raise RegistryError("closure-input supports only '-' for stdin")
    text = sys.stdin.read(MAX_INLINE_JSON_BYTES + 1)
    if len(text.encode("utf-8")) > MAX_INLINE_JSON_BYTES:
        raise RegistryError("closure-input exceeds input size limit")
    return parse_json_arg(text, "closure-input")


def closure_non_grants(result):
    return {
        "approval_granted": result.get("approval_granted") is True,
        "execution_authorized": result.get("execution_authorized") is True,
        "commit_authorized": result.get("commit_authorized") is True,
        "push_authorized": result.get("push_authorized") is True,
        "integration_authorized": result.get("integration_authorized") is True,
        "release_authorized": result.get("release_authorized") is True,
        "operation_started": result.get("operation_started") is True,
        "background_action_started": result.get("background_action_started") is True,
        "broad_reaudit_started": result.get("broad_reaudit_started") is True,
        "schedule_created": result.get("schedule_created") is True,
        "lifecycle_mutated": result.get("lifecycle_mutated") is True,
        "next_stage_started": result.get("next_stage_started") is True,
    }


def evaluate_closure_input(args):
    from aos.runtime.technical_closure_evaluator import evaluate_technical_closure

    return evaluate_technical_closure(parse_closure_input_arg(args))


def render_closure_command(command_id, args):
    result = evaluate_closure_input(args)
    if command_id == "PREPARE_CLOSURE":
        return result
    if result.get("response_kind") == "CONTRACT_ERROR":
        return result
    if command_id == "STATUS":
        return {
            "kind": "closure_status",
            "task_id": result["task_id"],
            "technical_status": result["technical_status"],
            "control_status": result["control_status"],
            "closure_status": result["closure_status"],
            "subject_digest": result["subject_digest"],
            "evaluation_input_digest": result["evaluation_input_digest"],
            "result_digest": result["result_digest"],
            "binding_changed": result["binding_changed"],
            "evaluation_input_changed": result["evaluation_input_changed"],
            "reopened": result["reopened"],
            "next_required_action": result["next_required_action"],
            "continue_allowed": False,
        }
    if command_id == "NEXT":
        return {
            "kind": "closure_next",
            "next_required_action": result["next_required_action"],
            "continue_allowed": False,
            "operation_started": False,
            "next_stage_started": False,
        }
    if command_id == "SHOW_DETAILS":
        return {
            "kind": "closure_details",
            "reason_codes": result["reason_codes"],
            "stale_inputs": result["stale_inputs"],
            "binding": {
                "subject_digest": result["subject_digest"],
                "evaluation_input_digest": result["evaluation_input_digest"],
                "binding_changed": result["binding_changed"],
                "evaluation_input_changed": result["evaluation_input_changed"],
                "reopened": result["reopened"],
            },
            "previous_result_summary": {
                "binding_changed": result["binding_changed"],
                "evaluation_input_changed": result["evaluation_input_changed"],
                "reopened": result["reopened"],
            },
            "required_human_decision": result["required_human_decision"],
            "review_trigger_references": {
                "broad_reaudit_may_be_proposed": result["broad_reaudit_may_be_proposed"],
                "broad_reaudit_started": False,
            },
            "non_grants": closure_non_grants(result),
            "continue_allowed": False,
        }
    raise RegistryError(f"closure command not implemented: {command_id}")


def render_stop_command():
    from aos.runtime.technical_closure_contracts import terminal_stop_result

    return terminal_stop_result()


def render_planning_command(command_id, args):
    from aos.runtime.simple_control_planning import (
        assign_risk_profile,
        confirm_scope,
        create_explained_scope_proposal,
        create_user_intent,
        recommend_risk_profile,
        revise_scope_proposal,
        validate_analysis_package,
    )

    repo = repository_binding()
    if command_id == "ANALYZE":
        intent = create_user_intent(args.task_text, task_id="AOS-FARM.681.4") if args.task_text else parse_json_arg(args.intent_json, "intent-json")
        if not args.analysis_json:
            return {
                "kind": "analyze",
                "intent_record": intent,
                "intent_record_created": True,
                "analysis_status": "NOT_RUN",
                "control_state": "CONTROL_ANALYZING",
                "plan_ready": False,
                "execution_authorized": False,
            }
        analysis = parse_json_arg(args.analysis_json, "analysis-json")
        validation = validate_analysis_package(intent, analysis, repo)
        return {"kind": "analyze", "intent_record": intent, **validation}

    if command_id == "PLAN":
        intent = parse_json_arg(args.intent_json, "intent-json")
        analysis = parse_json_arg(args.analysis_json, "analysis-json")
        proposal = create_explained_scope_proposal(intent, analysis, repo)
        return {"kind": "plan", "proposal": proposal, "execution_authorized": False}

    if command_id == "REVISE_SCOPE":
        proposal = parse_json_arg(args.proposal_json, "proposal-json")
        revision = parse_json_arg(args.revision_json, "revision-json")
        revised = revise_scope_proposal(proposal, revision)
        return {"kind": "revision", "proposal": revised, "execution_authorized": False}

    if command_id == "ACCEPT_SCOPE":
        proposal = parse_json_arg(args.proposal_json, "proposal-json")
        record = confirm_scope(
            proposal,
            task_id="AOS-FARM.681.4",
            actor_reference=args.actor,
            confirm=args.confirm,
            proposal_binding=proposal.get("proposal_binding"),
        )
        return {"kind": "scope_confirmation", "scope_confirmation_record": record}

    if command_id == "SELECT_RISK":
        proposal = parse_json_arg(args.proposal_json, "proposal-json")
        recommendation = recommend_risk_profile(proposal)
        if not args.select:
            return {"kind": "risk_menu", "recommendation": recommendation, "execution_authorized": False}
        confirmation = parse_json_arg(args.scope_confirmation_json, "scope-confirmation-json")
        record = assign_risk_profile(proposal, confirmation, args.select, actor_reference=args.actor, confirm=args.confirm)
        return {"kind": "risk_assignment", "recommendation": recommendation, "risk_profile_assignment_record": record}

    raise RegistryError(f"planning command not implemented: {command_id}")


def render_validation_command(command_id, args):
    from aos.runtime.simple_control_status import (
        next_step,
        show_details,
        status_card,
        validation_result_with_details,
    )

    bundle = parse_bundle_arg(args)
    validation = validation_result_with_details(bundle)
    if command_id == "VALIDATE":
        return validation
    if command_id == "STATUS":
        return status_card(validation, locale=args.locale or "en")
    if command_id == "NEXT":
        return next_step(validation)
    if command_id == "SHOW_DETAILS":
        return show_details(bundle, validation)
    raise RegistryError(f"validation command not implemented: {command_id}")


def render_execution_command(args):
    from aos.runtime.simple_control_execution import assemble_orchestrator_result

    if args.apply or args.reconcile_only:
        from aos.runtime.simple_control_operations import (
            OperationError,
            active_repository_root,
            apply_execution_package,
            reconcile_operation,
        )

        if Path.cwd().resolve() == active_repository_root().resolve():
            raise RegistryError("apply/reconcile mode is blocked against active AOS-FARM repository")
        package = parse_execution_package_arg(args)
        if not args.operation_id:
            raise RegistryError("operation-id is required")
        try:
            if args.reconcile_only:
                return reconcile_operation(package, args.operation_id, Path.cwd())
            witness = parse_json_arg(args.production_witness_json, "production-witness-json")
            return apply_execution_package(package, witness, args.operation_id, Path.cwd())
        except OperationError as exc:
            raise RegistryError(str(exc)) from exc

    bundle = parse_bundle_arg(args)
    request = parse_execution_request_arg(args)
    witness = parse_json_arg(args.execution_witness_json, "execution-witness-json")
    return assemble_orchestrator_result(bundle, request, witness, repository_root=repo_root())


def render_git_command(command_id, args):
    from aos.runtime.simple_control_git import (
        GitControlError,
        apply_commit,
        apply_push,
        create_commit_preview,
        create_push_preview,
        reconcile_commit,
        reconcile_push,
    )

    try:
        if command_id == "COMMIT":
            manifest = parse_candidate_manifest_arg(args)
            request = parse_json_arg(args.commit_request_json, "commit-request-json")
            if args.reconcile_only:
                return reconcile_commit(Path.cwd(), manifest, request)
            if args.apply:
                witness = parse_json_arg(args.commit_witness_json, "commit-witness-json")
                return apply_commit(Path.cwd(), manifest, request, witness)
            return create_commit_preview(Path.cwd(), manifest, request)
        if command_id == "PUSH":
            request = parse_push_request_arg(args)
            if args.reconcile_only:
                return reconcile_push(Path.cwd(), request)
            if args.apply:
                witness = parse_json_arg(args.push_witness_json, "push-witness-json")
                return apply_push(Path.cwd(), request, witness)
            return create_push_preview(Path.cwd(), request)
    except GitControlError as exc:
        raise RegistryError(str(exc)) from exc
    raise RegistryError(f"Git command not implemented: {command_id}")


def render_details(command):
    availability = command.get("availability", {})
    return {
        "kind": "details",
        "details": {
            "command_id": command.get("command_id"),
            "contract_version": command.get("contract_version"),
            "operation_class": command.get("operation_class"),
            "availability": availability.get("available", False),
            "reason_code": availability.get("reason_code"),
            "grants": command.get("grants", []),
            "non_grants": command.get("non_grants", []),
            "effects": declared_effects(command),
            "implementation_status": command.get("implementation_status"),
        },
    }


def suggestions_for(token, alias_index, command_registry):
    read_only_commands = READ_ONLY_IMPLEMENTED
    choices = []
    for alias, matches in alias_index["global"].items():
        if any(command_id in read_only_commands for _locale, command_id in matches):
            choices.append(alias)
    return difflib.get_close_matches(normalize_token(token).casefold(), choices, n=3, cutoff=0.6)


def handle_command(raw_input, explicit_locale=None, details=False, args=None):
    command_registry, locale_registry, alias_index = load_registries()
    normalized_input, token, menu_marker = parse_surface_input(raw_input)
    locale = choose_locale(explicit_locale, token, locale_registry, alias_index)
    response = base_response(raw_input, normalized_input, locale)

    if menu_marker == "MENU":
        response.update({
            "resolved_command_id": "MENU",
            "available": True,
            "operation_class": "PURE_READ",
            "result": render_menu(command_registry, locale_registry, locale),
        })
        return response, EXIT_OK

    command_id = resolve_command(token, locale, alias_index)
    if not command_id:
        response.update({
            "reason_code": "UNKNOWN_COMMAND",
            "result": {
                "kind": "unknown_command",
                "suggestions": suggestions_for(token, alias_index, command_registry),
                "suggestion_executed": False,
            },
        })
        return response, EXIT_UNKNOWN

    commands = command_records(command_registry)
    command = commands[command_id]
    availability = command.get("availability", {})
    response.update({
        "resolved_command_id": command_id,
        "available": availability.get("available", False),
        "reason_code": availability.get("reason_code"),
        "operation_class": command.get("operation_class"),
        "grants": command.get("grants", []),
        "non_grants": command.get("non_grants", []),
        "effects": declared_effects(command),
    })

    if details:
        response["result"] = render_details(command)
    elif command_id == "HELP":
        response["result"] = render_help(locale)
    elif command_id == "LANGUAGE":
        response["result"] = render_language(locale, locale_registry)
    elif command_id == "STOP":
        response["result"] = render_stop_command()
    elif args and args.closure_input and command_id in {"STATUS", "NEXT", "SHOW_DETAILS", "PREPARE_CLOSURE"}:
        response["result"] = render_closure_command(command_id, args)
    elif command_id in PLANNING_IMPLEMENTED:
        response["result"] = render_planning_command(command_id, args)
    elif command_id in VALIDATION_IMPLEMENTED:
        response["result"] = render_validation_command(command_id, args)
    elif command_id in CLOSURE_IMPLEMENTED:
        raise RegistryError("PREPARE_CLOSURE requires --closure-input -")
    elif command_id in EXECUTION_IMPLEMENTED:
        response["result"] = render_execution_command(args)
    elif command_id in GIT_IMPLEMENTED:
        response["result"] = render_git_command(command_id, args)
    else:
        response["result"] = {
            "kind": "unavailable_command",
            "message": "Operation not started.",
            "request_is_authorization": False,
        }

    if not response["available"]:
        return response, EXIT_UNAVAILABLE
    if response["result"].get("response_kind") == "CONTRACT_ERROR":
        return response, EXIT_USAGE
    if command_id == "VALIDATE":
        validation_status = response["result"].get("validation_status")
        if validation_status == "UNKNOWN":
            return response, EXIT_UNKNOWN_BLOCKED
        if validation_status == "FAIL":
            return response, EXIT_VALIDATION_FAILED
    return response, EXIT_OK


def render_text(response):
    command_id = response.get("resolved_command_id")
    if response["result"].get("kind") == "menu":
        lines = ["Simple Control Surface", "Command input is not authorization."]
        for item in response["result"]["commands"]:
            reason = f" reason={item['reason_code']}" if item["reason_code"] else ""
            lines.append(f"[{item['group']}] {item['label']} /{item['primary_alias']} ({item['command_id']}) available={item['available']}{reason}")
        return "\n".join(lines)
    if response["result"].get("kind") == "help":
        return "Help: command requests are not authorization. PASS and Evidence are not approval."
    if response["result"].get("kind") == "language":
        return f"Language: {response['locale']} supported={', '.join(response['result']['supported_locales'])}; no persistent setting created."
    if response["result"].get("kind") == "details":
        return json.dumps(response["result"]["details"], indent=2, ensure_ascii=False)
    if response["result"].get("validation_version") == 1:
        return f"Validation bundle: {response['result']['validation_status']}. Approval: not provided. Execution authorization: not provided."
    if response["result"].get("kind") == "status":
        return f"Status: {response['result']['control_state_label']}. Validation={response['result']['validation_status']}. Execution authorization: not provided."
    if response["result"].get("kind") == "next":
        return f"Next: {response['result']['recommended_command']} available={response['result']['available']}. Operation not started."
    if response["result"].get("kind") == "closure_status":
        return f"Closure status: {response['result']['closure_status']}. Next action: {response['result']['next_required_action']}. Continue allowed: false."
    if response["result"].get("kind") == "closure_next":
        return f"Closure next: {response['result']['next_required_action']}. Operation not started."
    if response["result"].get("kind") == "closure_details":
        return json.dumps(response["result"], indent=2, ensure_ascii=False)
    if response["result"].get("response_kind") == "TECHNICAL_CLOSURE_RESULT":
        return f"Technical closure: {response['result']['closure_status']}. Approval: not provided. Continue allowed: false."
    if response["result"].get("response_kind") == "CONTRACT_ERROR":
        return "Technical closure contract error. Operation not started."
    if response["result"].get("response_kind") == "TERMINAL_COMMAND_RESULT":
        return "Stop: terminal read-only response. No operation started."
    if response["result"].get("kind") == "execute_preview":
        return "Execution package prepared. Files were not modified. Operation Control Foundation is required for actual execution."
    if response["result"].get("operation_state") == "OPERATION_COMPLETED":
        return "File changes prepared. Commit was not performed. Push was not performed. Approval was not provided."
    if response["result"].get("reconciliation_result"):
        return f"Reconciliation: {response['result']['reconciliation_result']}. Operation not repeated."
    if response["result"].get("commit_state") == "COMMIT_COMPLETED":
        return "Commit created. Push was not performed. Integration is not authorized. Result approval was not provided."
    if response["result"].get("push_state") == "PUSH_COMPLETED":
        return "Exact commit pushed to Build branch. Integration was not performed. Release is not authorized."
    if command_id:
        return f"{command_id}: unavailable. reason={response['reason_code']}. Operation not started."
    return f"Unknown command. suggestions={response['result'].get('suggestions', [])}. Operation not started."


def build_parser():
    parser = argparse.ArgumentParser(description="Read-only AOS Simple Control Surface adapter.")
    parser.add_argument("--locale", choices=["en", "ru"], help="Locale for this invocation only.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--details", action="store_true", help="Show registry metadata for a command.")
    parser.add_argument("--task-text", help="Free-form user task text for /analyze.")
    parser.add_argument("--intent-json", help="Inline User Intent Record JSON.")
    parser.add_argument("--analysis-json", help="Inline Analysis Package JSON.")
    parser.add_argument("--proposal-json", help="Inline Explained Scope Proposal JSON.")
    parser.add_argument("--revision-json", help="Inline revision JSON.")
    parser.add_argument("--scope-confirmation-json", help="Inline Scope Confirmation Record JSON.")
    parser.add_argument("--bundle-json", help="Inline Validation Bundle JSON.")
    parser.add_argument("--bundle-stdin", action="store_true", help="Read bounded Validation Bundle JSON from stdin.")
    parser.add_argument("--closure-input", help="Use '-' to read deterministic technical closure JSON from stdin.")
    parser.add_argument("--execution-request-json", help="Inline Execution Request JSON.")
    parser.add_argument("--execution-request-stdin", action="store_true", help="Read bounded Execution Request JSON from stdin.")
    parser.add_argument("--execution-witness-json", help="Inline Execution Authorization Witness JSON.")
    parser.add_argument("--apply", action="store_true", help="Apply an exact execution package in a non-active sandbox only.")
    parser.add_argument("--reconcile-only", action="store_true", help="Reconcile an operation without applying side effects.")
    parser.add_argument("--operation-id", help="Operation ID for apply or reconcile-only mode.")
    parser.add_argument("--execution-package-json", help="Inline Execution Package JSON for apply or reconcile-only mode.")
    parser.add_argument("--execution-package-stdin", action="store_true", help="Read bounded Execution Package JSON from stdin.")
    parser.add_argument("--production-witness-json", help="Inline Production Execution Authorization Witness JSON.")
    parser.add_argument("--candidate-manifest-json", help="Inline Candidate Manifest JSON for /commit.")
    parser.add_argument("--candidate-manifest-stdin", action="store_true", help="Read bounded Candidate Manifest JSON from stdin.")
    parser.add_argument("--commit-request-json", help="Inline Commit Request JSON.")
    parser.add_argument("--commit-witness-json", help="Inline Commit Authorization Witness JSON.")
    parser.add_argument("--push-request-json", help="Inline Push Request JSON.")
    parser.add_argument("--push-request-stdin", action="store_true", help="Read bounded Push Request JSON from stdin.")
    parser.add_argument("--push-witness-json", help="Inline Push Authorization Witness JSON.")
    parser.add_argument("--actor", help="Declared human actor reference for decision preparation.")
    parser.add_argument("--confirm", action="store_true", help="Explicitly confirm a decision-preparation command.")
    parser.add_argument("--select", choices=["LOW_RISK_FAST", "MEDIUM_RISK_GUIDED", "HIGH_RISK_PROTECTED", "DESTRUCTIVE_OR_CANONICAL"], help="Selected Risk Profile for decision preparation.")
    parser.add_argument("command", nargs="?", help="Slash command, for example /, /help, /помощь, or '/aos help'.")
    return parser


def emit_response(response, as_json):
    if as_json:
        print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        print(render_text(response))


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_usage(sys.stderr)
        return EXIT_USAGE
    try:
        response, exit_code = handle_command(args.command, explicit_locale=args.locale, details=args.details, args=args)
    except InputBlocked as exc:
        response = base_response(args.command, args.command, args.locale or "en")
        response.update({
            "reason_code": "UNICODE_OR_AMBIGUITY_BLOCKED",
            "result": {"kind": "blocked_input", "message": str(exc)},
        })
        emit_response(response, args.json)
        return EXIT_UNICODE_BLOCKED
    except RegistryError as exc:
        response = base_response(args.command, args.command, args.locale or "en")
        response.update({
            "reason_code": "COMMAND_REGISTRY_INVALID",
            "result": {"kind": "registry_error", "message": str(exc)},
        })
        emit_response(response, args.json)
        return EXIT_REGISTRY_INVALID
    emit_response(response, args.json)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
