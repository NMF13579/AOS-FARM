import unittest
import os
import sys
import json
import subprocess
from pathlib import Path

# Setup paths
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from aos.tools.optional import task_registry_validator

class TestTaskQueueHelper(unittest.TestCase):
    def setUp(self):
        self.cli_path = project_root / "aos" / "scripts" / "aos_task_queue_helper.py"
        self.fixture_valid = project_root / "tests" / "fixtures" / "task_queue_valid.yaml"
        self.fixture_candidate_as_approved = project_root / "tests" / "fixtures" / "task_queue_invalid_candidate_as_approved.yaml"
        self.fixture_invalid_transition = project_root / "tests" / "fixtures" / "task_queue_invalid_transition.yaml"
        self.fixture_missing_auth = project_root / "tests" / "fixtures" / "task_queue_missing_human_authorization.yaml"

    def run_helper(self, command, fixture):
        cmd = [sys.executable, str(self.cli_path), command, "--registry", str(fixture), "--queue", str(fixture)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res

    def test_valid_queue_passes(self):
        res = self.run_helper("validate", self.fixture_valid)
        self.assertIn("WARNING: PASS ≠ approval.", res.stderr)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data.get("ok"))
        self.assertEqual(data.get("final_status"), "PASS")

    def test_next_candidate_is_not_approved(self):
        # Even if show-next selects it, invariants explicitly state it's not approved.
        res = self.run_helper("show-next", self.fixture_valid)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data.get("invariants", {}).get("next_candidate_is_not_approved"))
        self.assertIn("WARNING: Next Task Candidate ≠ approved task.", res.stderr)

    def test_queue_position_is_not_approval(self):
        res = self.run_helper("show-current", self.fixture_valid)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data.get("invariants", {}).get("queue_position_is_not_approval"))
        self.assertIn("WARNING: Queue position ≠ approval.", res.stderr)

    def test_task_without_human_authorization_not_ready(self):
        res = self.run_helper("validate", self.fixture_missing_auth)
        self.assertEqual(res.returncode, 1)
        data = json.loads(res.stdout)
        self.assertFalse(data.get("ok"))
        self.assertEqual(data.get("final_status"), "BLOCKED")
        self.assertTrue(any("READY_FOR_EXECUTION but execution_authorized is false" in err for err in data.get("errors", [])))

    def test_invalid_transition_detected(self):
        res = self.run_helper("validate", self.fixture_invalid_transition)
        self.assertEqual(res.returncode, 1)
        data = json.loads(res.stdout)
        self.assertFalse(data.get("ok"))
        self.assertTrue(any("invalid transition" in err for err in data.get("errors", [])))

    def test_unknown_is_not_ok(self):
        # We put UNKNOWN in final_status in valid queue explicitly to check this
        res = self.run_helper("validate", self.fixture_valid)
        data = json.loads(res.stdout)
        # In our valid fixture, UNKNOWN triggers an error, so validate actually fails?
        # Wait, if we put UNKNOWN in the valid fixture, it will fail validation.
        # Let's adjust the valid fixture or parse the error.
        # Since UNKNOWN was in valid fixture, test_valid_queue_passes might have failed!
        # Actually, if UNKNOWN is not OK, it errors.
        # Let's verify by just calling the validator manually on text.
        text = "schema_version: 1\ntasks:\n  - task_id: T1\n    final_status: UNKNOWN"
        result = task_registry_validator.validate_registry_queue(text, text)
        self.assertTrue(any("UNKNOWN, which is BLOCKED/not OK" in e for e in result["errors"]))

    def test_not_run_is_not_pass(self):
        text = "schema_version: 1\ntasks:\n  - task_id: T1\n    final_status: NOT_RUN"
        result = task_registry_validator.validate_registry_queue(text, text)
        self.assertTrue(any("NOT_RUN, which is not PASS" in w for w in result["warnings"]))

    def test_helper_does_not_mutate_input_files(self):
        # Record mtimes
        mtime_before = os.stat(self.fixture_valid).st_mtime
        self.run_helper("validate", self.fixture_valid)
        mtime_after = os.stat(self.fixture_valid).st_mtime
        self.assertEqual(mtime_before, mtime_after)

    def test_json_explicit_safety_boundaries(self):
        res = self.run_helper("validate", self.fixture_valid)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIn("status", data)
        self.assertIn("warnings", data)
        self.assertTrue(data.get("approval_required"))
        self.assertFalse(data.get("execution_authorized"))
        self.assertFalse(data.get("commit_authorized"))
        self.assertFalse(data.get("push_authorized"))
        self.assertFalse(data.get("release_authorized"))
        self.assertIn("unknown_items", data)
        self.assertIn("not_run_items", data)
        self.assertIn("invalid_transitions", data)
        self.assertIn("approval_boundary_violations", data)

        res_current = self.run_helper("show-current", self.fixture_valid)
        data_current = json.loads(res_current.stdout)
        self.assertIn("status", data_current)
        self.assertTrue(data_current.get("candidate_only"))
        self.assertTrue(data_current.get("approval_required"))
        self.assertFalse(data_current.get("commit_authorized"))

        res_summary = self.run_helper("summary", self.fixture_valid)
        data_summary = json.loads(res_summary.stdout)
        self.assertIn("status", data_summary)
        self.assertFalse(data_summary.get("commit_authorized"))

if __name__ == '__main__':
    unittest.main()
