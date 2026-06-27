import unittest
import subprocess
import json
import os

class TestHumanResultAcceptanceChecker(unittest.TestCase):
    def setUp(self):
        self.script_path = os.path.join(os.path.dirname(__file__), '../../aos/scripts/aos_result_acceptance.py')
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), '../fixtures/result_acceptance')

    def run_checker(self, fixture_rel_path):
        fixture_path = os.path.join(self.fixtures_dir, fixture_rel_path)
        cmd = ["python3", self.script_path, "validate", "--decision", fixture_path, "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_accept_result_pass(self):
        res = self.run_checker('positive/accept_result_pass.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'PASS')

    def test_accept_result_with_warnings(self):
        res = self.run_checker('positive/accept_result_with_warnings.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'PASS_WITH_WARNINGS')

    def test_accept_not_enough_evidence_with_acknowledgement(self):
        res = self.run_checker('warning/accept_not_enough_evidence_with_acknowledgement.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'PASS_WITH_WARNINGS')

    def test_missing_human_decision(self):
        res = self.run_checker('negative/missing_human_decision.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_unknown_human_decision(self):
        res = self.run_checker('negative/unknown_human_decision.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_accept_blocked_task_quality(self):
        res = self.run_checker('negative/accept_blocked_task_quality.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_accept_unknown_required_field(self):
        res = self.run_checker('negative/accept_unknown_required_field.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_accept_not_run_required_check(self):
        res = self.run_checker('negative/accept_not_run_required_check.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_needs_changes_without_follow_up(self):
        res = self.run_checker('negative/needs_changes_without_follow_up.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_reject_without_reason(self):
        res = self.run_checker('negative/reject_without_reason.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_commit_authorized_true(self):
        res = self.run_checker('negative/commit_authorized_true.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_push_authorized_true(self):
        res = self.run_checker('negative/push_authorized_true.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_next_task_started_true(self):
        res = self.run_checker('negative/next_task_started_true.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_lifecycle_mutation_authorized_true(self):
        res = self.run_checker('negative/lifecycle_mutation_true.json')
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data['status'], 'BLOCKED')

    def test_invalid_json(self):
        res = self.run_checker('malformed/invalid_json.json')
        self.assertEqual(res.returncode, 2)
        # Should exit with code 2 and not produce json output properly
