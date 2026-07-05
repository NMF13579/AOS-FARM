import os
import sys
import unittest
from pathlib import Path
import tempfile
import io
from unittest.mock import patch

current_dir = Path(__file__).parent.resolve()
scripts_dir = current_dir.parent / "aos" / "scripts"
sys.path.insert(0, str(scripts_dir))

import aos_install

class TestAOSInstall(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.test_dir.name)
        self.aos_root = self.repo_root / "aos" / "root"
        self.aos_root.mkdir(parents=True, exist_ok=True)
        
    def tearDown(self):
        self.test_dir.cleanup()

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_clean_target(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / "AGENTS.md").touch()
        (self.aos_root / "llms.txt").touch()
        
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
            
        self.assertIn("**install_status:** PASS", output)
        self.assertIn("planned_creates", output)
        self.assertIn("aos/root/AGENTS.md -> /AGENTS.md", output)

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_existing_agents_conflict(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / "AGENTS.md").touch()
        
        # Create conflict
        (self.repo_root / "AGENTS.md").touch()
        
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
            
        self.assertIn("**install_status:** HUMAN_REVIEW_REQUIRED", output)
        self.assertIn("aos/root/AGENTS.md -> AGENTS.md (target file already exists)", output)

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_existing_llms_conflict(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / "llms.txt").touch()
        
        # Create conflict
        (self.repo_root / "llms.txt").touch()
        
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
            
        self.assertIn("**install_status:** HUMAN_REVIEW_REQUIRED", output)

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_clean_target_maps_gitignore_template_to_root_gitignore(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / ".gitignore.template").touch()
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
        self.assertIn("aos/root/.gitignore.template -> /.gitignore", output)

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_does_not_plan_root_template_artifacts_as_root_runtime_files(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / "ROOT_INSTALL_GUIDE.md").touch()
        (self.aos_root / "ROOT_FILES_MANIFEST.md").touch()
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
        self.assertNotIn("ROOT_INSTALL_GUIDE.md -> /ROOT_INSTALL_GUIDE.md", output)
        self.assertNotIn("ROOT_FILES_MANIFEST.md -> /ROOT_FILES_MANIFEST.md", output)

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_existing_gitignore_requires_manual_snippet_merge(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / "gitignore.snippet").touch()
        (self.repo_root / ".gitignore").touch()
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
        self.assertIn("aos/root/gitignore.snippet -> existing /.gitignore manual merge", output)

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_does_not_plan_gitignore_snippet_as_root_file(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / "gitignore.snippet").touch()
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
        self.assertNotIn("gitignore.snippet -> /gitignore.snippet", output)

    @patch('aos_install.get_repo_root')
    def test_install_dry_run_existing_advisory_workflow_conflict_or_pending(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        workflows = self.aos_root / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "aos-advisory.yml").touch()
        
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
            
        self.assertIn("**install_status:** PASS", output)
        
        # Conflict
        target_workflows = self.repo_root / ".github" / "workflows"
        target_workflows.mkdir(parents=True, exist_ok=True)
        (target_workflows / "aos-advisory.yml").touch()
        
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            aos_install.run_dry_run()
            output = fake_out.getvalue()
            
        self.assertIn("**install_status:** HUMAN_REVIEW_REQUIRED", output)

    def test_install_dry_run_blocks_git_path(self):
        safe, reason = aos_install.check_path_safety(Path(".git/config"), Path("."))
        self.assertFalse(safe)
        self.assertIn(".git/", reason)

    def test_install_dry_run_blocks_aos_tmp_path(self):
        safe, reason = aos_install.check_path_safety(Path(".aos-tmp/log.txt"), Path("."))
        self.assertFalse(safe)
        self.assertIn(".aos-tmp/", reason)

    def test_install_dry_run_blocks_project_code_folders(self):
        safe, reason = aos_install.check_path_safety(Path("project/src/index.js"), Path("."))
        self.assertFalse(safe)
        self.assertIn("project/", reason)

    def test_apply_is_not_implemented(self):
        # We can test this by running the main function or checking the logic
        with patch('sys.argv', ['aos_install.py', '--apply']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                try:
                    aos_install.main()
                except SystemExit as e:
                    self.assertEqual(e.code, 0)
                output = fake_out.getvalue()
                self.assertIn("apply_status: NOT_IMPLEMENTED", output)

if __name__ == '__main__':
    unittest.main()
