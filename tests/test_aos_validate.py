import unittest
import json
import subprocess
import os
import contextlib
import importlib.util
import io
import sys
import tempfile
from unittest import mock
from pathlib import Path


MODULE_PATH = os.path.join("aos", "scripts", "aos_validate.py")
sys.path.insert(0, os.path.abspath(os.path.join("aos", "scripts")))
SPEC = importlib.util.spec_from_file_location("aos_validate_module", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

class TestAosValidate(unittest.TestCase):
    def assertAggregateNotPass(self, result):
        self.assertNotEqual(MODULE.determine_overall_status([result]), "PASS")

    def selector_result(self, payload, return_code=0, stdout=None):
        return {
            "command": "python3 aos/scripts/aos_next_task_selection.py --json",
            "status": "PASS" if return_code == 0 else "FAILED",
            "return_code": return_code,
            "process_exit_status": "EXIT_ZERO" if return_code == 0 else "EXIT_NON_ZERO",
            "stdout": json.dumps(payload) if stdout is None else stdout,
            "stderr": "",
        }

    def installer_result(self, install_status="HUMAN_REVIEW_REQUIRED", blocked_reasons=None, return_code=0):
        if blocked_reasons is None:
            blocked_reasons = []
        blocked_lines = "\n".join(f"- {reason}" for reason in blocked_reasons) if blocked_reasons else "- [none]"
        stdout = f"""# AOS-FARM Installer Plan

**install_status:** {install_status}
**apply_status:** NOT_REQUESTED

### existing_targets
- /aos/

### conflicts
- aos/ -> aos/ (target folder already exists)

### blocked_reasons
{blocked_lines}

**approval_claimed:** false
**execution_authorized:** false
"""
        return {
            "command": "python3 aos/scripts/aos_install.py --dry-run",
            "status": "PASS" if return_code == 0 else "FAILED",
            "return_code": return_code,
            "process_exit_status": "EXIT_ZERO" if return_code == 0 else "EXIT_NON_ZERO",
            "stdout": stdout,
            "stderr": "",
        }

    def consumer_result(self, final_status="PASS", dry_run_status="HUMAN_REVIEW_REQUIRED", return_code=0):
        report = {
            "package_integrity": {"status": "PASS"},
            "target_install_state": {"status": "PASS"},
            "installer_dry_run": {
                "status": "COMPLETED",
                "dry_run_install_status": dry_run_status,
            },
            "final_status": final_status,
            "approval_claimed": False,
            "execution_authorized": False,
        }
        stdout = "--- JSON REPORT ---\n" + json.dumps(report, indent=2) + "\n-------------------"
        return {
            "command": "python3 aos/scripts/aos_consumer_self_test.py",
            "status": "PASS" if return_code == 0 else "FAILED",
            "return_code": return_code,
            "process_exit_status": "EXIT_ZERO" if return_code == 0 else "EXIT_NON_ZERO",
            "stdout": stdout,
            "stderr": "",
        }

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

    def test_selector_human_review_required_advisory_does_not_block_technical_health(self):
        result = self.selector_result({
            "final_status": "HUMAN_REVIEW_REQUIRED",
            "selection_status": "RECONCILED",
            "next_candidate": "AOS-FARM.TEST",
            "approval_claimed": False,
            "execution_authorized": False,
        })
        self.assertEqual(MODULE.normalize_child_result(result), "PASS")
        advisory = MODULE.collect_advisories([result])[0]
        self.assertEqual(advisory["source"], "aos_next_task_selection.py")
        self.assertEqual(advisory["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(advisory["next_candidate"], "AOS-FARM.TEST")
        self.assertFalse(advisory["blocking_technical_health"])
        self.assertFalse(advisory["approval_granted"])
        self.assertFalse(advisory["execution_authorized"])

    def test_installer_dry_run_human_review_required_advisory_does_not_block_technical_health(self):
        result = self.installer_result()
        self.assertEqual(MODULE.normalize_child_result(result), "PASS")
        advisory = MODULE.collect_advisories([result])[0]
        self.assertEqual(advisory["source"], "aos_install.py --dry-run")
        self.assertEqual(advisory["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertTrue(advisory["advisory"])
        self.assertFalse(advisory["blocking_technical_health"])

    def test_consumer_self_test_embedded_installer_review_advisory_does_not_block_technical_health(self):
        result = self.consumer_result()
        self.assertEqual(MODULE.normalize_child_result(result), "PASS")
        advisory = MODULE.collect_advisories([result])[0]
        self.assertEqual(advisory["source"], "aos_consumer_self_test.py")
        self.assertEqual(advisory["status"], "PASS")
        self.assertEqual(advisory["embedded_advisory_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertFalse(advisory["blocking_technical_health"])

    def test_revised_advisory_contract_exposes_control_metadata_without_false_approval(self):
        readiness_audit = {
            "status": "PASS",
            "counts": {
                "active_ready_count": 1,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
            "active_blockers": [],
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
        command_results = {
            " ".join(["python3", "aos/scripts/aos_next_task_selection.py", "--json"]): self.selector_result({
                "final_status": "HUMAN_REVIEW_REQUIRED",
                "selection_status": "RECONCILED",
                "next_candidate": "AOS-FARM.TEST",
                "approval_claimed": False,
                "execution_authorized": False,
            }),
            " ".join(["python3", "aos/scripts/aos_install.py", "--dry-run"]): self.installer_result(),
            " ".join(["python3", "aos/scripts/aos_consumer_self_test.py"]): self.consumer_result(),
        }
        validation_commands = [
            ["python3", "aos/scripts/aos_install.py", "--dry-run"],
            ["python3", "aos/scripts/aos_consumer_self_test.py"],
            ["python3", "aos/scripts/aos_next_task_selection.py", "--json"],
        ]

        def fake_run_command(cmd):
            return command_results[" ".join(cmd)]

        buf = io.StringIO()
        with mock.patch.object(MODULE, "VALIDATION_COMMANDS", validation_commands), \
             mock.patch.object(MODULE, "run_command", side_effect=fake_run_command), \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "--json"]), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        self.assertEqual(data["technical_status"], "PASS")
        self.assertEqual(data["overall_status"], "PASS")
        self.assertEqual(data["control_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertTrue(data["human_review_required"])
        self.assertFalse(data["approval_granted"])
        self.assertFalse(data["execution_authorized"])
        sources = {advisory["source"] for advisory in data["advisories"]}
        self.assertEqual(sources, {
            "aos_next_task_selection.py",
            "aos_install.py --dry-run",
            "aos_consumer_self_test.py",
        })

    def test_selector_unknown_blocked_still_blocks(self):
        result = self.selector_result({"final_status": "UNKNOWN_BLOCKED", "next_candidate": "AOS-FARM.TEST"})
        self.assertEqual(MODULE.normalize_child_result(result), "UNKNOWN_BLOCKED")

    def test_selector_not_run_still_blocks(self):
        result = self.selector_result({"final_status": "NOT_RUN", "next_candidate": "AOS-FARM.TEST"})
        self.assertEqual(MODULE.normalize_child_result(result), "NOT_RUN")

    def test_selector_malformed_json_blocks(self):
        result = self.selector_result({}, stdout="{not-json")
        self.assertEqual(MODULE.normalize_child_result(result), "UNKNOWN_BLOCKED")

    def test_selector_missing_candidate_human_review_blocks(self):
        result = self.selector_result({"final_status": "HUMAN_REVIEW_REQUIRED", "next_candidate": None})
        self.assertEqual(MODULE.normalize_child_result(result), "UNKNOWN_BLOCKED")

    def test_advisory_nonzero_exit_blocks(self):
        self.assertNotEqual(MODULE.normalize_child_result(self.installer_result(return_code=1)), "PASS")

    def test_consumer_self_test_failure_still_blocks(self):
        result = self.consumer_result(final_status="BLOCKED")
        self.assertNotEqual(MODULE.normalize_child_result(result), "PASS")

    def test_installer_blocked_reasons_still_block(self):
        result = self.installer_result(blocked_reasons=["unsafe target path"])
        self.assertNotEqual(MODULE.normalize_child_result(result), "PASS")

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

    def test_required_sources_present_preserves_pass(self):
        readiness_audit = {
            "status": "PASS",
            "counts": {
                "active_ready_count": 1,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
        }
        buf = io.StringIO()
        with mock.patch.object(MODULE, "VALIDATION_COMMANDS", []), \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "--json"]), \
             mock.patch("os.path.exists", return_value=True), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        self.assertEqual(data["overall_status"], "PASS")
        self.assertEqual(data["required_sources"]["status"], "PASS")

    def test_missing_required_source_blocks_pass_and_outputs_json(self):
        readiness_audit = {
            "status": "PASS",
            "counts": {
                "active_ready_count": 1,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
        }
        buf = io.StringIO()

        def mock_exists(path):
            if path == "00_AOS_Core_Control.md":
                return False
            return True

        with mock.patch.object(MODULE, "VALIDATION_COMMANDS", []), \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "--json"]), \
             mock.patch("os.path.exists", side_effect=mock_exists), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        self.assertEqual(data["overall_status"], "BLOCKED_REQUIRED_SOURCES_MISSING")
        self.assertEqual(data["required_sources"]["status"], "FAIL")
        self.assertIn("00_AOS_Core_Control.md", data["required_sources"]["missing"])

    def test_help_shows_conditional_scope_contract_option_without_running_children(self):
        buf = io.StringIO()
        with mock.patch.object(MODULE, "run_command") as run_command, \
             mock.patch("sys.argv", ["aos_validate.py", "--help"]), \
             self.assertRaises(SystemExit) as raised, \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("--conditional-scope-contract", buf.getvalue())
        run_command.assert_not_called()

    def test_default_validation_context_preserves_existing_conditional_child_command(self):
        commands = MODULE.build_validation_commands()
        conditional = [
            command for command in commands
            if "aos/scripts/aos_conditional_scope_check.py" in command
        ]
        self.assertEqual(len(conditional), 1)
        self.assertEqual(conditional[0], [sys.executable, "aos/scripts/aos_conditional_scope_check.py", "--json"])
        self.assertEqual(
            MODULE.default_conditional_scope_contract_context(),
            {"source": "DEFAULT_TEMPLATE", "path": None, "sha256": None},
        )

    def test_explicit_conditional_scope_contract_forwarded_only_to_conditional_child(self):
        context = {"source": "EXPLICIT_CLI", "path": ".aos-tmp/ctx file.json", "sha256": "a" * 64}
        commands = MODULE.build_validation_commands(context)
        conditional = [
            command for command in commands
            if "aos/scripts/aos_conditional_scope_check.py" in command
        ][0]
        self.assertEqual(
            conditional,
            [
                sys.executable,
                "aos/scripts/aos_conditional_scope_check.py",
                "--contract",
                ".aos-tmp/ctx file.json",
                "--json",
            ],
        )
        self.assertIn(".aos-tmp/ctx file.json", conditional)
        self.assertEqual(conditional.count(".aos-tmp/ctx file.json"), 1)
        for command in commands:
            if command is conditional:
                continue
            self.assertNotIn("--contract", command)
            self.assertNotIn(".aos-tmp/ctx file.json", command)

    def test_explicit_conditional_scope_contract_path_safety_accepts_relative_regular_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            contract = repo / ".aos-tmp" / "ctx" / "conditional-scope-contract.json"
            contract.parent.mkdir(parents=True)
            contract.write_text('{"contract": true}\n', encoding="utf-8")

            context = MODULE.resolve_conditional_scope_contract_context(
                ".aos-tmp/ctx/conditional-scope-contract.json",
                repo_root=repo,
            )

        self.assertEqual(context["source"], "EXPLICIT_CLI")
        self.assertEqual(context["path"], ".aos-tmp/ctx/conditional-scope-contract.json")
        self.assertEqual(
            context["sha256"],
            "11aee6a0615d8db4fd606e441057b965799d94b4dae4f8619fd58a895f3f5ee3",
        )

    def test_explicit_conditional_scope_contract_path_safety_blocks_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            regular = repo / ".aos-tmp" / "ctx" / "contract.json"
            regular.parent.mkdir(parents=True)
            regular.write_text("{}", encoding="utf-8")
            directory = repo / ".aos-tmp" / "directory"
            directory.mkdir()
            symlink = repo / ".aos-tmp" / "ctx" / "link.json"
            symlink.symlink_to(regular)
            parent_symlink = repo / ".aos-tmp" / "parent-link"
            parent_symlink.symlink_to(regular.parent, target_is_directory=True)

            unsafe_values = [
                "",
                str(regular),
                "../contract.json",
                ".aos-tmp/missing.json",
                ".aos-tmp/directory",
                ".aos-tmp/ctx/link.json",
                ".aos-tmp/parent-link/contract.json",
                ".aos-tmp/ctx/bad\x00.json",
                ".aos-tmp/ctx/bad\n.json",
            ]
            for value in unsafe_values:
                with self.subTest(value=value):
                    with self.assertRaises(ValueError):
                        MODULE.resolve_conditional_scope_contract_context(value, repo_root=repo)

    def test_main_outputs_explicit_validation_context_and_preserves_child_status(self):
        readiness_audit = {
            "status": "PASS",
            "counts": {
                "active_ready_count": 1,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
        }
        with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp:
            contract = Path(tmp) / "contract with spaces.json"
            contract.write_text('{"contract": true}\n', encoding="utf-8")
            contract_arg = contract.relative_to(Path.cwd()).as_posix()
            conditional_stdout = json.dumps({
                "final_status": "PASS",
                "reason_code": "CONDITIONAL_SCOPE_VALID",
                "approval_claimed_by_validator": False,
            })
            conditional_command = [
                sys.executable,
                "aos/scripts/aos_conditional_scope_check.py",
                "--contract",
                contract_arg,
                "--json",
            ]
            command_results = {
                " ".join(conditional_command): {
                    "command": " ".join(conditional_command),
                    "status": "PASS",
                    "return_code": 0,
                    "process_exit_status": "EXIT_ZERO",
                    "stdout": conditional_stdout,
                    "stderr": "",
                }
            }

            def fake_run_command(cmd):
                return command_results[" ".join(cmd)]

            buf = io.StringIO()
            with mock.patch.object(MODULE, "VALIDATION_COMMANDS", [[sys.executable, "aos/scripts/aos_conditional_scope_check.py", "--json"]]), \
                 mock.patch.object(MODULE, "run_command", side_effect=fake_run_command), \
                 mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
                 mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
                 mock.patch("sys.argv", ["aos_validate.py", "all", "--conditional-scope-contract", contract_arg, "--json"]), \
                 contextlib.redirect_stdout(buf):
                MODULE.main()

            data = json.loads(buf.getvalue())

        context = data["validation_context"]["conditional_scope_contract"]
        self.assertEqual(context["source"], "EXPLICIT_CLI")
        self.assertEqual(context["path"], contract_arg)
        self.assertEqual(context["sha256"], "11aee6a0615d8db4fd606e441057b965799d94b4dae4f8619fd58a895f3f5ee3")
        conditional_result = data["results"][0]
        self.assertEqual(conditional_result["conditional_scope_contract_source"], "EXPLICIT_CLI")
        self.assertEqual(conditional_result["child_final_status"], "PASS")
        self.assertEqual(conditional_result["child_reason_code"], "CONDITIONAL_SCOPE_VALID")
        self.assertFalse(data["approval_granted"])
        self.assertFalse(data["commit_authorized"])

    def test_invalid_explicit_contract_path_fails_closed_without_running_children(self):
        readiness_audit = {"status": "PASS", "counts": {}}
        buf = io.StringIO()
        with mock.patch.object(MODULE, "run_command") as run_command, \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "all", "--conditional-scope-contract", "/tmp/contract.json", "--json"]), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        run_command.assert_not_called()
        self.assertEqual(data["overall_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(data["results"][0]["status"], "FAILED")
        self.assertEqual(data["results"][0]["final_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(data["results"][0]["reason_code"], "CONDITIONAL_SCOPE_CONTRACT_PATH_INVALID")
        self.assertEqual(data["validation_context"]["conditional_scope_contract"]["source"], "INVALID")

    def test_help_shows_integration_contract_options_without_running_children(self):
        buf = io.StringIO()
        with mock.patch.object(MODULE, "run_command") as run_command, \
             mock.patch("sys.argv", ["aos_validate.py", "--help"]), \
             self.assertRaises(SystemExit) as raised, \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("--integration-contract", buf.getvalue())
        self.assertIn("--integration-source-oid", buf.getvalue())
        self.assertIn("--integration-target-oid", buf.getvalue())
        run_command.assert_not_called()

    def test_default_validation_context_does_not_run_integration_checker(self):
        commands = MODULE.build_validation_commands()
        self.assertFalse(any("aos_integration_contract_check.py" in command for command in commands))
        self.assertEqual(
            MODULE.default_integration_contract_context(),
            {
                "source": "NOT_PROVIDED",
                "path": None,
                "observed_source_oid": None,
                "observed_target_oid": None,
                "contract_sha256": None,
            },
        )

    def test_explicit_integration_contract_forwarded_only_to_integration_child(self):
        context = {
            "source": "EXPLICIT_CLI",
            "path": "aos/integration/contracts/contract with spaces.yaml",
            "observed_source_oid": "1" * 40,
            "observed_target_oid": "2" * 40,
            "contract_sha256": "a" * 64,
        }
        commands = MODULE.build_validation_commands(integration_contract=context)
        integration = [
            command for command in commands
            if "aos/scripts/aos_integration_contract_check.py" in command
        ][0]
        self.assertEqual(
            integration,
            [
                sys.executable,
                "aos/scripts/aos_integration_contract_check.py",
                "--contract",
                "aos/integration/contracts/contract with spaces.yaml",
                "--repository-root",
                ".",
                "--observed-source-oid",
                "1" * 40,
                "--observed-target-oid",
                "2" * 40,
                "--json",
            ],
        )
        self.assertEqual(integration.count("aos/integration/contracts/contract with spaces.yaml"), 1)
        for command in commands:
            if command is integration:
                continue
            self.assertNotIn("--integration-contract", command)
            self.assertNotIn("--observed-source-oid", command)
            self.assertNotIn("--observed-target-oid", command)
            self.assertNotIn("aos/integration/contracts/contract with spaces.yaml", command)

    def test_partial_integration_options_fail_closed_without_running_children(self):
        readiness_audit = {"status": "PASS", "counts": {}}
        buf = io.StringIO()
        with mock.patch.object(MODULE, "run_command") as run_command, \
             mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
             mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
             mock.patch("sys.argv", ["aos_validate.py", "all", "--integration-contract", "aos/integration/contracts/example.yaml", "--json"]), \
             contextlib.redirect_stdout(buf):
            MODULE.main()

        data = json.loads(buf.getvalue())
        run_command.assert_not_called()
        self.assertEqual(data["overall_status"], "UNKNOWN_BLOCKED")
        self.assertEqual(data["results"][0]["reason_code"], "INTEGRATION_CONTRACT_CONTEXT_INCOMPLETE")
        self.assertEqual(data["validation_context"]["integration_contract"]["source"], "INVALID")

    def test_main_preserves_integration_child_status_and_context_metadata(self):
        readiness_audit = {
            "status": "PASS",
            "counts": {
                "active_ready_count": 1,
                "active_blocked_count": 0,
                "active_human_review_required_count": 0,
                "excluded_terminal_count": 0,
                "excluded_legacy_count": 0,
                "malformed_exclusion_count": 0,
            },
        }
        with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp:
            contract = Path(tmp) / "aos" / "integration" / "contracts" / "contract.json"
            contract.parent.mkdir(parents=True)
            contract.write_text('{"contract": true}\n', encoding="utf-8")
            contract_arg = contract.relative_to(Path.cwd()).as_posix()
            child_stdout = json.dumps({
                "final_status": "PASS",
                "reason_code": "INTEGRATION_CONTRACT_VALID",
                "approval_granted": False,
                "integration_authorized": False,
            })
            integration_command = [
                sys.executable,
                "aos/scripts/aos_integration_contract_check.py",
                "--contract",
                contract_arg,
                "--repository-root",
                ".",
                "--observed-source-oid",
                "1" * 40,
                "--observed-target-oid",
                "2" * 40,
                "--json",
            ]
            command_results = {
                " ".join(integration_command): {
                    "command": " ".join(integration_command),
                    "status": "PASS",
                    "return_code": 0,
                    "process_exit_status": "EXIT_ZERO",
                    "stdout": child_stdout,
                    "stderr": "",
                }
            }

            def fake_run_command(cmd):
                return command_results[" ".join(cmd)]

            buf = io.StringIO()
            with mock.patch.object(MODULE, "VALIDATION_COMMANDS", []), \
                 mock.patch.object(MODULE, "run_command", side_effect=fake_run_command), \
                 mock.patch.object(MODULE, "build_readiness_audit", return_value=readiness_audit), \
                 mock.patch.object(MODULE.aos_architecture_document_check, "get_validate_all_report", return_value={"status": "PASS"}), \
                 mock.patch("sys.argv", [
                     "aos_validate.py",
                     "all",
                     "--integration-contract",
                     contract_arg,
                     "--integration-source-oid",
                     "1" * 40,
                     "--integration-target-oid",
                     "2" * 40,
                     "--json",
                 ]), \
                 contextlib.redirect_stdout(buf):
                MODULE.main()

            data = json.loads(buf.getvalue())

        context = data["validation_context"]["integration_contract"]
        self.assertEqual(context["source"], "EXPLICIT_CLI")
        self.assertEqual(context["path"], contract_arg)
        self.assertEqual(context["observed_source_oid"], "1" * 40)
        self.assertEqual(context["observed_target_oid"], "2" * 40)
        self.assertEqual(context["contract_sha256"], "11aee6a0615d8db4fd606e441057b965799d94b4dae4f8619fd58a895f3f5ee3")
        result = data["results"][0]
        self.assertEqual(result["integration_contract_source"], "EXPLICIT_CLI")
        self.assertEqual(result["child_final_status"], "PASS")
        self.assertEqual(result["child_reason_code"], "INTEGRATION_CONTRACT_VALID")
        self.assertFalse(data["approval_granted"])
        self.assertFalse(data["commit_authorized"])

    def test_integration_child_blocked_remains_blocking(self):
        result = {
            "command": "python3 aos/scripts/aos_integration_contract_check.py --json",
            "status": "PASS",
            "return_code": 0,
            "process_exit_status": "EXIT_ZERO",
            "stdout": json.dumps({"final_status": "BLOCKED", "reason_code": "CONTRACT_BINDING_MISMATCH"}),
            "stderr": "",
        }
        self.assertEqual(MODULE.normalize_child_result(result), "BLOCKED")

if __name__ == '__main__':
    unittest.main()

    def test_duplicate_workspace_child_pass(self):
        import subprocess
        from aos.scripts.aos_validate import main
        import sys
        import json
        with patch("subprocess.run") as mock_run, patch("sys.argv", ["aos_validate.py", "--json"]), patch("sys.stdout") as mock_stdout:
            mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout='{"final_status": "PASS", "summary": {"suspicious_count": 0}}', stderr="")
            main()
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            data = json.loads(output)
            assert data["duplicate_workspace_status"] == "PASS"

    def test_duplicate_workspace_child_failed_or_blocked(self):
        import subprocess
        from aos.scripts.aos_validate import main
        import sys
        import json
        with patch("subprocess.run") as mock_run, patch("sys.argv", ["aos_validate.py", "--json"]), patch("sys.stdout") as mock_stdout:
            def side_effect(cmd, **kwargs):
                if "aos_duplicate_workspace_check.py" in " ".join(cmd):
                    return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='{"final_status": "FAILED_OR_BLOCKED", "summary": {}}', stderr="")
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='PASS', stderr="")
            mock_run.side_effect = side_effect
            main()
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            data = json.loads(output)
            assert data["duplicate_workspace_status"] == "FAILED_OR_BLOCKED"
            assert data["overall_status"] in ("FAILED_OR_BLOCKED", "UNKNOWN_BLOCKED")

    def test_duplicate_workspace_child_human_review_required(self):
        import subprocess
        from aos.scripts.aos_validate import main
        import sys
        import json
        with patch("subprocess.run") as mock_run, patch("sys.argv", ["aos_validate.py", "--json"]), patch("sys.stdout") as mock_stdout:
            def side_effect(cmd, **kwargs):
                if "aos_duplicate_workspace_check.py" in " ".join(cmd):
                    return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='{"final_status": "HUMAN_REVIEW_REQUIRED", "summary": {}}', stderr="")
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='PASS', stderr="")
            mock_run.side_effect = side_effect
            main()
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            data = json.loads(output)
            assert data["duplicate_workspace_status"] == "HUMAN_REVIEW_REQUIRED"
            assert data["overall_status"] in ("HUMAN_REVIEW_REQUIRED", "UNKNOWN_BLOCKED", "FAILED_OR_BLOCKED")

    def test_duplicate_workspace_child_unknown_blocked(self):
        import subprocess
        from aos.scripts.aos_validate import main
        import sys
        import json
        with patch("subprocess.run") as mock_run, patch("sys.argv", ["aos_validate.py", "--json"]), patch("sys.stdout") as mock_stdout:
            def side_effect(cmd, **kwargs):
                if "aos_duplicate_workspace_check.py" in " ".join(cmd):
                    return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='{"final_status": "UNKNOWN_BLOCKED", "summary": {}}', stderr="")
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='PASS', stderr="")
            mock_run.side_effect = side_effect
            main()
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            data = json.loads(output)
            assert data["duplicate_workspace_status"] == "UNKNOWN_BLOCKED"
            assert data["overall_status"] == "UNKNOWN_BLOCKED"

    def test_duplicate_workspace_child_not_run(self):
        import subprocess
        from aos.scripts.aos_validate import main
        import sys
        import json
        with patch("subprocess.run") as mock_run, patch("sys.argv", ["aos_validate.py", "--json"]), patch("sys.stdout") as mock_stdout:
            def side_effect(cmd, **kwargs):
                if "aos_duplicate_workspace_check.py" in " ".join(cmd):
                    raise FileNotFoundError("script not found")
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='PASS', stderr="")
            mock_run.side_effect = side_effect
            main()
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            data = json.loads(output)
            assert data["duplicate_workspace_status"] == "UNKNOWN_BLOCKED"

    def test_duplicate_workspace_invalid_json(self):
        import subprocess
        from aos.scripts.aos_validate import main
        import sys
        import json
        with patch("subprocess.run") as mock_run, patch("sys.argv", ["aos_validate.py", "--json"]), patch("sys.stdout") as mock_stdout:
            def side_effect(cmd, **kwargs):
                if "aos_duplicate_workspace_check.py" in " ".join(cmd):
                    return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='invalid json', stderr="")
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='PASS', stderr="")
            mock_run.side_effect = side_effect
            main()
            output = "".join(call[0][0] for call in mock_stdout.write.call_args_list)
            data = json.loads(output)
            assert data["duplicate_workspace_status"] == "UNKNOWN_BLOCKED"
