import re
from typing import Dict, Any
from aos.runtime.package_directory_loader import safe_load_package_directory
from aos.runtime.package_integrity_verifier import verify_package_integrity

def orchestrate_package_integrity(
    approved_package_root: str,
    package_directory: str,
    expected_package_id: str
) -> Dict[str, Any]:
    
    if not isinstance(expected_package_id, str) or not re.match(r"^sha256:[0-9a-f]{64}$", expected_package_id):
        return {
            "schema_version": 1,
            "technical_status": "FAIL",
            "integrity_status": "NOT_RUN",
            "freshness_status": "NOT_RUN",
            "control_status": "BLOCKED",
            "package_id": expected_package_id if isinstance(expected_package_id, str) else None,
            "package_directory_name": None,
            "loader_status": "NOT_RUN",
            "artifact_results": {},
            "reason_codes": ["INVALID_EXPECTED_PACKAGE_ID_FORMAT"],
            "approval_granted": False,
            "execution_authorized": False,
            "github_remote_mutation_performed": False,
            "protected_operation_performed": False,
            "package_directory_safely_loaded": False,
            "artifact_integrity_verified": False,
            "package_identity_verified": False,
            "freshness_verified": False,
            "human_approval_present": False,
            "merge_authorized": False,
            "authenticity_proven": False
        }

    loader_res = safe_load_package_directory(approved_package_root, package_directory)
    
    if loader_res["technical_status"] != "PASS":
        return {
            "schema_version": 1,
            "technical_status": loader_res["technical_status"],
            "integrity_status": "NOT_RUN",
            "freshness_status": "NOT_RUN",
            "control_status": loader_res["control_status"],
            "package_id": expected_package_id,
            "package_directory_name": loader_res.get("package_directory_name"),
            "loader_status": loader_res["technical_status"],
            "artifact_results": {},
            "reason_codes": sorted(list(set(loader_res.get("reason_codes", [])))),
            "approval_granted": False,
            "execution_authorized": False,
            "github_remote_mutation_performed": False,
            "protected_operation_performed": False,
            "package_directory_safely_loaded": False,
            "artifact_integrity_verified": False,
            "package_identity_verified": False,
            "freshness_verified": False,
            "human_approval_present": False,
            "merge_authorized": False,
            "authenticity_proven": False
        }
        
    pkg_dir_name = loader_res["package_directory_name"]
    expected_digest = expected_package_id.split(":")[1]
    
    if pkg_dir_name != f"sha256-{expected_digest}" and not re.match(r"^\.sha256-" + expected_digest + r"\.staging-[a-f0-9]+$", pkg_dir_name):
        reasons = set(loader_res.get("reason_codes", []))
        reasons.add("PACKAGE_DIRECTORY_ID_MISMATCH")
        return {
            "schema_version": 1,
            "technical_status": "FAIL",
            "integrity_status": "FAIL",
            "freshness_status": "NOT_RUN",
            "control_status": "BLOCKED",
            "package_id": expected_package_id,
            "package_directory_name": pkg_dir_name,
            "loader_status": "PASS",
            "artifact_results": {},
            "reason_codes": sorted(list(reasons)),
            "approval_granted": False,
            "execution_authorized": False,
            "github_remote_mutation_performed": False,
            "protected_operation_performed": False,
            "package_directory_safely_loaded": True,
            "artifact_integrity_verified": False,
            "package_identity_verified": False,
            "freshness_verified": False,
            "human_approval_present": False,
            "merge_authorized": False,
            "authenticity_proven": False
        }
        
    core_artifacts = {k: v for k, v in loader_res["artifact_bytes"].items() if k != "human-preview.md"}
    verifier_res = verify_package_integrity(
        core_artifacts,
        loader_res["manifest_object"],
        expected_package_id
    )
    
    all_reasons = set(loader_res.get("reason_codes", [])) | set(verifier_res.get("reason_codes", []))
    
    if loader_res["technical_status"] == "UNKNOWN" or verifier_res["technical_status"] == "UNKNOWN":
        tech_status = "UNKNOWN"
    elif loader_res["technical_status"] == "FAIL" or verifier_res["technical_status"] == "FAIL":
        tech_status = "FAIL"
    else:
        tech_status = "PASS"
        
    if loader_res["control_status"] == "UNKNOWN_BLOCKED" or verifier_res["control_status"] == "UNKNOWN_BLOCKED":
        ctrl_status = "UNKNOWN_BLOCKED"
    elif loader_res["control_status"] == "BLOCKED" or verifier_res["control_status"] == "BLOCKED":
        ctrl_status = "BLOCKED"
    else:
        ctrl_status = "HUMAN_REVIEW_REQUIRED"

    is_success = tech_status == "PASS" and verifier_res["integrity_status"] == "PASS"
    
    return {
        "schema_version": 1,
        "technical_status": tech_status,
        "integrity_status": verifier_res["integrity_status"],
        "freshness_status": "NOT_RUN",
        "control_status": ctrl_status,
        "package_id": expected_package_id,
        "package_directory_name": pkg_dir_name,
        "loader_status": "PASS",
        "artifact_results": verifier_res.get("artifact_results", {}),
        "reason_codes": sorted(list(all_reasons)),
        "approval_granted": False,
        "execution_authorized": False,
        "github_remote_mutation_performed": False,
        "protected_operation_performed": False,
        "package_directory_safely_loaded": True,
        "artifact_integrity_verified": is_success,
        "package_identity_verified": is_success,
        "freshness_verified": False,
        "human_approval_present": False,
        "merge_authorized": False,
        "authenticity_proven": False
    }
