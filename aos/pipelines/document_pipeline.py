from __future__ import annotations
"""Minimal local document pipeline boundary.

This module intentionally stops at intake, metadata extraction, best-effort
text parsing, warning-based parser states, and local processing/index status.
It does not implement retrieval, chat, embeddings, vector storage, analytics,
network calls, production RAG, or workflow wiring.
"""



from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Optional, Sequence, Mapping, TYPE_CHECKING
import os



TEXT_EXTENSIONS = {".txt", ".md"}
WARNING_ONLY_EXTENSIONS = {".pdf", ".docx"}


@dataclass(frozen=True)
class DocumentMetadata:
    filename: str
    extension: str
    byte_size: int
    content_type: str


@dataclass(frozen=True)
class DocumentPipelineRecord:
    document_id: str
    metadata: DocumentMetadata
    parser_status: str
    index_status: str
    text: Optional[str]
    warnings: tuple[str, ...]


def ingest_path(path: str | Path) -> DocumentPipelineRecord:
    """Read a local file and process it through the document pipeline boundary."""
    file_path = Path(path)
    return ingest_document(file_path.name, file_path.read_bytes())


def ingest_document(filename: str, content: bytes | str) -> DocumentPipelineRecord:
    """Create a deterministic local document-pipeline record.

    TXT and MD content are parsed as best-effort UTF-8 text. PDF and DOCX are
    accepted as bounded warning states without claiming parser coverage.
    Unsupported extensions are rejected without raising for normal inputs.
    """
    content_bytes = _to_bytes(content)
    metadata = _metadata(filename, content_bytes)
    document_id = _document_id(metadata.filename, content_bytes)

    if metadata.extension in TEXT_EXTENSIONS:
        text, warnings = _parse_text(content_bytes)
        return DocumentPipelineRecord(
            document_id=document_id,
            metadata=metadata,
            parser_status="parsed",
            index_status="ready_for_local_index",
            text=text,
            warnings=warnings,
        )

    if metadata.extension in WARNING_ONLY_EXTENSIONS:
        return DocumentPipelineRecord(
            document_id=document_id,
            metadata=metadata,
            parser_status="warning",
            index_status="not_indexed_parser_warning",
            text=None,
            warnings=(
                f"{metadata.extension[1:].upper()} parser is not implemented in slice 1; "
                "document accepted for metadata only.",
            ),
        )

    return DocumentPipelineRecord(
        document_id=document_id,
        metadata=metadata,
        parser_status="rejected",
        index_status="not_indexed_rejected",
        text=None,
        warnings=(f"Unsupported document extension: {metadata.extension or '<none>'}.",),
    )


def _metadata(filename: str, content: bytes) -> DocumentMetadata:
    normalized_name = Path(filename).name.strip()
    extension = Path(normalized_name).suffix.lower()
    return DocumentMetadata(
        filename=normalized_name,
        extension=extension,
        byte_size=len(content),
        content_type=_content_type(extension),
    )


def _content_type(extension: str) -> str:
    return {
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }.get(extension, "application/octet-stream")


def _parse_text(content: bytes) -> tuple[str, tuple[str, ...]]:
    try:
        return content.decode("utf-8"), ()
    except UnicodeDecodeError:
        return content.decode("utf-8", errors="replace"), (
            "Text decoded with replacement characters after UTF-8 decode warning.",
        )


def _document_id(filename: str, content: bytes) -> str:
    digest = sha256()
    digest.update(filename.encode("utf-8"))
    digest.update(b"\0")
    digest.update(content)
    return digest.hexdigest()


def _to_bytes(content: bytes | str) -> bytes:
    if isinstance(content, bytes):
        return content
    return content.encode("utf-8")


def ingest_batch(paths: Sequence[str | Path]) -> DocumentManifest:
    """Read a batch of local files and return a deduplicated manifest."""
    records = {}
    for path in paths:
        if not Path(path).is_file():
            continue
        record = ingest_path(path)
        if record.document_id not in records:
            records[record.document_id] = record
    return DocumentManifest(records_by_id=records)


def ingest_directory(directory: str | Path, recursive: bool = False) -> DocumentManifest:
    """Read all files in a directory and return a manifest."""
    dir_path = Path(directory)
    paths = []
    if recursive:
        for root, _, files in os.walk(dir_path):
            for file in files:
                paths.append(Path(root) / file)
    else:
        if dir_path.is_dir():
            for p in dir_path.iterdir():
                if p.is_file():
                    paths.append(p)
    return ingest_batch(paths)





if TYPE_CHECKING:
    from aos.pipelines.document_pipeline import DocumentPipelineRecord


@dataclass(frozen=True)
class DocumentManifest:
    """A deterministic registry of document pipeline records."""

    records_by_id: Mapping[str, DocumentPipelineRecord] = field(default_factory=dict)

    @property
    def total_documents(self) -> int:
        return len(self.records_by_id)

    @property
    def parsed_documents(self) -> int:
        return sum(1 for r in self.records_by_id.values() if r.parser_status == "parsed")

    @property
    def warning_documents(self) -> int:
        return sum(1 for r in self.records_by_id.values() if r.parser_status == "warning")

    @property
    def rejected_documents(self) -> int:
        return sum(1 for r in self.records_by_id.values() if r.parser_status == "rejected")

    @property
    def aggregated_warnings(self) -> Sequence[str]:
        warnings = []
        for r in self.records_by_id.values():
            if r.warnings:
                for w in r.warnings:
                    warnings.append(f"[{r.metadata.filename}] {w}")
        return tuple(warnings)
