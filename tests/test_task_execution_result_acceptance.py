import unittest
import os
import json
from aos.scripts.aos_task_quality_check import check_result_acceptance

FIXTURES_DIR = "tests/fixtures/task_execution_result_acceptance"


class TestTaskExecutionResultAcceptance(unittest.TestCase):

    def run_check(self, filename):
        path = os.path.join(FIXTURES_DIR, filename)
        return check_result_acceptance(path)

    # ── Positive ────────────────────────────────────────────────────────────

    def test_valid_result_acceptance_requires_human_review(self):
        result = self.run_check("valid_result_acceptance.json")
        self.assertEqual(result["status"], "RESULT_ACCEPTANCE_READY_FOR_HUMAN_REVIEW")
        self.assertTrue(result["human_review_required"])
        self.assertFalse(result["approval_granted"])

    # ── Negative: final_status APPROVED ─────────────────────────────────────

    def test_final_status_approved_is_blocked(self):
        result = self.run_check("negative_final_status_approved.json")
        self.assertIn("BLOCKED", result["status"])
        self.assertTrue(len(result["blocked_reasons"]) > 0)

    # ── Negative: missing required field ────────────────────────────────────

    def test_missing_changed_files_is_schema_invalid(self):
        result = self.run_check("negative_missing_changed_files.json")
        self.assertEqual(result["status"], "RESULT_ACCEPTANCE_SCHEMA_INVALID")
        self.assertTrue(
            any("changed_files" in r for r in result["blocked_reasons"]),
            "Expected 'changed_files' in blocked_reasons"
        )

    # ── Negative: UNKNOWN without human_review_required ─────────────────────

    def test_unknown_without_human_review_is_unknown_blocked(self):
        result = self.run_check("negative_unknown_without_human_review.json")
        self.assertEqual(result["status"], "RESULT_ACCEPTANCE_UNKNOWN_BLOCKED")
        self.assertTrue(len(result["blocked_reasons"]) > 0)

    # ── Negative: NOT_RUN treated as PASS ───────────────────────────────────

    def test_not_run_is_not_pass(self):
        result = self.run_check("negative_not_run_treated_as_pass.json")
        self.assertIn("BLOCKED", result["status"])
        self.assertTrue(
            any("NOT_RUN" in r for r in result["blocked_reasons"]),
            "Expected 'NOT_RUN' in blocked_reasons"
        )

    # ── Negative: OUT_OF_SCOPE without human_review_required ────────────────

    def test_out_of_scope_without_human_review_is_blocked(self):
        result = self.run_check("negative_out_of_scope_without_human_review.json")
        self.assertIn("BLOCKED", result["status"])
        self.assertTrue(
            any("OUT_OF_SCOPE" in r for r in result["blocked_reasons"]),
            "Expected 'OUT_OF_SCOPE' in blocked_reasons"
        )

    # ── Authorization invariants (valid fixture) ─────────────────────────────

    def test_validator_never_grants_approval_or_authorization(self):
        result = self.run_check("valid_result_acceptance.json")
        self.assertFalse(result.get("approval_granted", True),
                         "approval_granted must always be False")
        self.assertFalse(result.get("commit_authorized", True),
                         "commit_authorized must always be False")
        self.assertFalse(result.get("push_authorized", True),
                         "push_authorized must always be False")
        self.assertFalse(result.get("merge_authorized", True),
                         "merge_authorized must always be False")
        self.assertFalse(result.get("release_authorized", True),
                         "release_authorized must always be False")


if __name__ == "__main__":
    unittest.main()
