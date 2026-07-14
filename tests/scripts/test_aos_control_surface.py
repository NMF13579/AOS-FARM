import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = "aos/scripts/aos_control_surface.py"
SCRIPT_ABS = Path(SCRIPT).resolve()
COMMAND_REGISTRY = Path("aos/config/simple-control-command-registry.yaml")
LOCALE_REGISTRY = Path("aos/config/simple-control-locale-registry.yaml")
SCOPED_PATHS = [
    "aos/scripts/aos_control_surface.py",
    "tests/scripts/test_aos_control_surface.py",
    "tests/fixtures/simple_control",
    "aos/runtime/technical_closure_contracts.py",
    "aos/runtime/technical_closure_evaluator.py",
]


def run_surface(*args):
    return subprocess.run(
        ["python3", "-B", SCRIPT, *args],
        capture_output=True,
        text=True,
    )


def run_json(*args):
    result = run_surface("--json", *args)
    return result, json.loads(result.stdout)


class TestAOSControlSurface(unittest.TestCase):
    def test_slash_opens_menu(self):
        result, data = run_json("/")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["resolved_command_id"], "MENU")
        self.assertEqual(data["result"]["kind"], "menu")
        self.assertEqual(len(data["result"]["commands"]), 17)
        self.assertFalse(data["operation_started"])
        self.assertFalse(data["authority"])

    def test_help_aliases_resolve(self):
        for command in ["/help", "/помощь"]:
            result, data = run_json("--locale", "ru", command)
            self.assertEqual(result.returncode, 0, command)
            self.assertEqual(data["resolved_command_id"], "HELP")
            self.assertTrue(data["available"])
            self.assertFalse(data["operation_started"])

    def test_language_aliases_resolve(self):
        for command in ["/language", "/язык"]:
            result, data = run_json("--locale", "ru", command)
            self.assertEqual(result.returncode, 0, command)
            self.assertEqual(data["resolved_command_id"], "LANGUAGE")
            self.assertIn("supported_locales", data["result"])
            self.assertFalse(data["result"]["persistent_setting_created"])

    def test_locale_resolution_and_fallback(self):
        result, data = run_json("--locale", "ru", "/")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["locale"], "ru")
        labels = {item["command_id"]: item["label"] for item in data["result"]["commands"]}
        self.assertEqual(labels["HELP"], "Помощь")

        result, data = run_json("/help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["locale"], "en")

        result, data = run_json("--locale", "ru", "/help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["resolved_command_id"], "HELP")
        self.assertEqual(data["locale"], "ru")

    def test_namespace_resolution(self):
        for command in ["/aos help", "/aos помощь"]:
            result, data = run_json("--locale", "ru", command)
            self.assertEqual(result.returncode, 0, command)
            self.assertEqual(data["resolved_command_id"], "HELP")

    def test_nfc_normalization_helper(self):
        from aos.scripts.aos_control_surface import normalize_token

        self.assertEqual(normalize_token("cafe\u0301"), "café")

    def test_details_shows_registry_metadata_only(self):
        result, data = run_json("--details", "/help")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["result"]["kind"], "details")
        details = data["result"]["details"]
        self.assertEqual(details["command_id"], "HELP")
        self.assertEqual(details["operation_class"], "PURE_READ")
        self.assertIn("effects", details)
        self.assertNotIn("task_state", details)

    def test_python_help_is_usage_only(self):
        result = run_surface("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout.lower())
        self.assertNotIn("operation_started", result.stdout)

    def test_unavailable_commands_do_not_start(self):
        cases = [
            ("/integrate", "INTEGRATE", "INTEGRATION_MECHANISM_NOT_APPROVED"),
        ]
        for command, command_id, reason in cases:
            result, data = run_json("--locale", "ru", command)
            self.assertEqual(result.returncode, 4, command)
            self.assertEqual(data["resolved_command_id"], command_id)
            self.assertFalse(data["available"])
            self.assertEqual(data["reason_code"], reason)
            self.assertFalse(data["operation_started"])

    def closure_input(self, required_decision="NONE"):
        from tests.runtime.test_technical_closure_evaluator import prepared_input

        payload = prepared_input()
        payload["authorization_frontier"]["required_human_decision"] = required_decision
        return payload

    def run_closure_json(self, command, payload):
        return subprocess.run(
            ["python3", "-B", SCRIPT, "--json", command, "--closure-input", "-"],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
        )

    def test_closure_status_next_and_details_are_terminal_read_only(self):
        payload = self.closure_input("HUMAN_PUSH_DECISION")
        for command, expected_kind in [
            ("/status", "closure_status"),
            ("/next", "closure_next"),
            ("/details", "closure_details"),
        ]:
            result = self.run_closure_json(command, payload)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["resolved_command_id"], {
                "/status": "STATUS",
                "/next": "NEXT",
                "/details": "SHOW_DETAILS",
            }[command])
            self.assertEqual(data["result"]["kind"], expected_kind)
            self.assertFalse(data["operation_started"])
            self.assertFalse(data["result"]["continue_allowed"])
            self.assertFalse(data["result"].get("next_stage_started", False))
        next_data = json.loads(self.run_closure_json("/next", payload).stdout)
        self.assertEqual(next_data["result"]["next_required_action"], "HUMAN_PUSH_DECISION")

    def test_prepare_closure_outputs_full_result_without_filesystem_write(self):
        payload = self.closure_input()
        before = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        result = self.run_closure_json("/prepare-closure", payload)
        after = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, after)
        data = json.loads(result.stdout)
        self.assertEqual(data["resolved_command_id"], "PREPARE_CLOSURE")
        self.assertEqual(data["result"]["response_kind"], "TECHNICAL_CLOSURE_RESULT")
        self.assertEqual(data["result"]["closure_status"], "CLOSURE_TECHNICALLY_CLOSED")
        self.assertFalse(data["result"]["approval_granted"])
        self.assertFalse(data["result"]["next_stage_started"])

    def test_prepare_closure_contract_error_uses_exit_2(self):
        payload = self.closure_input()
        payload["subject"]["scope_digest"] = "bad"
        result = self.run_closure_json("/prepare-closure", payload)
        self.assertEqual(result.returncode, 2)
        data = json.loads(result.stdout)
        self.assertEqual(data["result"]["response_kind"], "CONTRACT_ERROR")
        self.assertIsNone(data["result"]["subject_digest"])

    def test_stop_returns_terminal_result_without_evaluator_or_input(self):
        result = run_json("/stop")
        self.assertEqual(result[0].returncode, 0, result[0].stdout + result[0].stderr)
        data = result[1]
        self.assertEqual(data["resolved_command_id"], "STOP")
        self.assertEqual(data["result"]["response_kind"], "TERMINAL_COMMAND_RESULT")
        self.assertEqual(data["result"]["next_required_action"], "NO_FURTHER_AUTOMATIC_ACTION")
        self.assertFalse(data["result"]["closure_result_mutated"])
        self.assertNotIn("technical_status", data["result"])

    def test_execute_requires_structured_preview_inputs(self):
        result, data = run_json("/execute")
        self.assertEqual(result.returncode, 5)
        self.assertEqual(data["resolved_command_id"], None)
        self.assertEqual(data["reason_code"], "COMMAND_REGISTRY_INVALID")
        self.assertFalse(data["operation_started"])

    def test_git_commands_require_structured_inputs(self):
        for command in ["/commit", "/комит", "/push", "/пуш"]:
            result, data = run_json("--locale", "ru", command)
            self.assertEqual(result.returncode, 5, command)
            self.assertEqual(data["resolved_command_id"], None)
            self.assertEqual(data["reason_code"], "COMMAND_REGISTRY_INVALID")
            self.assertFalse(data["operation_started"])

    def test_execute_apply_mode_is_sandbox_only(self):
        from aos.runtime.simple_control_operations import create_operation_id, create_production_execution_witness
        from tests.runtime.test_simple_control_operations import TestSimpleControlOperations

        helper = TestSimpleControlOperations()
        package = helper.make_package([helper.make_action("out.txt", content="prepared")])
        operation_id = create_operation_id(package)
        witness = create_production_execution_witness(operation_id, package, "human-owner")
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    "python3",
                    "-B",
                    str(SCRIPT_ABS),
                    "--json",
                    "/execute",
                    "--apply",
                    "--operation-id",
                    operation_id,
                    "--execution-package-json",
                    json.dumps(package),
                    "--production-witness-json",
                    json.dumps(witness),
                ],
                cwd=tmp,
                capture_output=True,
                text=True,
            )
        data = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["resolved_command_id"], "EXECUTE")
        self.assertEqual(data["result"]["operation_state"], "OPERATION_COMPLETED")
        self.assertFalse(data["result"]["commit_performed"])
        self.assertFalse(data["result"]["push_performed"])
        self.assertFalse(data["result"]["platform_enforced"])

    def test_validation_commands_are_read_only_available(self):
        from tests.runtime.test_simple_control_status import TestSimpleControlStatus

        helper = TestSimpleControlStatus()
        bundle = helper.make_bundle()
        bundle_json = json.dumps(bundle)
        for command_id, command in [
            ("VALIDATE", "/validate"),
            ("STATUS", "/status"),
            ("NEXT", "/next"),
            ("SHOW_DETAILS", "/details"),
        ]:
            result, data = run_json(command, "--bundle-json", bundle_json)
            self.assertEqual(result.returncode, 0, command + result.stdout + result.stderr)
            self.assertEqual(data["resolved_command_id"], command_id)
            self.assertFalse(data["operation_started"])
            self.assertFalse(data["authority"])
            self.assertFalse(data["effects"]["tracked_worktree_write"])
            self.assertFalse(data["effects"]["temp_write"])

    def test_unicode_blocks_unsafe_input(self):
        unsafe = [
            "/he\u200blp",
            "/help\u202e",
            "/cоммит",
            "/help\nnow",
            "/help\x07",
            "/aos  help",
            "/аos help",
            "/help\ufe0f",
        ]
        for command in unsafe:
            result, data = run_json("--locale", "ru", command)
            self.assertEqual(result.returncode, 3, repr(command))
            self.assertFalse(data["operation_started"])
            self.assertEqual(data["reason_code"], "UNICODE_OR_AMBIGUITY_BLOCKED")

    def test_unregistered_confusable_alias_is_not_executed(self):
        result, data = run_json("/һелр")
        self.assertEqual(result.returncode, 6)
        self.assertIsNone(data["resolved_command_id"])
        self.assertFalse(data["operation_started"])
        self.assertIn("suggestions", data["result"])

    def test_duplicate_normalized_alias_in_registry_is_blocked(self):
        from aos.scripts.aos_control_surface import RegistryError, build_alias_index

        commands = json.loads(COMMAND_REGISTRY.read_text(encoding="utf-8"))
        locales = json.loads(LOCALE_REGISTRY.read_text(encoding="utf-8"))
        locales["locales"]["en"]["commands"]["HELP"]["aliases"].append("café")
        locales["locales"]["en"]["commands"]["STATUS"]["aliases"].append("cafe\u0301")
        with self.assertRaises(RegistryError):
            build_alias_index(commands, locales)

    def test_registry_failures_are_fail_closed(self):
        from aos.scripts.aos_control_surface import RegistryError, load_json_file, load_registries

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "aos/config").mkdir(parents=True)
            shutil.copy(COMMAND_REGISTRY, root / COMMAND_REGISTRY)
            shutil.copy(LOCALE_REGISTRY, root / LOCALE_REGISTRY)

            (root / COMMAND_REGISTRY).unlink()
            with self.assertRaises(RegistryError):
                load_registries(root)

            (root / COMMAND_REGISTRY).write_text("{bad", encoding="utf-8")
            with self.assertRaises(RegistryError):
                load_json_file(root / COMMAND_REGISTRY)

            shutil.copy(COMMAND_REGISTRY, root / COMMAND_REGISTRY)
            locales = json.loads((root / LOCALE_REGISTRY).read_text(encoding="utf-8"))
            locales["locales"]["en"]["commands"]["NOPE"] = {"primary_alias": "nope", "aliases": ["nope"]}
            (root / LOCALE_REGISTRY).write_text(json.dumps(locales), encoding="utf-8")
            with self.assertRaises(RegistryError):
                load_registries(root)

    def test_no_write_side_effects_for_help(self):
        before = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all", "--", *SCOPED_PATHS],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        result, data = run_json("/help")
        self.assertEqual(result.returncode, 0)
        after = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all", "--", *SCOPED_PATHS],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.assertEqual(before, after)
        self.assertFalse(data["effects"]["tracked_worktree_write"])
        self.assertFalse(data["effects"]["git_index_write"])
        self.assertFalse(data["effects"]["remote_ref_write"])

    def test_claim_ceiling(self):
        result, data = run_json("/help")
        self.assertEqual(result.returncode, 0)
        encoded = json.dumps(data)
        self.assertFalse(data["authority"])
        self.assertFalse(data["operation_started"])
        self.assertFalse(data["risk_profile_assigned"])
        self.assertFalse(data["lifecycle_mutated"])
        self.assertFalse(data["platform_enforced"])
        self.assertNotIn("human_approval\": true", encoded)
        self.assertNotIn("approval_granted\": true", encoded)


if __name__ == "__main__":
    unittest.main()
