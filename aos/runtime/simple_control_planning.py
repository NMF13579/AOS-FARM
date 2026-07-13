import datetime
import hashlib
import json


ROUTES = {"NARROW_LOCAL_TASK", "FEATURE_OR_BEHAVIOR_CHANGE", "ARCHITECTURE_OR_CONTROL_CHANGE", "UNKNOWN"}
RISK_ORDER = ["LOW_RISK_FAST", "MEDIUM_RISK_GUIDED", "HIGH_RISK_PROTECTED", "DESTRUCTIVE_OR_CANONICAL"]


class PlanningError(Exception):
    pass


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def bind_payload(payload):
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def create_user_intent(user_requested_outcome, task_id=None, explicit_user_constraints=None, explicit_user_actions=None):
    if not user_requested_outcome or not user_requested_outcome.strip():
        raise PlanningError("user intent must not be empty")
    record = {
        "intent_id": "intent-" + hashlib.sha256(user_requested_outcome.strip().encode("utf-8")).hexdigest()[:16],
        "task_id": task_id,
        "user_requested_outcome": user_requested_outcome.strip(),
        "explicit_user_constraints": explicit_user_constraints or [],
        "explicit_user_actions": explicit_user_actions or [],
        "received_at": now_iso(),
        "documentation_route": "UNKNOWN",
        "scope_confirmed": False,
        "risk_profile_assigned_by_human": False,
        "execution_authorized": False,
    }
    return record


def validate_analysis_package(intent, package, repository_binding):
    if package.get("intent_binding") != bind_payload(intent):
        raise PlanningError("analysis package intent binding mismatch")
    if package.get("repository_binding") != repository_binding:
        raise PlanningError("analysis package repository binding mismatch")
    route = package.get("documentation_route")
    if route not in ROUTES:
        raise PlanningError("invalid documentation route")
    if route == "UNKNOWN":
        raise PlanningError("documentation route UNKNOWN blocks planning")
    if package.get("grants"):
        raise PlanningError("analysis package cannot contain grants")
    if route == "FEATURE_OR_BEHAVIOR_CHANGE" and not package.get("specification_reference"):
        raise PlanningError("feature route requires Specification reference")
    if route == "ARCHITECTURE_OR_CONTROL_CHANGE" and not package.get("architecture_decision_reference"):
        raise PlanningError("architecture route requires Architecture Decision reference")
    if not package.get("evidence_references"):
        raise PlanningError("analysis package requires evidence references")
    visible_unknown_fields = [
        field for field in ["protected_or_canonical_impact", "destructive_impact", "lifecycle_impact"]
        if package.get(field) == "unknown"
    ]
    return {
        "analysis_status": "PASS",
        "control_state": "CONTROL_ANALYZED",
        "plan_ready": True,
        "visible_unknown_fields": visible_unknown_fields,
        "approval": False,
        "execution_authorized": False,
    }


def recommend_risk_from_analysis(analysis):
    reasons = []
    if "unknown" in [analysis.get("protected_or_canonical_impact"), analysis.get("destructive_impact"), analysis.get("lifecycle_impact")]:
        return {"minimum": "UNKNOWN", "recommended": "UNKNOWN", "reasons": ["impact contains UNKNOWN"], "advisory": True, "assigned": False, "default_selection": None}
    if analysis.get("destructive_impact") == "true":
        return {"minimum": "DESTRUCTIVE_OR_CANONICAL", "recommended": "DESTRUCTIVE_OR_CANONICAL", "reasons": ["destructive impact"], "advisory": True, "assigned": False, "default_selection": None}
    if analysis.get("protected_or_canonical_impact") == "true" or analysis.get("lifecycle_impact") == "true":
        reasons.append("protected/canonical or lifecycle impact")
        return {"minimum": "HIGH_RISK_PROTECTED", "recommended": "HIGH_RISK_PROTECTED", "reasons": reasons, "advisory": True, "assigned": False, "default_selection": None}
    reasons.append("planning flow requires protected governance boundary")
    return {"minimum": "HIGH_RISK_PROTECTED", "recommended": "HIGH_RISK_PROTECTED", "reasons": reasons, "advisory": True, "assigned": False, "default_selection": None}


def create_explained_scope_proposal(intent, analysis, repository_binding, previous=None):
    validation = validate_analysis_package(intent, analysis, repository_binding)
    risk = recommend_risk_from_analysis(analysis)
    version = 1 if previous is None else previous["proposal_version"] + 1
    proposal = {
        "proposal_id": "proposal-" + bind_payload({"intent": intent["intent_id"], "analysis": analysis["analysis_id"], "version": version})[:16],
        "proposal_version": version,
        "previous_proposal_binding": None if previous is None else previous["proposal_binding"],
        "intent_binding": bind_payload(intent),
        "analysis_binding": bind_payload(analysis),
        "repository_baseline_binding": repository_binding,
        "goal": analysis["goal"],
        "documentation_route": analysis["documentation_route"],
        "user_explicit_actions": intent.get("explicit_user_actions", []),
        "required_product_actions": analysis.get("required_product_actions", []),
        "mandatory_control_actions": analysis.get("mandatory_control_actions", []),
        "optional_improvements": analysis.get("optional_improvements", []),
        "read_scope": {"exact_paths": analysis.get("candidate_read_paths", []), "allowed_patterns": [], "allowed_components": analysis.get("affected_components", [])},
        "write_scope": {"exact_paths": analysis.get("candidate_write_paths", []), "bounded_directories": [], "forbidden_paths": []},
        "discovery_scope": {"read_only": True, "allowed_components": analysis.get("affected_components", []), "automatic_write_permission": False},
        "validation": {"required": analysis.get("validation_requirements", []), "optional": []},
        "unknowns": analysis.get("unknowns", []),
        "blockers": analysis.get("blockers", []),
        "risk_recommendation": risk,
        "human_checkpoints": ["scope_confirmation", "Risk_Profile_assignment", "execution_authorization"],
        "non_grants": ["execution", "commit", "push", "integration", "merge", "release", "lifecycle_mutation"],
        "analysis_validation": validation,
    }
    proposal["proposal_binding"] = bind_payload(proposal)
    return proposal


def revise_scope_proposal(proposal, revision):
    if revision.get("remove_mandatory_control"):
        raise PlanningError("REQUIRED_CONTROL_CANNOT_BE_WAIVED")
    if revision.get("remove_required_product_action") and not revision.get("goal_reduction"):
        raise PlanningError("required product action removal requires Goal reduction")
    new_proposal = json.loads(json.dumps(proposal))
    new_proposal["proposal_version"] = proposal["proposal_version"] + 1
    new_proposal["previous_proposal_binding"] = proposal["proposal_binding"]
    new_proposal["revision_reasons"] = revision
    if revision.get("goal_reduction"):
        new_proposal["goal"] = revision["goal_reduction"]
    remove_optional = set(revision.get("remove_optional", []))
    if remove_optional:
        new_proposal["optional_improvements"] = [
            item for item in new_proposal["optional_improvements"] if item.get("action") not in remove_optional
        ]
    if revision.get("additional_restrictions"):
        new_proposal.setdefault("revision_restrictions", []).extend(revision["additional_restrictions"])
    if revision.get("remove_required_product_action"):
        remove_required = set(revision["remove_required_product_action"])
        new_proposal["required_product_actions"] = [
            item for item in new_proposal["required_product_actions"] if item.get("action") not in remove_required
        ]
    new_proposal["risk_recommendation"]["reasons"] = list(new_proposal["risk_recommendation"].get("reasons", [])) + ["risk reassessed after revision"]
    new_proposal.pop("proposal_binding", None)
    new_proposal["proposal_binding"] = bind_payload(new_proposal)
    return new_proposal


def confirm_scope(proposal, task_id, actor_reference, confirm, proposal_binding=None):
    if not confirm:
        raise PlanningError("explicit confirmation required")
    if not actor_reference:
        raise PlanningError("actor required")
    if proposal_binding and proposal_binding != proposal["proposal_binding"]:
        raise PlanningError("proposal binding mismatch")
    return {
        "decision_type": "SCOPE_CONFIRMATION",
        "decision_id": "scope-" + proposal["proposal_binding"][:16],
        "task_id": task_id,
        "proposal_id": proposal["proposal_id"],
        "proposal_version": proposal["proposal_version"],
        "proposal_binding": proposal["proposal_binding"],
        "actor_reference": actor_reference,
        "actor_role": "human",
        "authentication_level": "LOCAL_DECLARED",
        "decision_channel": "CLI",
        "decision_value": "CONFIRMED",
        "issued_at": now_iso(),
        "grants": ["scope_confirmation"],
        "non_grants": ["Risk_Profile_assignment", "execution", "commit", "push", "integration", "release", "lifecycle_mutation"],
        "execution_authorized": False,
        "risk_profile_assigned_by_human": False,
        "approval": False,
        "persistence": False,
    }


def recommend_risk_profile(proposal):
    risk = proposal["risk_recommendation"].copy()
    risk["advisory"] = True
    risk["assigned"] = False
    risk["default_selection"] = None
    return risk


def risk_at_least(selected, minimum):
    if minimum == "UNKNOWN":
        return False
    return RISK_ORDER.index(selected) >= RISK_ORDER.index(minimum)


def assign_risk_profile(proposal, scope_confirmation, selected, actor_reference, confirm):
    if not confirm:
        raise PlanningError("explicit Risk Profile confirmation required")
    if not actor_reference or actor_reference.lower().startswith("agent"):
        raise PlanningError("human actor required")
    if scope_confirmation.get("proposal_binding") != proposal["proposal_binding"]:
        raise PlanningError("scope confirmation is not bound to this proposal")
    minimum = proposal["risk_recommendation"]["minimum"]
    if selected not in RISK_ORDER:
        raise PlanningError("invalid selected Risk Profile")
    if not risk_at_least(selected, minimum):
        raise PlanningError("selected Risk Profile is below minimum")
    return {
        "decision_type": "RISK_PROFILE_ASSIGNMENT",
        "decision_id": "risk-" + proposal["proposal_binding"][:16],
        "task_id": scope_confirmation["task_id"],
        "proposal_binding": proposal["proposal_binding"],
        "minimum_Risk_Profile": minimum,
        "selected_Risk_Profile": selected,
        "actor_reference": actor_reference,
        "actor_role": "human",
        "authentication_level": "LOCAL_DECLARED",
        "decision_channel": "CLI",
        "issued_at": now_iso(),
        "grants": ["Risk_Profile_assignment"],
        "non_grants": ["execution", "commit", "push", "integration", "release", "lifecycle_mutation"],
        "execution_authorized": False,
        "approval": False,
        "persistence": False,
    }
