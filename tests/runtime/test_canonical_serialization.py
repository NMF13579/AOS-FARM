import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aos.runtime.strict_json import parse_strict_json, AOSRuntimeError
from aos.runtime.canonical_serialization import canonicalize_validated_json

def test_canonicalize_primitives():
    assert canonicalize_validated_json(None) == b"null"
    assert canonicalize_validated_json(True) == b"true"
    assert canonicalize_validated_json(False) == b"false"
    assert canonicalize_validated_json(123) == b"123"
    assert canonicalize_validated_json(-123) == b"-123"

def test_canonicalize_empty():
    assert canonicalize_validated_json([]) == b"[]"
    assert canonicalize_validated_json({}) == b"{}"

def test_canonicalize_arrays():
    # order is preserved
    assert canonicalize_validated_json([3, 1, 2]) == b"[3,1,2]"

def test_canonicalize_objects_utf16_sorting():
    # RFC 8785 sorting check. 
    # Example: "a", "b"
    assert canonicalize_validated_json({"b": 1, "a": 2}) == b'{"a":2,"b":1}'

    # supplementary characters vs BMP
    # \uD800 \uDF46 vs \uE000
    # U+10346 vs U+E000
    # UTF-16 code units: D800 DF46 vs E000
    # D800 < E000, so U+10346 should come BEFORE U+E000
    # Let's test this
    obj = {"\U00010346": 1, "\uE000": 2}
    result = canonicalize_validated_json(obj)
    # in Python code points: \uE000 < \U00010346, but in UTF-16 D800 < E000
    # So "\U00010346" must come first
    expected = b'{"\xf0\x90\x8d\x86":1,"\xee\x80\x80":2}'
    assert result == expected

def test_string_escaping():
    # solidus not escaped
    assert canonicalize_validated_json("/") == b'"/"'
    # quote escaped
    assert canonicalize_validated_json('"') == b'"\\""'
    # backslash escaped
    assert canonicalize_validated_json('\\') == b'"\\\\"'
    # control characters
    assert canonicalize_validated_json('\n') == b'"\\n"'
    assert canonicalize_validated_json('\r') == b'"\\r"'
    assert canonicalize_validated_json('\t') == b'"\\t"'
    assert canonicalize_validated_json('\b') == b'"\\b"'
    assert canonicalize_validated_json('\f') == b'"\\f"'
    assert canonicalize_validated_json('\x01') == b'"\\u0001"'
    assert canonicalize_validated_json('\x1f') == b'"\\u001f"'

def test_reject_unvalidated_input():
    with pytest.raises(AOSRuntimeError) as exc:
        canonicalize_validated_json(1.23)
    assert exc.value.error_code == "CANONICALIZATION_INPUT_NOT_VALIDATED"

    with pytest.raises(AOSRuntimeError) as exc:
        canonicalize_validated_json({"key": (1, 2)})
    assert exc.value.error_code == "CANONICALIZATION_INPUT_NOT_VALIDATED"

def test_reject_lone_surrogate_in_canonicalizer():
    # Even if somehow passed validation
    with pytest.raises(AOSRuntimeError):
        canonicalize_validated_json("\uD800")
