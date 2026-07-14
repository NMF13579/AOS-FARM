import re
from aos.runtime.strict_json import parse_strict_json, AOSRuntimeError

class IntentLoadError(Exception):
    pass

def load_merge_intent(content: str) -> dict:
    if not isinstance(content, str):
        raise IntentLoadError("Content must be a string")
        
    if "# Merge Authorization Intent" not in content:
        raise IntentLoadError("Missing or invalid fixed Markdown title")
        
    blocks = re.findall(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if len(blocks) != 1:
        raise IntentLoadError(f"Expected exactly 1 JSON block, found {len(blocks)}")
        
    text_without_title = content.replace("# Merge Authorization Intent", "", 1)
    text_without_block = re.sub(r'```json\s*.*?\s*```', '', text_without_title, flags=re.DOTALL)
    if text_without_block.strip():
        raise IntentLoadError("Arbitrary text outside allowed envelope is rejected")

    json_bytes = blocks[0].encode('utf-8')
    try:
        data = parse_strict_json(json_bytes)
    except AOSRuntimeError as e:
        raise IntentLoadError(f"JSON error: {e.message}") from e

    required_fields = ["schema_version", "operation", "repository", "pull_request", "merge_method"]
    allowed_fields = required_fields + ["expected_head_oid"]
    
    for f in required_fields:
        if f not in data:
            raise IntentLoadError(f"Missing required field: {f}")
            
    for k in data.keys():
        if k not in allowed_fields:
            raise IntentLoadError(f"Unknown or forbidden field: {k}")

    pr = data["pull_request"]
    if isinstance(pr, bool) or not isinstance(pr, int):
        raise IntentLoadError("pull_request must be an integer (bool rejected)")
        
    if data["schema_version"] != 1:
        raise IntentLoadError("schema_version must be 1")
        
    if data["operation"] != "merge":
        raise IntentLoadError("Unsupported operation")
        
    if data["merge_method"] != "merge_commit":
        raise IntentLoadError("Unsupported merge method")
        
    repo = data["repository"]
    if not isinstance(repo, str) or not re.match(r'^[\w.-]+/[\w.-]+$', repo):
        raise IntentLoadError("Invalid repository format")
        
    if "expected_head_oid" in data:
        oid = data["expected_head_oid"]
        if not isinstance(oid, str) or not re.match(r'^[a-fA-F0-9]{40}$', oid):
            raise IntentLoadError("Invalid expected_head_oid format")
            
    for k, v in data.items():
        if isinstance(v, (dict, list)):
            raise IntentLoadError(f"Nested arbitrary structures rejected: {k}")

    return data
