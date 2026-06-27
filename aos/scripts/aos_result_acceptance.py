import argparse
import json
import sys
import os

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

    if args.command == "validate":
        result = checker.validate(args.decision)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Status: {result['status']}")
            print(f"Reason: {result['reason']}")
            
        if result["status"] == "BLOCKED" and result["reason"] == "Invalid JSON in decision file.":
            sys.exit(2)
            
    elif args.command == "summary":
        result = checker.validate(args.decision)
        print(f"Acceptance Status: {result['status']}")
    
    elif args.command == "user-summary":
        result = checker.validate(args.decision)
        print("=== User Summary ===")
        print(f"Status: {result['status']}")
        print(f"Details: {result['reason']}")

if __name__ == "__main__":
    main()
