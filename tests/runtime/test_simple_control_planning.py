import json
import subprocess
import unittest
from copy import deepcopy


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


class TestSimpleControlPlanning(unittest.TestCase):
    def make_intent(self):
        from aos.runtime.simple_control_planning import create_user_intent

        return create_user_intent(
            "Fix NOT_RUN handling",
            task_id="AOS-FARM.681.4",
            explicit_user_constraints=["do not execute"],
            explicit_user_actions=["analyze only"],
        )

    def make_analysis(self, intent, **overrides):
        from aos.runtime.simple_control_planning import bind_payload

        payload = {
            "analysis_id": "analysis-1",
            "intent_binding": bind_payload(intent),
            "repository_binding": REPO_BINDING,
            "documentation_route": "NARROW_LOCAL_TASK",
            "goal": "Fix NOT_RUN handling",
            "affected_components": ["Governance / Control Module"],
            "candidate_read_paths": ["aos/scripts/aos_validate.py"],
            "candidate_write_paths": ["aos/scripts/aos_validate.py"],
            "protected_or_canonical_impact": "false",
            "destructive_impact": "false",
            "lifecycle_impact": "false",
            "required_product_actions": [{"action": "Adjust NOT_RUN handling", "reason": "requested outcome", "source": "analysis", "removable_only_with_goal_reduction": True}],
            "mandatory_control_actions": [{"action": "Preserve NOT_RUN != PASS", "reason": "Minimal Safety Floor", "removable": False}],
            "optional_improvements": [{"action": "Add extra docs", "reason": "optional polish", "included": False}],
            "validation_requirements": ["targeted tests"],
            "unknowns": [],
            "blockers": [],
            "evidence_references": ["00_AOS_Core_Control.md"],
            "grants": [],
        }
        payload.update(overrides)
        return payload

    def test_user_intent_record_and_empty_blocking(self):
        from aos.runtime.simple_control_planning import PlanningError, bind_payload, create_user_intent

        intent = self.make_intent()
        self.assertEqual(intent["documentation_route"], "UNKNOWN")
        self.assertFalse(intent["scope_confirmed"])
        self.assertFalse(intent["execution_authorized"])
        self.assertNotIn("task_brief_status", intent)
        self.assertEqual(bind_payload(intent), bind_payload(deepcopy(intent)))
        with self.assertRaises(PlanningError):
            create_user_intent("   ")

    def test_analysis_package_validation(self):
        from aos.runtime.simple_control_planning import PlanningError, validate_analysis_package

        intent = self.make_intent()
        analysis = self.make_analysis(intent, protected_or_canonical_impact="unknown")
        result = validate_analysis_package(intent, analysis, REPO_BINDING)
        self.assertEqual(result["analysis_status"], "PASS")
        self.assertEqual(result["control_state"], "CONTROL_ANALYZED")
        self.assertIn("protected_or_canonical_impact", result["visible_unknown_fields"])
        self.assertFalse(result["approval"])
        self.assertFalse(result["execution_authorized"])

        bad = self.make_analysis(intent, intent_binding="wrong")
        with self.assertRaises(PlanningError):
            validate_analysis_package(intent, bad, REPO_BINDING)

        bad = self.make_analysis(intent, grants=["execution"])
        with self.assertRaises(PlanningError):
            validate_analysis_package(intent, bad, REPO_BINDING)

    def test_documentation_route_requirements(self):
        from aos.runtime.simple_control_planning import PlanningError, validate_analysis_package

        intent = self.make_intent()
        feature = self.make_analysis(intent, documentation_route="FEATURE_OR_BEHAVIOR_CHANGE", specification_reference=None)
        with self.assertRaises(PlanningError):
            validate_analysis_package(intent, feature, REPO_BINDING)

        architecture = self.make_analysis(intent, documentation_route="ARCHITECTURE_OR_CONTROL_CHANGE", architecture_decision_reference=None)
        with self.assertRaises(PlanningError):
            validate_analysis_package(intent, architecture, REPO_BINDING)

        unknown = self.make_analysis(intent, documentation_route="UNKNOWN")
        with self.assertRaises(PlanningError):
            validate_analysis_package(intent, unknown, REPO_BINDING)

    def test_explained_scope_proposal_and_binding(self):
        from aos.runtime.simple_control_planning import create_explained_scope_proposal

        intent = self.make_intent()
        analysis = self.make_analysis(intent)
        proposal = create_explained_scope_proposal(intent, analysis, REPO_BINDING)
        self.assertEqual(proposal["proposal_version"], 1)
        self.assertEqual(proposal["documentation_route"], "NARROW_LOCAL_TASK")
        self.assertFalse(proposal["discovery_scope"]["automatic_write_permission"])
        self.assertFalse(proposal["optional_improvements"][0]["included"])
        self.assertIn("scope_confirmation", proposal["human_checkpoints"])
        self.assertIn("execution", proposal["non_grants"])
        self.assertEqual(proposal["proposal_binding"], create_explained_scope_proposal(intent, analysis, REPO_BINDING)["proposal_binding"])

    def test_revision_rules(self):
        from aos.runtime.simple_control_planning import PlanningError, create_explained_scope_proposal, revise_scope_proposal

        intent = self.make_intent()
        proposal = create_explained_scope_proposal(intent, self.make_analysis(intent), REPO_BINDING)
        revised = revise_scope_proposal(proposal, {"remove_optional": ["Add extra docs"], "additional_restrictions": ["no broad refactor"]})
        self.assertEqual(revised["proposal_version"], 2)
        self.assertEqual(revised["previous_proposal_binding"], proposal["proposal_binding"])
        self.assertNotEqual(revised["proposal_binding"], proposal["proposal_binding"])

        with self.assertRaises(PlanningError):
            revise_scope_proposal(proposal, {"remove_mandatory_control": ["Preserve NOT_RUN != PASS"]})
        with self.assertRaises(PlanningError):
            revise_scope_proposal(proposal, {"remove_required_product_action": ["Adjust NOT_RUN handling"]})
        reduced = revise_scope_proposal(proposal, {"goal_reduction": "Only document the gap", "remove_required_product_action": ["Adjust NOT_RUN handling"]})
        self.assertEqual(reduced["goal"], "Only document the gap")

    def test_scope_confirmation_and_risk_assignment(self):
        from aos.runtime.simple_control_planning import (
            PlanningError,
            assign_risk_profile,
            confirm_scope,
            create_explained_scope_proposal,
            recommend_risk_profile,
        )

        intent = self.make_intent()
        proposal = create_explained_scope_proposal(intent, self.make_analysis(intent), REPO_BINDING)
        recommendation = recommend_risk_profile(proposal)
        self.assertTrue(recommendation["advisory"])
        self.assertFalse(recommendation["assigned"])
        self.assertIsNone(recommendation["default_selection"])

        with self.assertRaises(PlanningError):
            confirm_scope(proposal, task_id="AOS-FARM.681.4", actor_reference="", confirm=True)
        confirmation = confirm_scope(proposal, task_id="AOS-FARM.681.4", actor_reference="human-owner", confirm=True)
        self.assertEqual(confirmation["decision_type"], "SCOPE_CONFIRMATION")
        self.assertFalse(confirmation["execution_authorized"])
        self.assertIn("Risk_Profile_assignment", confirmation["non_grants"])

        with self.assertRaises(PlanningError):
            assign_risk_profile(proposal, confirmation, "LOW_RISK_FAST", actor_reference="human-owner", confirm=True)
        assignment = assign_risk_profile(proposal, confirmation, "HIGH_RISK_PROTECTED", actor_reference="human-owner", confirm=True)
        self.assertEqual(assignment["decision_type"], "RISK_PROFILE_ASSIGNMENT")
        self.assertFalse(assignment["execution_authorized"])
        self.assertIn("execution", assignment["non_grants"])
        with self.assertRaises(PlanningError):
            assign_risk_profile(proposal, confirmation, "HIGH_RISK_PROTECTED", actor_reference="agent", confirm=True)

    def test_cli_analyze_without_package_is_not_run(self):
        result, data = run_json("/analyze", "--task-text", "Fix NOT_RUN handling")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["resolved_command_id"], "ANALYZE")
        self.assertEqual(data["result"]["analysis_status"], "NOT_RUN")
        self.assertEqual(data["result"]["control_state"], "CONTROL_ANALYZING")
        self.assertFalse(data["operation_started"])
        self.assertFalse(data["result"]["execution_authorized"])

    def test_cli_plan_accept_scope_and_select_risk(self):
        from aos.runtime.simple_control_planning import create_explained_scope_proposal

        intent = self.make_intent()
        analysis = self.make_analysis(intent)
        proposal = create_explained_scope_proposal(intent, analysis, REPO_BINDING)
        proposal_json = json.dumps(proposal)

        result, data = run_json("/plan", "--analysis-json", json.dumps(analysis), "--intent-json", json.dumps(intent))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["resolved_command_id"], "PLAN")
        self.assertEqual(data["result"]["proposal"]["proposal_version"], 1)
        self.assertFalse(data["operation_started"])

        result, data = run_json("/принять-план", "--proposal-json", proposal_json, "--actor", "human-owner", "--confirm")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["resolved_command_id"], "ACCEPT_SCOPE")
        self.assertFalse(data["result"]["scope_confirmation_record"]["execution_authorized"])

        result, data = run_json("/риск", "--proposal-json", proposal_json)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(data["result"]["recommendation"]["assigned"])

        confirmation = data = run_json("/принять-план", "--proposal-json", proposal_json, "--actor", "human-owner", "--confirm")[1]["result"]["scope_confirmation_record"]
        result, data = run_json("/риск", "--proposal-json", proposal_json, "--scope-confirmation-json", json.dumps(confirmation), "--select", "HIGH_RISK_PROTECTED", "--actor", "human-owner", "--confirm")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["result"]["risk_profile_assignment_record"]["selected_Risk_Profile"], "HIGH_RISK_PROTECTED")
        self.assertFalse(data["result"]["risk_profile_assignment_record"]["execution_authorized"])


if __name__ == "__main__":
    unittest.main()
