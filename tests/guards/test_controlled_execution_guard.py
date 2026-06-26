from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import shutil
import unittest

MODULE_PATH = Path("aos/tools/optional/controlled_execution_guard.py").resolve()
SPEC = importlib.util.spec_from_file_location("aos_controlled_execution_guard_core", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
import sys
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

BLOCKED = MODULE.BLOCKED
HUMAN_REVIEW_REQUIRED = MODULE.HUMAN_REVIEW_REQUIRED
PASS = MODULE.PASS
UNKNOWN_BLOCKED = MODULE.UNKNOWN_BLOCKED
postcheck = MODULE.postcheck
precheck = MODULE.precheck
scopecheck = MODULE.scopecheck
guard_main = MODULE.main

FIXTURES = Path("aos/reports/examples/controlled-execution-guard/fixtures")
REPORT_FIXTURES = FIXTURES / "reports"


class ControlledExecutionGuardTests(unittest.TestCase):
    def test_valid_package_passes_precheck(self):
        result = precheck(FIXTURES / "valid_package.yaml")
        self.assertEqual(result.status, PASS)

    def test_missing_human_authorization_blocks(self):
        result = precheck(FIXTURES / "missing_human_authorization.yaml")
        self.assertEqual(result.status, BLOCKED)

    def test_missing_risk_profile_blocks_or_requires_human_review(self):
        result = precheck(FIXTURES / "missing_risk_profile.yaml")
        self.assertIn(result.status, {HUMAN_REVIEW_REQUIRED, UNKNOWN_BLOCKED})

    def test_risk_profile_not_human_assigned_requires_human_review(self):
        result = precheck(FIXTURES / "risk_profile_not_human_assigned.yaml")
        self.assertEqual(result.status, HUMAN_REVIEW_REQUIRED)

    def test_missing_authorized_files_blocks(self):
        result = precheck(FIXTURES / "missing_authorized_files.yaml")
        self.assertEqual(result.status, BLOCKED)

    def test_unknown_scope_unknown_blocked(self):
        result = precheck(FIXTURES / "unknown_scope.yaml")
        self.assertEqual(result.status, UNKNOWN_BLOCKED)

    def test_not_run_cannot_be_pass(self):
        result = postcheck(FIXTURES / "valid_package.yaml", REPORT_FIXTURES / "not_run_treated_as_pass.md")
        self.assertEqual(result.status, BLOCKED)

    def test_approval_claim_blocks(self):
        result = precheck(FIXTURES / "approval_claimed.yaml")
        self.assertEqual(result.status, BLOCKED)

    def test_evidence_cannot_claim_approval(self):
        result = postcheck(FIXTURES / "valid_package.yaml", REPORT_FIXTURES / "approval_claimed_report.md")
        self.assertEqual(result.status, BLOCKED)

    def test_commit_claim_blocks(self):
        result = precheck(FIXTURES / "commit_claimed.yaml")
        self.assertEqual(result.status, BLOCKED)

    def test_push_claim_blocks(self):
        result = precheck(FIXTURES / "push_claimed.yaml")
        self.assertEqual(result.status, BLOCKED)

    def test_changed_file_outside_scope_blocks(self):
        result = scopecheck(
            FIXTURES / "changed_file_outside_scope.yaml",
            FIXTURES / "changed_file_outside_scope.yaml",
        )
        self.assertEqual(result.status, BLOCKED)

    def test_missing_evidence_blocks(self):
        result = postcheck(FIXTURES / "valid_package.yaml", REPORT_FIXTURES / "missing_evidence_report.md")
        self.assertEqual(result.status, BLOCKED)

    def test_guard_pass_does_not_emit_approval(self):
        result = precheck(FIXTURES / "valid_package.yaml")
        dumped = result.to_dict()
        self.assertEqual(dumped["status"], PASS)
        self.assertNotIn("approved", dumped["details"])

    def test_guard_pass_does_not_emit_commit_authorization(self):
        result = precheck(FIXTURES / "valid_package.yaml")
        dumped = result.to_dict()
        self.assertNotIn("commit_authorized", dumped["details"])

    def test_guard_pass_does_not_emit_push_authorization(self):
        result = precheck(FIXTURES / "valid_package.yaml")
        dumped = result.to_dict()
        self.assertNotIn("push_authorized", dumped["details"])

    def test_runtime_mode_does_not_require_development_sources_inside_aos(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            aos_root = project_root / "aos"
            target_fixture_dir = aos_root / "reports" / "examples" / "controlled-execution-guard" / "fixtures"
            target_checkpoint_dir = aos_root / "reports" / "human-checkpoints" / "examples"
            target_fixture_dir.mkdir(parents=True)
            (target_fixture_dir / "reports").mkdir(parents=True)
            target_checkpoint_dir.mkdir(parents=True)
            shutil.copy(FIXTURES / "valid_package.yaml", target_fixture_dir / "valid_package.yaml")
            shutil.copy(REPORT_FIXTURES / "valid_report.md", target_fixture_dir / "reports" / "valid_report.md")
            shutil.copy(
                Path("aos/reports/human-checkpoints/examples/aos-farm-438-controlled-execution-authorization-example.md"),
                target_checkpoint_dir / "aos-farm-438-controlled-execution-authorization-example.md",
            )

            result = precheck(
                "reports/examples/controlled-execution-guard/fixtures/valid_package.yaml",
                project_root=project_root,
                aos_root=aos_root,
            )
            self.assertEqual(result.status, PASS)
            self.assertFalse((project_root / "00_AOS_Core_Control.md").exists())

    def test_aos_root_and_project_root_are_accepted_and_used(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            aos_root = project_root / "embedded-aos"
            target_fixture_dir = aos_root / "reports" / "examples" / "controlled-execution-guard" / "fixtures"
            target_checkpoint_dir = aos_root / "reports" / "human-checkpoints" / "examples"
            target_fixture_dir.mkdir(parents=True)
            target_checkpoint_dir.mkdir(parents=True)
            shutil.copy(FIXTURES / "valid_package.yaml", target_fixture_dir / "valid_package.yaml")
            shutil.copy(
                Path("aos/reports/human-checkpoints/examples/aos-farm-438-controlled-execution-authorization-example.md"),
                target_checkpoint_dir / "aos-farm-438-controlled-execution-authorization-example.md",
            )

            exit_code = guard_main(
                [
                    "--project-root",
                    str(project_root),
                    "--aos-root",
                    str(aos_root),
                    "precheck",
                    "--package",
                    "reports/examples/controlled-execution-guard/fixtures/valid_package.yaml",
                ]
            )
            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
