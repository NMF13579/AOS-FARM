import unittest
from unittest.mock import patch
import sys
from pathlib import Path

current_dir = Path(__file__).parent.resolve()
scripts_dir = current_dir.parent / "aos" / "scripts"
sys.path.insert(0, str(scripts_dir))

import aos_doctor

class TestAOSDoctor(unittest.TestCase):

    def test_determine_overall_status_ran_0_tests(self):
        # A test run with 0 tests is NOT a strong PASS
        results = [{
            "command": "python3 -m unittest discover -s tests -p test*.py",
            "status": "PASS",
            "stdout": "Ran 0 tests in 0.000s\nOK",
            "stderr": ""
        }]
        overall = aos_doctor.determine_overall_status(results)
        self.assertEqual(overall, "FAILED_OR_BLOCKED")
        self.assertEqual(results[0]["status"], "FAILED")
        self.assertEqual(results[0]["reason"], "Ran 0 tests is not a strong PASS")

    def test_determine_overall_status_ran_n_tests(self):
        # Normal tests PASS
        results = [{
            "command": "python3 -m unittest discover -s tests -p test*.py",
            "status": "PASS",
            "stdout": "Ran 5 tests in 0.010s\nOK",
            "stderr": ""
        }]
        overall = aos_doctor.determine_overall_status(results)
        self.assertEqual(overall, "PASS")

    def test_explicit_unittest_discovery_path(self):
        # Check that COMMANDS_TO_AGGREGATE includes the specific explicit path
        cmds = aos_doctor.COMMANDS_TO_AGGREGATE
        has_explicit = any(c == ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test*.py"] for c in cmds)
        self.assertTrue(has_explicit)

if __name__ == '__main__':
    unittest.main()
