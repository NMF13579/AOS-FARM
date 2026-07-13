import json
import subprocess
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


SCRIPT = "aos/scripts/aos_simple_control_contract_check.py"
ARCHITECTURE = "aos/docs/workflow/simple-control-surface.md"
COMMANDS = "aos/config/simple-control-command-registry.yaml"
LOCALES = "aos/config/simple-control-locale-registry.yaml"
STATE_SCHEMA = "aos/schemas/simple-control-state.schema.json"
WITNESS_SCHEMA = "aos/schemas/human-decision-witness.schema.json"


class TestSimpleControlContractCheck(unittest.TestCase):
    def run_check(self, *args):
        return subprocess.run(
            ["python3", SCRIPT, "--json", *args],
            capture_output=True,
            text=True,
        )

    def load_json(self, path):
        return json.loads(Path(path).read_text(encoding="utf-8"))

    def write_json(self, path, payload):
        Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def with_temp_contracts(self, tmp_dir):
        tmp_path = Path(tmp_dir)
        arch = tmp_path / "simple-control-surface.md"
        commands = tmp_path / "simple-control-command-registry.yaml"
        locales = tmp_path / "simple-control-locale-registry.yaml"
        state = tmp_path / "simple-control-state.schema.json"
        witness = tmp_path / "human-decision-witness.schema.json"

        arch.write_text(Path(ARCHITECTURE).read_text(encoding="utf-8"), encoding="utf-8")
        self.write_json(commands, self.load_json(COMMANDS))
        self.write_json(locales, self.load_json(LOCALES))
        self.write_json(state, self.load_json(STATE_SCHEMA))
        self.write_json(witness, self.load_json(WITNESS_SCHEMA))

        args = [
            "--architecture-contract", str(arch),
            "--command-registry", str(commands),
            "--locale-registry", str(locales),
            "--state-schema", str(state),
            "--human-witness-schema", str(witness),
        ]
        return args, arch, commands, locales, state, witness

    def assert_invalid(self, result, expected_fragment):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["final_status"], "CONTRACT_INVALID")
        self.assertFalse(data["approval_granted"])
        self.assertFalse(data["execution_authorized"])
        self.assertFalse(data["commit_authorized"])
        self.assertFalse(data["push_authorized"])
        self.assertFalse(data["integration_authorized"])
        self.assertIn(expected_fragment, "\n".join(data["failures"]))

    def mutate(self, callback):
        with tempfile.TemporaryDirectory() as tmp_dir:
            args, arch, commands, locales, state, witness = self.with_temp_contracts(tmp_dir)
            callback(arch, commands, locales, state, witness)
            return self.run_check(*args)

    def test_help_exits_zero(self):
        result = subprocess.run(["python3", SCRIPT, "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("simple control", result.stdout.lower())

    def test_repository_contract_is_valid_and_has_claim_ceiling(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["final_status"], "CONTRACT_VALID")
        self.assertFalse(data["approval_granted"])
        self.assertFalse(data["execution_authorized"])
        self.assertFalse(data["commit_authorized"])
        self.assertFalse(data["push_authorized"])
        self.assertFalse(data["integration_authorized"])
        self.assertFalse(data["platform_enforced"])
        self.assertFalse(data["runtime_implemented"])
        forbidden_claims = {
            "APPROVED",
            "EXECUTION_AUTHORIZED",
            "COMMIT_AUTHORIZED",
            "PUSH_AUTHORIZED",
            "INTEGRATION_AUTHORIZED",
        }
        self.assertNotIn(data["final_status"], forbidden_claims)

    def test_duplicate_command_id_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            data["commands"].append(deepcopy(data["commands"][0]))
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "duplicate command_id")

    def test_missing_command_contract_version_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            del data["commands"][0]["contract_version"]
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "missing required field contract_version")

    def test_write_command_without_human_decision_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            execute = next(cmd for cmd in data["commands"] if cmd["command_id"] == "EXECUTE")
            execute["required_human_decisions"] = []
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "write-related command EXECUTE requires human decision")

    def test_commit_granting_push_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            commit = next(cmd for cmd in data["commands"] if cmd["command_id"] == "COMMIT")
            commit["grants"] = ["push"]
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "COMMIT must not grant push")

    def test_push_granting_integration_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            push = next(cmd for cmd in data["commands"] if cmd["command_id"] == "PUSH")
            push["grants"] = ["integration"]
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "PUSH must not grant integration")

    def test_integrate_available_while_mechanism_unknown_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            integrate = next(cmd for cmd in data["commands"] if cmd["command_id"] == "INTEGRATE")
            integrate["availability"]["available"] = True
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "INTEGRATE must stay unavailable")

    def test_skeleton_claimed_as_implementation_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            data["commands"][0]["implementation_status"] = "IMPLEMENTED"
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "implementation_status must be NOT_IMPLEMENTED or IMPLEMENTED_READ_ONLY")

    def test_locale_alias_for_unknown_command_is_invalid(self):
        def change(_arch, _commands, locales, _state, _witness):
            data = self.load_json(locales)
            data["locales"]["en"]["commands"]["NOPE"] = {
                "primary_alias": "nope",
                "aliases": ["nope"],
                "label": "Nope",
                "description": "Nope",
            }
            self.write_json(locales, data)
        self.assert_invalid(self.mutate(change), "unknown command_id in locale")

    def test_duplicate_alias_is_invalid(self):
        def change(_arch, _commands, locales, _state, _witness):
            data = self.load_json(locales)
            data["locales"]["en"]["commands"]["STATUS"]["aliases"].append("help")
            self.write_json(locales, data)
        self.assert_invalid(self.mutate(change), "duplicate alias")

    def test_normalized_alias_collision_is_invalid(self):
        def change(_arch, _commands, locales, _state, _witness):
            data = self.load_json(locales)
            data["locales"]["en"]["commands"]["HELP"]["aliases"].append("café")
            data["locales"]["en"]["commands"]["STATUS"]["aliases"].append("cafe\u0301")
            self.write_json(locales, data)
        self.assert_invalid(self.mutate(change), "normalized alias collision")

    def test_mixed_script_write_alias_is_invalid(self):
        def change(_arch, _commands, locales, _state, _witness):
            data = self.load_json(locales)
            data["locales"]["ru"]["commands"]["COMMIT"]["aliases"].append("cоммит")
            self.write_json(locales, data)
        self.assert_invalid(self.mutate(change), "mixed-script alias")

    def test_invisible_unicode_alias_is_invalid(self):
        def change(_arch, _commands, locales, _state, _witness):
            data = self.load_json(locales)
            data["locales"]["en"]["commands"]["HELP"]["aliases"].append("he\u200blp")
            self.write_json(locales, data)
        self.assert_invalid(self.mutate(change), "invisible or control character")

    def test_missing_english_fallback_is_invalid(self):
        def change(_arch, _commands, locales, _state, _witness):
            data = self.load_json(locales)
            data["default_fallback"] = "ru"
            self.write_json(locales, data)
        self.assert_invalid(self.mutate(change), "default_fallback must be en")

    def test_locale_registry_containing_grants_is_invalid(self):
        def change(_arch, _commands, locales, _state, _witness):
            data = self.load_json(locales)
            data["locales"]["en"]["commands"]["HELP"]["grants"] = ["execution"]
            self.write_json(locales, data)
        self.assert_invalid(self.mutate(change), "locale registry must not define grants")

    def test_state_schema_untyped_status_is_invalid(self):
        def change(_arch, _commands, _locales, state, _witness):
            data = self.load_json(state)
            data["properties"]["status"] = {"type": "string"}
            self.write_json(state, data)
        self.assert_invalid(self.mutate(change), "untyped top-level status is forbidden")

    def test_state_schema_generic_authorized_is_invalid(self):
        def change(_arch, _commands, _locales, state, _witness):
            data = self.load_json(state)
            data["properties"]["authorization"]["properties"]["authorized"] = {"const": True}
            self.write_json(state, data)
        self.assert_invalid(self.mutate(change), "generic authorized flag is forbidden")

    def test_pass_setting_approval_is_invalid(self):
        def change(_arch, _commands, _locales, state, _witness):
            data = self.load_json(state)
            data["properties"]["approval"]["properties"]["approval_status"]["enum"].append("PASS")
            self.write_json(state, data)
        self.assert_invalid(self.mutate(change), "PASS must not be an approval status")

    def test_evidence_setting_approval_is_invalid(self):
        def change(_arch, _commands, _locales, state, _witness):
            data = self.load_json(state)
            data["properties"]["approval"]["properties"]["approval_status"]["enum"].append("EVIDENCE")
            self.write_json(state, data)
        self.assert_invalid(self.mutate(change), "Evidence must not be an approval status")

    def test_not_run_treated_as_pass_is_invalid(self):
        def change(_arch, _commands, _locales, state, _witness):
            data = self.load_json(state)
            data["properties"]["validation"]["properties"]["not_run_counts_as_pass"] = {"const": True}
            self.write_json(state, data)
        self.assert_invalid(self.mutate(change), "NOT_RUN must not count as PASS")

    def test_unknown_treated_as_ok_is_invalid(self):
        def change(_arch, _commands, _locales, state, _witness):
            data = self.load_json(state)
            data["properties"]["validation"]["properties"]["unknown_counts_as_ok"] = {"const": True}
            self.write_json(state, data)
        self.assert_invalid(self.mutate(change), "UNKNOWN must not count as OK")

    def test_missing_actor_in_human_witness_is_invalid(self):
        def change(_arch, _commands, _locales, _state, witness):
            data = self.load_json(witness)
            data["required"].remove("actor_reference")
            self.write_json(witness, data)
        self.assert_invalid(self.mutate(change), "actor_reference is required")

    def test_commit_witness_reused_for_push_is_invalid(self):
        def change(_arch, _commands, _locales, _state, witness):
            data = self.load_json(witness)
            data["properties"]["decision_type"]["enum"].append("commit_or_push")
            self.write_json(witness, data)
        self.assert_invalid(self.mutate(change), "decision_type must stay separated")

    def test_expired_witness_allowed_by_schema_is_invalid(self):
        def change(_arch, _commands, _locales, _state, witness):
            data = self.load_json(witness)
            data["properties"]["expired_decision_usable"] = {"const": True}
            self.write_json(witness, data)
        self.assert_invalid(self.mutate(change), "expired decisions must not be usable")

    def test_consumed_single_use_witness_allowed_by_schema_is_invalid(self):
        def change(_arch, _commands, _locales, _state, witness):
            data = self.load_json(witness)
            data["properties"]["consumed_single_use_decision_usable"] = {"const": True}
            self.write_json(witness, data)
        self.assert_invalid(self.mutate(change), "consumed single-use decisions must not be reusable")

    def test_authorized_execution_package_without_human_witness_is_invalid(self):
        def change(_arch, commands, _locales, _state, _witness):
            data = self.load_json(commands)
            execute = next(cmd for cmd in data["commands"] if cmd["command_id"] == "EXECUTE")
            execute["preconditions"].append("controlled_execution_package_authorized_true")
            execute["required_human_decisions"] = []
            self.write_json(commands, data)
        self.assert_invalid(self.mutate(change), "authorized execution package requires Human Decision Witness")

    def test_ui_adapter_declared_as_authority_is_invalid(self):
        def change(arch, _commands, _locales, _state, _witness):
            text = arch.read_text(encoding="utf-8")
            arch.write_text(
                text.replace(
                    "Simple Control Surface | UI adapter | none",
                    "Simple Control Surface | UI adapter | approval authority",
                ),
                encoding="utf-8",
            )
        self.assert_invalid(self.mutate(change), "Simple Control Surface must not be authority")


if __name__ == "__main__":
    unittest.main()
