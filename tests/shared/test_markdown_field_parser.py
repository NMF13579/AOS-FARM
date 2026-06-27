from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import textwrap
import unittest
import sys

MODULE_PATH = Path("aos/tools/optional/markdown_field_parser.py").resolve()
SPEC = importlib.util.spec_from_file_location("aos_markdown_field_parser", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

NOT_RUN = MODULE.NOT_RUN
UNKNOWN = MODULE.UNKNOWN
parse_boolean_field = MODULE.parse_boolean_field
parse_markdown_file = MODULE.parse_markdown_file
parse_markdown_text = MODULE.parse_markdown_text


class MarkdownFieldParserTests(unittest.TestCase):
    def test_simple_string_field_extraction(self):
        result = parse_markdown_text("task_id: AOS-FARM.441.3\n")
        self.assertEqual(result.fields["task_id"], "AOS-FARM.441.3")

    def test_boolean_true_extraction(self):
        result = parse_markdown_text("approved: true\n")
        self.assertIs(result.fields["approved"], True)
        self.assertIs(parse_boolean_field(result.fields, "approved"), True)

    def test_boolean_false_extraction(self):
        result = parse_markdown_text("commit_performed: false\n")
        self.assertIs(result.fields["commit_performed"], False)
        self.assertIs(parse_boolean_field(result.fields, "commit_performed"), False)

    def test_status_field_extraction(self):
        result = parse_markdown_text("final_status: HUMAN_REVIEW_REQUIRED\n")
        self.assertEqual(
            result.status_fields,
            {"final_status": "HUMAN_REVIEW_REQUIRED"},
        )

    def test_missing_required_fields_reported(self):
        result = parse_markdown_text(
            "task_id: AOS-FARM.441.3\n",
            required_fields=["task_id", "branch", "final_status"],
        )
        self.assertEqual(result.missing_required_fields, ["branch", "final_status"])

    def test_comments_and_blank_lines_are_handled_safely(self):
        text = textwrap.dedent(
            """

            <!-- comment -->
            // comment
            # Heading
            branch: build/deterministic-control-helpers-mvp

            """
        )
        result = parse_markdown_text(text)
        self.assertEqual(
            result.fields["branch"],
            "build/deterministic-control-helpers-mvp",
        )
        self.assertEqual(result.malformed_lines, [])
        self.assertEqual(len(result.ignored_lines), 1)

    def test_duplicate_key_handling_is_deterministic(self):
        result = parse_markdown_text(
            "status: DRAFT\nstatus: HUMAN_REVIEW_REQUIRED\n"
        )
        self.assertEqual(result.fields["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(result.duplicate_keys, ["status"])

    def test_malformed_lines_do_not_crash_parser(self):
        text = "task_id AOS-FARM.441.3\n: broken\nbranch: build/example\n"
        result = parse_markdown_text(text)
        self.assertEqual(result.fields["branch"], "build/example")
        self.assertEqual(len(result.malformed_lines), 1)
        self.assertEqual(len(result.ignored_lines), 1)

    def test_unknown_remains_unknown_and_blocking(self):
        result = parse_markdown_text("status: UNKNOWN\n")
        self.assertEqual(result.status_fields["status"], UNKNOWN)
        self.assertEqual(result.blocking_status_fields["status"], UNKNOWN)
        self.assertNotEqual(result.status_fields["status"], "OK")

    def test_not_run_remains_not_run_and_not_pass(self):
        result = parse_markdown_text("validation_result: NOT_RUN\n")
        self.assertEqual(result.status_fields["validation_result"], NOT_RUN)
        self.assertEqual(result.blocking_status_fields["validation_result"], NOT_RUN)
        self.assertNotEqual(result.status_fields["validation_result"], "PASS")

    def test_parse_markdown_file_reads_markdown_from_disk(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "report.md"
            path.write_text("task_id: AOS-FARM.441.3\n", encoding="utf-8")
            result = parse_markdown_file(path)
        self.assertEqual(result.fields["task_id"], "AOS-FARM.441.3")


if __name__ == "__main__":
    unittest.main()
