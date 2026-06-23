import tempfile
import unittest
from pathlib import Path

from agentos.pipelines.document_pipeline import ingest_batch, ingest_directory
from agentos.pipelines.document_manifest import DocumentManifest


class DocumentManifestTests(unittest.TestCase):
    def test_ingest_batch_deduplicates_by_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path1 = Path(tmpdir) / "notes.txt"
            path1.write_text("same content", encoding="utf-8")
            
            path2 = Path(tmpdir) / "duplicate.txt"
            path2.write_text("same content", encoding="utf-8")
            
            manifest = ingest_batch([path1, path1, path2])
            
            # Since document_id includes filename, path1 and path2 have DIFFERENT IDs 
            # because the filenames ("notes.txt" vs "duplicate.txt") are different.
            # But path1 duplicated in the list should be deduplicated.
            self.assertEqual(manifest.total_documents, 2)
            self.assertEqual(manifest.parsed_documents, 2)
            self.assertEqual(manifest.warning_documents, 0)
            self.assertEqual(manifest.rejected_documents, 0)

    def test_ingest_directory_aggregates_stats_and_warnings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1 parsed
            (Path(tmpdir) / "doc1.txt").write_text("text", encoding="utf-8")
            # 1 warning (pdf)
            (Path(tmpdir) / "doc2.pdf").write_bytes(b"%PDF-1.4")
            # 1 rejected (png)
            (Path(tmpdir) / "doc3.png").write_bytes(b"image")
            
            manifest = ingest_directory(tmpdir)
            
            self.assertEqual(manifest.total_documents, 3)
            self.assertEqual(manifest.parsed_documents, 1)
            self.assertEqual(manifest.warning_documents, 1)
            self.assertEqual(manifest.rejected_documents, 1)
            
            warnings = manifest.aggregated_warnings
            self.assertEqual(len(warnings), 2)
            self.assertTrue(any("doc2.pdf" in w for w in warnings))
            self.assertTrue(any("doc3.png" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
