import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


MODULE_PATH = os.path.join("aos", "scripts", "aos_integration_contract_check.py")
SPEC = importlib.util.spec_from_file_location("aos_integration_contract_check", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


REQUIRED_CHECKS = [
    "aos-integration / candidate-binding",
    "aos-integration / contract",
    "aos-integration / focused-tests",
    "aos-integration / full-pytest",
    "aos-integration / protected-paths",
    "aos-integration / semantic-guard",
]


class IntegrationContractFixture:
    def __init__(self, test_case):
        self.test_case = test_case
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self._git(["init", "-b", "dev"])
        self._git(["config", "user.name", "Test User"])
        self._git(["config", "user.email", "test@example.invalid"])
        (self.root / "README.md").write_text("base\n", encoding="utf-8")
        self._git(["add", "README.md"])
        self._git(["commit", "-m", "base"])
        self.target_oid = self._git(["rev-parse", "HEAD"])
        self._git(["checkout", "-b", "build/test"])
        (self.root / "src").mkdir()
        (self.root / "src" / "feature.txt").write_text("feature\n", encoding="utf-8")
        self._git(["add", "src/feature.txt"])
        self._git(["commit", "-m", "feature"])
        self.source_oid = self._git(["rev-parse", "HEAD"])
        self.parent_oid = self._git(["rev-parse", "HEAD^"])
        self.tree_oid = self._git(["rev-parse", "HEAD^{tree}"])
        self.remote_url = "git@github.com:NMF13579/AOS-FARM.git"
        self._git(["remote", "add", "origin", self.remote_url])

    def cleanup(self):
        self.tmp.cleanup()

    def _git(self, args, check=True):
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=check,
        )
        return result.stdout.strip()

    def sha256_from_source(self, path):
        result = subprocess.run(
            ["git", "show", f"{self.source_oid}:{path}"],
            cwd=self.root,
            capture_output=True,
            check=True,
        )
        return hashlib.sha256(result.stdout).hexdigest()

    def base_contract(self):
        files = [
            {
                "path": "src/feature.txt",
                "state": "ADDED",
                "mode": "100644",
                "sha256": self.sha256_from_source("src/feature.txt"),
            }
        ]
        contract = {
            "schema_version": 1,
            "contract_type": "AOS_INTEGRATION_CONTRACT",
            "task_id": "AOS-FARM.681",
            "repository": {
                "identity": "NMF13579/AOS-FARM",
                "remote_url": self.remote_url,
            },
            "source": {
                "branch": "build/test",
                "commit_oid": self.source_oid,
                "parent_oid": self.parent_oid,
                "tree_oid": self.tree_oid,
            },
            "target": {
                "branch": "dev",
                "expected_head_oid": self.target_oid,
            },
            "candidate": {
                "manifest_binding": MODULE.compute_candidate_manifest_binding(
                    "NMF13579/AOS-FARM",
                    self.source_oid,
                    self.tree_oid,
                    files,
                ),
                "files": files,
            },
            "integration": {
                "method": "GITHUB_PR_MERGE_COMMIT",
                "exact_commit_preservation": "REQUIRED_AS_MERGE_PARENT_OR_ANCESTOR",
                "target_must_be_current": True,
            },
            "check_policy": {
                "policy_version": 1,
                "required_checks": list(REQUIRED_CHECKS),
                "advisory_checks": ["aos-integration / future-platform-audit"],
            },
            "invalidation": {
                "source_commit_change": True,
                "target_head_change": True,
                "candidate_manifest_change": True,
                "check_policy_change": True,
                "integration_method_change": True,
            },
            "authorization_boundary": {
                "contract_is_approval": False,
                "integration_authorized": False,
                "merge_authorized": False,
                "release_authorized": False,
                "human_decision_required": True,
            },
        }
        binding = MODULE.compute_contract_binding(contract)
        contract["contract_id"] = "integration-" + binding[:16]
        contract["contract_binding"] = binding
        return contract

    def write_contract(self, contract, name="valid.yaml"):
        contract_dir = self.root / "aos" / "integration" / "contracts"
        contract_dir.mkdir(parents=True, exist_ok=True)
        path = contract_dir / name
        path.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self._git(["add", path.relative_to(self.root).as_posix()])
        return path.relative_to(self.root).as_posix()

    def run_checker(self, contract_path, source_oid=None, target_oid=None):
        argv = [
            "aos_integration_contract_check.py",
            "--contract",
            contract_path,
            "--repository-root",
            str(self.root),
            "--observed-source-oid",
            source_oid or self.source_oid,
            "--observed-target-oid",
            target_oid or self.target_oid,
            "--json",
        ]
        buf = io.StringIO()
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(buf):
            try:
                MODULE.main()
            except SystemExit as exc:
                exit_code = exc.code
        return exit_code, json.loads(buf.getvalue())


class TestAosIntegrationContractCheck(unittest.TestCase):
    def setUp(self):
        self.fixture = IntegrationContractFixture(self)

    def tearDown(self):
        self.fixture.cleanup()

    def test_deterministic_contract_construction_excludes_derived_fields(self):
        contract = self.fixture.base_contract()
        expected_binding = contract["contract_binding"]
        expected_id = contract["contract_id"]

        self.assertEqual(MODULE.compute_contract_binding(contract), expected_binding)
        self.assertEqual(MODULE.expected_contract_id(expected_binding), expected_id)
        payload = MODULE.contract_binding_payload(contract)
        self.assertNotIn("contract_id", payload)
        self.assertNotIn("contract_binding", payload)
        self.assertFalse(MODULE.FIXED_POINT_SEARCH_USED)

        reordered = json.loads(json.dumps(contract))
        reordered = {key: reordered[key] for key in reversed(list(reordered.keys()))}
        self.assertEqual(MODULE.compute_contract_binding(reordered), expected_binding)
        self.assertEqual(MODULE.expected_contract_id(expected_binding), expected_id)

    def test_valid_tracked_json_compatible_yaml_contract_passes_without_approval(self):
        contract = self.fixture.base_contract()
        path = self.fixture.write_contract(contract, "valid.yaml")

        exit_code, result = self.fixture.run_checker(path)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["final_status"], "PASS")
        self.assertEqual(result["reason_code"], "INTEGRATION_CONTRACT_VALID")
        self.assertTrue(result["technical_contract_valid"])
        self.assertTrue(result["contract_binding_verified"])
        self.assertTrue(result["contract_id_verified"])
        self.assertFalse(result["approval_granted"])
        self.assertFalse(result["integration_authorized"])
        self.assertFalse(result["merge_authorized"])
        self.assertFalse(result["release_authorized"])
        self.assertEqual(result["claim_ceiling"], "ADVISORY_VALIDATED_DURABLE_INTEGRATION_CONTRACT")
        self.assertEqual(result["candidate_file_count"], 1)
        self.assertEqual(result["protected_paths"], [])
        self.assertNotIn(str(self.fixture.root), json.dumps(result))

    def test_valid_tracked_json_contract_passes(self):
        contract = self.fixture.base_contract()
        path = self.fixture.write_contract(contract, "valid.json")

        exit_code, result = self.fixture.run_checker(path)

        self.assertEqual(exit_code, 0)
        self.assertEqual(result["final_status"], "PASS")
        self.assertEqual(result["contract_path"], path)

    def test_binding_and_id_mismatches_block(self):
        cases = [
            ("bad-binding.yaml", {"contract_binding": "0" * 64}, "CONTRACT_BINDING_MISMATCH"),
            ("bad-id.yaml", {"contract_id": "integration-0000000000000000"}, "CONTRACT_ID_BINDING_MISMATCH"),
            ("upper-binding.yaml", {"contract_binding": "A" * 64}, "CONTRACT_BINDING_MISMATCH"),
            ("short-binding.yaml", {"contract_binding": "a" * 63}, "CONTRACT_BINDING_MISMATCH"),
            ("bad-prefix.yaml", {"contract_id": "candidate-abcdefabcdefabcd"}, "CONTRACT_ID_BINDING_MISMATCH"),
        ]
        for name, updates, reason in cases:
            with self.subTest(name=name):
                contract = self.fixture.base_contract()
                contract.update(updates)
                path = self.fixture.write_contract(contract, name)
                exit_code, result = self.fixture.run_checker(path)
                self.assertEqual(exit_code, 2)
                self.assertEqual(result["final_status"], "BLOCKED")
                self.assertEqual(result["reason_code"], reason)
                self.assertFalse(result["technical_contract_valid"])

    def test_rejects_binding_algorithms_that_include_derived_fields(self):
        contract = self.fixture.base_contract()
        payload_with_id = copy.deepcopy(contract)
        payload_with_id.pop("contract_binding")
        binding_with_id = MODULE.canonical_sha256(payload_with_id)
        payload_with_binding = copy.deepcopy(contract)
        payload_with_binding.pop("contract_id")
        binding_with_binding = MODULE.canonical_sha256(payload_with_binding)

        for name, bad_binding in [
            ("binding-includes-id.yaml", binding_with_id),
            ("binding-includes-binding.yaml", binding_with_binding),
            ("candidate-derived-id.yaml", contract["candidate"]["manifest_binding"]),
        ]:
            with self.subTest(name=name):
                mutated = self.fixture.base_contract()
                if name == "candidate-derived-id.yaml":
                    mutated["contract_id"] = "integration-" + bad_binding[:16]
                else:
                    mutated["contract_binding"] = bad_binding
                    mutated["contract_id"] = "integration-" + bad_binding[:16]
                path = self.fixture.write_contract(mutated, name)
                exit_code, result = self.fixture.run_checker(path)
                self.assertEqual(exit_code, 2)
                self.assertIn(result["reason_code"], {"CONTRACT_BINDING_MISMATCH", "CONTRACT_ID_BINDING_MISMATCH"})

    def test_authoritative_field_mutations_invalidate_binding(self):
        mutations = {
            "repository identity": lambda c: c["repository"].update({"identity": "Other/Repo"}),
            "remote URL": lambda c: c["repository"].update({"remote_url": "git@example.invalid:Other/Repo.git"}),
            "source commit": lambda c: c["source"].update({"commit_oid": "1" * 40}),
            "source parent": lambda c: c["source"].update({"parent_oid": "2" * 40}),
            "source tree": lambda c: c["source"].update({"tree_oid": "3" * 40}),
            "target head": lambda c: c["target"].update({"expected_head_oid": "4" * 40}),
            "candidate manifest": lambda c: c["candidate"].update({"manifest_binding": "5" * 64}),
            "candidate path": lambda c: c["candidate"]["files"][0].update({"path": "src/other.txt"}),
            "candidate sha": lambda c: c["candidate"]["files"][0].update({"sha256": "6" * 64}),
            "candidate state": lambda c: c["candidate"]["files"][0].update({"state": "MODIFIED"}),
            "candidate mode": lambda c: c["candidate"]["files"][0].update({"mode": "100755"}),
            "integration method": lambda c: c["integration"].update({"method": "LOCAL_MERGE"}),
            "preservation": lambda c: c["integration"].update({"exact_commit_preservation": "OPTIONAL"}),
            "required checks": lambda c: c["check_policy"]["required_checks"].append("z-extra"),
            "advisory checks": lambda c: c["check_policy"]["advisory_checks"].append("z-advisory"),
            "invalidation policy": lambda c: c["invalidation"].update({"target_head_change": False}),
            "authorization boundary": lambda c: c["authorization_boundary"].update({"human_decision_required": False}),
            "task id": lambda c: c.update({"task_id": "AOS-FARM.999"}),
        }
        original = self.fixture.base_contract()
        original_binding = original["contract_binding"]
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                changed = copy.deepcopy(original)
                mutate(changed)
                self.assertNotEqual(MODULE.compute_contract_binding(changed), original_binding)

    def test_path_safety_and_parser_fail_closed(self):
        contract = self.fixture.base_contract()
        valid_path = self.fixture.write_contract(contract, "valid.yaml")
        active = self.fixture.root / valid_path
        untracked = self.fixture.root / "aos" / "integration" / "contracts" / "untracked.yaml"
        untracked.write_text(active.read_text(encoding="utf-8"), encoding="utf-8")
        template = self.fixture.root / "aos" / "templates" / "execution-artifacts" / "template.yaml"
        template.parent.mkdir(parents=True)
        template.write_text(active.read_text(encoding="utf-8"), encoding="utf-8")
        directory = self.fixture.root / "aos" / "integration" / "contracts" / "directory"
        directory.mkdir()
        symlink = self.fixture.root / "aos" / "integration" / "contracts" / "link.yaml"
        symlink.symlink_to(active)

        cases = [
            str(active),
            "../outside.yaml",
            ".aos-tmp/contract.yaml",
            "aos/templates/execution-artifacts/template.yaml",
            "aos/integration/contracts/missing.yaml",
            "aos/integration/contracts/untracked.yaml",
            "aos/integration/contracts/directory",
            "aos/integration/contracts/link.yaml",
        ]
        for path_value in cases:
            with self.subTest(path_value=path_value):
                exit_code, result = self.fixture.run_checker(path_value)
                self.assertEqual(exit_code, 2)
                self.assertEqual(result["final_status"], "UNKNOWN_BLOCKED")
                self.assertEqual(result["reason_code"], "INTEGRATION_CONTRACT_PATH_INVALID")

    def test_duplicate_keys_and_unknown_fields_block(self):
        path = self.fixture.root / "aos" / "integration" / "contracts" / "duplicate.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"schema_version":1,"schema_version":1}\n', encoding="utf-8")
        self.fixture._git(["add", path.relative_to(self.fixture.root).as_posix()])
        exit_code, result = self.fixture.run_checker(path.relative_to(self.fixture.root).as_posix())
        self.assertEqual(exit_code, 2)
        self.assertEqual(result["final_status"], "UNKNOWN_BLOCKED")

        contract = self.fixture.base_contract()
        contract["unexpected"] = True
        path = self.fixture.write_contract(contract, "unknown.yaml")
        exit_code, result = self.fixture.run_checker(path)
        self.assertEqual(exit_code, 2)
        self.assertEqual(result["reason_code"], "CONTRACT_SCHEMA_INVALID")

    def test_observation_and_git_semantic_mismatches_block(self):
        contract = self.fixture.base_contract()
        cases = [
            ("stale-source.yaml", contract, "0" * 40, self.fixture.target_oid, "SOURCE_COMMIT_STALE"),
            ("stale-target.yaml", contract, self.fixture.source_oid, "0" * 40, "TARGET_HEAD_STALE"),
        ]
        for name, candidate, source, target, reason in cases:
            with self.subTest(name=name):
                path = self.fixture.write_contract(copy.deepcopy(candidate), name)
                exit_code, result = self.fixture.run_checker(path, source, target)
                self.assertEqual(exit_code, 2)
                self.assertEqual(result["final_status"], "BLOCKED")
                self.assertEqual(result["reason_code"], reason)

        semantic_cases = [
            ("wrong-parent.yaml", lambda c: c["source"].update({"parent_oid": "1" * 40}), "SOURCE_PARENT_MISMATCH"),
            ("wrong-tree.yaml", lambda c: c["source"].update({"tree_oid": "2" * 40}), "SOURCE_TREE_MISMATCH"),
            ("not-descendant.yaml", lambda c: c["target"].update({"expected_head_oid": self.fixture.source_oid}), "SOURCE_TARGET_RELATION_INVALID"),
            ("wrong-branch.yaml", lambda c: c["source"].update({"branch": "feature/test"}), "SOURCE_BRANCH_INVALID"),
            ("wrong-target-branch.yaml", lambda c: c["target"].update({"branch": "main"}), "TARGET_BRANCH_INVALID"),
        ]
        for name, mutate, reason in semantic_cases:
            with self.subTest(name=name):
                candidate = self.fixture.base_contract()
                mutate(candidate)
                binding = MODULE.compute_contract_binding(candidate)
                candidate["contract_binding"] = binding
                candidate["contract_id"] = MODULE.expected_contract_id(binding)
                path = self.fixture.write_contract(candidate, name)
                exit_code, result = self.fixture.run_checker(path, target_oid=candidate["target"]["expected_head_oid"])
                self.assertEqual(exit_code, 2)
                self.assertEqual(result["reason_code"], reason)

    def test_non_ancestor_source_is_blocked_not_unknown(self):
        self.fixture._git(["checkout", "dev"])
        (self.fixture.root / "target-new.txt").write_text("target\n", encoding="utf-8")
        self.fixture._git(["add", "target-new.txt"])
        self.fixture._git(["commit", "-m", "target moves"])
        moved_target_oid = self.fixture._git(["rev-parse", "HEAD"])

        contract = self.fixture.base_contract()
        contract["target"]["expected_head_oid"] = moved_target_oid
        binding = MODULE.compute_contract_binding(contract)
        contract["contract_binding"] = binding
        contract["contract_id"] = MODULE.expected_contract_id(binding)
        path = self.fixture.write_contract(contract, "source-not-fresh.yaml")

        exit_code, result = self.fixture.run_checker(path, target_oid=moved_target_oid)

        self.assertEqual(exit_code, 2)
        self.assertEqual(result["final_status"], "BLOCKED")
        self.assertEqual(result["reason_code"], "SOURCE_NOT_FRESH")

    def test_merge_base_ancestor_return_codes_are_classified(self):
        with mock.patch("subprocess.run", return_value=mock.Mock(returncode=0, stderr="", stdout="")):
            MODULE.check_target_is_ancestor(self.fixture.root, self.fixture.target_oid, self.fixture.source_oid)

        with mock.patch("subprocess.run", return_value=mock.Mock(returncode=1, stderr="", stdout="")):
            with self.assertRaises(MODULE.ContractError) as ctx:
                MODULE.check_target_is_ancestor(self.fixture.root, self.fixture.target_oid, self.fixture.source_oid)
            self.assertEqual(ctx.exception.status, MODULE.BLOCKED)
            self.assertEqual(ctx.exception.reason, "SOURCE_NOT_FRESH")

        with mock.patch("subprocess.run", return_value=mock.Mock(returncode=128, stderr="fatal: bad object", stdout="")):
            with self.assertRaises(MODULE.ContractError) as ctx:
                MODULE.check_target_is_ancestor(self.fixture.root, self.fixture.target_oid, self.fixture.source_oid)
            self.assertEqual(ctx.exception.status, MODULE.UNKNOWN_BLOCKED)
            self.assertEqual(ctx.exception.reason, "GIT_OBSERVATION_ERROR")

    def test_candidate_manifest_and_file_semantics(self):
        cases = [
            ("duplicate-path.yaml", lambda c: c["candidate"]["files"].append(copy.deepcopy(c["candidate"]["files"][0])), "CANDIDATE_FILES_INVALID", False),
            ("unsorted.yaml", lambda c: c["candidate"]["files"].append({"path": "aaa.txt", "state": "ADDED", "mode": "100644", "sha256": "a" * 64}), "CANDIDATE_FILES_INVALID", False),
            ("unsafe.yaml", lambda c: c["candidate"]["files"][0].update({"path": ".git/config"}), "CANDIDATE_FILES_INVALID", False),
            ("manifest.yaml", lambda c: c["candidate"].update({"manifest_binding": "0" * 64}), "CANDIDATE_MANIFEST_BINDING_MISMATCH", False),
            ("mode.yaml", lambda c: c["candidate"]["files"][0].update({"mode": "100755"}), "CANDIDATE_DIFF_MISMATCH", True),
            ("sha.yaml", lambda c: c["candidate"]["files"][0].update({"sha256": "0" * 64}), "CANDIDATE_DIFF_MISMATCH", True),
        ]
        for name, mutate, reason, recompute_manifest in cases:
            with self.subTest(name=name):
                contract = self.fixture.base_contract()
                mutate(contract)
                if recompute_manifest:
                    contract["candidate"]["manifest_binding"] = MODULE.compute_candidate_manifest_binding(
                        "NMF13579/AOS-FARM",
                        contract["source"]["commit_oid"],
                        contract["source"]["tree_oid"],
                        contract["candidate"]["files"],
                    )
                binding = MODULE.compute_contract_binding(contract)
                contract["contract_binding"] = binding
                contract["contract_id"] = MODULE.expected_contract_id(binding)
                path = self.fixture.write_contract(contract, name)
                exit_code, result = self.fixture.run_checker(path)
                self.assertEqual(exit_code, 2)
                self.assertEqual(result["reason_code"], reason)

    def test_required_check_policy_and_illegal_authorization_claims_block(self):
        cases = [
            ("missing-check.yaml", lambda c: c["check_policy"]["required_checks"].pop(), "CHECK_POLICY_INVALID"),
            ("renamed-check.yaml", lambda c: c["check_policy"]["required_checks"].__setitem__(0, "renamed"), "CHECK_POLICY_INVALID"),
            ("duplicate-check.yaml", lambda c: c["check_policy"]["required_checks"].append(c["check_policy"]["required_checks"][0]), "CHECK_POLICY_INVALID"),
            ("overlap.yaml", lambda c: c["check_policy"]["advisory_checks"].append(c["check_policy"]["required_checks"][0]), "CHECK_POLICY_INVALID"),
            ("approval.yaml", lambda c: c["authorization_boundary"].update({"contract_is_approval": True}), "CONTRACT_ILLEGAL_AUTHORIZATION_CLAIM"),
            ("integration.yaml", lambda c: c["authorization_boundary"].update({"integration_authorized": True}), "CONTRACT_ILLEGAL_AUTHORIZATION_CLAIM"),
            ("merge.yaml", lambda c: c["authorization_boundary"].update({"merge_authorized": True}), "CONTRACT_ILLEGAL_AUTHORIZATION_CLAIM"),
            ("release.yaml", lambda c: c["authorization_boundary"].update({"release_authorized": True}), "CONTRACT_ILLEGAL_AUTHORIZATION_CLAIM"),
            ("human.yaml", lambda c: c["authorization_boundary"].update({"human_decision_required": False}), "CONTRACT_ILLEGAL_AUTHORIZATION_CLAIM"),
        ]
        for name, mutate, reason in cases:
            with self.subTest(name=name):
                contract = self.fixture.base_contract()
                mutate(contract)
                binding = MODULE.compute_contract_binding(contract)
                contract["contract_binding"] = binding
                contract["contract_id"] = MODULE.expected_contract_id(binding)
                path = self.fixture.write_contract(contract, name)
                exit_code, result = self.fixture.run_checker(path)
                self.assertEqual(exit_code, 2)
                self.assertEqual(result["reason_code"], reason)

    def test_protected_path_requires_human_review(self):
        protected = self.fixture.root / "00_AOS_Core_Control.md"
        protected.write_text("protected\n", encoding="utf-8")
        self.fixture._git(["add", "00_AOS_Core_Control.md"])
        self.fixture._git(["commit", "-m", "protected"])
        source_oid = self.fixture._git(["rev-parse", "HEAD"])
        parent_oid = self.fixture._git(["rev-parse", "HEAD^"])
        tree_oid = self.fixture._git(["rev-parse", "HEAD^{tree}"])
        contract = self.fixture.base_contract()
        files = [{
            "path": "00_AOS_Core_Control.md",
            "state": "ADDED",
            "mode": "100644",
            "sha256": hashlib.sha256(b"protected\n").hexdigest(),
        }]
        contract["source"].update({"commit_oid": source_oid, "parent_oid": parent_oid, "tree_oid": tree_oid})
        contract["candidate"]["files"] = files
        contract["candidate"]["manifest_binding"] = MODULE.compute_candidate_manifest_binding(
            "NMF13579/AOS-FARM", source_oid, tree_oid, files
        )
        binding = MODULE.compute_contract_binding(contract)
        contract["contract_binding"] = binding
        contract["contract_id"] = MODULE.expected_contract_id(binding)
        path = self.fixture.write_contract(contract, "protected.yaml")

        exit_code, result = self.fixture.run_checker(path, source_oid=source_oid)

        self.assertEqual(exit_code, 3)
        self.assertEqual(result["final_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(result["reason_code"], "PROTECTED_PATH_INTEGRATION_REVIEW_REQUIRED")
        self.assertTrue(result["technical_contract_valid"])
        self.assertEqual(result["protected_paths"], ["00_AOS_Core_Control.md"])
        self.assertFalse(result["integration_authorized"])

    def test_help_has_no_side_effects(self):
        buf = io.StringIO()
        with mock.patch.object(MODULE, "validate_contract") as validate_contract, \
             mock.patch.object(sys, "argv", ["aos_integration_contract_check.py", "--help"]), \
             self.assertRaises(SystemExit) as raised, \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("--contract", buf.getvalue())
        validate_contract.assert_not_called()


if __name__ == "__main__":
    unittest.main()
