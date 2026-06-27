#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_module():
    script_path = Path(__file__).resolve()
    module_path = script_path.parent.parent / "tools" / "optional" / "evidence_to_backlog_validator.py"
    spec = importlib.util.spec_from_file_location("aos_evidence_to_backlog_validator_core", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load evidence-to-backlog validator module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    module = _load_module()
    try:
        return module.main(argv)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        if code == 0:
            return 0
        payload = {
            "approval_claimed": False,
            "command": " ".join(argv if argv is not None else sys.argv[1:]),
            "commit_authorized": False,
            "errors": ["invalid arguments"],
            "execution_authorized": False,
            "final_status": "BLOCKED",
            "next_task_started": False,
            "push_authorized": False,
        }
        print(json.dumps(payload, sort_keys=True), file=sys.stderr)
        return code


if __name__ == "__main__":
    sys.exit(main())
