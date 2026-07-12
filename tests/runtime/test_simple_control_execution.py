import datetime
import contextlib
import io
import json
import subprocess
import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest import mock

from aos.runtime.simple_control_planning import (
    assign_risk_profile,
    bind_payload,
    confirm_scope,
    create_explained_scope_proposal,
    create_user_intent,
)
from aos.runtime.simple_control_status import validation_result_with_details


SCRIPT = "aos/scripts/aos_control_surface.py"
REPO_BINDING = {
    "repository": "NMF13579/AOS-FARM",
    "branch": "build/aos-farm-680-candidate-freeze",
    "head": "b1b9e7bd66db81598e1d02c0db9f4915d2b933af",
}


def run_json(*args, stdin=None):
    from aos.scripts import aos_control_surface

    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        returncode = aos_control_surface.main(["--json", *args])
    result = SimpleNamespace(returncode=returncode, stdout=stdout.getvalue(), stderr=stderr.getvalue())
    return result, json.loads(result.stdout)


class TestSimpleControlExecution(unittest.TestCase):
    def deterministic_git(self, tracked_diff="", staged_diff="", *, remote="git@github.com:NMF13579/AOS-FARM.git", branch="build/aos-farm-680-candidate-freeze", head="b1b9e7bd66db81598e1d02c0db9f4915d2b933af", fail_args=None):
        fail_args = fail_args or set()

        def fake_run_git(_repo_root, args):
            key = tuple(args)
            if key in fail_args:
                from aos.runtime.simple_control_execution import ExecutionError

                raise ExecutionError("deterministic git failure")
            responses = {
                ("remote", "get-url", "origin"): remote,
                ("branch", "--show-current"): branch,
                ("rev-parse", "HEAD"): head,
                ("diff", "--name-status"): tracked_diff,
                ("diff", "--cached", "--name-status"): staged_diff,
            }
            if key not in responses:
                raise AssertionError(f"unexpected git args: {args}")
            return responses[key]

        return mock.patch("aos.runtime.simple_control_execution._run_git", side_effect=fake_run_git)

    def clean_repository_observation(self):
        return self.deterministic_git()

    def make_intent(self):
        return create_user_intent("Prepare scoped execution package", task_id="AOS-FARM.681.6")

    def make_analysis(self, intent, **overrides):
        payload = {
            "analysis_id": "analysis-681-6",
            "intent_binding": bind_payload(intent),
            "repository_binding": REPO_BINDING,
            "documentation_route": "NARROW_LOCAL_TASK",
            "goal": "Prepare scoped execution package",
            "affected_components": ["Simple Control Surface"],
            "candidate_read_paths": ["aos/runtime/simple_control_status.py"],
            "candidate_write_paths": ["aos/runtime/example_target.py"],
            "protected_or_canonical_impact": "false",
            "destructive_impact": "false",
            "lifecycle_impact": "false",
            "required_product_actions": [{"action": "Create exact target", "reason": "requested outcome", "source": "analysis", "removable_only_with_goal_reduction": True}],
            "mandatory_control_actions": [{"action": "Stop before side effect", "reason": "681.6 boundary", "removable": False}],
            "optional_improvements": [],
            "validation_requirements": ["targeted execution tests"],
            "unknowns": [],
            "blockers": [],
            "evidence_references": ["02_AOS_Governance_Control_Module_and_Safety_Rules.md"],
            "grants": [],
        }
        payload.update(overrides)
        return payload

    def make_bundle(self):
        intent = self.make_intent()
        analysis = self.make_analysis(intent)
        proposal = create_explained_scope_proposal(intent, analysis, REPO_BINDING)
        confirmation = confirm_scope(proposal, "AOS-FARM.681.6", "human-owner", True)
        risk = assign_risk_profile(proposal, confirmation, "HIGH_RISK_PROTECTED", "human-owner", True)
        return {
            "bundle_version": 1,
            "task_id": "AOS-FARM.681.6",
            "user_intent": intent,
            "analysis_package": analysis,
            "scope_proposal": proposal,
            "scope_confirmation": confirmation,
            "risk_profile_assignment": risk,
            "execution_authorization": None,
            "repository_observation": None,
        }

    def make_request(self, bundle, **overrides):
        from aos.runtime.simple_control_execution import create_execution_request

        action = {
            "action_id": "action-1",
            "action_type": "CREATE_FILE",
            "relative_path": "aos/runtime/example_target.py",
            "expected_preimage": {"existence": False, "sha256": None},
            "proposed_content": {"encoding": "UTF-8", "sha256": bind_payload({"content": "hello"}), "size_bytes": 11},
            "scope_binding": bundle["scope_proposal"]["proposal_binding"],
            "reason": "requested outcome",
            "source_reference": "analysis-681-6",
        }
        request = create_execution_request(bundle, [action], REPO_BINDING)
        request.update(overrides)
        return request

    def make_witness(self, request, **overrides):
        from aos.runtime.simple_control_execution import create_execution_authorization_witness

        witness = create_execution_authorization_witness(request, "human-owner")
        witness.update(overrides)
        return witness

    def test_execution_request_and_witness_validation(self):
        from aos.runtime.simple_control_execution import ExecutionError, create_execution_request, create_preview

        bundle = self.make_bundle()
        request = self.make_request(bundle)
        witness = self.make_witness(request)
        with self.clean_repository_observation():
            preview = create_preview(bundle, request, witness, repository_root=".")
        self.assertTrue(preview["execution_request_valid"])
        self.assertTrue(preview["execution_authorization_valid"])
        self.assertTrue(preview["repository_observation_current"])
        self.assertTrue(preview["execution_preview_created"])
        self.assertFalse(preview["production_operation_started"])
        self.assertFalse(preview["repository_files_modified"])
        self.assertEqual(preview["control_state"], "CONTROL_READY_FOR_EXECUTION")

        with self.assertRaises(ExecutionError):
            with self.clean_repository_observation():
                create_preview(bundle, request, None, repository_root=".")
        with self.assertRaises(ExecutionError):
            with self.clean_repository_observation():
                create_preview(bundle, request, self.make_witness(request, decision_type="COMMIT_AUTHORIZATION"), repository_root=".")
        with self.assertRaises(ExecutionError):
            with self.clean_repository_observation():
                create_preview(bundle, request, self.make_witness(request, actor_reference=""), repository_root=".")
        expired = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        with self.assertRaises(ExecutionError):
            with self.clean_repository_observation():
                create_preview(bundle, request, self.make_witness(request, expires_at=expired), repository_root=".")
        with self.assertRaises(ExecutionError):
            with self.clean_repository_observation():
                create_preview(bundle, request, self.make_witness(request, consumed_at="2026-07-13T00:00:00Z"), repository_root=".")

    def test_path_safety_scope_expansion_and_action_blocking(self):
        from aos.runtime.simple_control_execution import ExecutionError, assemble_orchestrator_result

        bundle = self.make_bundle()
        request = self.make_request(bundle)
        for bad_path in ["/tmp/outside", "../outside", "aos/runtime/example_target.py/../../bad.py"]:
            bad = deepcopy(request)
            bad["planned_actions"][0]["relative_path"] = bad_path
            with self.assertRaises(ExecutionError):
                assemble_orchestrator_result(bundle, bad, self.make_witness(bad), repository_root=".")

        bad = deepcopy(request)
        bad["planned_actions"][0]["action_type"] = "DELETE"
        with self.assertRaises(ExecutionError):
            assemble_orchestrator_result(bundle, bad, self.make_witness(bad), repository_root=".")

        expansion = deepcopy(request)
        expansion["planned_actions"][0]["relative_path"] = "aos/runtime/out_of_scope.py"
        result = assemble_orchestrator_result(bundle, expansion, self.make_witness(expansion), repository_root=".")
        self.assertFalse(result["execution_package_created"])
        self.assertEqual(result["control_state"], "CONTROL_SCOPE_EXPANSION_REQUIRED")
        self.assertEqual(result["reason_code"], "WRITE_SCOPE_EXPANSION_REQUIRED")
        self.assertIn("scope_expansion_proposal", result)

    def test_execution_package_claim_ceiling(self):
        from aos.runtime.simple_control_execution import assemble_orchestrator_result

        bundle = self.make_bundle()
        request = self.make_request(bundle)
        with self.clean_repository_observation():
            result = assemble_orchestrator_result(bundle, request, self.make_witness(request), repository_root=".")
        package = result["execution_package"]
        self.assertTrue(result["execution_package_created"])
        self.assertEqual(package["execution_backend"]["status"], "NOT_BOUND")
        self.assertFalse(package["production_execution"]["available"])
        self.assertEqual(package["production_execution"]["reason_code"], "OPERATION_CONTROL_FOUNDATION_NOT_IMPLEMENTED")
        self.assertNotIn("commit", package["grants"])
        self.assertNotIn("push", package["grants"])
        self.assertFalse(package["approval"])
        self.assertFalse(package["evidence_of_success"])
        self.assertFalse(result["repository_files_modified"])

    def test_repository_observation_blocks_wrong_baseline(self):
        from aos.runtime.simple_control_execution import ExecutionError, observe_repository

        with self.clean_repository_observation():
            observation = observe_repository(".", REPO_BINDING, [])
        self.assertTrue(observation["current"])
        self.assertEqual(observation["branch"], REPO_BINDING["branch"])
        self.assertEqual(observation["head"], REPO_BINDING["head"])
        self.assertFalse(observation["git_metadata_mutated"])

        wrong = dict(REPO_BINDING, head="0" * 40)
        with self.assertRaises(ExecutionError):
            with self.clean_repository_observation():
                observe_repository(".", wrong, [])

    def test_repository_observation_blocks_deterministic_dirty_states(self):
        from aos.runtime.simple_control_execution import ExecutionError, observe_repository

        dirty_cases = [
            ("DIRTY_TRACKED", "M\taos/runtime/simple_control_execution.py", ""),
            ("DIRTY_STAGED", "", "A\taos/runtime/example_target.py"),
            ("EXACT_MIXED_STATE", "M\taos/runtime/simple_control_execution.py", "A\taos/runtime/example_target.py"),
        ]
        for label, tracked_diff, staged_diff in dirty_cases:
            with self.subTest(label=label):
                with self.deterministic_git(tracked_diff=tracked_diff, staged_diff=staged_diff):
                    with self.assertRaises(ExecutionError):
                        observe_repository(".", REPO_BINDING, [])

    def test_repository_observation_failure_is_unknown_blocking_exception(self):
        from aos.runtime.simple_control_execution import ExecutionError, observe_repository

        with self.deterministic_git(fail_args={("remote", "get-url", "origin")}):
            with self.assertRaises(ExecutionError):
                observe_repository(".", REPO_BINDING, [])

    def test_cli_execute_preview_mode(self):
        bundle = self.make_bundle()
        request = self.make_request(bundle)
        witness = self.make_witness(request)
        with self.clean_repository_observation():
            result, data = run_json("/execute", "--execution-request-json", json.dumps(request), "--execution-witness-json", json.dumps(witness), "--bundle-json", json.dumps(bundle))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["resolved_command_id"], "EXECUTE")
        self.assertTrue(data["result"]["execution_preview_created"])
        self.assertTrue(data["result"]["execution_package_created"])
        self.assertFalse(data["result"]["production_operation_started"])
        self.assertFalse(data["result"]["repository_files_modified"])
        self.assertFalse(data["effects"]["git_index_write"])
        self.assertFalse(data["effects"]["git_object_write"])

    def test_no_side_effect_boundary_for_execute(self):
        bundle = self.make_bundle()
        request = self.make_request(bundle)
        witness = self.make_witness(request)
        before = subprocess.run(["git", "status", "--short", "--untracked-files=all", "--", "aos/runtime", "tests/runtime"], capture_output=True, text=True, check=True).stdout
        with self.clean_repository_observation():
            result, data = run_json("/execute", "--execution-request-json", json.dumps(request), "--execution-witness-json", json.dumps(witness), "--bundle-json", json.dumps(bundle))
        after = subprocess.run(["git", "status", "--short", "--untracked-files=all", "--", "aos/runtime", "tests/runtime"], capture_output=True, text=True, check=True).stdout
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, after)
        self.assertFalse(data["operation_started"])
        self.assertFalse(data["platform_enforced"])


if __name__ == "__main__":
    unittest.main()
