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

if __name__ == '__main__':
    unittest.main()
