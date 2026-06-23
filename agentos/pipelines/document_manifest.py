from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping, Sequence

if TYPE_CHECKING:
    from agentos.pipelines.document_pipeline import DocumentPipelineRecord


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
