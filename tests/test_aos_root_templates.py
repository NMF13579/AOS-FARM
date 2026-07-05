import os
import unittest
from pathlib import Path

class TestAOSRootTemplates(unittest.TestCase):
    def setUp(self):
        self.current_dir = Path(__file__).parent.resolve()
        self.repo_root = self.current_dir.parent
        self.aos_root = self.repo_root / "aos" / "root"

    def test_root_templates_are_not_identical_placeholders(self):
        guide = (self.aos_root / "ROOT_INSTALL_GUIDE.md").read_text()
        manifest = (self.aos_root / "ROOT_FILES_MANIFEST.md").read_text()
        section = (self.aos_root / "README_AOS_SECTION.md").read_text()
        snippet = (self.aos_root / "gitignore.snippet").read_text()

        self.assertNotEqual(guide, manifest)
        self.assertNotEqual(guide, section)
        self.assertNotEqual(manifest, section)
        self.assertNotEqual(snippet, guide)

    def test_gitignore_snippet_is_gitignore_content(self):
        snippet = (self.aos_root / "gitignore.snippet").read_text()
        self.assertIn("/.aos-tmp/", snippet)
        self.assertNotIn("AOS is a self-contained consumer kit.", snippet)

    def test_root_manifest_mentions_required_root_files(self):
        manifest = (self.aos_root / "ROOT_FILES_MANIFEST.md").read_text()
        self.assertIn("AGENTS.md", manifest)
        self.assertIn("llms.txt", manifest)

    def test_root_install_guide_mentions_manual_transfer(self):
        guide = (self.aos_root / "ROOT_INSTALL_GUIDE.md").read_text()
        self.assertIn("Copy `/aos/`", guide)
        self.assertIn("Manual Transfer Steps", guide)

    def test_gitignore_template_exists_and_contains_aos_block(self):
        template = (self.aos_root / ".gitignore.template").read_text()
        self.assertIn("/.aos-tmp/", template)

if __name__ == '__main__':
    unittest.main()
