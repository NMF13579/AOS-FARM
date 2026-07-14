import os
import re
import stat
from pathlib import Path
from typing import Dict, Any
from aos.runtime.strict_json import parse_strict_json, AOSRuntimeError

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB per file
MAX_TOTAL_SIZE = 30 * 1024 * 1024 # 30 MB total

EXPECTED_FILES = {
    "normalized-intent.json",
    "decision-state-snapshot.json",
    "merge-authorization-package.json",
    "artifact-manifest.json",
    "human-preview.md"
}

def _fail(reason_codes: set) -> dict:
    return {
        "schema_version": 1,
        "technical_status": "FAIL",
        "control_status": "BLOCKED",
        "package_directory_name": None,
        "artifact_bytes": {},
        "non_integrity_artifacts": {},
        "manifest_object": None,
        "observed_file_metadata": {},
        "reason_codes": sorted(list(reason_codes))
    }

def _unknown(reason_codes: set) -> dict:
    return {
        "schema_version": 1,
        "technical_status": "UNKNOWN",
        "control_status": "UNKNOWN_BLOCKED",
        "package_directory_name": None,
        "artifact_bytes": {},
        "non_integrity_artifacts": {},
        "manifest_object": None,
        "observed_file_metadata": {},
        "reason_codes": sorted(list(reason_codes))
    }

def safe_load_package_directory(
    approved_package_root: str,
    package_directory: str
) -> Dict[str, Any]:
    
    reasons = set()
    
    try:
        root_path = Path(approved_package_root)
        pkg_path = Path(package_directory)
    except Exception:
        return _unknown({"PACKAGE_ROOT_INVALID"})
        
    try:
        if root_path.is_symlink():
            return _fail({"PACKAGE_ROOT_INVALID"})
        if pkg_path.is_symlink():
            return _fail({"PACKAGE_DIRECTORY_SYMLINK_FORBIDDEN"})
    except OSError:
        return _unknown({"PACKAGE_READ_ERROR"})
        
    try:
        resolved_root = root_path.resolve(strict=True)
        resolved_pkg = pkg_path.resolve(strict=True)
    except FileNotFoundError as e:
        return _unknown({"PACKAGE_ROOT_INVALID"})
    except OSError:
        return _unknown({"PACKAGE_READ_ERROR"})
        
    if resolved_root == resolved_pkg:
        return _fail({"PACKAGE_PATH_OUTSIDE_ROOT"})
        
    try:
        resolved_pkg.relative_to(resolved_root)
    except ValueError:
        return _fail({"PACKAGE_PATH_OUTSIDE_ROOT"})
        
    if not (re.match(r"^sha256-[0-9a-f]{64}$", resolved_pkg.name) or re.match(r"^\.sha256-[0-9a-f]{64}\.staging-[a-f0-9]+$", resolved_pkg.name)):
        return _fail({"PACKAGE_DIRECTORY_NAME_INVALID"})
        
    try:
        entries = list(resolved_pkg.iterdir())
    except PermissionError:
        return _unknown({"PACKAGE_READ_PERMISSION_DENIED"})
    except OSError:
        return _unknown({"PACKAGE_READ_ERROR"})
        
    actual_names = set()
    total_size = 0
    
    for entry in entries:
        actual_names.add(entry.name)
        
        try:
            if entry.is_symlink():
                reasons.add("PACKAGE_ARTIFACT_SYMLINK_FORBIDDEN")
                continue
                
            entry_stat = entry.lstat()
            
            if stat.S_ISDIR(entry_stat.st_mode):
                reasons.add("PACKAGE_NESTED_DIRECTORY_FORBIDDEN")
                continue
                
            if not stat.S_ISREG(entry_stat.st_mode):
                reasons.add("PACKAGE_SPECIAL_FILE_FORBIDDEN")
                continue
                
            if entry_stat.st_size > MAX_FILE_SIZE:
                reasons.add("PACKAGE_FILE_TOO_LARGE")
                continue
                
            total_size += entry_stat.st_size
            if total_size > MAX_TOTAL_SIZE:
                reasons.add("PACKAGE_TOTAL_SIZE_TOO_LARGE")
                
        except PermissionError:
            reasons.add("PACKAGE_READ_PERMISSION_DENIED")
        except OSError:
            reasons.add("PACKAGE_READ_ERROR")
            
    if actual_names != EXPECTED_FILES:
        reasons.add("PACKAGE_ARTIFACT_SET_MISMATCH")
        
    if reasons:
        return _fail(reasons)
        
    artifacts = {}
    observed = {}
    
    for name in EXPECTED_FILES:
        file_path = resolved_pkg / name
        try:
            pre_stat = file_path.lstat()
            
            with open(file_path, "rb") as f:
                fd = f.fileno()
                post_stat = os.fstat(fd)
                
                if pre_stat.st_dev != post_stat.st_dev or \
                   pre_stat.st_ino != post_stat.st_ino or \
                   pre_stat.st_size != post_stat.st_size:
                    reasons.add("PACKAGE_FILE_CHANGED_DURING_READ")
                    continue
                    
                data = f.read()
                
                if len(data) != pre_stat.st_size:
                    reasons.add("PACKAGE_FILE_CHANGED_DURING_READ")
                    continue
                    
            artifacts[name] = data
            observed[name] = {
                "st_dev": post_stat.st_dev,
                "st_ino": post_stat.st_ino,
                "st_size": post_stat.st_size
            }
        except PermissionError:
            reasons.add("PACKAGE_READ_PERMISSION_DENIED")
        except OSError:
            reasons.add("PACKAGE_READ_ERROR")
            
    if reasons:
        return _fail(reasons)
        
    manifest_bytes = artifacts.pop("artifact-manifest.json")
    manifest_obj = None
    try:
        manifest_obj = parse_strict_json(manifest_bytes)
    except AOSRuntimeError:
        reasons.add("PACKAGE_MANIFEST_JSON_INVALID")
        
    if reasons:
        return _fail(reasons)
        
    if not isinstance(manifest_obj, dict):
        return _fail({"PACKAGE_MANIFEST_JSON_INVALID"})
        
    preview_bytes = artifacts.pop("human-preview.md", None)
    return {
        "schema_version": 1,
        "package_directory_name": resolved_pkg.name,
        "artifact_bytes": artifacts,
        "non_integrity_artifacts": {"human-preview.md": preview_bytes} if preview_bytes is not None else {},
        "manifest_object": manifest_obj,
        "observed_file_metadata": observed,
        "technical_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "reason_codes": []
    }
