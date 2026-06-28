import sys
import os

LIFECYCLE_STATUSES = {"DRAFT", "READY_FOR_EXECUTION", "IN_PROGRESS", "HUMAN_REVIEW_REQUIRED", "BLOCKED", "APPROVED", "REJECTED", "CLOSED"}
QUEUE_STATUSES = {"BACKLOG", "NEXT", "IN_PROGRESS", "BLOCKED", "DONE"}
QUEUE_MODES = {"AUTO", "MANUAL", "PINNED"}
QUEUE_PRIORITIES = {"LOW", "NORMAL", "HIGH"}
TEMPLATE_LEVELS = {"S", "M", "L"}

REQUIRED_YAML_FIELDS = {
    "task_id", "title", "type", "template_level", "status", "queue_mode",
    "queue_position", "queue_status", "queue_priority", "risk_profile",
    "risk_assigned_by", "approval_status", "human_checkpoint_required",
    "validator_status", "evidence_status", "log_uri", "log_status", "owner",
    "created_at", "updated_at"
}

def parse_yaml_frontmatter(content):
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        return None, 0
    
    yaml_data = {}
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break
        
        line = lines[i]
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            
            if val == 'null':
                val = None
            elif val == 'true':
                val = True
            elif val == 'false':
                val = False
            elif val.isdigit():
                val = int(val)
                
            yaml_data[key] = val
            
    if end_idx == -1:
        return None, 0
        
    return yaml_data, end_idx

def validate_task_document(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Failed to read file: {e}"]
        
    yaml_data, end_idx = parse_yaml_frontmatter(content)
    if not yaml_data:
        return False, ["Missing or invalid YAML frontmatter."]
        
    messages = []
    is_valid = True
    
    missing_fields = REQUIRED_YAML_FIELDS - set(yaml_data.keys())
    if missing_fields:
        messages.append(f"Missing required YAML fields: {missing_fields}")
        is_valid = False
        
    for bad_field in ["rank", "generated_rank", "queue_rank"]:
        if bad_field in yaml_data:
            messages.append(f"YAML contains generated rank field '{bad_field}'.")
            is_valid = False
            
    if yaml_data.get("status") not in LIFECYCLE_STATUSES:
        messages.append(f"Invalid status: {yaml_data.get('status')}")
        is_valid = False
        
    if yaml_data.get("queue_status") not in QUEUE_STATUSES:
        messages.append(f"Invalid queue_status: {yaml_data.get('queue_status')}")
        is_valid = False
        
    if yaml_data.get("queue_priority") not in QUEUE_PRIORITIES:
        messages.append(f"Invalid queue_priority: {yaml_data.get('queue_priority')}")
        is_valid = False

    if yaml_data.get("queue_mode") not in QUEUE_MODES:
        messages.append(f"Invalid queue_mode: {yaml_data.get('queue_mode')}")
        is_valid = False
        
    qmode = yaml_data.get("queue_mode")
    qpos = yaml_data.get("queue_position")
    
    if qmode == "AUTO" and qpos is not None:
        messages.append("queue_position must be null when queue_mode is AUTO")
        is_valid = False
    elif qmode in ("MANUAL", "PINNED"):
        if not isinstance(qpos, int) or qpos <= 0:
            messages.append(f"queue_position must be integer > 0 when queue_mode is {qmode}")
            is_valid = False
            
    body = '\n'.join(content.split('\n')[end_idx+1:])
    level = yaml_data.get("template_level")
    
    required_sections = ["## Задача", "## Done когда", "## История", "## Evidence", "## ⛔ Решение"]
    if level in ("M", "L"):
        required_sections.append("## Contract")
    if level == "L":
        required_sections.extend(["## Protected/canonical boundary", "## Risk notes", "## Rollback / recovery note"])
        
    for section in required_sections:
        if section not in body:
            messages.append(f"Missing required section: {section}")
            is_valid = False
            
    bad_approval_values = ["PASS", "Evidence", "CI PASS", "queue rank", "queue_position", "queue_priority", "queue_status", "validator PASS"]
    if yaml_data.get("approval_status") in bad_approval_values:
        messages.append(f"Invalid approval_status (cannot treat '{yaml_data.get('approval_status')}' as approval).")
        is_valid = False
        
    for k, v in yaml_data.items():
        if v == "OK" and k != "title":
            messages.append("Found 'OK' value, treating UNKNOWN as OK is forbidden.")
            is_valid = False
        if v == "PASS" and k != "title":
            messages.append("Found 'PASS' value, treating NOT_RUN as PASS is forbidden.")
            is_valid = False
            
    if yaml_data.get("queue_status") == "NEXT" and yaml_data.get("status") == "READY_FOR_EXECUTION":
        messages.append("queue_status: NEXT does not create READY_FOR_EXECUTION")
        is_valid = False
        
    if yaml_data.get("queue_status") == "DONE" and yaml_data.get("status") == "CLOSED":
        messages.append("queue_status: DONE does not create CLOSED")
        is_valid = False
        
    if "auto approval" in body.lower() or "auto-approved" in body.lower() or yaml_data.get("approval_status") == "AUTO_APPROVED":
         messages.append("Auto approval is forbidden.")
         is_valid = False
         
    return is_valid, messages

def load_all_tasks(tasks_dir="tasks"):
    tasks = []
    if not os.path.isdir(tasks_dir):
        return tasks
    for filename in os.listdir(tasks_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(tasks_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    yaml_data, _ = parse_yaml_frontmatter(f.read())
                    if yaml_data:
                        if yaml_data.get("task_id") == filename[:-3]:
                            yaml_data['_filepath'] = filepath
                            tasks.append(yaml_data)
            except:
                pass
    return tasks

def cmd_validate(filepath):
    is_valid, msgs = validate_task_document(filepath)
    if is_valid:
        print(f"PASS: {filepath} is valid.")
        sys.exit(0)
    else:
        print(f"FAIL: {filepath} is invalid:")
        for m in msgs:
            print(f"  - {m}")
        sys.exit(1)

def cmd_registry_check():
    tasks = load_all_tasks()
    print("task_id | status | queue_status | queue_mode | risk_profile | validator_status | evidence_status | approval_status | title")
    for t in tasks:
        print(f"{t.get('task_id')} | {t.get('status')} | {t.get('queue_status')} | {t.get('queue_mode')} | {t.get('risk_profile')} | {t.get('validator_status')} | {t.get('evidence_status')} | {t.get('approval_status')} | {t.get('title')}")
    print("---")
    print("Registry check complete. No files written.")

def calculate_queue(tasks):
    active_tasks = [t for t in tasks if t.get("status") != "CLOSED"]
    
    pinned = sorted([t for t in active_tasks if t.get("queue_mode") == "PINNED"], key=lambda x: x.get("queue_position", 9999))
    manual = sorted([t for t in active_tasks if t.get("queue_mode") == "MANUAL"], key=lambda x: x.get("queue_position", 9999))
    auto = sorted([t for t in active_tasks if t.get("queue_mode") == "AUTO"], key=lambda x: x.get("created_at", ""))
    
    pinned_positions = [t.get("queue_position") for t in pinned]
    if len(pinned_positions) != len(set(pinned_positions)):
        print("FAIL: duplicate queue_position within active PINNED tasks", file=sys.stderr)
        sys.exit(1)
        
    manual_positions = [t.get("queue_position") for t in manual]
    if len(manual_positions) != len(set(manual_positions)):
        print("FAIL: duplicate queue_position within active MANUAL tasks", file=sys.stderr)
        sys.exit(1)
        
    common = set(pinned_positions).intersection(set(manual_positions))
    if common:
        print(f"WARN: same queue_position across PINNED and MANUAL: {common}", file=sys.stderr)
        
    queue = []
    rank = 1
    for t in pinned + manual + auto:
        t['_rank'] = rank
        queue.append(t)
        rank += 1
        
    return queue

def cmd_queue_list():
    tasks = load_all_tasks()
    queue = calculate_queue(tasks)
    print("rank | mode | position | priority | queue_status | lifecycle | risk_profile | approval_status | task_id | title")
    for t in queue:
        pos = t.get('queue_position')
        pos = pos if pos is not None else 'null'
        print(f"{t['_rank']} | {t.get('queue_mode')} | {pos} | {t.get('queue_priority')} | {t.get('queue_status')} | {t.get('status')} | {t.get('risk_profile')} | {t.get('approval_status')} | {t.get('task_id')} | {t.get('title')}")
    print("---")
    print("Queue list complete. No files written.")

def cmd_queue_next():
    tasks = load_all_tasks()
    queue = calculate_queue(tasks)
    if queue:
        print(f"Next task: {queue[0]['task_id']}")
    else:
        print("Queue is empty.")
    print("Next candidate is not approval.")
    print("Next candidate is not execution authorization.")
    print("Risk Profile must be assigned separately.")
    print("Human approval cannot be simulated.")

def cmd_queue_explain(task_id):
    tasks = load_all_tasks()
    queue = calculate_queue(tasks)
    target = next((t for t in queue if t['task_id'] == task_id), None)
    if not target:
        print(f"Task {task_id} not found in active queue.")
        sys.exit(1)
        
    print(f"Task {task_id} is ranked {target['_rank']}.")
    print("Explanation: Rank is dynamically calculated based on PINNED > MANUAL > AUTO rules.")
    print("queue rank is not execution authority.")
    print("approval_status does not create approval.")

def cmd_log_check(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            yaml_data, _ = parse_yaml_frontmatter(f.read())
    except:
        print(f"FAIL: could not read {filepath}", file=sys.stderr)
        sys.exit(1)
        
    if not yaml_data:
         print(f"FAIL: invalid task document {filepath}", file=sys.stderr)
         sys.exit(1)
         
    task_id = yaml_data.get("task_id")
    log_uri = yaml_data.get("log_uri")
    
    if not log_uri:
         print(f"FAIL: log_uri is missing", file=sys.stderr)
         sys.exit(1)
         
    if not str(log_uri).startswith(f".aos-tmp/tasks/{task_id}/"):
         print(f"FAIL: log_uri must be inside .aos-tmp/tasks/{task_id}/", file=sys.stderr)
         sys.exit(1)
         
    if not os.path.exists(log_uri):
         print("WARN: log file does not exist (NOT_FOUND)")
         sys.exit(0)
         
    allowed_events = {"SESSION_STARTED", "FILE_READ", "FILE_EDITED", "COMMAND", "COMMAND_RESULT", "VALIDATION_STARTED", "VALIDATION_RESULT", "ERROR", "RETRY", "SUMMARY", "SESSION_ENDED"}
    
    with open(log_uri, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            print(f"FAIL: log line malformed: {line}")
            sys.exit(1)
            
        line_task_id = parts[1]
        if not line_task_id:
            print("FAIL: log line missing task_id")
            sys.exit(1)
            
        if line_task_id != task_id:
            print(f"FAIL: wrong task_id in log line. Expected {task_id}, got {line_task_id}")
            sys.exit(1)
            
        event_type = parts[3]
        if event_type not in allowed_events:
            print(f"FAIL: invalid event_type {event_type} in log line")
            sys.exit(1)
            
    print("PASS: log is valid.")

def main():
    if len(sys.argv) < 2:
        print("Usage: aos_task_document_check.py [mode]")
        sys.exit(1)
        
    mode = sys.argv[1]
    
    if mode == "validate":
        if len(sys.argv) < 3:
            sys.exit(1)
        cmd_validate(sys.argv[2])
    elif mode == "registry" and len(sys.argv) == 3 and sys.argv[2] == "--check":
        cmd_registry_check()
    elif mode == "queue":
        if len(sys.argv) < 3:
            sys.exit(1)
        sub = sys.argv[2]
        if sub == "--list":
            cmd_queue_list()
        elif sub == "--next":
            cmd_queue_next()
        elif sub == "--explain":
            if len(sys.argv) < 4:
                sys.exit(1)
            cmd_queue_explain(sys.argv[3])
    elif mode == "log-check":
        if len(sys.argv) < 3:
            sys.exit(1)
        cmd_log_check(sys.argv[2])
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
