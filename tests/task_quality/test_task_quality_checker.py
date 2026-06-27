import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from aos.tools.optional.task_quality_checker import TaskQualityChecker

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), '../fixtures/task_quality')

class TestTaskQualityChecker(unittest.TestCase):
    def test_positive_pass(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'positive/pass.json'))
        self.assertEqual(checker.validate(), "PASS")

    def test_warning_pass_with_warnings(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'warning/pass_with_warnings.json'))
        self.assertEqual(checker.validate(), "PASS_WITH_WARNINGS")

    def test_not_enough_evidence_missing_optional(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'not_enough_evidence/missing_optional_evidence.json'))
        self.assertEqual(checker.validate(), "NOT_ENOUGH_EVIDENCE")

    def test_negative_missing_required_artifact(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'negative/missing_required_artifact.json'))
        self.assertEqual(checker.validate(), "BLOCKED")

    def test_negative_not_run_required_validation(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'negative/not_run_required_validation.json'))
        self.assertEqual(checker.validate(), "BLOCKED")

    def test_negative_unknown_required_validation(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'negative/unknown_required_validation.json'))
        self.assertEqual(checker.validate(), "BLOCKED")

    def test_negative_human_review_required_false(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'negative/human_review_required_false.json'))
        self.assertEqual(checker.validate(), "BLOCKED")

    def test_negative_forbidden_approval_claim(self):
        checker = TaskQualityChecker(os.path.join(FIXTURES_DIR, 'negative/forbidden_approval_claim.json'))
        self.assertEqual(checker.validate(), "BLOCKED")

if __name__ == '__main__':
    unittest.main()
