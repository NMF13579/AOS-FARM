import pytest
from aos.runtime.merge_intent_loader import load_merge_intent, IntentLoadError

def test_valid_json_intent():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": 2,
  "merge_method": "merge_commit"
}
```
"""
    data = load_merge_intent(content)
    assert data["pull_request"] == 2

def test_missing_field():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge"
}
```
"""
    with pytest.raises(IntentLoadError, match="Missing required field"):
        load_merge_intent(content)

def test_unknown_field():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": 2,
  "merge_method": "merge_commit",
  "extra": "value"
}
```
"""
    with pytest.raises(IntentLoadError, match="Unknown or forbidden field"):
        load_merge_intent(content)

def test_duplicate_key():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": 2,
  "pull_request": 3,
  "merge_method": "merge_commit"
}
```
"""
    with pytest.raises(IntentLoadError, match="Duplicate key"):
        load_merge_intent(content)

def test_multiple_json_blocks():
    content = """# Merge Authorization Intent
```json
{}
```
```json
{}
```
"""
    with pytest.raises(IntentLoadError, match="Expected exactly 1 JSON block"):
        load_merge_intent(content)

def test_wrong_fence_language():
    content = """# Merge Authorization Intent
```yaml
{}
```
"""
    with pytest.raises(IntentLoadError, match="Expected exactly 1 JSON block"):
        load_merge_intent(content)

def test_free_text_outside_allowed_envelope():
    content = """# Merge Authorization Intent
Hello world
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": 2,
  "merge_method": "merge_commit"
}
```
"""
    with pytest.raises(IntentLoadError, match="Arbitrary text outside allowed envelope"):
        load_merge_intent(content)

def test_float_rejection():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": 2.5,
  "merge_method": "merge_commit"
}
```
"""
    with pytest.raises(IntentLoadError, match="Float not allowed"):
        load_merge_intent(content)

def test_nan_infinity_rejection():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": NaN,
  "merge_method": "merge_commit"
}
```
"""
    with pytest.raises(IntentLoadError, match="Constant not allowed|MALFORMED_JSON"):
        load_merge_intent(content)

def test_bool_as_int_pull_request():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": true,
  "merge_method": "merge_commit"
}
```
"""
    with pytest.raises(IntentLoadError, match="pull_request must be an integer"):
        load_merge_intent(content)

def test_unsupported_operation():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "unknown",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": 2,
  "merge_method": "merge_commit"
}
```
"""
    with pytest.raises(IntentLoadError, match="Unsupported operation"):
        load_merge_intent(content)

def test_unsupported_merge_method():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "NMF13579/AOS-FARM",
  "pull_request": 2,
  "merge_method": "rebase"
}
```
"""
    with pytest.raises(IntentLoadError, match="Unsupported merge method"):
        load_merge_intent(content)

def test_invalid_repository():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "invalid repo",
  "pull_request": 2,
  "merge_method": "merge_commit"
}
```
"""
    with pytest.raises(IntentLoadError, match="Invalid repository format"):
        load_merge_intent(content)

def test_invalid_expected_head_oid():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "a/b",
  "pull_request": 2,
  "merge_method": "merge_commit",
  "expected_head_oid": "short"
}
```
"""
    with pytest.raises(IntentLoadError, match="Invalid expected_head_oid format"):
        load_merge_intent(content)

def test_forbidden_fields():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "a/b",
  "pull_request": 2,
  "merge_method": "merge_commit",
  "sha256": "hash"
}
```
"""
    with pytest.raises(IntentLoadError, match="Unknown or forbidden field"):
        load_merge_intent(content)

def test_nested_arbitrary_object():
    content = """# Merge Authorization Intent
```json
{
  "schema_version": 1,
  "operation": "merge",
  "repository": "a/b",
  "pull_request": 2,
  "merge_method": "merge_commit",
  "expected_head_oid": {"nested": "value"}
}
```
"""
    with pytest.raises(IntentLoadError, match="Invalid expected_head_oid format|Nested arbitrary structures"):
        load_merge_intent(content)

def test_toml_block_rejected():
    content = """# Merge Authorization Intent
```toml
schema_version = 1
```
"""
    with pytest.raises(IntentLoadError, match="Expected exactly 1 JSON block"):
        load_merge_intent(content)
