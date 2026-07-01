import tempfile
import unittest
from pathlib import Path

from aos.pipelines.document_pipeline import ingest_document, ingest_path


class DocumentPipelineTests(unittest.TestCase):
    def test_ingests_markdown_as_text_record(self):
        record = ingest_document("policy.md", "# Policy\nUse local docs only.")

        self.assertEqual(record.metadata.filename, "policy.md")
        self.assertEqual(record.metadata.extension, ".md")
        self.assertEqual(record.metadata.content_type, "text/markdown")
        self.assertEqual(record.metadata.byte_size, len("# Policy\nUse local docs only.".encode("utf-8")))
        self.assertEqual(record.parser_status, "parsed")
        self.assertEqual(record.index_status, "ready_for_local_index")
        self.assertEqual(record.text, "# Policy\nUse local docs only.")
        self.assertEqual(record.warnings, ())

    def test_document_id_is_deterministic_for_same_input(self):
        first = ingest_document("notes.txt", b"same bytes")
        second = ingest_document("notes.txt", b"same bytes")

        self.assertEqual(first.document_id, second.document_id)

    def test_pdf_is_warning_based_metadata_only(self):
        record = ingest_document("handbook.pdf", b"%PDF-1.7")

        self.assertEqual(record.metadata.extension, ".pdf")
        self.assertEqual(record.metadata.content_type, "application/pdf")
        self.assertEqual(record.parser_status, "warning")
        self.assertEqual(record.index_status, "not_indexed_parser_warning")
        self.assertIsNone(record.text)
        self.assertIn("PDF parser is not implemented", record.warnings[0])

    def test_docx_is_warning_based_metadata_only(self):
        record = ingest_document("handbook.docx", b"PK\x03\x04")

        self.assertEqual(record.metadata.extension, ".docx")
        self.assertEqual(record.parser_status, "warning")
        self.assertEqual(record.index_status, "not_indexed_parser_warning")
        self.assertIsNone(record.text)
        self.assertIn("DOCX parser is not implemented", record.warnings[0])

    def test_unsupported_extension_is_rejected_not_parsed(self):
        record = ingest_document("image.png", b"not a document")

        self.assertEqual(record.metadata.extension, ".png")
        self.assertEqual(record.metadata.content_type, "application/octet-stream")
        self.assertEqual(record.parser_status, "rejected")
        self.assertEqual(record.index_status, "not_indexed_rejected")
        self.assertIsNone(record.text)
        self.assertIn("Unsupported document extension", record.warnings[0])

    def test_ingest_path_reads_local_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "local.txt"
            path.write_text("local content", encoding="utf-8")

            record = ingest_path(path)

        self.assertEqual(record.metadata.filename, "local.txt")
        self.assertEqual(record.text, "local content")
        self.assertEqual(record.parser_status, "parsed")

    def test_invalid_utf8_text_is_warning_based_best_effort(self):
        record = ingest_document("legacy.txt", b"\xff")

        self.assertEqual(record.parser_status, "parsed")
        self.assertEqual(record.text, "\ufffd")
        self.assertEqual(
            record.warnings,
            ("Text decoded with replacement characters after UTF-8 decode warning.",),
        )


if __name__ == "__main__":
    unittest.main()
