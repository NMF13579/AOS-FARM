#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    script_path = Path(__file__).resolve()
    module_path = script_path.parent.parent / "tools" / "optional" / "lifecycle_guard.py"
    spec = importlib.util.spec_from_file_location("aos_lifecycle_guard_core", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load lifecycle guard module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    module = _load_module()
    return module.main(argv)


if __name__ == "__main__":
    sys.exit(main())
