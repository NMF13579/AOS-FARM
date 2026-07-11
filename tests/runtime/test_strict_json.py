import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aos.runtime.strict_json import parse_strict_json, AOSRuntimeError

def test_valid_json():
    assert parse_strict_json(b'{"key": "value"}') == {"key": "value"}
    assert parse_strict_json(b'[1, 2, 3]') == [1, 2, 3]
    assert parse_strict_json(b'true') is True
    assert parse_strict_json(b'null') is None
    assert parse_strict_json(b'9007199254740991') == 9007199254740991
    assert parse_strict_json(b'-9007199254740991') == -9007199254740991

def test_invalid_utf8():
    with pytest.raises(AOSRuntimeError) as exc:
        parse_strict_json(b'{"key": "\xff"}')
    assert exc.value.error_code == "INVALID_UTF8"

def test_duplicate_keys():
    with pytest.raises(AOSRuntimeError) as exc:
        parse_strict_json(b'{"key": 1, "key": 2}')
    assert exc.value.error_code == "DUPLICATE_OBJECT_KEY"

def test_float_rejected():
    with pytest.raises(AOSRuntimeError) as exc:
        parse_strict_json(b'{"key": 1.23}')
    assert exc.value.error_code == "FLOAT_NOT_ALLOWED"

def test_nan_infinity_rejected():
    with pytest.raises(AOSRuntimeError) as exc:
        parse_strict_json(b'{"key": NaN}')
    assert exc.value.error_code == "NON_FINITE_NUMBER_NOT_ALLOWED"

def test_integer_bounds():
    with pytest.raises(AOSRuntimeError) as exc:
        parse_strict_json(b'{"key": 9007199254740992}')
    assert exc.value.error_code == "INTEGER_OUT_OF_RANGE"
    
    with pytest.raises(AOSRuntimeError) as exc:
        parse_strict_json(b'{"key": -9007199254740992}')
    assert exc.value.error_code == "INTEGER_OUT_OF_RANGE"

def test_lone_surrogate():
    with pytest.raises(AOSRuntimeError) as exc:
        parse_strict_json(b'{"key": "\\uD800"}')
    assert exc.value.error_code == "LONE_SURROGATE_NOT_ALLOWED"

def test_unicode_preservation():
    val = parse_strict_json(b'{"key": "\\u00e9"}')
    assert val["key"] == "\u00e9"
    # test NFC / NFD separation
    nfc = parse_strict_json(b'{"key": "\\u00e9"}')
    nfd = parse_strict_json(b'{"key": "e\\u0301"}')
    assert nfc["key"] != nfd["key"]
