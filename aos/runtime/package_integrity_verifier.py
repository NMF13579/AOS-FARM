import hashlib
from typing import Dict, Any
import copy
from aos.runtime.strict_json import parse_strict_json, AOSRuntimeError
from aos.runtime.package_identity import generate_package_identity

EXPECTED_ARTIFACTS = {
    "normalized-intent.json",
    "decision-state-snapshot.json",
    "merge-authorization-package.json"
}

FORBIDDEN_ARTIFACTS = {
    "artifact-manifest.json",
    "verification-result.json",
    "human-preview.md",
    "approval-witness.json",
    "consumption-record.json"
}

ALLOWED_WRAPPER_FIELDS = {
    "schema_version",
    "package_id",
    "package_core"
}

def _fail(reason_codes: set) -> dict:
    return {
        "schema_version": 1,
        "technical_status": "FAIL",
        "integrity_status": "FAIL",
        "control_status": "BLOCKED",
        "package_id": None,
        "artifact_results": {},
        "reason_codes": sorted(list(reason_codes)),
        "approval_granted": False,
        "execution_authorized": False
    }

def _unknown(reason_codes: set) -> dict:
    return {
        "schema_version": 1,
        "technical_status": "UNKNOWN",
        "integrity_status": "UNKNOWN",
        "control_status": "UNKNOWN_BLOCKED",
        "package_id": None,
        "artifact_results": {},
        "reason_codes": sorted(list(reason_codes)),
        "approval_granted": False,
        "execution_authorized": False
    }

def verify_package_integrity(
    artifacts: Dict[str, bytes],
    manifest: Dict[str, Any],
    expected_package_id: str
) -> Dict[str, Any]:
    
    artifacts = copy.deepcopy(artifacts)
    manifest = copy.deepcopy(manifest)
    
    reasons = set()
    
    if not isinstance(artifacts, dict) or not isinstance(manifest, dict) or not isinstance(expected_package_id, str):
        return _unknown({"UNSUPPORTED_INPUT"})
        
    actual_names = set(artifacts.keys())
    if actual_names != EXPECTED_ARTIFACTS:
        reasons.add("ARTIFACT_SET_MISMATCH")
        
    for f in FORBIDDEN_ARTIFACTS:
        if f in actual_names:
            reasons.add("ARTIFACT_SET_MISMATCH")
            
    manifest_entries = manifest.get("artifacts", [])
    if not isinstance(manifest_entries, list):
        return _unknown({"UNSUPPORTED_INPUT"})
        
    manifest_paths = set()
    for entry in manifest_entries:
        if not isinstance(entry, dict):
            return _unknown({"UNSUPPORTED_INPUT"})
        path = entry.get("relative_path")
        if not isinstance(path, str):
            return _unknown({"UNSUPPORTED_INPUT"})
        manifest_paths.add(path)
        
    if manifest_paths != EXPECTED_ARTIFACTS:
        reasons.add("MANIFEST_SET_MISMATCH")
        
    for path, data in artifacts.items():
        if not isinstance(data, bytes):
            return _unknown({"UNSUPPORTED_INPUT"})
            
        entry = next((e for e in manifest_entries if e.get("relative_path") == path), None)
        if not entry:
            continue
            
        if len(data) != entry.get("byte_length"):
            reasons.add("ARTIFACT_LENGTH_MISMATCH")
            
        if hashlib.sha256(data).hexdigest() != entry.get("sha256"):
            reasons.add("ARTIFACT_DIGEST_MISMATCH")
            
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            reasons.add("ARTIFACT_ENCODING_INVALID")
            
        if data.startswith(b'\xef\xbb\xbf'):
            reasons.add("ARTIFACT_BOM_FORBIDDEN")
            
        if b"\r\n" in data:
            reasons.add("ARTIFACT_LINE_ENDINGS_INVALID")
            
        has_terminal_lf = data.endswith(b"\n")
        if has_terminal_lf != entry.get("terminal_lf"):
            reasons.add("ARTIFACT_TERMINAL_LF_MISMATCH")
            
    package_data = artifacts.get("merge-authorization-package.json")
    if package_data:
        try:
            package_json = parse_strict_json(package_data)
        except AOSRuntimeError:
            reasons.add("PACKAGE_JSON_INVALID")
            package_json = None
    else:
        package_json = None
        
    if package_json:
        if not isinstance(package_json, dict):
            reasons.add("PACKAGE_JSON_INVALID")
        else:
            package_core = package_json.get("package_core")
            if not package_core or not isinstance(package_core, dict):
                reasons.add("PACKAGE_CORE_INVALID")
            else:
                try:
                    identity = generate_package_identity(package_core)
                    calculated_id = identity["package_id"]
                    if calculated_id != expected_package_id:
                        reasons.add("PACKAGE_ID_MISMATCH")
                    if package_json.get("package_id") != expected_package_id:
                        reasons.add("PACKAGE_ID_MISMATCH")
                except ValueError as e:
                    reasons.add("PACKAGE_CORE_INVALID")
                    
            for k in package_json.keys():
                if k not in ALLOWED_WRAPPER_FIELDS:
                    reasons.add("FORBIDDEN_PACKAGE_FIELD")
                    
    if reasons:
        return _fail(reasons)
        
    return {
        "schema_version": 1,
        "technical_status": "PASS",
        "integrity_status": "PASS",
        "control_status": "HUMAN_REVIEW_REQUIRED",
        "package_id": expected_package_id,
        "artifact_results": {},
        "reason_codes": [],
        "approval_granted": False,
        "execution_authorized": False
    }
