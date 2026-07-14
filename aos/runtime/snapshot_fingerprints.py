import hashlib
import json
from typing import Any
from aos.runtime.canonical_serialization import canonicalize_validated_json

def _compute_sha256(val: Any) -> str:
    canonical_bytes = canonicalize_validated_json(val)
    digest = hashlib.sha256(canonical_bytes).hexdigest()
    return f"sha256:{digest}"

def _is_forbidden_key(k: str) -> bool:
    k_lower = k.lower()
    if k_lower in ("created_at", "updated_at", "submitted_at", "closed_at", "merged_at", "started_at", "completed_at", "pushed_at"):
        return True
    if k_lower.endswith("_url") or k_lower == "url" or k_lower == "_links":
        return True
    if k_lower in ("error", "error_code", "error_message", "reason", "exception"):
        return True
    if k_lower in ("cursor", "endcursor", "startcursor", "hasnextpage", "haspreviouspage", "pageinfo"):
        return True
    return False

def _clean_data(val: Any) -> Any:
    if isinstance(val, float):
        raise ValueError("Float is rejected")
        
    if isinstance(val, dict):
        clean_dict = {}
        for k, v in val.items():
            if not isinstance(k, str):
                continue
            if _is_forbidden_key(k):
                continue
            clean_dict[k] = _clean_data(v)
        return clean_dict
        
    elif isinstance(val, list):
        cleaned_list = [_clean_data(item) for item in val]
        
        if all(isinstance(item, dict) for item in cleaned_list):
            if all("sha" in item for item in cleaned_list):
                cleaned_list.sort(key=lambda x: str(x.get("sha", "")))
            elif all("id" in item for item in cleaned_list):
                cleaned_list.sort(key=lambda x: str(x.get("id", "")))
            elif all("name" in item for item in cleaned_list):
                cleaned_list.sort(key=lambda x: str(x.get("name", "")))
            elif all("filename" in item for item in cleaned_list):
                cleaned_list.sort(key=lambda x: str(x.get("filename", "")))
            else:
                cleaned_list.sort(key=lambda x: json.dumps(x, sort_keys=True))
        elif all(isinstance(item, str) for item in cleaned_list):
            cleaned_list.sort()
            
        return cleaned_list
        
    elif isinstance(val, str):
        if val.startswith("/") and len(val) > 1 and "github.com" not in val:
            raise ValueError("Local absolute path is rejected where prohibited.")
        return val
        
    else:
        return val

def fingerprint_repository_identity(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_pr_anchor(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_commit_set(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_required_checks(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_review_threads(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_effective_reviews(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_blocking_reviews(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_required_policy(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_rulesets(value: Any) -> str:
    return _compute_sha256(_clean_data(value))

def fingerprint_protected_paths(value: Any) -> str:
    return _compute_sha256(_clean_data(value))
