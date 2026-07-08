import os
import re
import unittest


class TestAOSExecutorHandoffTemplate(unittest.TestCase):
    def setUp(self):
        self.template_path = "aos/templates/execution-packages/executor-handoff-package-template.yaml"
        self.readme_path = "aos/templates/execution-packages/README.md"
        self.controlled_template_path = (
            "aos/templates/execution-packages/controlled-execution-package-template.yaml"
        )
        for path in [self.template_path, self.readme_path, self.controlled_template_path]:
            self.assertTrue(os.path.exists(path), f"{path} not found")
        with open(self.template_path, "r", encoding="utf-8") as f:
            self.template = f.read()
        with open(self.readme_path, "r", encoding="utf-8") as f:
            self.readme = f.read()
        with open(self.controlled_template_path, "r", encoding="utf-8") as f:
            self.controlled_template = f.read()
        self.normalized_template = re.sub(r"\s+", " ", self.template)
        self.normalized_readme = re.sub(r"\s+", " ", self.readme)

    def assert_false_default(self, field):
        self.assertRegex(self.template, rf"(?m)^\s*{field}:\s*false\s*$")

    def test_neutral_executor_handoff_template_exists_with_required_sections(self):
        for required in [
            "task_id:",
            "source_task_brief_path:",
            "scope:",
            "allowed_changes:",
            "forbidden_changes:",
            "non_goals:",
            "validation_instructions:",
            "expected_final_report:",
            "risk_profile:",
            "human_witness:",
            "known_unknowns_and_blockers:",
            "protected_canonical_boundary:",
            "destructive_operation_boundary:",
            "approval_boundary:",
            "execution_authorization_boundary:",
            "commit_boundary:",
            "push_boundary:",
            "merge_boundary:",
            "release_boundary:",
            "lifecycle_mutation_boundary:",
            "scope_expansion_boundary:",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, self.template)

    def test_neutral_executor_handoff_false_default_authorizations(self):
        for field in [
            "approval_granted",
            "execution_authorized",
            "commit_authorized",
            "push_authorized",
            "merge_authorized",
            "release_authorized",
            "scope_expansion_authorized",
            "protected_canonical_change_authorized",
            "destructive_operation_authorized",
            "lifecycle_mutation_authorized",
        ]:
            with self.subTest(field=field):
                self.assert_false_default(field)

    def test_neutral_executor_handoff_requires_human_boundaries(self):
        self.assertRegex(self.template, r"(?m)^\s*requires_human_review:\s*true\s*$")
        self.assertRegex(
            self.template,
            r"(?m)^\s*requires_human_execution_authorization:\s*true\s*$",
        )
        self.assertNotRegex(self.template, r"(?m)^\s*requires_human_review:\s*false\s*$")

    def test_neutral_executor_handoff_excludes_unsafe_permissions(self):
        for boundary in [
            "Executor Handoff Package is not approval",
            "Executor Handoff Package is not execution authorization",
            "does not grant commit, push, merge, release, lifecycle mutation, destructive operation, protected/canonical mutation, or scope expansion",
            "Readiness is not execution permission",
            "Evidence is not approval",
            "Validator PASS is not approval",
        ]:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.normalized_template)

    def test_controlled_execution_package_requires_explicit_human_authorization(self):
        self.assertIn("human_execution_authorization:", self.controlled_template)
        self.assertRegex(self.controlled_template, r"(?m)^\s*authorized:\s*true\s*$")
        self.assertIn("authorized_by: human", self.controlled_template)
        self.assertIn("authorization_artifact:", self.controlled_template)
        self.assertIn(
            "Controlled Execution Package is the authorized execution context only after explicit human execution authorization exists",
            self.normalized_readme,
        )


if __name__ == "__main__":
    unittest.main()
