import argparse
import sys
import os

ALLOWED_MODES = ["dry-run", "validate", "next-safe-step", "generate-handoff", "generate-verification"]

def parse_task(filepath):
    task_data = {
        "fields_present": [],
        "execution_authorized": False,
        "commit_authorized": False,
        "push_authorized": False,
        "status": "UNKNOWN",
        "unknowns_present": False,
        "not_run_present": False
    }
    
    with open(filepath, 'r') as f:
        content = f.read()
        
        # Super basic parser for MVP
        if "Task ID:" in content: task_data["fields_present"].append("Task ID")
        if "Current Status:" in content: 
            for line in content.split('\n'):
                if "Current Status:" in line:
                    task_data["status"] = line.split("Current Status:")[1].strip()
        
        if "execution_authorized: true" in content: task_data["execution_authorized"] = True
        if "commit_authorized: true" in content: task_data["commit_authorized"] = True
        if "push_authorized: true" in content: task_data["push_authorized"] = True
        
        if "UNKNOWN" in content and "Known UNKNOWNs:" not in content: # rough heuristic
            task_data["unknowns_present"] = True
        if "NOT_RUN" in content and "Known NOT_RUNs:" not in content:
            task_data["not_run_present"] = True
            
    return task_data

def validate(task_data):
    # Check transitions
    if task_data["status"] == "IN_PROGRESS" and not task_data["execution_authorized"]:
        return "HELPER_BLOCKED_UNSAFE_TRANSITION"
    
    if task_data["status"] == "COMMITTED" and not task_data["commit_authorized"]:
        return "HELPER_BLOCKED_UNSAFE_TRANSITION"
        
    if task_data["status"] == "PUSHED" and not task_data["push_authorized"]:
        return "HELPER_BLOCKED_UNSAFE_TRANSITION"
        
    if task_data["status"] in ["EXECUTION_AUTHORIZED"] and not task_data["execution_authorized"]:
        return "HELPER_BLOCKED_MISSING_APPROVAL"
        
    if task_data["unknowns_present"]:
        return "HELPER_UNKNOWN_BLOCKED"
        
    if task_data["not_run_present"]:
        return "HELPER_DRY_RUN_PASS_WITH_WARNINGS"
        
    return "HELPER_DRY_RUN_PASS"

def main():
    parser = argparse.ArgumentParser(description="Thin Task Queue Helper")
    parser.add_argument("--task", required=True, help="Path to task markdown file")
    parser.add_argument("--mode", required=True, choices=ALLOWED_MODES, help="Helper mode")
    parser.add_argument("--output", help="Output path for generators")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.task):
        print("HELPER_INVALID_INPUT")
        sys.exit(1)
        
    task_data = parse_task(args.task)
    status = validate(task_data)
    
    if args.mode in ["dry-run", "validate"]:
        print(f"helper_mode: {args.mode}")
        print(f"final_helper_status: {status}")
    elif args.mode == "next-safe-step":
        print(f"final_helper_status: {status}")
        if status == "HELPER_DRY_RUN_PASS":
            print("recommended_next_safe_step: Proceed to next lifecycle phase based on Human Authorization.")
        else:
            print("recommended_next_safe_step: Fix blocking issues or missing approvals.")
    elif args.mode in ["generate-handoff", "generate-verification"]:
        if not args.output:
            print("HELPER_INVALID_INPUT: --output required for generators")
            sys.exit(1)
        if status not in ["HELPER_DRY_RUN_PASS", "HELPER_DRY_RUN_PASS_WITH_WARNINGS"]:
            print(f"Cannot generate: {status}")
            sys.exit(1)
        with open(args.output, 'w') as f:
            f.write(f"Generated {args.mode} for {args.task}\n")
        print(f"final_helper_status: {status}")
        print(f"Generated file at {args.output}")

if __name__ == "__main__":
    main()
