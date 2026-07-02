import unittest
import json
import subprocess
import os

class TestAosReviewPackage(unittest.TestCase):
    def test_aos_review_package_default(self):
        result = subprocess.run(["python3", "aos/scripts/aos_review_package.py", "--since", "HEAD", "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, msg=f"aos_review_package failed: {result.stderr}")
        
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
        self.assertFalse(data.get("approval_claimed"))
        self.assertFalse(data.get("commit_authorized"))
        self.assertFalse(data.get("push_authorized"))
        self.assertFalse(data.get("release_authorized"))
        
        self.assertEqual(data.get("validation_status"), "NOT_RUN")
        self.assertIn(data.get("package_status"), ["READY_FOR_HUMAN_REVIEW", "UNKNOWN_BLOCKED"])
        
    def test_aos_review_package_validation(self):
        result = subprocess.run(["python3", "aos/scripts/aos_review_package.py", "--since", "HEAD", "--include-validation", "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, msg=f"aos_review_package failed: {result.stderr}")
        
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
        self.assertNotEqual(data.get("validation_status"), "NOT_RUN")
        self.assertIn(data.get("package_status"), ["READY_FOR_HUMAN_REVIEW", "CHANGES_REQUIRED", "UNKNOWN_BLOCKED"])

if __name__ == '__main__':
    unittest.main()
