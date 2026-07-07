import unittest
import json
import subprocess
import os

class TestAosValidate(unittest.TestCase):
    def test_aos_validate_orchestration_only(self):
        # ensure it runs without error and outputs correct boundary fields
        try:
            result = subprocess.run(
                ["python3", "aos/scripts/aos_validate.py", "all", "--json"],
                capture_output=True,
                text=True,
                timeout=20,
            )
        except subprocess.TimeoutExpired as exc:
            self.fail(f"aos_validate.py timed out: {exc}")
        self.assertEqual(result.returncode, 0, msg=f"aos_validate failed: {result.stderr}")
        
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
        self.assertFalse(data.get("approval_claimed"))
        self.assertFalse(data.get("commit_authorized"))
        self.assertFalse(data.get("push_authorized"))
        self.assertFalse(data.get("release_authorized"))
        
        self.assertIn("results", data)
        self.assertTrue(isinstance(data["results"], list))
        self.assertTrue(len(data["results"]) > 0)

    def test_architecture_integration_in_json(self):
        result = subprocess.run(
            ["python3", "aos/scripts/aos_validate.py", "all", "--json"],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        
        # Check architecture is included
        arch_results = [r for r in data["results"] if r.get("command") == "aos_architecture_document_check.get_validate_all_report"]
        self.assertEqual(len(arch_results), 1)
        arch = arch_results[0]
        
        self.assertIn(arch.get("status"), ["PASS", "NOT_RUN", "UNKNOWN_BLOCKED", "BLOCKED", "FAILED", "CONFLICT_BLOCKED", "HUMAN_REVIEW_REQUIRED"])
        self.assertFalse(arch.get("approval_claimed"))
        self.assertFalse(arch.get("execution_authorized", False))
        self.assertFalse(arch.get("implementation_authorized", False))
        self.assertFalse(arch.get("release_authorized", False))
        
        # ensure not_run or unknown_blocked is not passed
        self.assertNotEqual(data.get("overall_status"), "UNKNOWN")

    def test_architecture_integration_no_recursion(self):
        with open("aos/scripts/aos_validate.py", "r") as f:
            content = f.read()
        
        self.assertNotIn("subprocess.run(['python3', 'aos/scripts/aos_architecture_document_check.py', 'validate-all'])", content)
        self.assertNotIn('subprocess.run(["python3", "aos/scripts/aos_architecture_document_check.py", "validate-all"])', content)
        
        # the integration should just call the imported function
        self.assertIn("aos_architecture_document_check.get_validate_all_report()", content)

if __name__ == '__main__':
    unittest.main()
