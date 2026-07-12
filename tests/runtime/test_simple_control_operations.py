import datetime
import hashlib
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from aos.runtime.simple_control_planning import bind_payload


BASELINE = {
    "repository": "NMF13579/AOS-FARM",
    "branch": "build/aos-farm-680-candidate-freeze",
    "head": "b1b9e7bd66db81598e1d02c0db9f4915d2b933af",
}


def digest_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class TestSimpleControlOperations(unittest.TestCase):
    def make_action(self, relative_path, action_type="CREATE_FILE", content="hello", preimage=None):
        expected = {"existence": preimage is not None, "sha256": preimage}
        return {
            "action_id": "action-" + relative_path.replace("/", "-"),
            "action_type": action_type,
            "relative_path": relative_path,
            "expected_preimage": expected,
            "proposed_content": {
                "encoding": "UTF-8",
                "text": content,
                "sha256": digest_text(content),
                "size_bytes": len(content.encode("utf-8")),
            },
            "scope_binding": "scope-binding",
            "reason": "test action",
            "source_reference": "test",
        }

    def make_package(self, actions):
        package = {
            "package_version": 1,
            "package_id": "pkg-test",
            "task_id": "AOS-FARM.681.7",
            "operation_class": "SCOPED_EXECUTION_PREPARATION",
            "request_binding": "request-binding",
            "preview_binding": "preview-binding",
            "authorization_binding": "preview-auth-binding",
            "repository_observation_binding": "observation-binding",
            "repository_baseline_binding": BASELINE,
            "candidate_actions": actions,
            "required_validation": ["operation tests"],
            "mandatory_controls": [{"action": "single-use witness", "removable": False}],
            "execution_backend": {"status": "CONTROLLED_LOCAL_WRITE_BOUND"},
            "production_execution": {"available": True},
            "grants": ["handoff_to_future_controlled_executor"],
            "non_grants": ["commit", "push", "integration", "release", "lifecycle_mutation"],
            "approval": False,
            "evidence_of_success": False,
        }
        package["package_binding"] = bind_payload(package)
        return package

    def make_witness(self, operation_id, package, **overrides):
        from aos.runtime.simple_control_operations import create_production_execution_witness

        witness = create_production_execution_witness(operation_id, package, "human-owner")
        witness.update(overrides)
        return witness

    def test_operation_id_and_binding_conflict(self):
        from aos.runtime.simple_control_operations import (
            OperationError,
            create_operation_id,
            validate_operation_id,
        )

        package = self.make_package([self.make_action("out.txt")])
        operation_id = create_operation_id(package)
        self.assertEqual(operation_id, create_operation_id(package))
        validate_operation_id(operation_id)
        with self.assertRaises(OperationError):
            validate_operation_id("")
        with self.assertRaises(OperationError):
            validate_operation_id("../bad")

        changed = self.make_package([self.make_action("other.txt")])
        self.assertNotEqual(package["package_binding"], changed["package_binding"])

    def test_production_witness_validation(self):
        from aos.runtime.simple_control_operations import (
            OperationError,
            create_operation_id,
            validate_production_witness,
        )

        package = self.make_package([self.make_action("out.txt")])
        operation_id = create_operation_id(package)
        witness = self.make_witness(operation_id, package)
        self.assertTrue(validate_production_witness(witness, operation_id, package))
        self.assertNotIn("commit", witness["grants"])
        self.assertNotIn("production_file_mutation", witness["grants"])

        bad_cases = [
            {"decision_type": "EXECUTION_AUTHORIZATION"},
            {"operation_binding": "other"},
            {"execution_package_binding": "other"},
            {"repository_baseline_binding": {"repository": "wrong", "branch": "x", "head": "y"}},
            {"actor_reference": ""},
            {"consumed_at": "2026-07-13T00:00:00Z"},
            {"grants": ["apply_exact_execution_package_once", "commit"]},
        ]
        for override in bad_cases:
            with self.assertRaises(OperationError, msg=str(override)):
                validate_production_witness(self.make_witness(operation_id, package, **override), operation_id, package)

        expired = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        with self.assertRaises(OperationError):
            validate_production_witness(self.make_witness(operation_id, package, expires_at=expired), operation_id, package)

    def test_create_file_apply_and_completed_retry(self):
        from aos.runtime.simple_control_operations import apply_execution_package, create_operation_id

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = self.make_package([self.make_action("out.txt", content="hello")])
            operation_id = create_operation_id(package)
            witness = self.make_witness(operation_id, package)

            result = apply_execution_package(package, witness, operation_id, root)
            self.assertEqual(result["operation_state"], "OPERATION_COMPLETED")
            self.assertEqual(result["control_state"], "CONTROL_CHANGES_PREPARED")
            self.assertTrue(result["side_effect_verified"])
            self.assertEqual((root / "out.txt").read_text(encoding="utf-8"), "hello")
            self.assertFalse(result["commit_performed"])
            self.assertFalse(result["push_performed"])
            self.assertEqual(result["approval_status"], "NOT_PROVIDED")
            self.assertEqual(result["Evidence_status"], "NOT_RUN")

            retry = apply_execution_package(package, witness, operation_id, root)
            self.assertEqual(retry["reconciliation_result"], "ALREADY_COMPLETED_VERIFIED")
            self.assertFalse(retry["side_effect_repeated"])

    def test_replace_file_apply_preserves_mode_and_blocks_preimage_mismatch(self):
        from aos.runtime.simple_control_operations import OperationError, apply_execution_package, create_operation_id, sha256_file

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "replace.txt"
            target.write_text("old", encoding="utf-8")
            os.chmod(target, 0o640)
            package = self.make_package([self.make_action("replace.txt", "REPLACE_FILE", "new", sha256_file(target))])
            operation_id = create_operation_id(package)
            result = apply_execution_package(package, self.make_witness(operation_id, package), operation_id, root)
            self.assertEqual(result["operation_state"], "OPERATION_COMPLETED")
            self.assertEqual(target.read_text(encoding="utf-8"), "new")
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o640)

            bad = self.make_package([self.make_action("replace.txt", "REPLACE_FILE", "newer", "wrong")])
            with self.assertRaises(OperationError):
                apply_execution_package(bad, self.make_witness(create_operation_id(bad), bad), create_operation_id(bad), root)

    def test_path_safety_and_symlink_blocks(self):
        from aos.runtime.simple_control_operations import OperationError, apply_execution_package, create_operation_id

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for bad in ["/tmp/out", "../out", "00_AOS_Core_Control.md", "aos/templates/execution-packages/x.yaml"]:
                package = self.make_package([self.make_action(bad)])
                operation_id = create_operation_id(package)
                with self.assertRaises(OperationError, msg=bad):
                    apply_execution_package(package, self.make_witness(operation_id, package), operation_id, root)

            (root / "real").mkdir()
            (root / "link").symlink_to(root / "real")
            package = self.make_package([self.make_action("link/out.txt")])
            operation_id = create_operation_id(package)
            with self.assertRaises(OperationError):
                apply_execution_package(package, self.make_witness(operation_id, package), operation_id, root)

    def test_reconciliation_results(self):
        from aos.runtime.simple_control_operations import reconcile_operation

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = self.make_package([self.make_action("one.txt", content="one"), self.make_action("two.txt", content="two")])
            operation_id = "op-" + package["package_binding"][:24]

            self.assertEqual(reconcile_operation(package, operation_id, root)["reconciliation_result"], "SAFE_TO_RETRY")
            (root / "one.txt").write_text("one", encoding="utf-8")
            self.assertEqual(reconcile_operation(package, operation_id, root)["reconciliation_result"], "PARTIALLY_COMPLETED")
            (root / "two.txt").write_text("two", encoding="utf-8")
            self.assertEqual(reconcile_operation(package, operation_id, root)["reconciliation_result"], "ALREADY_COMPLETED_VERIFIED")
            (root / "two.txt").write_text("unexpected", encoding="utf-8")
            self.assertEqual(reconcile_operation(package, operation_id, root)["reconciliation_result"], "UNKNOWN_BLOCKED")

    def test_multi_action_partial_failure_records_completed_action(self):
        from aos.runtime.simple_control_operations import apply_execution_package, create_operation_id

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = self.make_package([
                self.make_action("a.txt", content="a"),
                self.make_action("b.txt", content="b"),
            ])
            operation_id = create_operation_id(package)
            from aos.runtime import simple_control_operations as ops

            real_apply = ops.apply_action

            def fail_second(repository_root, action):
                if action["relative_path"] == "b.txt":
                    raise ops.OperationError("injected post-precondition failure")
                return real_apply(repository_root, action)

            with mock.patch("aos.runtime.simple_control_operations.apply_action", side_effect=fail_second):
                result = apply_execution_package(package, self.make_witness(operation_id, package), operation_id, root)
            self.assertEqual(result["operation_state"], "OPERATION_RECONCILIATION_REQUIRED")
            self.assertFalse(result["rollback_available"])
            self.assertEqual(result["completed_actions"], ["action-a.txt"])
            self.assertTrue((root / "a.txt").exists())

    def test_active_repository_apply_guard(self):
        from aos.runtime.simple_control_operations import OperationError, active_repository_root, apply_execution_package, create_operation_id

        package = self.make_package([self.make_action("should-not-write.txt")])
        operation_id = create_operation_id(package)
        with self.assertRaises(OperationError):
            apply_execution_package(package, self.make_witness(operation_id, package), operation_id, active_repository_root())


if __name__ == "__main__":
    unittest.main()
