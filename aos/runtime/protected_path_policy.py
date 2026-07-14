import json
import os
import re

class PolicyLoadError(Exception):
    def __init__(self, message, reason_code="PROTECTED_PATH_POLICY_UNKNOWN"):
        super().__init__(message)
        self.reason_code = reason_code

def normalize_path(p: str) -> str:
    if not p:
        raise PolicyLoadError("Empty path is not allowed")
    if os.path.isabs(p):
        raise PolicyLoadError(f"Absolute paths are rejected: {p}")
    if p.startswith("../") or "/../" in p or p.endswith("/.."):
        raise PolicyLoadError(f"Path traversal is rejected: {p}")
    if p == ".." or p == ".":
        raise PolicyLoadError(f"Path traversal is rejected: {p}")
    
    p = p.replace("\\", "/")
    p = re.sub(r'/+', '/', p)
    return p

def load_protected_path_policy(policy_path: str) -> list:
    try:
        if os.path.islink(policy_path):
            raise PolicyLoadError("Symlinks are not allowed for policy file")
            
        with open(policy_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not isinstance(data, dict):
            raise PolicyLoadError("Policy must be a JSON object")
            
        if data.get("schema_version") != 1:
            raise PolicyLoadError("Unsupported schema version")
            
        for k in data.keys():
            if k not in ["schema_version", "protected_paths"]:
                raise PolicyLoadError(f"Additional property not allowed: {k}")
            
        paths = data.get("protected_paths")
        if not isinstance(paths, list):
            raise PolicyLoadError("protected_paths must be a list")
            
        normalized = []
        for p in paths:
            if not isinstance(p, str):
                raise PolicyLoadError("Paths must be strings")
            norm_p = normalize_path(p)
            if norm_p in normalized:
                raise PolicyLoadError(f"Duplicate path after normalization: {norm_p}")
            normalized.append(norm_p)
            
        return normalized
        
    except FileNotFoundError:
        raise PolicyLoadError("Policy file is missing")
    except json.JSONDecodeError:
        raise PolicyLoadError("Policy file is malformed")
    except Exception as e:
        if isinstance(e, PolicyLoadError):
            raise e
        raise PolicyLoadError(f"Unreadable policy: {e}")
