import os
import unittest
import subprocess
import json
import sys
from aos.scripts.aos_task_quality_check import check_task_quality

class TestAOSTaskQualityCheck(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures', 'task_quality_check')
        self.script_path = os.path.join(os.path.dirname(__file__), '..', 'aos', 'scripts', 'aos_task_quality_check.py')

    def test_valid_functional_intent_reports_human_review_required(self):
        fixture_path = os.path.join(self.fixtures_dir, 'valid_functional_intent.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "TASK_QUALITY_FUNCTIONAL_INTENT_REPORTED_HUMAN_REVIEW_REQUIRED")
        self.assertEqual(result["verification_status"], "VERIFIED")
        self.assertEqual(result["verification_method"], "script_run")
        self.assertEqual(len(result["blocked_reasons"]), 0)

    def test_missing_functional_intent_warns_but_does_not_approve(self):
        fixture_path = os.path.join(self.fixtures_dir, 'missing_functional_intent.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "FUNCTIONAL_INTENT_MISSING_HUMAN_REVIEW_REQUIRED")
        self.assertTrue(any("functional_intent is missing" in w for w in result["warnings"]))

    def test_not_run_is_blocked(self):
        fixture_path = os.path.join(self.fixtures_dir, 'not_run_functional_intent.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED")
        self.assertTrue(any("NOT_RUN" in r for r in result["blocked_reasons"]))

    def test_not_verified_cannot_be_verified(self):
        fixture_path = os.path.join(self.fixtures_dir, 'not_verified_but_verified.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED")
        self.assertTrue(any("cannot produce verification_status VERIFIED" in r for r in result["blocked_reasons"]))

    def test_empty_declared_purpose_is_blocked(self):
        fixture_path = os.path.join(self.fixtures_dir, 'empty_declared_purpose.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED")
        self.assertTrue(any("declared_purpose is empty or missing" in r for r in result["blocked_reasons"]))

    def test_empty_forbidden_behaviors_warns(self):
        fixture_path = os.path.join(self.fixtures_dir, 'empty_forbidden_behaviors.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "TASK_QUALITY_FUNCTIONAL_INTENT_REPORTED_HUMAN_REVIEW_REQUIRED")
        self.assertTrue(any("forbidden_behaviors is empty" in w for w in result["warnings"]))

    def test_non_authority_boundary_false_is_blocked(self):
        fixture_path = os.path.join(self.fixtures_dir, 'non_authority_boundary_false.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED")
        self.assertTrue(any("must not be false" in r for r in result["blocked_reasons"]))

    def test_partial_requires_human_review(self):
        fixture_path = os.path.join(self.fixtures_dir, 'partial_requires_human_review.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertEqual(result["status"], "TASK_QUALITY_FUNCTIONAL_INTENT_BLOCKED")
        self.assertTrue(any("human_review_required must not be false" in r for r in result["blocked_reasons"]))

    def test_validator_never_grants_approval(self):
        fixture_path = os.path.join(self.fixtures_dir, 'valid_functional_intent.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertNotEqual(result["status"], "APPROVED")
        self.assertNotEqual(result["status"], "PASS")

    def test_validator_never_authorizes_commit_push_merge_release(self):
        fixture_path = os.path.join(self.fixtures_dir, 'valid_functional_intent.quality-package.json')
        result = check_task_quality(fixture_path)
        self.assertFalse(result["commit_authorized"])
        self.assertFalse(result["push_authorized"])
        self.assertFalse(result["merge_authorized"])
        self.assertFalse(result["release_authorized"])
        self.assertFalse(result["approval_granted"])

    def test_summarize_output_shape(self):
        fixture_path = os.path.join(self.fixtures_dir, 'valid_functional_intent.quality-package.json')
        cmd = [sys.executable, self.script_path, 'summarize', '--package', fixture_path]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Status: TASK_QUALITY_FUNCTIONAL_INTENT_REPORTED_HUMAN_REVIEW_REQUIRED", proc.stdout)

if __name__ == '__main__':
    unittest.main()
