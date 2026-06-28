import unittest
import os
import json
from pathlib import Path
import sys

# Setup paths
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from aos.scripts.aos_code_quality_control import validate_package, summarize

class TestCodeQualityControl(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = project_root / "tests" / "fixtures" / "code_quality_control"

    def test_all_fixtures(self):
        # We know what the expected output is based on the fixture name
        for file_path in self.fixtures_dir.glob("*.yaml"):
            result = validate_package(file_path)

            if file_path.name.startswith("valid_"):
                self.assertIn(
                    result["status"],
                    ["CODE_QUALITY_REPORTED_HUMAN_REVIEW_REQUIRED", "OVERENGINEERING_REVIEW_REQUIRED"],
                    f"Expected valid but failed for {file_path.name}: {result.get('reason', '')}"
                )
                self.assertNotIn("APPROVAL", result["status"])
                self.assertNotIn("PASS", result["status"])
            elif file_path.name.startswith("invalid_"):
                self.assertIn(
                    result["status"],
                    ["CODE_QUALITY_BLOCKED", "HUMAN_REVIEW_REQUIRED"],
                    f"Expected blocked but passed for {file_path.name}: {result['reason']}"
                )

    def test_summarize_shape(self):
        # We can pick any fixture to test the shape
        fixture_path = next(self.fixtures_dir.glob("*.yaml"))
        summary = summarize(fixture_path)

        self.assertIn("status", summary)
        self.assertIn("package", summary)
        self.assertEqual(summary["package"], str(fixture_path))

        self.assertIn("human_review_required", summary)
        self.assertTrue(summary["human_review_required"])

        self.assertIn("approval_granted", summary)
        self.assertFalse(summary["approval_granted"])

        self.assertIn("commit_authorized", summary)
        self.assertFalse(summary["commit_authorized"])

        self.assertIn("push_authorized", summary)
        self.assertFalse(summary["push_authorized"])

        self.assertIn("release_authorized", summary)
        self.assertFalse(summary["release_authorized"])

        self.assertIn("blocked_reasons_count", summary)

        # New overengineering assertions
        self.assertIn("overengineering_review_required", summary)
        self.assertTrue(summary["overengineering_review_required"])
        self.assertIn("overengineering_controls_present", summary)
        self.assertIn("warnings", summary)

        # Verify forbidden emits
        summary_str = json.dumps(summary)
        self.assertNotIn("APPROVED", summary_str)
        self.assertNotIn("READY_FOR_COMMIT", summary_str)
        self.assertNotIn("READY_FOR_PUSH", summary_str)
        self.assertNotIn("READY_FOR_MERGE", summary_str)
        self.assertNotIn("READY_FOR_RELEASE", summary_str)
        self.assertNotIn("PASS-as-approval", summary_str)

    def test_missing_overengineering_controls(self):
        temp_file = Path("temp_missing_oe.yaml")
        temp_file.write_text(
            "risk_profile: HIGH_RISK\n"
            "risk_profile_assigned_by: human\n"
            "execution_authorized: true\n"
            "allowed_files:\n  - a\n"
            "forbidden_files:\n  - b\n"
            "required_tests:\n  - c\n"
            "required_checks:\n  - d\n"
        )

        result = validate_package(temp_file)
        self.assertEqual(result["status"], "OVERENGINEERING_REVIEW_REQUIRED")
        self.assertFalse(result["overengineering_controls_present"])
        self.assertIn("warnings", result)
        self.assertEqual(result["warnings"], ["overengineering_controls section missing"])
        self.assertTrue(result["overengineering_review_required"])

        # Clean up
        if temp_file.exists():
            temp_file.unlink()

if __name__ == "__main__":
    unittest.main()
