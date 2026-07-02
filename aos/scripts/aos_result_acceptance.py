import argparse
import json
import sys
import os
from aos.scripts.aos_semantic_guard import collect_semantic_guard_violations

# Add parent directory to path so we can import the tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from aos.tools.optional.human_result_acceptance_checker import HumanResultAcceptanceChecker
except ImportError:
    # fallback for testing
    from tools.optional.human_result_acceptance_checker import HumanResultAcceptanceChecker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "summary", "user-summary"])
    parser.add_argument("--decision", required=True)
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()

    checker = HumanResultAcceptanceChecker()

    try:
        violations = collect_semantic_guard_violations({"decision": args.decision})
        if violations:
            result = {"status": "BLOCKED", "reason": ", ".join(violations)}
        else:
            result = checker.validate(args.decision)
    except Exception as e:
        result = {"status": "BLOCKED", "reason": f"Exception: {e}"}

    if args.command == "validate":
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Status: {result['status']}")
            print(f"Reason: {result.get('reason', '')}")
            
    elif args.command == "summary":
        print(f"Acceptance Status: {result['status']}")
    
    elif args.command == "user-summary":
        print("=== User Summary ===")
        print(f"Status: {result['status']}")
        print(f"Details: {result.get('reason', '')}")

if __name__ == "__main__":
    main()
