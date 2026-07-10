import unittest
from unittest.mock import patch
import sys
import json
import io
from pathlib import Path

current_dir = Path(__file__).parent.resolve()
scripts_dir = current_dir.parent / "aos" / "scripts"
sys.path.insert(0, str(scripts_dir))

import aos_doctor

class TestAOSDoctor(unittest.TestCase):

    def test_determine_overall_status_ran_0_tests_unittest(self):
        results = [{
            "command": "python3 -m unittest discover -s tests -p test*.py",
            "status": "PASS",
            "stdout": "Ran 0 tests in 0.000s\nOK",
            "stderr": ""
        }]
        overall = aos_doctor.determine_overall_status(results)
        self.assertEqual(overall, "FAILED_OR_BLOCKED")
        self.assertEqual(results[0]["status"], "FAILED")
        self.assertEqual(results[0]["reason"], "0 tests executed is not a strong PASS")

    def test_determine_overall_status_ran_0_tests_pytest(self):
        results = [{
            "command": "python3 -m pytest",
            "status": "PASS",
            "stdout": "collected 0 items",
            "stderr": ""
        }]
        overall = aos_doctor.determine_overall_status(results)
        self.assertEqual(overall, "FAILED_OR_BLOCKED")
        self.assertEqual(results[0]["status"], "FAILED")
        self.assertEqual(results[0]["reason"], "0 tests executed is not a strong PASS")

    def test_determine_overall_status_ran_n_tests(self):
        results = [{
            "command": "python3 -m pytest",
            "status": "PASS",
            "stdout": "503 passed in 67.97s",
            "stderr": ""
        }]
        overall = aos_doctor.determine_overall_status(results)
        self.assertEqual(overall, "PASS")

    def test_explicit_pytest_path(self):
        cmds = aos_doctor.COMMANDS_TO_AGGREGATE
        has_explicit = any(c == [sys.executable, "-m", "pytest"] for c in cmds)
        self.assertTrue(has_explicit)

    @patch('aos_doctor.subprocess.run')
    def test_sys_executable_and_no_shell(self, mock_run):
        for cmd in aos_doctor.COMMANDS_TO_AGGREGATE:
            self.assertEqual(cmd[0], sys.executable)
            
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        aos_doctor.run_command(["ls"])
        mock_run.assert_called_with(["ls"], capture_output=True, text=True, timeout=120)

    @patch('aos_doctor.run_command')
    def test_missing_pytest_diagnostics(self, mock_run_command):
        def side_effect(cmd):
            if cmd == [sys.executable, "-c", "import pytest"]:
                return {
                    "command": " ".join(cmd),
                    "status": "FAILED",
                    "return_code": 1,
                    "stdout": "",
                    "stderr": "Traceback..."
                }
            return {
                "command": " ".join(cmd),
                "status": "PASS",
                "return_code": 0,
                "stdout": "503 passed in 60s" if "-m pytest" in " ".join(cmd) else ( '{"final_status":"PASS"}' if "aos_duplicate_workspace_check.py" in " ".join(cmd) else ""),
                "stderr": ""
            }
        
        mock_run_command.side_effect = side_effect
        
        with patch('sys.argv', ['aos_doctor.py', '--json']):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                aos_doctor.main()
                output = json.loads(mock_stdout.getvalue())
        
        pytest_check = next(r for r in output["results"] if r["command"] == f"{sys.executable} -c import pytest")
        self.assertEqual(pytest_check["status"], "FAILED")
        
        self.assertIn("pytest", pytest_check["reason"])
        self.assertIn(sys.executable, pytest_check["reason"])
        self.assertIn("requirements-dev.txt", pytest_check["reason"])
        self.assertIn(f"{sys.executable} -m pip install -r requirements-dev.txt", pytest_check["reason"])
        
        runner_check = next(r for r in output["results"] if "pytest" in r["command"] and "-m" in r["command"])
        self.assertEqual(runner_check["status"], "NOT_RUN")
        self.assertEqual(runner_check["reason"], "Skipped due to missing pytest dependency")
        
        self.assertEqual(len(output["results"]), len(aos_doctor.COMMANDS_TO_AGGREGATE))
        self.assertEqual(output["overall_status"], "FAILED_OR_BLOCKED")
        
        pip_cmds = [cmd for cmd in aos_doctor.COMMANDS_TO_AGGREGATE if "pip" in cmd]
        self.assertEqual(len(pip_cmds), 0)

    @patch('aos_doctor.run_command')
    def test_available_pytest(self, mock_run_command):
        def side_effect(cmd):
            return {
                "command": " ".join(cmd),
                "status": "PASS",
                "return_code": 0,
                "stdout": "503 passed in 60s" if "-m pytest" in " ".join(cmd) else ( '{"final_status":"PASS"}' if "aos_duplicate_workspace_check.py" in " ".join(cmd) else ""),
                "stderr": ""
            }
        mock_run_command.side_effect = side_effect
        
        with patch('sys.argv', ['aos_doctor.py', '--json']):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                aos_doctor.main()
                output = json.loads(mock_stdout.getvalue())
                
        pytest_check = next(r for r in output["results"] if "import pytest" in r["command"])
        self.assertEqual(pytest_check["status"], "PASS")
        
        runner_check = next(r for r in output["results"] if "-m pytest" in r["command"])
        self.assertEqual(runner_check["status"], "PASS")
        
        self.assertEqual(output["overall_status"], "PASS")

if __name__ == '__main__':
    unittest.main()


    def test_checker_pass(self):
        from aos.scripts.aos_doctor import determine_overall_status
        results = [{"command": "aos_duplicate_workspace_check.py", "status": "PASS", "stdout": '{"final_status": "PASS"}'}]
        assert determine_overall_status(results) == "PASS"

    def test_checker_failed_or_blocked(self):
        from aos.scripts.aos_doctor import determine_overall_status
        results = [{"command": "aos_duplicate_workspace_check.py", "status": "PASS", "stdout": '{"final_status": "FAILED_OR_BLOCKED"}'}]
        assert determine_overall_status(results) == "FAILED_OR_BLOCKED"

    def test_checker_human_review_required(self):
        from aos.scripts.aos_doctor import determine_overall_status
        results = [{"command": "aos_duplicate_workspace_check.py", "status": "PASS", "stdout": '{"final_status": "HUMAN_REVIEW_REQUIRED"}'}]
        assert determine_overall_status(results) == "FAILED_OR_BLOCKED"

    def test_checker_unknown_blocked(self):
        from aos.scripts.aos_doctor import determine_overall_status
        results = [{"command": "aos_duplicate_workspace_check.py", "status": "PASS", "stdout": '{"final_status": "UNKNOWN_BLOCKED"}'}]
        assert determine_overall_status(results) == "UNKNOWN_BLOCKED"

    def test_checker_not_run(self):
        from aos.scripts.aos_doctor import determine_overall_status
        results = [{"command": "aos_duplicate_workspace_check.py", "status": "NOT_RUN", "stdout": ''}]
        assert determine_overall_status(results) == "UNKNOWN_BLOCKED"

    def test_checker_invalid_output(self):
        from aos.scripts.aos_doctor import determine_overall_status
        results = [{"command": "aos_duplicate_workspace_check.py", "status": "PASS", "stdout": 'not json'}]
        assert determine_overall_status(results) == "UNKNOWN_BLOCKED"
