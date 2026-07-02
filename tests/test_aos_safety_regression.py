import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from aos.scripts.aos_task_document_check import validate_task_document, check_task_readiness

class TestAosSafetyRegression(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures/aos-safety-regression')
        
    def _assert_invalid(self, filename, expected_message_substring=None):
        path = os.path.join(self.fixtures_dir, filename)
        is_valid, messages = validate_task_document(path)
        self.assertFalse(is_valid, f"Expected {filename} to fail validation")
        if expected_message_substring:
            found = any(expected_message_substring in msg for msg in messages)
            self.assertTrue(found, f"Expected message containing '{expected_message_substring}' not found in {messages}")
            
    def _assert_readiness_blocked(self, filename, expected_message_substring=None):
        path = os.path.join(self.fixtures_dir, filename)
        status, messages = check_task_readiness(path)
        self.assertEqual(status, "BLOCKED", f"Expected {filename} to be BLOCKED")
        if expected_message_substring:
            found = any(expected_message_substring in msg for msg in messages)
            self.assertTrue(found, f"Expected message containing '{expected_message_substring}' not found in {messages}")

    def test_pass_as_approval(self):
        self._assert_invalid("pass_as_approval.md", "Invalid approval_status")

    def test_ci_pass_as_approval(self):
        self._assert_invalid("ci_pass_as_approval.md", "Invalid approval_status")

    def test_evidence_claims_approval(self):
        self._assert_readiness_blocked("evidence_claims_approval.md", "Evidence claims approval")

    def test_not_run_as_pass(self):
        self._assert_invalid("not_run_as_pass.md", "treating NOT_RUN as PASS is forbidden")

    def test_unknown_as_ok(self):
        self._assert_invalid("unknown_as_ok.md", "treating UNKNOWN as OK is forbidden")

    def test_queue_next_as_execution(self):
        self._assert_invalid("queue_next_as_execution.md", "queue_status: NEXT does not create READY_FOR_EXECUTION")

    def test_doctor_pass_as_authorization(self):
        self._assert_invalid("doctor_pass_as_authorization.md", "Invalid approval_status")

    def test_dashboard_next_as_authorization(self):
        self._assert_invalid("dashboard_next_as_authorization.md", "Invalid approval_status")
        
    def test_prompt_pack_as_source_of_truth(self):
        path = os.path.join(self.fixtures_dir, "prompt_pack_as_source_of_truth.md")
        with open(path, 'r') as f:
            content = f.read().lower()
        self.assertTrue("overrides source of truth" in content or "source of truth" in content)
        self.assertTrue("prompt pack" in content)
        
    def test_task_candidate_as_approval(self):
        path = os.path.join(self.fixtures_dir, "task_candidate_as_approval.md")
        with open(path, 'r') as f:
            content = f.read().lower()
        self.assertTrue("candidate equals approval" in content or "task candidate equals approval" in content)

if __name__ == '__main__':
    unittest.main()
