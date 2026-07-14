import hashlib
from typing import Dict, Any

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

def build_artifact_manifest(artifacts: Dict[str, bytes], generator_version: str) -> Dict[str, Any]:
    if not generator_version or not isinstance(generator_version, str):
        raise ValueError("Invalid generator version")
    
    if "/" in generator_version or "\\" in generator_version:
        raise ValueError("Local path in generator version rejected")
        
    actual_names = set(artifacts.keys())
    missing = EXPECTED_ARTIFACTS - actual_names
    if missing:
        raise ValueError(f"Missing expected artifacts: {missing}")
        
    extra = actual_names - EXPECTED_ARTIFACTS
    if extra:
        raise ValueError(f"Extra artifacts rejected: {extra}")
        
    for f in FORBIDDEN_ARTIFACTS:
        if f in actual_names:
            raise ValueError(f"Forbidden artifact: {f}")
            
    entries = []
    
    for path, data in artifacts.items():
        if not isinstance(path, str) or not isinstance(data, bytes):
            raise ValueError("Invalid types")
            
        if path.startswith("/"):
            raise ValueError("Absolute path rejected")
        if ".." in path:
            raise ValueError("Traversal rejected")
        if "\\" in path:
            raise ValueError("Backslash rejected")
            
        if not data:
            raise ValueError("Empty artifact")
            
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("Invalid UTF-8 rejected")
            
        if data.startswith(b'\xef\xbb\xbf'):
            raise ValueError("BOM rejected")
            
        if b"\r\n" in data:
            raise ValueError("CRLF rejected")
            
        has_terminal_lf = data.endswith(b"\n")
        digest = hashlib.sha256(data).hexdigest()
        
        entries.append({
            "relative_path": path,
            "byte_length": len(data),
            "sha256": digest,
            "encoding": "UTF-8",
            "line_endings": "LF",
            "terminal_lf": has_terminal_lf,
            "generator_version": generator_version
        })
        
    entries.sort(key=lambda x: x["relative_path"])
    
    return {
        "schema_version": 1,
        "artifacts": entries
    }
