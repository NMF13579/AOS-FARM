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
        self.repo_root = Path(self.test_dir.name) / "target"
        self.repo_root.mkdir()

        self.source_dir = Path(self.test_dir.name) / "source"
        self.source_dir.mkdir()

        self.aos_root = self.source_dir / "aos" / "root"
        self.aos_root.mkdir(parents=True, exist_ok=True)
        (self.aos_root / "AGENTS.md").touch()
        (self.aos_root / "llms.txt").touch()

    def tearDown(self):
        self.test_dir.cleanup()

    @patch('aos_install.get_repo_root')
    def test_apply_requires_exact_confirmation(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'WRONG']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                with self.assertRaises(SystemExit) as cm:
                    aos_install.main(source_package_root=self.source_dir)
                self.assertEqual(cm.exception.code, 1)
                output = fake_out.getvalue()
                self.assertIn("apply_status: APPLY_BLOCKED", output)
                self.assertIn("reason: exact Human confirmation string mismatch", output)
                self.assertIn("files_changed: []", output)
                self.assertIn("partial_writes: false", output)

    @patch('aos_install.get_repo_root')
    def test_apply_safe_create_clean_target(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("apply_status: APPLY_DONE", output)
                self.assertTrue((self.repo_root / "AGENTS.md").exists())
                self.assertTrue((self.repo_root / "llms.txt").exists())
                self.assertIn("**files_changed:**", output)
                self.assertIn("READY_FOR_FIRST_START", output)

    @patch('aos_install.get_repo_root')
    def test_apply_safe_create_with_existing_gitignore_appends_aos_block(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / ".gitignore.template").touch()
        target_gitignore = self.repo_root / ".gitignore"
        target_gitignore.write_text("node_modules/\n")

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)

        content = target_gitignore.read_text(encoding="utf-8")
        self.assertIn("node_modules/\n", content)
        self.assertIn("/.aos-tmp/", content)

    @patch('aos_install.get_repo_root')
    def test_apply_existing_gitignore_with_aos_block_is_noop(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / ".gitignore.template").touch()
        target_gitignore = self.repo_root / ".gitignore"
        target_gitignore.write_text("node_modules/\n/.aos-tmp/\n")

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)

        content = target_gitignore.read_text(encoding="utf-8")
        self.assertEqual(content.count("/.aos-tmp/"), 1)

    @patch('aos_install.get_repo_root')
    def test_apply_existing_agents_blocks_without_changes(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        target_agents = self.repo_root / "AGENTS.md"
        target_agents.write_text("existing")

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                with self.assertRaises(SystemExit):
                    aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("HUMAN_REVIEW_REQUIRED", output)
                self.assertIn("files_changed: []", output)
                self.assertIn("partial_writes: false", output)
        self.assertEqual(target_agents.read_text(), "existing")

    @patch('aos_install.get_repo_root')
    def test_apply_existing_llms_blocks_without_changes(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        target_llms = self.repo_root / "llms.txt"
        target_llms.write_text("existing")

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                with self.assertRaises(SystemExit):
                    aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("HUMAN_REVIEW_REQUIRED", output)
                self.assertIn("files_changed: []", output)
                self.assertIn("partial_writes: false", output)

    @patch('aos_install.get_repo_root')
    def test_apply_existing_aos_blocks_without_changes(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.repo_root / "aos").mkdir()
        (self.repo_root / "aos" / "something.md").touch()

        # To trigger the check, let's say the template has something to copy to aos/something.md
        aos_sub = self.aos_root / "aos"
        aos_sub.mkdir(parents=True, exist_ok=True)
        (aos_sub / "something.md").touch()

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                with self.assertRaises(SystemExit):
                    aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("HUMAN_REVIEW_REQUIRED", output)
                self.assertIn("files_changed: []", output)

    @patch('aos_install.get_repo_root')
    def test_apply_gitignore_conflict_markers_blocks_without_changes(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / ".gitignore.template").touch()
        target_gitignore = self.repo_root / ".gitignore"
        target_gitignore.write_text("<<<<<<< HEAD\na\n=======\nb\n>>>>>>> branch")

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                with self.assertRaises(SystemExit):
                    aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("HUMAN_REVIEW_REQUIRED", output)
                self.assertIn("files_changed: []", output)

    @patch('aos_install.get_repo_root')
    def test_apply_does_not_touch_readme(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / "README.md").touch()
        (self.aos_root / "README_AOS_SECTION.md").touch()

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)

        self.assertFalse((self.repo_root / "README.md").exists())
        self.assertFalse((self.repo_root / "README_AOS_SECTION.md").exists())

    @patch('aos_install.get_repo_root')
    def test_apply_does_not_touch_workflows(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        workflows = self.aos_root / ".github" / "workflows"
        workflows.mkdir(parents=True, exist_ok=True)
        (workflows / "aos-advisory.yml").touch()

        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)

        self.assertFalse((self.repo_root / ".github" / "workflows" / "aos-advisory.yml").exists())

    @patch('aos_install.get_repo_root')
    def test_apply_does_not_commit(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("execution_authorized: false", output)
                self.assertNotIn("git commit", output)

    @patch('aos_install.get_repo_root')
    def test_apply_does_not_push(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertNotIn("git push", output)

    @patch('aos_install.get_repo_root')
    def test_apply_done_self_test_ready_for_first_start(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("READY_FOR_FIRST_START", output)

    @patch('aos_install.get_repo_root')
    def test_apply_done_does_not_report_human_review_required(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertNotIn("install_status: HUMAN_REVIEW_REQUIRED", output)
                self.assertNotIn("HUMAN_REVIEW_REQUIRED", output)

    @patch('aos_install.get_repo_root')
    def test_apply_done_tutor_does_not_say_apply_blocked(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--apply', '--safe-create-and-gitignore-append', '--confirm', 'AOS INSTALL SAFE CREATE OK', '--tutor']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertNotIn("Apply is blocked", output)
                self.assertIn("Apply was completed successfully.", output)
                self.assertIn("The target repo now has the required AOS first-start files.", output)
                self.assertIn("Apply DONE is not approval.", output)
                self.assertIn("READY_FOR_FIRST_START is not execution authorization.", output)

    @patch('aos_install.get_repo_root')
    def test_gitignore_existing_aos_block_is_no_change_not_unsafe(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        (self.aos_root / ".gitignore.template").touch()
        target_gitignore = self.repo_root / ".gitignore"
        target_gitignore.write_text("node_modules/\n/.aos-tmp/\n")

        with patch('sys.argv', ['aos_install.py', '--dry-run']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertNotIn("unsafe .gitignore", output)

    @patch('aos_install.get_repo_root')
    def test_tutor_output_explains_safe_create_plan(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--dry-run', '--tutor']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("TUTOR EXPLANATION", output)
                self.assertIn("What the installer wants to create", output)

    @patch('aos_install.get_repo_root')
    def test_tutor_output_explains_agents_boundary(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--dry-run', '--tutor']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("Why AGENTS.md and llms.txt are not modified automatically", output)

    @patch('aos_install.get_repo_root')
    def test_tutor_output_does_not_claim_approval(self, mock_get_repo_root):
        mock_get_repo_root.return_value = self.repo_root
        with patch('sys.argv', ['aos_install.py', '--dry-run', '--tutor']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                aos_install.main(source_package_root=self.source_dir)
                output = fake_out.getvalue()
                self.assertIn("Tutor output is not approval.", output)
                self.assertIn("Tutor output does not authorize execution", output)

if __name__ == '__main__':
    unittest.main()
