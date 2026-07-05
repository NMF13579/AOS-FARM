import unittest
import subprocess
import os
import json
import sys
import tempfile

class TestAosArchitectureDocumentCheck(unittest.TestCase):
    def setUp(self):
        self.script_path = "aos/scripts/aos_architecture_document_check.py"
        self.assertTrue(os.path.exists(self.script_path), "Script not found at expected path")

    def run_cli(self, args):
        cmd = [sys.executable, self.script_path] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError:
            report = None
        return result, report

    # 1. Brief
    def test_valid_brief(self):
        res, report = self.run_cli(["brief", "--file", "tests/fixtures/architecture/valid_architecture_brief.md"])
        self.assertEqual(res.returncode, 0)
        self.assertIsNotNone(report)
        self.assertEqual(report.get("status"), "PASS")

    def test_invalid_brief_missing_fields(self):
        res, report = self.run_cli(["brief", "--file", "tests/fixtures/architecture/invalid_brief_missing_required_field.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_invalid_brief_positive_authority(self):
        res, report = self.run_cli(["brief", "--file", "tests/fixtures/architecture/invalid_brief_positive_authority.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_invalid_brief_missing_unknown_handling(self):
        res, report = self.run_cli(["brief", "--file", "tests/fixtures/architecture/invalid_brief_missing_unknown_handling.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "UNKNOWN_BLOCKED")

    # 2. ADR
    def test_valid_adr(self):
        res, report = self.run_cli(["adr", "--file", "tests/fixtures/architecture/valid_mini_adr_proposed.md"])
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")

    def test_invalid_adr_execution_authorized(self):
        res, report = self.run_cli(["adr", "--file", "tests/fixtures/architecture/invalid_mini_adr_execution_authorized.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_invalid_adr_missing_arch_ref(self):
        res, report = self.run_cli(["adr", "--file", "tests/fixtures/architecture/invalid_mini_adr_missing_architecture_ref.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    # 3. Matrix
    def test_valid_matrix(self):
        res, report = self.run_cli(["matrix", "--file", "tests/fixtures/architecture/valid_pattern_fit_matrix.md"])
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")

    def test_invalid_matrix_missing_unknowns(self):
        res, report = self.run_cli(["matrix", "--file", "tests/fixtures/architecture/invalid_matrix_missing_unknowns.md"])
        self.assertEqual(res.returncode, 1)
        self.assertIn(report.get("status"), ["UNKNOWN_BLOCKED", "BLOCKED"])

    def test_invalid_matrix_unknown_decision(self):
        res, report = self.run_cli(["matrix", "--file", "tests/fixtures/architecture/invalid_matrix_unknown_decision.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    # 4. Registry
    def test_valid_registry_proposed(self):
        res, report = self.run_cli(["registry", "--file", "tests/fixtures/architecture/valid_pattern_registry_proposed_only.md"])
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")

    def test_invalid_registry_active_no_checkpoint(self):
        res, report = self.run_cli(["registry", "--file", "tests/fixtures/architecture/invalid_pattern_registry_active_without_checkpoint.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_valid_registry_active_with_checkpoint(self):
        res, report = self.run_cli(["registry", "--file", "tests/fixtures/architecture/valid_registry_active_with_checkpoint_marker_human_review_required.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "HUMAN_REVIEW_REQUIRED")

    def test_invalid_registry_approved(self):
        res, report = self.run_cli(["registry", "--file", "tests/fixtures/architecture/invalid_stack_preset_registry_approved.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    # 5. Task Breakdown
    def test_valid_task_breakdown(self):
        res, report = self.run_cli(["task-breakdown", "--file", "tests/fixtures/architecture/valid_task_breakdown_traced.md"])
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")

    def test_invalid_task_breakdown_missing_origins(self):
        res, report = self.run_cli(["task-breakdown", "--file", "tests/fixtures/architecture/invalid_task_breakdown_missing_origin.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_invalid_task_breakdown_ready_for_execution(self):
        res, report = self.run_cli(["task-breakdown", "--file", "tests/fixtures/architecture/invalid_task_breakdown_ready_for_execution.md"])
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    # 6. Negative invariants
    def test_negative_invariants(self):
        content = """architecture_brief_id: AB-001
version: 0.1
status: DRAFT
technical_assignment_ref: TA-001
pattern_refs: [PATTERN-001]
stack_preset_refs: [STACK-001]
unknown_records: none
conflict_records: none
human_checkpoints: required
PASS ≠ approval.
READY_FOR_TASK_BREAKDOWN ≠ APPROVED.
READY_FOR_TASK_BREAKDOWN ≠ READY_FOR_EXECUTION.
Validator PASS does not authorize execution.
Validator PASS does not authorize commit.
Validator PASS does not authorize push.
Validator PASS does not authorize release.
HUMAN_REVIEW_REQUIRED does not mean approval exists.
"""
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            res, report = self.run_cli(["brief", "--file", temp_path])
            self.assertEqual(res.returncode, 0)
            self.assertEqual(report.get("status"), "PASS")
            auth_findings = report.get("authority_findings", [])
            self.assertEqual(len(auth_findings), 0)
        finally:
            os.remove(temp_path)

    # 7. Positive unsafe status
    def test_positive_unsafe_status(self):
        content = """architecture_brief_id: AB-001
version: 0.1
status: READY_FOR_EXECUTION
technical_assignment_ref: TA-001
pattern_refs: [PATTERN-001]
stack_preset_refs: [STACK-001]
unknown_records: none
conflict_records: none
human_checkpoints: required
"""
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            res, report = self.run_cli(["brief", "--file", temp_path])
            self.assertEqual(res.returncode, 1)
            self.assertEqual(report.get("status"), "BLOCKED")
            auth_findings = report.get("authority_findings", [])
            self.assertTrue(len(auth_findings) > 0, "Expected authority findings for unsafe status")
        finally:
            os.remove(temp_path)

    # 8. Unsafe Status Tokens tests
    def test_unsafe_status_not_approved_allowed(self):
        content = """adr_id: ADR-TEST
title: Test
status: PROPOSED
decided_by: User
technical_assignment_ref: none
architecture_brief_ref: none
related_patterns: none
related_unknowns: none
related_conflicts: none
approval_status: NOT_APPROVED
"""
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        try:
            res, report = self.run_cli(["adr", "--file", temp_path])
            self.assertEqual(res.returncode, 0)
            self.assertEqual(report.get("status"), "PASS")
        finally:
            os.remove(temp_path)

    def test_unsafe_status_approved_blocked(self):
        content = """adr_id: ADR-TEST\ntitle: Test\nstatus: APPROVED\ndecided_by: User\ntechnical_assignment_ref: none\narchitecture_brief_ref: none\nrelated_patterns: none\nrelated_unknowns: none\nrelated_conflicts: none\napproval_status: NOT_APPROVED\n"""
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        try:
            res, report = self.run_cli(["adr", "--file", temp_path])
            self.assertEqual(res.returncode, 1)
            self.assertEqual(report.get("status"), "BLOCKED")
        finally:
            os.remove(temp_path)

    def test_unsafe_status_approval_status_approved_blocked(self):
        content = """adr_id: ADR-TEST\ntitle: Test\nstatus: PROPOSED\ndecided_by: User\ntechnical_assignment_ref: none\narchitecture_brief_ref: none\nrelated_patterns: none\nrelated_unknowns: none\nrelated_conflicts: none\napproval_status: APPROVED\n"""
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        try:
            res, report = self.run_cli(["adr", "--file", temp_path])
            self.assertEqual(res.returncode, 1)
            self.assertEqual(report.get("status"), "BLOCKED")
        finally:
            os.remove(temp_path)

    def test_unsafe_status_ready_for_execution_blocked(self):
        content = """adr_id: ADR-TEST\ntitle: Test\nstatus: READY_FOR_EXECUTION\ndecided_by: User\ntechnical_assignment_ref: none\narchitecture_brief_ref: none\nrelated_patterns: none\nrelated_unknowns: none\nrelated_conflicts: none\napproval_status: NOT_APPROVED\n"""
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        try:
            res, report = self.run_cli(["adr", "--file", temp_path])
            self.assertEqual(res.returncode, 1)
            self.assertEqual(report.get("status"), "BLOCKED")
        finally:
            os.remove(temp_path)

    def test_unsafe_status_release_ready_blocked(self):
        content = """adr_id: ADR-TEST\ntitle: Test\nstatus: RELEASE_READY\ndecided_by: User\ntechnical_assignment_ref: none\narchitecture_brief_ref: none\nrelated_patterns: none\nrelated_unknowns: none\nrelated_conflicts: none\napproval_status: NOT_APPROVED\n"""
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        try:
            res, report = self.run_cli(["adr", "--file", temp_path])
            self.assertEqual(res.returncode, 1)
            self.assertEqual(report.get("status"), "BLOCKED")
        finally:
            os.remove(temp_path)

    # 9. Help / Unknown commands
    def test_help_command(self):
        cmd = [sys.executable, self.script_path, "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("AOS Architecture Document Check CLI", result.stdout)

    def test_unknown_command(self):
        res, report = self.run_cli(["invalid-command"])
        self.assertEqual(res.returncode, 2)
        self.assertIsNotNone(report)
        self.assertEqual(report.get("status"), "CLI_USAGE_ERROR")

if __name__ == '__main__':
    unittest.main()
