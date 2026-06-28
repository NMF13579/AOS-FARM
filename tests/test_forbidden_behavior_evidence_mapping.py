import unittest
import os
import json
from aos.scripts.aos_task_quality_check import check_forbidden_evidence_mapping

FIXTURES_DIR = "tests/fixtures/forbidden_behavior_evidence_mapping"

class TestForbiddenBehaviorEvidenceMapping(unittest.TestCase):

    def run_check(self, filename):
        path = os.path.join(FIXTURES_DIR, filename)
        return check_forbidden_evidence_mapping(path)

    def test_valid_mapping_requires_human_review(self):
        result = self.run_check("valid_mapping.json")
        self.assertEqual(result["status"], "FORBIDDEN_EVIDENCE_MAPPING_VALID_HUMAN_REVIEW_REQUIRED")
        self.assertTrue(result["human_review_required"])
        self.assertFalse(result["approval_granted"])

    def test_final_status_approved_is_blocked(self):
        result = self.run_check("negative_final_status_approved.json")
        self.assertIn("BLOCKED", result["status"])

    def test_missing_mapping_items_is_blocked(self):
        result = self.run_check("negative_missing_mapping_items.json")
        self.assertIn("BLOCKED", result["status"])

    def test_missing_evidence_item_is_blocked_or_human_review_required(self):
        result = self.run_check("negative_missing_evidence_item.json")
        self.assertIn("BLOCKED", result["status"])

    def test_unknown_without_human_review_is_blocked(self):
        result = self.run_check("negative_unknown_without_human_review.json")
        self.assertEqual(result["status"], "FORBIDDEN_EVIDENCE_MAPPING_UNKNOWN_BLOCKED")

    def test_validator_never_grants_approval_or_authorization(self):
        result = self.run_check("valid_mapping.json")
        self.assertFalse(result.get("approval_granted", True))
        self.assertFalse(result.get("commit_authorized", True))
        self.assertFalse(result.get("push_authorized", True))
        self.assertFalse(result.get("merge_authorized", True))
        self.assertFalse(result.get("release_authorized", True))

if __name__ == '__main__':
    unittest.main()
