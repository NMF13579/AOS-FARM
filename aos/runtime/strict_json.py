import json

class AOSRuntimeError(Exception):
    def __init__(self, status, error_code, message, layer, path=""):
        super().__init__(message)
        self.status = status
        self.error_code = error_code
        self.message = message
        self.layer = layer
        self.path = path

def _reject_duplicates(ordered_pairs):
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise AOSRuntimeError("ERROR", "DUPLICATE_OBJECT_KEY", f"Duplicate key: {k}", "json_parser")
        d[k] = v
    return d

def _reject_float(s):
    raise AOSRuntimeError("ERROR", "FLOAT_NOT_ALLOWED", f"Float not allowed: {s}", "json_parser")

def _check_int(s):
    try:
        val = int(s)
    except ValueError:
        raise AOSRuntimeError("ERROR", "INVALID_NUMBER", f"Invalid number format: {s}", "json_parser")
    if val < -9007199254740991 or val > 9007199254740991:
        raise AOSRuntimeError("ERROR", "INTEGER_OUT_OF_RANGE", f"Integer {val} out of range", "json_domain")
    return val

def _reject_constant(s):
    raise AOSRuntimeError("ERROR", "NON_FINITE_NUMBER_NOT_ALLOWED", f"Constant not allowed: {s}", "json_parser")

def _check_domain(val, path=""):
    if val is None or isinstance(val, bool):
        return
    elif isinstance(val, int):
        if val < -9007199254740991 or val > 9007199254740991:
            raise AOSRuntimeError("ERROR", "INTEGER_OUT_OF_RANGE", f"Integer out of bounds at {path}", "json_domain", path)
    elif isinstance(val, float):
        raise AOSRuntimeError("ERROR", "FLOAT_NOT_ALLOWED", f"Float not allowed at {path}", "json_domain", path)
    elif isinstance(val, str):
        for i, char in enumerate(val):
            if 0xD800 <= ord(char) <= 0xDFFF:
                raise AOSRuntimeError("ERROR", "LONE_SURROGATE_NOT_ALLOWED", f"Surrogate at {path}[{i}]", "json_domain", path)
    elif isinstance(val, list):
        for i, item in enumerate(val):
            _check_domain(item, f"{path}[{i}]")
    elif isinstance(val, dict):
        for k, v in val.items():
            if not isinstance(k, str):
                raise AOSRuntimeError("ERROR", "NON_STRING_OBJECT_KEY", f"Non-string key at {path}", "json_domain", path)
            for i, char in enumerate(k):
                if 0xD800 <= ord(char) <= 0xDFFF:
                    raise AOSRuntimeError("ERROR", "LONE_SURROGATE_NOT_ALLOWED", f"Surrogate in key at {path}[{i}]", "json_domain", path)
            _check_domain(v, f"{path}.{k}" if path else k)
    else:
        raise AOSRuntimeError("ERROR", "UNSUPPORTED_VALUE_TYPE", f"Unsupported type at {path}", "json_domain", path)

def parse_strict_json(b: bytes):
    if not isinstance(b, bytes):
        raise AOSRuntimeError("ERROR", "INVALID_INPUT_TYPE", "Input must be bytes", "utf8")
    try:
        s = b.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AOSRuntimeError("ERROR", "INVALID_UTF8", str(e), "utf8")
    
    try:
        obj = json.loads(s, 
            object_pairs_hook=_reject_duplicates,
            parse_float=_reject_float,
            parse_int=_check_int,
            parse_constant=_reject_constant
        )
    except AOSRuntimeError:
        raise
    except json.JSONDecodeError as e:
        raise AOSRuntimeError("ERROR", "MALFORMED_JSON", str(e), "json_parser")
    except Exception as e:
        raise AOSRuntimeError("ERROR", "MALFORMED_JSON", str(e), "json_parser")
    
    _check_domain(obj)
    return obj
