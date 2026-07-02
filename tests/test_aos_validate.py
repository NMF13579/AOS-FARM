import unittest
import json
import subprocess
import os

class TestAosValidate(unittest.TestCase):
    def test_aos_validate_orchestration_only(self):
        # ensure it runs without error and outputs correct boundary fields
        result = subprocess.run(["python3", "aos/scripts/aos_validate.py", "all", "--json"], capture_output=True, text=True)
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

if __name__ == '__main__':
    unittest.main()
