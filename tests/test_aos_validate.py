import unittest
import json
import subprocess
import os
import contextlib
import importlib.util
import io
import sys
from unittest import mock


MODULE_PATH = os.path.join("aos", "scripts", "aos_validate.py")
sys.path.insert(0, os.path.abspath(os.path.join("aos", "scripts")))
SPEC = importlib.util.spec_from_file_location("aos_validate_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

class TestAosValidate(unittest.TestCase):
    def assertAggregateNotPass(self, result):
        self.assertNotEqual(MODULE.determine_overall_status([result]), "PASS")

    def test_nested_human_review_required_blocks_overall_pass(self):
        self.assertAggregateNotPass({
            "status": "PASS",
            "return_code": 0,
            "stdout": "Final Status: HUMAN_REVIEW_REQUIRED",
            "stderr": "",
        })

    def test_nested_unknown_blocked_blocks_overall_pass(self):
        self.assertAggregateNotPass({
            "status": "PASS",
            "return_code": 0,
            "stdout": "Final Status: UNKNOWN_BLOCKED",
            "stderr": "",
        })

    def test_nested_blocked_blocks_overall_pass(self):
        self.assertAggregateNotPass({
            "status": "PASS",
            "return_code": 0,
            "stdout": "Final Status: BLOCKED",
            "stderr": "",
        })

    def test_required_not_run_blocks_overall_pass(self):
        self.assertAggregateNotPass({
            "status": "NOT_RUN",
            "reason": "required child check not available",
        })

    def test_unknown_nested_status_blocks_overall_pass(self):
        self.assertAggregateNotPass({
            "status": "PASS",
            "return_code": 0,
            "stdout": "Final Status: SURPRISE_STATUS",
            "stderr": "",
        })

    def test_malformed_child_status_blocks_overall_pass(self):
        self.assertAggregateNotPass({
            "status": "",
            "return_code": 0,
            "stdout": "Final Status:",
            "stderr": "",
        })

    def test_child_non_zero_exit_blocks_overall_pass(self):
        self.assertAggregateNotPass({
            "status": "FAILED",
            "return_code": 1,
            "stdout": "Final Status: PASS",
            "stderr": "",
        })

    def test_all_required_checks_pass_aggregates_pass(self):
        overall = MODULE.determine_overall_status([
            {"status": "PASS", "return_code": 0, "stdout": "Final Status: PASS", "stderr": ""},
            {"status": "PASS", "return_code": 0, "stdout": "", "stderr": ""},
        ])
        self.assertEqual(overall, "PASS")

    def test_aos_validate_orchestration_only(self):
        # ensure it runs without error and outputs correct boundary fields
        try:
            result = subprocess.run(
                ["python3", "aos/scripts/aos_validate.py", "all", "--json"],
                capture_output=True,
                text=True,
                timeout=20,
            )
        except subprocess.TimeoutExpired as exc:
            self.fail(f"aos_validate.py timed out: {exc}")
        self.assertEqual(result.returncode, 0, msg=f"aos_validate failed: {result.stderr}")
        
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
        self.assertFalse(data.get("approval_claimed"))
        self.assertFalse(data.get("commit_authorized"))
        self.assertFalse(data.get("push_authorized"))
        self.assertFalse(data.get("release_authorized"))
        
        self.assertIn("results", data)
        self.assertTrue(isinstance(data["results"], list))
        self.assertTrue(len(data["results"]) > 0)
        self.assertIn("readiness_audit", data)
        self.assertIn("counts", data["readiness_audit"])

    def test_architecture_integration_in_json(self):
        result = subprocess.run(
            ["python3", "aos/scripts/aos_validate.py", "all", "--json"],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        
        # Check architecture is included
        arch_results = [r for r in data["results"] if r.get("command") == "aos_architecture_document_check.get_validate_all_report"]
        self.assertEqual(len(arch_results), 1)
        arch = arch_results[0]
        
        self.assertIn(arch.get("status"), ["PASS", "NOT_RUN", "UNKNOWN_BLOCKED", "BLOCKED", "FAILED", "CONFLICT_BLOCKED", "HUMAN_REVIEW_REQUIRED"])
        self.assertFalse(arch.get("approval_claimed"))
        self.assertFalse(arch.get("execution_authorized", False))
        self.assertFalse(arch.get("implementation_authorized", False))
        self.assertFalse(arch.get("release_authorized", False))
        
        # ensure not_run or unknown_blocked is not passed
        self.assertNotEqual(data.get("overall_status"), "UNKNOWN")

    def test_architecture_integration_no_recursion(self):
        with open("aos/scripts/aos_validate.py", "r") as f:
            content = f.read()
        
        self.assertNotIn("subprocess.run(['python3', 'aos/scripts/aos_architecture_document_check.py', 'validate-all'])", content)
        self.assertNotIn('subprocess.run(["python3", "aos/scripts/aos_architecture_document_check.py", "validate-all"])', content)
        
        # the integration should just call the imported function
        self.assertIn("aos_architecture_document_check.get_validate_all_report()", content)

    def test_malformed_exclusion_blocks_overall_pass(self):
        readiness_audit = {
            "status": "UNKNOWN_BLOCKED",
            "counts": {
                "active_ready_count": 0,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 1,
            },
            "active_blockers": [],
            "excluded_terminal_tasks": [],
            "excluded_legacy_tasks": [],
            "malformed_exclusions": [{"task_id": "AOS-FARM-TASK-9999", "readiness": "MALFORMED_EXCLUSION"}],
            "tasks": [],
            "explicit_not_pass_statement": [
                "EXCLUDED_TERMINAL is not PASS",
                "EXCLUDED_LEGACY is not PASS",
                "MALFORMED_EXCLUSION is blocker state",
            ],
        }
        arch_report = {"status": "PASS"}
        buf = io.StringIO()
        with mock.patch.object(MODULE, "VALIDATION_COMMANDS", []), \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value=arch_report), \
             mock.patch("sys.argv", ["aos_validate.py", "--json"]), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        self.assertEqual(data["overall_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(data["readiness_audit"]["counts"]["malformed_exclusion_count"], 1)

    def test_pass_requires_no_active_blockers_in_structured_readiness_output(self):
        readiness_audit = {
            "status": "BLOCKED",
            "counts": {
                "active_ready_count": 1,
                "active_blocked_count": 1,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 1,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
            "active_blockers": [{"task_id": "AOS-FARM-TASK-9998", "readiness": "BLOCKED"}],
            "excluded_terminal_tasks": [{"task_id": "AOS-FARM-TASK-9997", "readiness": "EXCLUDED_TERMINAL"}],
            "excluded_legacy_tasks": [],
            "malformed_exclusions": [],
            "tasks": [],
            "explicit_not_pass_statement": [
                "EXCLUDED_TERMINAL is not PASS",
                "EXCLUDED_LEGACY is not PASS",
                "MALFORMED_EXCLUSION is blocker state",
            ],
        }
        buf = io.StringIO()
        with mock.patch.object(MODULE, "VALIDATION_COMMANDS", []), \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "--json"]), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        self.assertEqual(data["overall_status"], "BLOCKED")
        self.assertEqual(data["readiness_audit"]["counts"]["active_blocked_count"], 1)

    def test_process_exit_status_uses_process_only_labels(self):
        self.assertEqual(MODULE.process_exit_status(0), "EXIT_ZERO")
        self.assertEqual(MODULE.process_exit_status(1), "EXIT_NON_ZERO")
        self.assertEqual(MODULE.process_exit_status(None), "NOT_RUN")
        self.assertEqual(MODULE.process_exit_status(process_error="timeout"), "TIMEOUT")
        self.assertEqual(MODULE.process_exit_status(process_error="error"), "PROCESS_ERROR")
        self.assertNotEqual(MODULE.process_exit_status(0), "PASS")

    def test_readiness_nonzero_exit_preserves_human_review_required(self):
        normalized = MODULE.normalize_child_result({
            "command": "python3 aos/scripts/aos_task_document_check.py task --readiness-all",
            "status": "FAILED",
            "return_code": 1,
            "process_exit_status": "EXIT_NON_ZERO",
            "stdout": "status: HUMAN_REVIEW_REQUIRED\nactive_human_review_required_count: 1",
            "stderr": "",
        })
        self.assertEqual(normalized, "HUMAN_REVIEW_REQUIRED")
        self.assertNotEqual(normalized, "FAIL")
        self.assertNotEqual(normalized, "PASS")

    def test_readiness_nonzero_exit_preserves_unknown_blocked(self):
        normalized = MODULE.normalize_child_result({
            "command": "python3 aos/scripts/aos_task_document_check.py task --readiness-all",
            "status": "FAILED",
            "return_code": 1,
            "process_exit_status": "EXIT_NON_ZERO",
            "stdout": "status: UNKNOWN_BLOCKED\nmalformed_exclusion_count: 1",
            "stderr": "",
        })
        self.assertEqual(normalized, "UNKNOWN_BLOCKED")
        self.assertNotEqual(normalized, "PASS")

    def test_non_readiness_nonzero_pass_output_stays_structural_fail(self):
        normalized = MODULE.normalize_child_result({
            "command": "python3 aos/scripts/some_other_check.py",
            "status": "PASS",
            "return_code": 1,
            "process_exit_status": "EXIT_NON_ZERO",
            "stdout": "Final Status: PASS",
            "stderr": "",
        })
        self.assertEqual(normalized, "FAIL")
        self.assertNotEqual(normalized, "HUMAN_REVIEW_REQUIRED")

    def test_process_error_is_not_relabelled_human_review_required(self):
        normalized = MODULE.normalize_child_result({
            "command": "python3 aos/scripts/aos_task_document_check.py task --readiness-all",
            "status": "NOT_RUN",
            "return_code": None,
            "process_exit_status": "PROCESS_ERROR",
            "stdout": "status: HUMAN_REVIEW_REQUIRED",
            "stderr": "",
        })
        self.assertEqual(normalized, "FAIL")
        self.assertNotEqual(normalized, "HUMAN_REVIEW_REQUIRED")

    def test_dashboard_readiness_excluded_legacy_does_not_poison_aggregate_status(self):
        normalized = MODULE.normalize_child_result({
            "command": "python3 aos/scripts/aos_queue_dashboard.py",
            "status": "PASS",
            "return_code": 0,
            "process_exit_status": "EXIT_ZERO",
            "stdout": "Readiness: EXCLUDED_LEGACY",
            "stderr": "",
        })
        self.assertEqual(normalized, "PASS")

    def test_excluded_legacy_does_not_normalize_to_pass(self):
        self.assertEqual(MODULE.normalize_status("EXCLUDED_LEGACY"), "UNKNOWN_BLOCKED")
        self.assertNotEqual(MODULE.normalize_status("EXCLUDED_LEGACY"), "PASS")

    def test_human_review_required_does_not_normalize_to_pass(self):
        self.assertEqual(MODULE.normalize_status("HUMAN_REVIEW_REQUIRED"), "HUMAN_REVIEW_REQUIRED")
        self.assertNotEqual(MODULE.normalize_status("HUMAN_REVIEW_REQUIRED"), "PASS")

    def test_unknown_actual_validation_child_status_still_fails_closed(self):
        normalized = MODULE.normalize_child_result({
            "command": "python3 aos/scripts/some_actual_validator.py",
            "status": "PASS",
            "return_code": 0,
            "process_exit_status": "EXIT_ZERO",
            "stdout": "Final Status: SURPRISE_STATUS",
            "stderr": "",
        })
        self.assertEqual(normalized, "UNKNOWN_BLOCKED")

    def test_readiness_human_review_blocks_overall_pass_in_json_report(self):
        readiness_audit = {
            "status": "HUMAN_REVIEW_REQUIRED",
            "readiness_inventory": {
                "active_ready_count": 0,
                "active_human_review_required_count": 1,
                "active_unknown_blocked_count": 0,
                "active_not_run_count": 0,
                "active_structural_fail_count": 0,
                "active_blocked_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
            "counts": {
                "active_ready_count": 0,
                "active_blocked_count": 0,
                "active_human_review_required_count": 1,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
            "active_blockers": [{
                "task_id": "AOS-FARM-TASK-9999",
                "semantic_status": "HUMAN_REVIEW_REQUIRED",
                "effective_status": "HUMAN_REVIEW_REQUIRED",
                "structural_status": "PASS",
                "process_exit_status": "NOT_RUN",
                "primary_blocker_category": "not_run_required_check",
                "blocker_categories": [{"category": "not_run_required_check"}],
                "next_required_action": "requires human decision; not resolved by agent",
            }],
            "blocker_resolution_boundary": {
                "blockers_resolved_by_agent": "none",
                "human_review_blockers_closed": "none",
                "approvals_created": "none",
                "witnesses_created": "none",
                "risk_profiles_assigned_by_agent": "none",
                "lifecycle_mutations_performed": "none",
            },
            "excluded_terminal_tasks": [],
            "excluded_legacy_tasks": [],
            "malformed_exclusions": [],
            "tasks": [],
            "explicit_not_pass_statement": [
                "EXCLUDED_TERMINAL is not PASS",
                "EXCLUDED_LEGACY is not PASS",
                "MALFORMED_EXCLUSION is blocker state",
            ],
        }
        buf = io.StringIO()
        with mock.patch.object(MODULE, "VALIDATION_COMMANDS", []), \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "--json"]), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        self.assertEqual(data["overall_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertFalse(data["approval_claimed"])
        self.assertFalse(data["commit_authorized"])
        self.assertFalse(data["push_authorized"])
        self.assertFalse(data["release_authorized"])

    def test_pass_output_keeps_approval_boundary_false(self):
        readiness_audit = {
            "status": "PASS",
            "counts": {
                "active_ready_count": 1,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 1,
                "excluded_legacy_count": 1,
                "malformed_exclusion_count": 0,
            },
            "active_blockers": [],
            "excluded_terminal_tasks": [{"task_id": "AOS-FARM-TASK-9997", "readiness": "EXCLUDED_TERMINAL"}],
            "excluded_legacy_tasks": [{"task_id": "AOS-FARM.463", "readiness": "EXCLUDED_LEGACY"}],
            "malformed_exclusions": [],
            "tasks": [],
            "explicit_not_pass_statement": [
                "EXCLUDED_TERMINAL is not PASS",
                "EXCLUDED_LEGACY is not PASS",
                "MALFORMED_EXCLUSION is blocker state",
            ],
        }
        buf = io.StringIO()
        with mock.patch.object(MODULE, "VALIDATION_COMMANDS", []), \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "--json"]), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        self.assertEqual(data["overall_status"], "PASS")
        self.assertFalse(data["approval_claimed"])
        self.assertFalse(data["commit_authorized"])
        self.assertFalse(data["push_authorized"])
        self.assertFalse(data["release_authorized"])
        self.assertEqual(
            data["readiness_audit"]["explicit_not_pass_statement"],
            [
                "EXCLUDED_TERMINAL is not PASS",
                "EXCLUDED_LEGACY is not PASS",
                "MALFORMED_EXCLUSION is blocker state",
            ],
        )

if __name__ == '__main__':
    unittest.main()
