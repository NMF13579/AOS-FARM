import unittest
import os
import json
from pathlib import Path
import sys

# Setup paths
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from aos.scripts.aos_code_quality_control import validate_package

class TestCodeQualityControl(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = project_root / "tests" / "fixtures" / "code_quality_control"

    def test_all_fixtures(self):
        # We know what the expected output is based on the fixture name
        for file_path in self.fixtures_dir.glob("*.yaml"):
            result = validate_package(file_path)
            
            if file_path.name.startswith("valid_"):
                self.assertEqual(
                    result["status"], 
                    "CODE_QUALITY_REPORTED_HUMAN_REVIEW_REQUIRED",
                    f"Expected valid but failed for {file_path.name}: {result['reason']}"
                )
                self.assertNotIn("APPROVAL", result["status"])
                self.assertNotIn("PASS", result["status"])
            elif file_path.name.startswith("invalid_"):
                self.assertIn(
                    result["status"], 
                    ["CODE_QUALITY_BLOCKED", "HUMAN_REVIEW_REQUIRED"],
                    f"Expected blocked but passed for {file_path.name}: {result['reason']}"
                )

if __name__ == "__main__":
    unittest.main()
