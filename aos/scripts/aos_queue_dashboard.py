#!/usr/bin/env python3
"""
AOS Queue Dashboard
Derived queue readability view.
Not queue authority. Not Source of Truth. Not lifecycle authority. Not approval authority.
"""

import sys
import os
import json
import argparse

# Import task logic from aos_task_document_check
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
try:
    from aos.scripts.aos_task_document_check import load_all_tasks, calculate_queue, check_task_readiness
except ImportError:
    print("Error: Could not import aos_task_document_check.py")
    sys.exit(1)

def get_dashboard_data():
    tasks = load_all_tasks("tasks")
    queue = calculate_queue(tasks)
    
    active_tasks = [t for t in tasks if t.get('status') not in ("CLOSED", "REJECTED")]
    
    next_candidate = None
    next_reason = "No candidate available"
    readiness_status = "UNKNOWN"
    blockers = []
    missing_decisions = []
    risk_profile = "UNKNOWN"
    evidence_status = "UNKNOWN"
    next_safe_action = "Wait for human review"
    forbidden_actions = [
        "Dashboard does not approve",
        "Dashboard does not assign Risk Profile",
        "Dashboard does not move queue",
        "Dashboard does not mutate lifecycle",
        "NEXT != approval",
        "NEXT != execution authorization"
    ]
    
    if queue:
        next_candidate_task = queue[0]
        next_candidate = next_candidate_task.get('task_id')
        risk_profile = next_candidate_task.get('risk_profile', 'UNKNOWN')
        evidence_status = next_candidate_task.get('evidence_status', 'UNKNOWN')
        
        # Determine why it is next
        queue_mode = next_candidate_task.get('queue_mode')
        if queue_mode == "PINNED":
            next_reason = "Task is PINNED"
        elif queue_mode == "MANUAL":
            next_reason = "Task is MANUAL and highest position"
        else:
            next_reason = "Task is AUTO and next in sequence"
            
        try:
            readiness_result = check_task_readiness(next_candidate_task['_filepath'], tasks)
            readiness_status = readiness_result[0]
            blockers = readiness_result[1]
        except Exception as e:
            readiness_status = "UNKNOWN_BLOCKED"
            blockers = [f"Exception checking readiness: {e}"]
            
        missing_decisions = [b for b in blockers if "human" in b.lower() or "approval" in b.lower() or "assign" in b.lower()]
        
        if readiness_status == "READY":
            next_safe_action = "Ready for execution if human has authorized"
        else:
            next_safe_action = "Resolve blockers"
            
    return {
        "active_task_count": len(active_tasks),
        "next_candidate": next_candidate,
        "why_it_is_next": next_reason,
        "readiness": readiness_status,
        "readiness_reasons": blockers,
        "missing_human_decisions": missing_decisions,
        "risk_profile_status": risk_profile,
        "evidence_status": evidence_status,
        "next_safe_action": next_safe_action,
        "forbidden_actions": forbidden_actions,
        "boundary_note": "Dashboard output is derived. Not Source of Truth. NEXT != approval. NEXT != execution authorization."
    }

def main():
    parser = argparse.ArgumentParser(description="AOS Queue Dashboard")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    data = get_dashboard_data()

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("=== AOS Queue Dashboard ===")
        print("Derived queue readability view. Not queue authority. Not Source of Truth.")
        print("NEXT != approval. NEXT != execution authorization.\n")
        
        print(f"Active Task Count: {data['active_task_count']}")
        print(f"Next Candidate:    {data['next_candidate']}")
        print(f"Why it is NEXT:    {data['why_it_is_next']}")
        print(f"Readiness:         {data['readiness']}")
        print(f"Risk Profile:      {data['risk_profile_status']}")
        print(f"Evidence Status:   {data['evidence_status']}")
        print(f"Next Safe Action:  {data['next_safe_action']}")
        
        if data['readiness_reasons']:
            print("\nReadiness reasons:")
            for b in data['readiness_reasons']:
                print(f"  - {b}")
                
        if data['missing_human_decisions']:
            print("\nMissing Human Decisions:")
            for d in data['missing_human_decisions']:
                print(f"  - {d}")
                
        print("\nForbidden Actions:")
        for f in data['forbidden_actions']:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
