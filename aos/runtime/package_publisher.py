import os
import json
import uuid
import re
from pathlib import Path
from typing import Dict, Any

from aos.runtime.canonical_serialization import canonicalize_validated_json
from aos.runtime.package_integrity_orchestrator import orchestrate_package_integrity

def atomic_publish_package(
    approved_package_root: str,
    package_id: str,
    artifact_bytes: Dict[str, bytes],
    artifact_manifest: Dict[str, Any]
) -> Dict[str, Any]:
    def _fail(reasons: list) -> Dict[str, Any]:
        return {
            "schema_version": 1,
            "package_id": package_id if isinstance(package_id, str) else None,
            "package_directory": None,
            "technical_status": "FAIL",
            "integrity_status": "NOT_RUN",
            "freshness_status": "NOT_RUN",
            "control_status": "BLOCKED",
            "published": False,
            "atomic_publish_completed": False,
            "existing_package_overwritten": False,
            "partial_package_published": False,
            "approval_granted": False,
            "execution_authorized": False,
            "github_remote_mutation_performed": False,
            "protected_operation_performed": False,
            "reason_codes": sorted(list(set(reasons)))
        }

    if not isinstance(package_id, str) or not re.match(r"^sha256:[0-9a-f]{64}$", package_id):
        return _fail(["PACKAGE_ID_INVALID"])

    digest = package_id.split(":")[1]
    final_dir_name = f"sha256-{digest}"

    try:
        root_path = Path(approved_package_root)
        if root_path.is_symlink():
            return _fail(["PACKAGE_ROOT_SYMLINK_FORBIDDEN"])
        resolved_root = root_path.resolve(strict=True)
    except FileNotFoundError:
        return _fail(["PACKAGE_ROOT_INVALID"])
    except OSError:
        return _fail(["PACKAGE_ROOT_INVALID"])

    final_pkg_path = resolved_root / final_dir_name

    if final_pkg_path.exists():
        return _fail(["PACKAGE_ALREADY_EXISTS"])

    allowed_artifacts = {
        "normalized-intent.json",
        "decision-state-snapshot.json",
        "merge-authorization-package.json",
        "human-preview.md"
    }

    actual_keys = set(artifact_bytes.keys())
    if actual_keys != allowed_artifacts:
        return _fail(["PACKAGE_ARTIFACT_SET_MISMATCH"])

    for name in actual_keys:
        if "/" in name or "\\" in name or name.startswith("."):
            return _fail(["PACKAGE_ARTIFACT_PATH_INVALID"])

    suffix = uuid.uuid4().hex
    staging_dir_name = f".{final_dir_name}.staging-{suffix}"
    staging_pkg_path = resolved_root / staging_dir_name

    try:
        staging_pkg_path.mkdir(parents=False, exist_ok=False)
    except Exception:
        return _fail(["PACKAGE_STAGING_CREATE_FAILED"])

    def _cleanup_and_fail(reasons: list) -> Dict[str, Any]:
        try:
            for item in staging_pkg_path.iterdir():
                item.unlink()
            staging_pkg_path.rmdir()
        except Exception:
            reasons.append("STAGING_CLEANUP_FAILED")
        return _fail(reasons)

    try:
        for name, data in artifact_bytes.items():
            file_path = staging_pkg_path / name
            with open(file_path, "xb") as f:
                f.write(data)

        manifest_path = staging_pkg_path / "artifact-manifest.json"
        manifest_bytes = canonicalize_validated_json(artifact_manifest)
        with open(manifest_path, "xb") as f:
            f.write(manifest_bytes + b"\n")
    except Exception:
        return _cleanup_and_fail(["PACKAGE_ARTIFACT_WRITE_FAILED"])

    ver_res = orchestrate_package_integrity(str(resolved_root), str(staging_pkg_path), package_id)
    if ver_res["technical_status"] != "PASS" or ver_res["integrity_status"] != "PASS":
        reasons = list(set(ver_res.get("reason_codes", []) + ["PACKAGE_STAGING_INTEGRITY_FAILED"]))
        return _cleanup_and_fail(reasons)

    if final_pkg_path.exists():
        return _cleanup_and_fail(["PACKAGE_ALREADY_EXISTS"])

    try:
        os.rename(staging_pkg_path, final_pkg_path)
    except OSError as e:
        if e.errno == 18:
            return _cleanup_and_fail(["PACKAGE_ATOMIC_RENAME_FAILED"])
        return _cleanup_and_fail(["PACKAGE_ATOMIC_RENAME_FAILED"])
    except Exception:
        return _cleanup_and_fail(["PACKAGE_ATOMIC_RENAME_FAILED"])

    if not final_pkg_path.exists() or final_pkg_path.is_symlink():
        return _fail(["PACKAGE_FINAL_VERIFICATION_FAILED"])

    manifest_final_path = final_pkg_path / "artifact-manifest.json"
    if not manifest_final_path.exists() or not manifest_final_path.is_file():
        return _fail(["PACKAGE_FINAL_VERIFICATION_FAILED"])

    return {
        "schema_version": 1,
        "package_id": package_id,
        "package_directory": final_dir_name,
        "technical_status": "PASS",
        "integrity_status": "PASS",
        "freshness_status": "NOT_RUN",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "published": True,
        "atomic_publish_completed": True,
        "existing_package_overwritten": False,
        "partial_package_published": False,
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "protected_operation_performed": False,
        "reason_codes": []
    }
