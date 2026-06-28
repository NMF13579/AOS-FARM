import sys
import argparse
import json
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aos.tools.optional.task_quality_checker import TaskQualityChecker

def main():
    parser = argparse.ArgumentParser(description="Task Quality Checker MVP")
    parser.add_argument("action", choices=["validate", "summary", "user-summary"])
    parser.add_argument("--package", required=True, help="Path to JSON package")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    try:
        checker = TaskQualityChecker(args.package)
        result = checker.validate()
    except json.JSONDecodeError:
        result = "BLOCKED"
    except Exception as e:
        result = "BLOCKED"
        
    if args.action == "validate":
        if args.json:
            print(json.dumps({"status": result}))
        else:
            print(f"Status: {result}")
    elif args.action == "summary":
        print(f"Summary Status: {result}")
    elif args.action == "user-summary":
        print(f"User Summary: {result}")

if __name__ == "__main__":
    main()
