from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


PASS = "PASS"
BLOCKED = "BLOCKED"
UNKNOWN = "UNKNOWN"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
NOT_RUN = "NOT_RUN"

BLOCKING_STATUS_VALUES = {
    BLOCKED,
    UNKNOWN,
    UNKNOWN_BLOCKED,
    HUMAN_REVIEW_REQUIRED,
    NOT_RUN,
}
KNOWN_STATUS_VALUES = BLOCKING_STATUS_VALUES | {PASS}
STATUS_FIELD_NAMES = {
    "status",
    "final_status",
    "validation_result",
    "validation_status",
}


@dataclass
class ParseResult:
    fields: dict[str, object]
    missing_required_fields: list[str] = field(default_factory=list)
    duplicate_keys: list[str] = field(default_factory=list)
    malformed_lines: list[str] = field(default_factory=list)
    ignored_lines: list[str] = field(default_factory=list)
    status_fields: dict[str, str] = field(default_factory=dict)
    blocking_status_fields: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "fields": self.fields,
            "missing_required_fields": self.missing_required_fields,
            "duplicate_keys": self.duplicate_keys,
            "malformed_lines": self.malformed_lines,
            "ignored_lines": self.ignored_lines,
            "status_fields": self.status_fields,
            "blocking_status_fields": self.blocking_status_fields,
        }


def parse_markdown_file(
    path: str | Path,
    required_fields: list[str] | tuple[str, ...] | None = None,
) -> ParseResult:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    return parse_markdown_text(text, required_fields=required_fields)


def parse_markdown_text(
    text: str,
    required_fields: list[str] | tuple[str, ...] | None = None,
) -> ParseResult:
    required = list(required_fields or [])
    fields: dict[str, object] = {}
    duplicate_keys: list[str] = []
    malformed_lines: list[str] = []
    ignored_lines: list[str] = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or _is_comment_line(stripped):
            continue
        if stripped.startswith("#"):
            ignored_lines.append(_format_line_issue(line_number, raw_line))
            continue
        if ":" not in stripped:
            ignored_lines.append(_format_line_issue(line_number, raw_line))
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        if not key:
            malformed_lines.append(_format_line_issue(line_number, raw_line))
            continue

        normalized_key = key
        parsed_value = _parse_scalar(value.strip())
        if normalized_key in fields and normalized_key not in duplicate_keys:
            duplicate_keys.append(normalized_key)
        fields[normalized_key] = parsed_value

    missing_required_fields = [
        field_name for field_name in required if field_name not in fields
    ]
    status_fields = extract_status_fields(fields)
    blocking_status_fields = {
        key: value
        for key, value in status_fields.items()
        if value in BLOCKING_STATUS_VALUES
    }

    return ParseResult(
        fields=fields,
        missing_required_fields=missing_required_fields,
        duplicate_keys=duplicate_keys,
        malformed_lines=malformed_lines,
        ignored_lines=ignored_lines,
        status_fields=status_fields,
        blocking_status_fields=blocking_status_fields,
    )


def extract_status_fields(fields: dict[str, object]) -> dict[str, str]:
    status_fields: dict[str, str] = {}
    for key, value in fields.items():
        if not isinstance(value, str):
            continue
        normalized_value = value.strip().upper()
        if key in STATUS_FIELD_NAMES or normalized_value in KNOWN_STATUS_VALUES:
            status_fields[key] = normalized_value
    return status_fields


def find_missing_required_fields(
    fields: dict[str, object],
    required_fields: list[str] | tuple[str, ...],
) -> list[str]:
    return [field_name for field_name in required_fields if field_name not in fields]


def parse_boolean_field(fields: dict[str, object], key: str) -> bool | None:
    value = fields.get(key)
    if isinstance(value, bool):
        return value
    return None


def _is_comment_line(line: str) -> bool:
    return line.startswith("<!--") or line.startswith("//")


def _parse_scalar(value: str) -> object:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return value


def _format_line_issue(line_number: int, raw_line: str) -> str:
    return f"line {line_number}: {raw_line.rstrip()}"
