from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import argparse
import json
import re


PASS = "PASS"
BLOCKED = "BLOCKED"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"
HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
NOT_RUN = "NOT_RUN"

EXIT_CODES = {PASS: 0, BLOCKED: 1, UNKNOWN_BLOCKED: 1, HUMAN_REVIEW_REQUIRED: 1, NOT_RUN: 1}
DEVELOPMENT_PROTECTED_FILES = {
    "00_AOS_Core_Control.md",
    "01_AOS_Assembly_Pipelines_and_Build_Roadmap.md",
    "02_AOS_Governance_Control_Module_and_Safety_Rules.md",
    "03_AOS_Future_and_Legacy_Reference_OPTIONAL.md",
}
FORBIDDEN_TRUE_KEYS = {
    "approved",
    "human_approved",
    "commit_authorized",
    "push_authorized",
    "merge_authorized",
    "release_authorized",
    "pass_is_approval",
    "evidence_is_approval",
    "ci_pass_is_approval",
}
GENERATED_MARKERS = ("__pycache__", ".pyc", ".pyo", ".DS_Store")
KNOWN_CHANGE_STATES = {"modified", "added", "deleted", "renamed"}


class InputError(ValueError):
    """Raised for invalid CLI inputs or parser failures."""


@dataclass
class GuardContext:
    project_root: Path
    aos_root: Path

    @classmethod
    def from_values(cls, project_root: str | Path = ".", aos_root: str | Path = "aos") -> "GuardContext":
        project_root_path = Path(project_root).resolve()
        aos_root_path = Path(aos_root)
        if not aos_root_path.is_absolute():
            aos_root_path = (project_root_path / aos_root_path).resolve()
        else:
            aos_root_path = aos_root_path.resolve()
        if not project_root_path.exists():
            raise InputError(f"project root not found: {project_root_path}")
        if not aos_root_path.exists():
            raise InputError(f"aos root not found: {aos_root_path}")
        return cls(project_root=project_root_path, aos_root=aos_root_path)

    def resolve_input_path(self, path_value: str | Path) -> Path:
        candidate = Path(path_value)
        if candidate.is_absolute():
            resolved = candidate.resolve()
            if not resolved.exists():
                raise InputError(f"file not found: {resolved}")
            return resolved

        search_order = [
            (self.project_root / candidate).resolve(),
            (self.aos_root / candidate).resolve(),
        ]
        for resolved in search_order:
            if resolved.exists():
                return resolved
        raise InputError(f"file not found relative to project_root or aos_root: {candidate}")


@dataclass
class GuardResult:
    mode: str
    status: str
    summary: str
    pass_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    unknown_items: list[str] = field(default_factory=list)
    not_run_items: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def exit_code(self) -> int:
        return EXIT_CODES[self.status]

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "status": self.status,
            "summary": self.summary,
            "pass": self.pass_items,
            "blocked": self.blocked_items,
            "unknown": self.unknown_items,
            "not_run": self.not_run_items,
            "details": self.details,
        }


def precheck(package_path: str | Path, project_root: str | Path = ".", aos_root: str | Path = "aos") -> GuardResult:
    context = GuardContext.from_values(project_root, aos_root)
    package_file = context.resolve_input_path(package_path)
    package = _load_structured_document(package_file)
    if not isinstance(package, dict):
        raise InputError("controlled execution package must be a mapping")
    return _validate_package(package, package_file, context)


def scopecheck(
    package_path: str | Path,
    changed_files_path: str | Path,
    project_root: str | Path = ".",
    aos_root: str | Path = "aos",
) -> GuardResult:
    context = GuardContext.from_values(project_root, aos_root)
    package_file = context.resolve_input_path(package_path)
    package = _load_structured_document(package_file)
    if not isinstance(package, dict):
        raise InputError("controlled execution package must be a mapping")

    package_result = _validate_package(package, package_file, context)
    if package_result.status != PASS:
        package_result.mode = "scopecheck"
        package_result.summary = "scopecheck blocked by invalid execution package"
        return package_result

    changed_file = context.resolve_input_path(changed_files_path)
    changed_doc = _load_structured_document(changed_file)
    changed_files = _extract_changed_files(changed_doc)
    if changed_files is None:
        return GuardResult(
            mode="scopecheck",
            status=UNKNOWN_BLOCKED,
            summary="changed file state is unknown",
            unknown_items=["changed_files input missing or unparseable"],
            details=_context_details(context),
        )

    authorized_files = {_normalize_repo_path(item) for item in _as_path_list(_nested_get(package, "scope.authorized_files"))}
    forbidden_files = {_normalize_repo_path(item) for item in _as_path_list(_nested_get(package, "scope.forbidden_files"))}
    protected_checkpoint = _nested_get(package, "scope.protected_canonical_checkpoint")

    pass_items: list[str] = []
    blocked_items: list[str] = []
    unknown_items: list[str] = []

    for entry in changed_files:
        status = str(entry.get("status", "modified")).strip().lower()
        path = _normalize_repo_path(str(entry.get("path", "")).strip())
        old_path = _normalize_repo_path(str(entry.get("old_path", "")).strip())

        if status not in KNOWN_CHANGE_STATES:
            unknown_items.append(f"unknown change state: {status} for {path or '<missing>'}")
            continue
        if not path:
            unknown_items.append("changed file path missing")
            continue
        if _is_generated_path(path) or (old_path and _is_generated_path(old_path)):
            blocked_items.append(f"generated/cache file included: {path}")
            continue
        if path in forbidden_files or (old_path and old_path in forbidden_files):
            blocked_items.append(f"forbidden file changed: {path}")
            continue
        if _is_development_protected_path(path) or _is_development_protected_path(old_path):
            if not protected_checkpoint:
                return GuardResult(
                    mode="scopecheck",
                    status=HUMAN_REVIEW_REQUIRED,
                    summary="protected/canonical change requires human checkpoint",
                    blocked_items=[f"protected/canonical change detected: {path or old_path}"],
                    details=_context_details(context),
                )
        if path not in authorized_files:
            blocked_items.append(f"changed file outside authorized scope: {path}")
            continue
        if status == "renamed" and old_path and old_path not in authorized_files:
            blocked_items.append(f"renamed file outside authorized scope: {old_path} -> {path}")
            continue
        pass_items.append(f"{status}: {path}")

    if unknown_items:
        return GuardResult(
            mode="scopecheck",
            status=UNKNOWN_BLOCKED,
            summary="scopecheck encountered unknown changed file state",
            pass_items=pass_items,
            blocked_items=blocked_items,
            unknown_items=unknown_items,
            details=_context_details(context),
        )
    if blocked_items:
        return GuardResult(
            mode="scopecheck",
            status=BLOCKED,
            summary="scopecheck detected out-of-scope or forbidden changes",
            pass_items=pass_items,
            blocked_items=blocked_items,
            details=_context_details(context),
        )
    return GuardResult(
        mode="scopecheck",
        status=PASS,
        summary="all changed files stay within the authorized scope",
        pass_items=pass_items or ["no out-of-scope changes detected"],
        details=_context_details(context),
    )


def postcheck(
    package_path: str | Path,
    report_path: str | Path,
    project_root: str | Path = ".",
    aos_root: str | Path = "aos",
) -> GuardResult:
    context = GuardContext.from_values(project_root, aos_root)
    package_file = context.resolve_input_path(package_path)
    package = _load_structured_document(package_file)
    if not isinstance(package, dict):
        raise InputError("controlled execution package must be a mapping")

    package_result = _validate_package(package, package_file, context)
    if package_result.status != PASS:
        package_result.mode = "postcheck"
        package_result.summary = "postcheck blocked by invalid execution package"
        return package_result

    report_file = context.resolve_input_path(report_path)
    report = _load_structured_document(report_file)
    if not isinstance(report, dict):
        return GuardResult(
            mode="postcheck",
            status=BLOCKED,
            summary="evidence report is missing or unparseable",
            blocked_items=["missing evidence report structure"],
            details=_context_details(context),
        )

    raw_text = report_file.read_text(encoding="utf-8")
    forbidden_claims = _find_forbidden_true_claims(report, raw_text)
    if forbidden_claims:
        return GuardResult(
            mode="postcheck",
            status=BLOCKED,
            summary="evidence report contains forbidden approval or authorization claims",
            blocked_items=forbidden_claims,
            details=_context_details(context),
        )

    required_fields = [
        "task_id",
        "branch",
        "changed_files",
        "diff_summary",
        "commands_run",
        "validation_results",
        "pass",
        "not_run",
        "unknown",
        "blocked",
        "out_of_scope_changes",
        "forbidden_actions_not_performed",
        "commit_performed",
        "push_performed",
        "merge_performed",
        "release_performed",
        "next_task_started",
        "approval_claimed",
        "human_review_required",
        "next_safe_step",
    ]
    missing = [field_name for field_name in required_fields if field_name not in report]
    if missing:
        return GuardResult(
            mode="postcheck",
            status=BLOCKED,
            summary="evidence report is missing required fields",
            blocked_items=[f"missing field: {field_name}" for field_name in missing],
            details=_context_details(context),
        )

    task_id = _nested_get(package, "task_id")
    branch_name = _nested_get(package, "branch.authorized_branch")
    blocked_items: list[str] = []
    unknown_items: list[str] = []
    not_run_items = [str(item) for item in report.get("not_run", [])]

    if report["task_id"] != task_id:
        blocked_items.append("report task_id does not match package task_id")
    if report["branch"] != branch_name:
        blocked_items.append("report branch does not match authorized branch")

    for key in ("commit_performed", "push_performed", "merge_performed", "release_performed", "next_task_started", "approval_claimed"):
        if bool(report.get(key)):
            blocked_items.append(f"{key} must be false")

    if not bool(report.get("human_review_required")):
        blocked_items.append("human_review_required must be true")

    unknown_list = [str(item) for item in report.get("unknown", [])]
    if unknown_list:
        unknown_items.extend(unknown_list)

    if _flag_is_true(report, "not_run_is_pass") or _flag_is_true(_nested_get(report, "validation_results", {}), "not_run_is_pass"):
        blocked_items.append("NOT_RUN treated as PASS")

    pass_entries = [str(item) for item in report.get("pass", [])]
    overlapping = sorted(set(pass_entries) & set(not_run_items))
    if overlapping:
        blocked_items.append(f"same evidence listed as PASS and NOT_RUN: {', '.join(overlapping)}")

    if blocked_items:
        return GuardResult(
            mode="postcheck",
            status=BLOCKED,
            summary="postcheck detected blocked evidence or boundary violations",
            blocked_items=blocked_items,
            not_run_items=not_run_items,
            unknown_items=unknown_items,
            details=_context_details(context),
        )
    if unknown_items:
        return GuardResult(
            mode="postcheck",
            status=UNKNOWN_BLOCKED,
            summary="postcheck found unknown evidence that must not be ignored",
            unknown_items=unknown_items,
            not_run_items=not_run_items,
            details=_context_details(context),
        )

    return GuardResult(
        mode="postcheck",
        status=PASS,
        summary="postcheck verified evidence boundary disclosures",
        pass_items=[
            "evidence report contains required execution boundary disclosures",
            "commit/push/merge/release remained unperformed",
            "human review remains required",
        ],
        not_run_items=not_run_items,
        details=_context_details(context),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Controlled Execution Guard MVP")
    parser.add_argument("--project-root", default=".", help="Host project root that contains the transferable aos/ bundle")
    parser.add_argument("--aos-root", default="aos", help="Path to the embedded transferable aos/ folder")

    subparsers = parser.add_subparsers(dest="command", required=True)

    precheck_parser = subparsers.add_parser("precheck", help="Validate execution package before work begins")
    precheck_parser.add_argument("--package", required=True, help="Path to controlled execution package YAML")

    postcheck_parser = subparsers.add_parser("postcheck", help="Validate evidence report after work completes")
    postcheck_parser.add_argument("--package", required=True, help="Path to controlled execution package YAML")
    postcheck_parser.add_argument("--report", required=True, help="Path to execution/evidence report")

    scope_parser = subparsers.add_parser("scopecheck", help="Validate changed files stay inside authorized scope")
    scope_parser.add_argument("--package", required=True, help="Path to controlled execution package YAML")
    scope_parser.add_argument("--changed-files", required=True, help="Path to structured changed-files input")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "precheck":
            result = precheck(args.package, project_root=args.project_root, aos_root=args.aos_root)
        elif args.command == "postcheck":
            result = postcheck(args.package, args.report, project_root=args.project_root, aos_root=args.aos_root)
        elif args.command == "scopecheck":
            result = scopecheck(
                args.package,
                args.changed_files,
                project_root=args.project_root,
                aos_root=args.aos_root,
            )
        else:
            raise InputError(f"unsupported command: {args.command}")
    except InputError as exc:
        print(json.dumps({"status": "INVALID_INPUT", "summary": str(exc)}, indent=2))
        return 2

    print(json.dumps(result.to_dict(), indent=2))
    return result.exit_code()


def _validate_package(package: dict[str, Any], package_path: Path, context: GuardContext) -> GuardResult:
    blocked_items: list[str] = []
    pass_items: list[str] = []

    if _nested_get(package, "task_id") in (None, ""):
        blocked_items.append("task_id is required")

    human_auth = _nested_get(package, "human_execution_authorization")
    if not isinstance(human_auth, dict):
        blocked_items.append("human_execution_authorization is required")
    else:
        if human_auth.get("authorized") is not True:
            blocked_items.append("human execution authorization must be explicitly true")
        if human_auth.get("authorized_by") != "human":
            blocked_items.append("human execution authorization must be assigned by human")
        if not human_auth.get("authorization_artifact"):
            blocked_items.append("human execution authorization artifact is required")

    risk_profile = _nested_get(package, "risk_profile")
    if not isinstance(risk_profile, dict):
        return GuardResult(
            mode="precheck",
            status=HUMAN_REVIEW_REQUIRED,
            summary="risk profile is missing and requires human review",
            unknown_items=["risk_profile block missing"],
            details=_context_details(context),
        )
    if not risk_profile.get("value"):
        return GuardResult(
            mode="precheck",
            status=HUMAN_REVIEW_REQUIRED,
            summary="risk profile value is missing and requires human review",
            unknown_items=["risk_profile.value missing"],
            details=_context_details(context),
        )
    if risk_profile.get("assigned_by") != "human":
        return GuardResult(
            mode="precheck",
            status=HUMAN_REVIEW_REQUIRED,
            summary="risk profile must be assigned by human",
            blocked_items=["risk_profile.assigned_by must equal human"],
            details=_context_details(context),
        )
    pass_items.append(f"risk profile present: {risk_profile['value']}")

    branch = _nested_get(package, "branch")
    if not isinstance(branch, dict):
        blocked_items.append("branch block is required")
    else:
        if not branch.get("authorized_branch"):
            blocked_items.append("branch.authorized_branch is required")
        if not branch.get("base_branch"):
            blocked_items.append("branch.base_branch is required")

    scope = _nested_get(package, "scope")
    if not isinstance(scope, dict):
        return GuardResult(
            mode="precheck",
            status=UNKNOWN_BLOCKED,
            summary="scope block missing or unknown",
            unknown_items=["scope block missing"],
            details=_context_details(context),
        )

    authorized_files = scope.get("authorized_files")
    if authorized_files is None:
        blocked_items.append("scope.authorized_files is required")
    elif _is_unknown_value(authorized_files):
        return GuardResult(
            mode="precheck",
            status=UNKNOWN_BLOCKED,
            summary="authorized scope is unknown",
            unknown_items=["scope.authorized_files is unknown"],
            details=_context_details(context),
        )
    elif not isinstance(authorized_files, list) or not authorized_files:
        blocked_items.append("scope.authorized_files must be a non-empty list")

    forbidden_files = scope.get("forbidden_files")
    if forbidden_files is None:
        blocked_items.append("scope.forbidden_files is required")
    elif _is_unknown_value(forbidden_files):
        return GuardResult(
            mode="precheck",
            status=UNKNOWN_BLOCKED,
            summary="forbidden scope is unknown",
            unknown_items=["scope.forbidden_files is unknown"],
            details=_context_details(context),
        )
    elif not isinstance(forbidden_files, list):
        blocked_items.append("scope.forbidden_files must be a list")

    allowed_changes = scope.get("allowed_changes")
    if allowed_changes is None:
        blocked_items.append("scope.allowed_changes is required")
    elif _is_unknown_value(allowed_changes):
        return GuardResult(
            mode="precheck",
            status=UNKNOWN_BLOCKED,
            summary="allowed changes are unknown",
            unknown_items=["scope.allowed_changes is unknown"],
            details=_context_details(context),
        )

    forbidden_changes = scope.get("forbidden_changes")
    if forbidden_changes is None:
        blocked_items.append("scope.forbidden_changes is required")
    elif _is_unknown_value(forbidden_changes):
        return GuardResult(
            mode="precheck",
            status=UNKNOWN_BLOCKED,
            summary="forbidden changes are unknown",
            unknown_items=["scope.forbidden_changes is unknown"],
            details=_context_details(context),
        )

    if _nested_get(package, "validation_plan") in (None, "", []):
        blocked_items.append("validation_plan is required")
    if _nested_get(package, "expected_evidence") in (None, "", []):
        blocked_items.append("expected_evidence is required")

    boundaries = _nested_get(package, "execution_boundaries")
    if not isinstance(boundaries, dict):
        blocked_items.append("execution_boundaries block is required")
    else:
        for key in (
            "commit_allowed",
            "push_allowed",
            "merge_allowed",
            "release_allowed",
            "next_task_allowed",
            "approval_claim_allowed",
        ):
            if boundaries.get(key) is not False:
                blocked_items.append(f"execution_boundaries.{key} must be false")

    if _find_forbidden_true_claims(package, package_path.read_text(encoding="utf-8")):
        blocked_items.append("package contains forbidden approval or authorization claim")

    if blocked_items:
        return GuardResult(
            mode="precheck",
            status=BLOCKED,
            summary="precheck detected blocked execution package issues",
            pass_items=pass_items,
            blocked_items=blocked_items,
            details=_context_details(context),
        )

    pass_items.append("human execution authorization present")
    pass_items.append("scope and execution boundaries are fully declared")
    return GuardResult(
        mode="precheck",
        status=PASS,
        summary="controlled execution package satisfies required guard boundaries",
        pass_items=pass_items,
        details=_context_details(context),
    )


def _context_details(context: GuardContext) -> dict[str, str]:
    return {
        "project_root": str(context.project_root),
        "aos_root": str(context.aos_root),
    }


def _extract_changed_files(document: Any) -> list[dict[str, Any]] | None:
    if isinstance(document, list):
        return [_normalize_changed_entry(item) for item in document]
    if isinstance(document, dict):
        if "changed_files" in document and isinstance(document["changed_files"], list):
            return [_normalize_changed_entry(item) for item in document["changed_files"]]
        if {"path", "status"} & set(document.keys()):
            return [_normalize_changed_entry(document)]
    return None


def _normalize_changed_entry(item: Any) -> dict[str, Any]:
    if isinstance(item, str):
        return {"path": item, "status": "modified"}
    if isinstance(item, dict):
        return dict(item)
    return {"path": "", "status": "unknown"}


def _normalize_repo_path(value: str) -> str:
    if not value:
        return ""
    normalized = value.replace("\\", "/")
    normalized = re.sub(r"^\./", "", normalized)
    return normalized.rstrip("/")


def _as_path_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _is_generated_path(path: str) -> bool:
    return any(marker in path for marker in GENERATED_MARKERS)


def _is_unknown_value(value: Any) -> bool:
    return isinstance(value, str) and value.strip().upper() == "UNKNOWN"


def _is_development_protected_path(path: str) -> bool:
    if not path:
        return False
    normalized = _normalize_repo_path(path)
    return any(normalized == protected or normalized.endswith(f"/{protected}") for protected in DEVELOPMENT_PROTECTED_FILES)


def _nested_get(document: Any, dotted_key: str, default: Any = None) -> Any:
    if isinstance(document, dict):
        current = document
        for part in dotted_key.split("."):
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
        return current
    return default


def _flag_is_true(document: Any, key: str) -> bool:
    return isinstance(document, dict) and document.get(key) is True


def _find_forbidden_true_claims(document: Any, raw_text: str) -> list[str]:
    findings: list[str] = []
    lowered = raw_text.lower()
    for key in FORBIDDEN_TRUE_KEYS:
        if _contains_true_value(document, key):
            findings.append(f"forbidden claim set true: {key}")
        if f"{key}: true" in lowered:
            findings.append(f"forbidden textual claim: {key}: true")
    return sorted(set(findings))


def _contains_true_value(document: Any, target_key: str) -> bool:
    if isinstance(document, dict):
        for key, value in document.items():
            if key == target_key and value is True:
                return True
            if _contains_true_value(value, target_key):
                return True
    elif isinstance(document, list):
        for item in document:
            if _contains_true_value(item, target_key):
                return True
    return False


def _load_structured_document(path: Path) -> Any:
    raw_text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    try:
        if suffix in {".yaml", ".yml"}:
            return _parse_simple_yaml(raw_text)
        if suffix == ".md":
            match = re.search(r"```yaml\n(.*?)\n```", raw_text, re.DOTALL)
            if not match:
                return None
            return _parse_simple_yaml(match.group(1))
    except ValueError as exc:
        raise InputError(f"yaml parse error in {path}: {exc}") from exc
    raise InputError(f"unsupported file type: {path.suffix}")


def _parse_simple_yaml(text: str) -> Any:
    lines = [line.rstrip("\n") for line in text.splitlines()]
    cleaned = []
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cleaned.append(line.rstrip())
    if not cleaned:
        return None
    value, index = _parse_block(cleaned, 0, 0)
    if index != len(cleaned):
        raise ValueError("unexpected trailing content")
    return value


def _parse_block(lines: list[str], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return None, index
    line = lines[index]
    current_indent = _count_indent(line)
    if current_indent < indent:
        return None, index
    if current_indent > indent:
        raise ValueError(f"unexpected indentation at line: {line}")
    if line[indent:].startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_mapping(lines: list[str], index: int, indent: int) -> tuple[dict[str, Any], int]:
    data: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        current_indent = _count_indent(line)
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ValueError(f"unexpected indentation at line: {line}")
        stripped = line[indent:]
        if stripped.startswith("- "):
            break
        if ":" not in stripped:
            raise ValueError(f"expected key/value pair at line: {line}")
        key, remainder = stripped.split(":", 1)
        key = key.strip()
        remainder = remainder.strip()
        index += 1
        if remainder:
            data[key] = _parse_scalar(remainder)
            continue
        if index < len(lines) and _count_indent(lines[index]) > indent:
            nested, index = _parse_block(lines, index, indent + 2)
            data[key] = nested
        else:
            data[key] = None
    return data, index


def _parse_list(lines: list[str], index: int, indent: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    while index < len(lines):
        line = lines[index]
        current_indent = _count_indent(line)
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ValueError(f"unexpected indentation at line: {line}")
        stripped = line[indent:]
        if not stripped.startswith("- "):
            break
        payload = stripped[2:].strip()
        index += 1
        if not payload:
            nested, index = _parse_block(lines, index, indent + 2)
            items.append(nested)
            continue
        if ":" in payload:
            key, remainder = payload.split(":", 1)
            entry: dict[str, Any] = {key.strip(): _parse_scalar(remainder.strip()) if remainder.strip() else None}
            if index < len(lines) and _count_indent(lines[index]) > indent:
                nested, index = _parse_block(lines, index, indent + 2)
                if isinstance(nested, dict):
                    entry.update(nested)
                else:
                    raise ValueError("list item mapping cannot be followed by non-mapping content")
            items.append(entry)
            continue
        items.append(_parse_scalar(payload))
    return items, index


def _parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _count_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))
