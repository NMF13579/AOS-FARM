import os
import sys
import json
import tempfile
import unittest
import io
from pathlib import Path
from unittest.mock import patch

# Add scripts dir to path to import
current_dir = Path(__file__).parent.resolve()
scripts_dir = current_dir.parent / "aos" / "scripts"
sys.path.insert(0, str(scripts_dir))

import aos_consumer_self_test

class TestAOSConsumerSelfTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_script_can_be_imported(self):
        self.assertTrue(hasattr(aos_consumer_self_test, 'check_package_integrity'))

    def test_package_integrity_detects_missing_files(self):
        # Empty repo_root should fail package integrity
        res = aos_consumer_self_test.check_package_integrity(self.repo_root)
        self.assertEqual(res["status"], "BLOCKED")
        self.assertTrue(len(res["missing_required"]) > 0)
        self.assertIn("aos/scripts/aos_consumer_self_test.py", res["missing_required"])

    def test_target_install_state_pending_templates(self):
        # Create fake templates
        aos_root = self.repo_root / "aos" / "root"
        aos_root.mkdir(parents=True, exist_ok=True)
        (aos_root / "llms.txt").touch()
        (aos_root / "AGENTS.md").touch()

        # Advisory workflow
        workflows = aos_root / ".github" / "workflows"
        workflows.mkdir(parents=True, exist_ok=True)
        (workflows / "aos-advisory.yml").touch()

        res = aos_consumer_self_test.check_target_install_state(self.repo_root)

        self.assertEqual(res["file_states"]["llms.txt"], "pending_from_template")
        self.assertEqual(res["file_states"]["AGENTS.md"], "pending_from_template")
        self.assertEqual(res["file_states"]["advisory_workflow"], "pending_from_template")

    def test_consumer_self_test_pending_root_entrypoints_is_not_fully_installed(self):
        # Create fake templates but no deployed files
        aos_root = self.repo_root / "aos" / "root"
        aos_root.mkdir(parents=True, exist_ok=True)
        (aos_root / "llms.txt").touch()
        (aos_root / "AGENTS.md").touch()

        res = aos_consumer_self_test.check_target_install_state(self.repo_root)
        self.assertEqual(res["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertIn("AGENTS.md", res["pending_entrypoints"])
        self.assertIn("llms.txt", res["pending_entrypoints"])
        self.assertTrue(any("Required root entrypoints are not deployed" in w for w in res["warnings"]))

    def test_target_install_state_tmp_boundary(self):
        tmp_dir = self.repo_root / ".aos-tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        (tmp_dir / "execution-report.md").touch()

        res = aos_consumer_self_test.check_target_install_state(self.repo_root)
        self.assertEqual(res["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertIn("execution-report.md", res["unexpected_tmp_files"])

    def test_output_contains_safety_statements(self):
        safety = aos_consumer_self_test.get_safety_boundaries()
        self.assertIn("self-test PASS ≠ approval", safety)
        self.assertIn("Evidence ≠ approval", safety)
        self.assertIn("Human approval cannot be simulated", safety)

    def test_no_mutation_during_checks(self):
        # Record state before
        before_files = set(self.repo_root.rglob('*'))

        # Run checks
        aos_consumer_self_test.check_package_integrity(self.repo_root)
        aos_consumer_self_test.check_target_install_state(self.repo_root)

        # Record state after
        after_files = set(self.repo_root.rglob('*'))

        self.assertEqual(before_files, after_files)

    @patch('aos_consumer_self_test.get_repo_root')
    def test_consumer_self_test_reports_ready_for_first_start_when_installed(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        aos_root = self.repo_root / "aos" / "root"
        aos_root.mkdir(parents=True, exist_ok=True)
        (aos_root / "llms.txt").touch()
        (aos_root / "AGENTS.md").touch()

        (self.repo_root / "llms.txt").touch()
        (self.repo_root / "AGENTS.md").touch()

        # Mock the installer run since it might fail if the environment isn't fully mocked
        with patch('aos_consumer_self_test.run_installer_dry_run') as mock_run:
            mock_run.return_value = {"status": "COMPLETED", "dry_run_install_status": "PASS", "evidence_note": ""}
            with patch('aos_consumer_self_test.check_package_integrity') as mock_pkg:
                mock_pkg.return_value = {"status": "PASS", "missing_required": [], "advisory_template_present": True, "warnings": []}

                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    try:
                        aos_consumer_self_test.main()
                    except SystemExit:
                        pass
                    output = fake_out.getvalue()

                self.assertIn("Installation Readiness: READY_FOR_FIRST_START", output)

    def test_installer_status_normalization(self):
        # Create fake installer script so check passes
        script_dir = self.repo_root / "aos" / "scripts"
        script_dir.mkdir(parents=True, exist_ok=True)
        (script_dir / "aos_install.py").touch()
        
        # Test status extraction from raw string
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "install_status: ** HUMAN_REVIEW_REQUIRED"
            mock_run.return_value.stderr = ""
            mock_run.return_value.returncode = 0
            res = aos_consumer_self_test.run_installer_dry_run(self.repo_root)
            self.assertEqual(res.get("dry_run_install_status"), "HUMAN_REVIEW_REQUIRED")
            
            mock_run.return_value.stdout = "**install_status:** `PASS`"
            mock_run.return_value.stderr = ""
            res = aos_consumer_self_test.run_installer_dry_run(self.repo_root)
            self.assertEqual(res.get("dry_run_install_status"), "PASS")

            mock_run.return_value.stdout = "install_status: garbage"
            mock_run.return_value.stderr = ""
            res = aos_consumer_self_test.run_installer_dry_run(self.repo_root)
            self.assertEqual(res.get("dry_run_install_status"), "UNKNOWN_BLOCKED")

    def test_target_install_state_tmp_hygiene_diagnostics(self):
        tmp_dir = self.repo_root / ".aos-tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        (tmp_dir / "review-note.txt").touch()

        res = aos_consumer_self_test.check_target_install_state(self.repo_root)
        self.assertEqual(res["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertIn("review-note.txt", res["unexpected_tmp_files"])
        self.assertTrue(any("contains review/report/handoff/evidence/checkpoint-like files" in w for w in res["warnings"]))

if __name__ == '__main__':
    unittest.main()
