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

    def run_registry_test(self, content):
        tmp_dir = ".aos-tmp" if os.path.isdir(".aos-tmp") else None
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", dir=tmp_dir) as f:
            f.write(content)
            temp_path = f.name
        try:
            res, report = self.run_cli(["registry", "--file", temp_path])
            return res, report
        finally:
            os.remove(temp_path)

    # 10. Registry Semantics
    def test_registry_semantics_proposed_passes(self):
        content = "id: PATTERN-001\nstatus: PROPOSED\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")

    def test_registry_semantics_proposed_not_approved_passes(self):
        content = "id: PATTERN-001\nstatus: PROPOSED\napproval_status: NOT_APPROVED\nhuman_review_required: true\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")

    def test_registry_semantics_prose_active_ignored(self):
        content = "id: PATTERN-001\nstatus: PROPOSED\nThey require human review before promotion to ACTIVE.\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")

    def test_registry_semantics_status_active_blocked_no_checkpoint(self):
        content = "id: PATTERN-001\nstatus: ACTIVE\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_registry_semantics_list_status_active_blocked_no_checkpoint(self):
        content = "id: PATTERN-001\n- status: ACTIVE\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_registry_semantics_active_with_checkpoint(self):
        content = "id: PATTERN-001\nstatus: ACTIVE\nhuman_checkpoint: true\napproved_by: User\napproved_at: 2026-07-06\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "HUMAN_REVIEW_REQUIRED")

    def test_registry_semantics_approved_blocked(self):
        content = "id: PATTERN-001\nstatus: PROPOSED\napproval_status: APPROVED\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_registry_semantics_execution_authorized_blocked(self):
        content = "id: PATTERN-001\nstatus: PROPOSED\nexecution_authorized: true\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_registry_semantics_release_authorized_blocked(self):
        content = "id: PATTERN-001\nstatus: PROPOSED\nrelease_authorized: true\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_registry_semantics_default_stack_blocked(self):
        content = "id: PATTERN-001\nstatus: PROPOSED\ndefault_stack: true\n"
        res, report = self.run_registry_test(content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def run_temp_cli(self, command, content):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md") as f:
            f.write(content)
            temp_path = f.name
        try:
            res, report = self.run_cli([command, "--file", temp_path])
            return res, report
        finally:
            os.remove(temp_path)

    def valid_evidence_packet(self):
        return """---
task_id: AOS-FARM.621
document_type: architecture_decision_evidence_packet
packet_status: READY_FOR_HUMAN_REVIEW
recommendation_status: CANDIDATE_ONLY
approval_status: NOT_REQUESTED
is_approval: false
is_execution_authorized: false
is_implementation_authorized: false
is_release_authorized: false
recommendation_confidence: MEDIUM
human_review_required: true
---
"""

    def valid_review_matrix(self):
        return """---
task_id: AOS-FARM.621
document_type: stack_fit_matrix
matrix_status: INCOMPLETE_WEIGHTS
approval_status: NOT_REQUESTED
human_weight_required: true
human_review_required: true
default_stack_selected: false
---

## Criteria weights

| Criterion | Weight | Human weight required | Evidence source |
|---|---|---|---|
| Markdown-first compatibility | UNASSIGNED_BY_HUMAN | true | ADR-0001 |
"""

    def valid_criteria_document(self):
        return """---
task_id: AOS-FARM.621
document_type: architecture_decision_criteria
criteria_status: READY_FOR_HUMAN_WEIGHTING
approval_status: NOT_REQUESTED
human_weight_required: true
human_review_required: true
is_approval: false
---

### Markdown-first compatibility

weight: UNASSIGNED_BY_HUMAN
source: ADR-0001 / registry / project constraint
human_weight_required: true
"""

    # 11. Recommendation Drift Guard: evidence semantics
    def test_evidence_candidate_only_recommendation_passes(self):
        res, report = self.run_temp_cli("evidence", self.valid_evidence_packet())
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")
        self.assertEqual(report.get("document_type"), "architecture_decision_evidence_packet")
        self.assertEqual(report.get("authority_findings"), [])

    def test_evidence_missing_is_approval_false_blocked(self):
        content = self.valid_evidence_packet().replace("is_approval: false\n", "")
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_evidence_missing_recommendation_confidence_requires_human_review(self):
        content = self.valid_evidence_packet().replace("recommendation_confidence: MEDIUM\n", "")
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "HUMAN_REVIEW_REQUIRED")
        self.assertNotEqual(report.get("status"), "PASS")

    def test_evidence_is_approval_true_blocked(self):
        content = self.valid_evidence_packet().replace("is_approval: false", "is_approval: true")
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_evidence_execution_authorized_alias_blocked(self):
        content = self.valid_evidence_packet() + "execution_authorized: true\n"
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_evidence_is_execution_authorized_true_blocked(self):
        content = self.valid_evidence_packet().replace("is_execution_authorized: false", "is_execution_authorized: true")
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_evidence_implementation_authorized_alias_blocked(self):
        content = self.valid_evidence_packet() + "implementation_authorized: true\n"
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_evidence_is_implementation_authorized_true_blocked(self):
        content = self.valid_evidence_packet().replace("is_implementation_authorized: false", "is_implementation_authorized: true")
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_evidence_release_authorized_alias_blocked(self):
        content = self.valid_evidence_packet() + "release_authorized: true\n"
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_evidence_is_release_authorized_true_blocked(self):
        content = self.valid_evidence_packet().replace("is_release_authorized: false", "is_release_authorized: true")
        res, report = self.run_temp_cli("evidence", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    # 12. Recommendation Drift Guard: matrix semantics
    def test_review_matrix_unassigned_human_weight_passes(self):
        res, report = self.run_temp_cli("matrix", self.valid_review_matrix())
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")
        self.assertEqual(report.get("document_type"), "stack_fit_matrix")
        self.assertEqual(report.get("authority_findings"), [])

    def test_review_matrix_criterion_without_weight_blocked(self):
        content = self.valid_review_matrix().replace(
            "| Markdown-first compatibility | UNASSIGNED_BY_HUMAN | true | ADR-0001 |",
            "| Markdown-first compatibility | true | ADR-0001 |"
        )
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_review_matrix_weight_must_blocked(self):
        content = self.valid_review_matrix().replace("UNASSIGNED_BY_HUMAN", "MUST")
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_review_matrix_weight_should_blocked(self):
        content = self.valid_review_matrix().replace("UNASSIGNED_BY_HUMAN", "SHOULD")
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_review_matrix_weight_nice_to_have_blocked(self):
        content = self.valid_review_matrix().replace("UNASSIGNED_BY_HUMAN", "NICE_TO_HAVE")
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_review_matrix_complete_status_blocked(self):
        content = self.valid_review_matrix().replace("matrix_status: INCOMPLETE_WEIGHTS", "matrix_status: COMPLETE")
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_review_matrix_default_stack_true_blocked(self):
        content = self.valid_review_matrix() + "default_stack: true\n"
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_review_matrix_approval_status_approved_blocked(self):
        content = self.valid_review_matrix().replace("approval_status: NOT_REQUESTED", "approval_status: APPROVED")
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_review_matrix_status_active_blocked(self):
        content = self.valid_review_matrix() + "status: ACTIVE\n"
        res, report = self.run_temp_cli("matrix", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    # 13. Recommendation Drift Guard: criteria semantics
    def test_criteria_unassigned_human_weight_passes(self):
        res, report = self.run_temp_cli("criteria", self.valid_criteria_document())
        self.assertEqual(res.returncode, 0)
        self.assertEqual(report.get("status"), "PASS")
        self.assertEqual(report.get("document_type"), "architecture_decision_criteria")
        self.assertEqual(report.get("authority_findings"), [])

    def test_criteria_weight_must_blocked(self):
        content = self.valid_criteria_document().replace("weight: UNASSIGNED_BY_HUMAN", "weight: MUST")
        res, report = self.run_temp_cli("criteria", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    def test_criteria_approval_status_approved_blocked(self):
        content = self.valid_criteria_document().replace("approval_status: NOT_REQUESTED", "approval_status: APPROVED")
        res, report = self.run_temp_cli("criteria", content)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(report.get("status"), "BLOCKED")

    # 14. validate-all semantics
    def test_validate_all_execution(self):
        res, report = self.run_cli(["validate-all", "--json"])
        self.assertEqual(res.returncode, 0)
        self.assertIsNotNone(report)
        self.assertEqual(report.get("status"), "PASS")
        self.assertEqual(report.get("approval_claimed"), False)
        self.assertEqual(report.get("execution_authorized"), False)
        self.assertEqual(report.get("implementation_authorized"), False)
        self.assertEqual(report.get("release_authorized"), False)
        
        checks = report.get("checks", [])
        self.assertTrue(len(checks) > 0)
        
        task_breakdown_checks = [c for c in checks if c.get("checker") == "task-breakdown"]
        self.assertTrue(len(task_breakdown_checks) > 0)
        self.assertEqual(task_breakdown_checks[0].get("result"), "PASS")
        self.assertEqual(task_breakdown_checks[0].get("file"), "tests/fixtures/architecture/valid_task_breakdown_traced.md")
        
        output_str = json.dumps(report)
        self.assertNotIn('"APPROVED"', output_str)
        self.assertNotIn('"READY_FOR_EXECUTION"', output_str)
        
    def test_validate_all_no_recursion(self):
        with open(self.script_path, "r") as f:
            content = f.read()
        self.assertNotIn("aos_validate.py", content)
        self.assertNotIn("aos_doctor.py", content)
        self.assertNotIn("unittest discover", content)
        self.assertNotIn("subprocess", content)
        self.assertNotIn("os.system", content)
        self.assertNotIn("Popen", content)

    def test_get_validate_all_report_import_safe(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        try:
            report = arch_check.get_validate_all_report()
            self.assertIsInstance(report, dict)
            self.assertIn("status", report)
            self.assertEqual(report.get("approval_claimed"), False)
            self.assertEqual(report.get("execution_authorized"), False)
            self.assertEqual(report.get("implementation_authorized"), False)
            self.assertEqual(report.get("release_authorized"), False)
        except SystemExit:
            self.fail("get_validate_all_report raised SystemExit")

    # 15. Structural Contract: Required Files, Markers, Unsafe Claims, Cross References
    def test_structural_required_file_missing(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        original_exists = os.path.exists
        def mock_exists(path):
            if path == "aos/docs/workflow/architecture-input-intake.md":
                return False
            return original_exists(path)
            
        arch_check.os.path.exists = mock_exists
        try:
            report = arch_check.get_validate_all_report()
            self.assertEqual(report.get("status"), "UNKNOWN_BLOCKED")
            missing_check = next((c for c in report["checks"] if c.get("id") == "ARCH-REQ-FILE" and c.get("status") == "UNKNOWN_BLOCKED"), None)
            self.assertIsNotNone(missing_check)
            self.assertEqual(missing_check.get("severity"), "error")
        finally:
            arch_check.os.path.exists = original_exists

    def test_structural_marker_missing_hard(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        original_read_text = arch_check.read_text
        def mock_read_text(path):
            if path == "aos/docs/workflow/architecture-decision-layer.md":
                return "Just some text without safety boundary", None
            return original_read_text(path)
            
        arch_check.read_text = mock_read_text
        try:
            report = arch_check.get_validate_all_report()
            # It now yields a WARNING because canonical doc alignment is outside scope
            # Warning does not block validate-all, so overall is PASS
            self.assertEqual(report.get("status"), "PASS")
            missing_check = next((c for c in report["checks"] if c.get("id") == "ARCH-MARKER-HARD" and c.get("status") == "WARNING"), None)
            self.assertIsNotNone(missing_check)
            self.assertIn("canonical doc alignment required", missing_check.get("message", ""))
        finally:
            arch_check.read_text = original_read_text

    def test_structural_marker_missing_recommended(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        original_read_text = arch_check.read_text
        
        # provide a text with hard boundaries but missing recommended
        def mock_read_text(path):
            if path == "aos/docs/workflow/architecture-decision-layer.md":
                text = "approval not claimed\nhuman review required\nimplementation not authorized\nrelease not authorized\nUNKNOWN not OK\nNOT_RUN not PASS\nPASS not approval\nEvidence not approval\nCI PASS not approval\nhuman approval cannot be simulated"
                return text, None
            return original_read_text(path)
            
        arch_check.read_text = mock_read_text
        try:
            report = arch_check.get_validate_all_report()
            missing_check = next((c for c in report["checks"] if c.get("id") == "ARCH-MARKER-REC" and c.get("status") == "WARNING"), None)
            self.assertIsNotNone(missing_check)
            # Warning does not bubble to overall FAILED/BLOCKED if it's just warning
            self.assertEqual(report.get("status"), "PASS") 
        finally:
            arch_check.read_text = original_read_text

    def test_structural_unsafe_positive_claim(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        original_read_text = arch_check.read_text
        def mock_read_text(path):
            if path == "aos/docs/workflow/architecture-decision-layer.md":
                return "The architecture approved and is ready.", None
            return original_read_text(path)
            
        arch_check.read_text = mock_read_text
        try:
            report = arch_check.get_validate_all_report()
            # FAILED maps to FAILED or FAILED_OR_BLOCKED in overall status depending on hierarchy, 
            # the hierarchy considers FAILED (2) less severe than UNKNOWN_BLOCKED (4).
            # We just need to check the exact check status
            check = next((c for c in report["checks"] if c.get("id") == "ARCH-UNSAFE-CLAIM" and c.get("status") == "FAILED"), None)
            self.assertIsNotNone(check)
            self.assertIn("architecture approved", check["message"].lower())
        finally:
            arch_check.read_text = original_read_text
            
    def test_structural_negative_claim_allowed(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        original_read_text = arch_check.read_text
        def mock_read_text(path):
            if path == "aos/docs/workflow/architecture-decision-layer.md":
                return "approval_claimed: false", None
            return original_read_text(path)
            
        arch_check.read_text = mock_read_text
        try:
            report = arch_check.get_validate_all_report()
            checks = [c for c in report["checks"] if c.get("id") == "ARCH-UNSAFE-CLAIM" and "approval_claimed: false" in c.get("message", "").lower()]
            self.assertEqual(len(checks), 0)
        finally:
            arch_check.read_text = original_read_text
            
    def test_structural_ambiguous_claim_unknown_blocked(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        original_read_text = arch_check.read_text
        def mock_read_text(path):
            if path == "aos/docs/workflow/architecture-decision-layer.md":
                return "approval state unclear but ready_for_execution mentioned", None
            return original_read_text(path)
            
        arch_check.read_text = mock_read_text
        try:
            report = arch_check.get_validate_all_report()
            # It should trigger UNKNOWN_BLOCKED on the check
            check = next((c for c in report["checks"] if c.get("id") == "ARCH-UNSAFE-CLAIM" and c.get("status") == "UNKNOWN_BLOCKED"), None)
            self.assertIsNotNone(check)
        finally:
            arch_check.read_text = original_read_text
            
    def test_cross_reference_missing(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        original_read_text = arch_check.read_text
        def mock_read_text(path):
            if path == "aos/START_HERE.md":
                return "Just empty text", None
            return original_read_text(path)
            
        arch_check.read_text = mock_read_text
        try:
            report = arch_check.get_validate_all_report()
            check = next((c for c in report["checks"] if c.get("id") == "ARCH-REF-START-HERE" and c.get("status") == "WARNING"), None)
            self.assertIsNotNone(check)
        finally:
            arch_check.read_text = original_read_text

    def test_json_includes_new_fields(self):
        import aos.scripts.aos_architecture_document_check as arch_check
        report = arch_check.get_validate_all_report()
        self.assertIn("summary", report)
        self.assertIn("passed", report["summary"])
        self.assertIn("warnings", report["summary"])
        self.assertIn("failed", report["summary"])
        self.assertIn("blocked", report["summary"])
        self.assertIn("not_run", report["summary"])
        self.assertEqual(report.get("human_review_required"), True)

if __name__ == '__main__':
    unittest.main()
