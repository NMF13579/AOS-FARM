import json
import subprocess
import unittest
from copy import deepcopy

from aos.runtime.simple_control_planning import (
    assign_risk_profile,
    bind_payload,
    confirm_scope,
    create_explained_scope_proposal,
    create_user_intent,
)


SCRIPT = "aos/scripts/aos_control_surface.py"
REPO_BINDING = {
    "repository": "NMF13579/AOS-FARM",
    "branch": "build/aos-farm-680-candidate-freeze",
    "head": "b1b9e7bd66db81598e1d02c0db9f4915d2b933af",
}


def run_json(*args):
    result = subprocess.run(
        ["python3", "-B", SCRIPT, "--json", *args],
        capture_output=True,
        text=True,
    )
    return result, json.loads(result.stdout)


class TestSimpleControlStatus(unittest.TestCase):
    def make_intent(self):
        return create_user_intent("Validate the planning bundle", task_id="AOS-FARM.681.5")

    def make_analysis(self, intent, **overrides):
        payload = {
            "analysis_id": "analysis-681-5",
            "intent_binding": bind_payload(intent),
            "repository_binding": REPO_BINDING,
            "documentation_route": "NARROW_LOCAL_TASK",
            "goal": "Validate the planning bundle",
            "affected_components": ["Simple Control Surface"],
            "candidate_read_paths": ["aos/runtime/simple_control_planning.py"],
            "candidate_write_paths": ["aos/runtime/simple_control_status.py"],
            "protected_or_canonical_impact": "false",
            "destructive_impact": "false",
            "lifecycle_impact": "false",
            "required_product_actions": [{"action": "Add read-only status validation", "reason": "requested outcome", "source": "analysis", "removable_only_with_goal_reduction": True}],
            "mandatory_control_actions": [{"action": "Preserve PASS != approval", "reason": "Minimal Safety Floor", "removable": False}],
            "optional_improvements": [{"action": "Add extra display polish", "reason": "optional", "included": False}],
            "validation_requirements": ["targeted status tests"],
            "unknowns": [],
            "blockers": [],
            "evidence_references": ["02_AOS_Governance_Control_Module_and_Safety_Rules.md"],
            "grants": [],
        }
        payload.update(overrides)
        return payload

    def make_bundle(self, include_analysis=True, include_proposal=True, include_confirmation=True, include_risk=True, **overrides):
        intent = self.make_intent()
        analysis = self.make_analysis(intent) if include_analysis else None
        proposal = create_explained_scope_proposal(intent, analysis, REPO_BINDING) if include_analysis and include_proposal else None
        confirmation = confirm_scope(proposal, "AOS-FARM.681.5", "human-owner", True) if proposal and include_confirmation else None
        risk = assign_risk_profile(proposal, confirmation, "HIGH_RISK_PROTECTED", "human-owner", True) if confirmation and include_risk else None
        bundle = {
            "bundle_version": 1,
            "task_id": "AOS-FARM.681.5",
            "user_intent": intent,
            "analysis_package": analysis,
            "scope_proposal": proposal,
            "scope_confirmation": confirmation,
            "risk_profile_assignment": risk,
            "execution_authorization": None,
            "repository_observation": None,
        }
        bundle.update(overrides)
        return bundle

    def test_bundle_validation_and_partial_states(self):
        from aos.runtime.simple_control_status import validate_bundle

        cases = [
            (self.make_bundle(include_analysis=False, include_proposal=False, include_confirmation=False, include_risk=False), "CONTROL_ANALYZING"),
            (self.make_bundle(include_proposal=False, include_confirmation=False, include_risk=False), "CONTROL_ANALYZED"),
            (self.make_bundle(include_confirmation=False, include_risk=False), "CONTROL_SCOPE_CONFIRMATION_REQUIRED"),
            (self.make_bundle(include_risk=False), "CONTROL_RISK_SELECTION_REQUIRED"),
            (self.make_bundle(), "CONTROL_EXECUTION_AUTHORIZATION_REQUIRED"),
        ]
        for bundle, state in cases:
            result = validate_bundle(bundle)
            self.assertEqual(result["validation_status"], "PASS")
            self.assertEqual(result["derived_control_state"], state)
            self.assertFalse(result["execution_authorized"])
            self.assertEqual(result["approval_status"], "NOT_PROVIDED")
            self.assertEqual(result["evidence_status"], "NOT_RUN")

    def test_binding_and_blocking_rules(self):
        from aos.runtime.simple_control_status import StatusError, validate_bundle

        missing_intent = self.make_bundle(user_intent=None)
        with self.assertRaises(StatusError):
            validate_bundle(missing_intent)

        bad = self.make_bundle()
        bad["analysis_package"]["intent_binding"] = "wrong"
        result = validate_bundle(bad)
        self.assertEqual(result["validation_status"], "FAIL")
        self.assertEqual(result["derived_control_state"], "CONTROL_BLOCKED")

        bad = self.make_bundle()
        bad["scope_confirmation"]["proposal_binding"] = "wrong"
        result = validate_bundle(bad)
        self.assertEqual(result["derived_control_state"], "CONTROL_BLOCKED")

        bad = self.make_bundle(execution_authorization=True)
        result = validate_bundle(bad)
        self.assertEqual(result["validation_status"], "FAIL")
        self.assertIn("execution authorization is not implemented", " ".join(result["blockers"]))

    def test_unknown_minimum_and_low_selection_are_blocked(self):
        from aos.runtime.simple_control_status import validate_bundle

        intent = self.make_intent()
        analysis = self.make_analysis(intent, protected_or_canonical_impact="unknown")
        unknown = self.make_bundle(include_analysis=False, include_proposal=False, include_confirmation=False, include_risk=False)
        unknown["analysis_package"] = analysis
        unknown["scope_proposal"] = create_explained_scope_proposal(intent, analysis, REPO_BINDING)
        unknown["scope_confirmation"] = confirm_scope(unknown["scope_proposal"], "AOS-FARM.681.5", "human-owner", True)
        result = validate_bundle(unknown)
        self.assertEqual(result["derived_control_state"], "CONTROL_UNKNOWN_BLOCKED")
        self.assertEqual(result["validation_status"], "UNKNOWN")

        low = self.make_bundle()
        low["risk_profile_assignment"] = deepcopy(low["risk_profile_assignment"])
        low["risk_profile_assignment"]["selected_Risk_Profile"] = "LOW_RISK_FAST"
        result = validate_bundle(low)
        self.assertEqual(result["derived_control_state"], "CONTROL_BLOCKED")
        self.assertEqual(result["validation_status"], "FAIL")

    def test_status_next_and_details_are_advisory(self):
        from aos.runtime.simple_control_status import next_step, show_details, status_card, validate_bundle

        bundle = self.make_bundle()
        result = validate_bundle(bundle)
        card = status_card(result, locale="en")
        self.assertEqual(card["approval_status"], "NOT_PROVIDED")
        self.assertFalse(card["execution_authorized"])
        self.assertFalse(card["status_is_source_of_truth"])

        step = next_step(result)
        self.assertEqual(step["recommended_command"], "EXECUTE")
        self.assertFalse(step["available"])
        self.assertFalse(step["operation_started"])

        details = show_details(bundle, result)
        self.assertEqual(details["proposal_binding"], bundle["scope_proposal"]["proposal_binding"])
        self.assertNotIn("environment", json.dumps(details).lower())

    def test_cli_validate_status_next_details(self):
        bundle = self.make_bundle()
        bundle_json = json.dumps(bundle)
        for command in ["/validate", "/status", "/next", "/details", "/проверить", "/статус", "/дальше", "/детали"]:
            result, data = run_json("--locale", "ru", command, "--bundle-json", bundle_json)
            self.assertEqual(result.returncode, 0, command + result.stdout + result.stderr)
            self.assertFalse(data["operation_started"])
            self.assertFalse(data["authority"])
            self.assertFalse(data["result"].get("execution_authorized", False))

    def test_cli_failed_bundle_uses_validation_exit_code(self):
        bundle = self.make_bundle()
        bundle["scope_confirmation"]["proposal_binding"] = "wrong"
        result, data = run_json("/validate", "--bundle-json", json.dumps(bundle))
        self.assertEqual(result.returncode, 7)
        self.assertEqual(data["result"]["validation_status"], "FAIL")
        self.assertFalse(data["result"]["execution_authorized"])


if __name__ == "__main__":
    unittest.main()
