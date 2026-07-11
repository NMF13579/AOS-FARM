import json
from .strict_json import AOSRuntimeError, _check_domain

def _to_utf16_code_units(s: str) -> list:
    units = []
    for char in s:
        cp = ord(char)
        if cp <= 0xFFFF:
            units.append(cp)
        else:
            cp -= 0x10000
            high = 0xD800 | (cp >> 10)
            low = 0xDC00 | (cp & 0x3FF)
            units.extend([high, low])
    return units

def _serialize(val) -> bytes:
    if val is None:
        return b"null"
    elif isinstance(val, bool):
        return b"true" if val else b"false"
    elif isinstance(val, int):
        return str(val).encode('utf-8')
    elif isinstance(val, str):
        return json.dumps(val, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    elif isinstance(val, list):
        items = [_serialize(item) for item in val]
        return b"[" + b",".join(items) + b"]"
    elif isinstance(val, dict):
        sorted_keys = sorted(val.keys(), key=_to_utf16_code_units)
        items = []
        for k in sorted_keys:
            k_str = json.dumps(k, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
            v_str = _serialize(val[k])
            items.append(k_str + b":" + v_str)
        return b"{" + b",".join(items) + b"}"
    else:
        # Should be unreachable if _check_domain succeeds
        raise AOSRuntimeError("ERROR", "CANONICALIZATION_INPUT_NOT_VALIDATED", "Unsupported type", "canonicalization")

def canonicalize_validated_json(val) -> bytes:
    # 1. Re-validate domain explicitly before canonicalization to ensure arbitrary python objects aren't processed.
    try:
        _check_domain(val)
    except AOSRuntimeError as e:
        # Wrap into canonicalization layer error for boundary enforcement
        raise AOSRuntimeError("ERROR", "CANONICALIZATION_INPUT_NOT_VALIDATED", str(e), "canonicalization", e.path)
    
    # 2. Serialize
    return _serialize(val)
