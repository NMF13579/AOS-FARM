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
