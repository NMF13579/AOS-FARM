import sys
import os
import re
import tempfile
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from aos.scripts.aos_semantic_guard import collect_semantic_guard_violations, collect_authority_claim_violations

LIFECYCLE_STATUSES = {"DRAFT", "READY_FOR_EXECUTION", "IN_PROGRESS", "HUMAN_REVIEW_REQUIRED", "BLOCKED", "APPROVED", "REJECTED", "CLOSED"}
QUEUE_STATUSES = {"BACKLOG", "NEXT", "IN_PROGRESS", "BLOCKED", "DONE"}
QUEUE_MODES = {"AUTO", "MANUAL", "PINNED"}
QUEUE_PRIORITIES = {"LOW", "NORMAL", "HIGH"}
TEMPLATE_LEVELS = {"S", "M", "L"}
NEXT_CANDIDATE_QUEUE_STATUSES = {"BACKLOG", "NEXT", "IN_PROGRESS"}
NON_NEXT_LIFECYCLE_STATUSES = {"BLOCKED", "CLOSED", "REJECTED"}

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

    semantic_violations = collect_authority_claim_violations(yaml_data, content)
    if semantic_violations:
        messages.extend(semantic_violations)
        is_valid = False

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

def is_next_candidate(task):
    return (
        task.get("queue_status") in NEXT_CANDIDATE_QUEUE_STATUSES
        and task.get("status") not in NON_NEXT_LIFECYCLE_STATUSES
    )

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
    candidates = [t for t in queue if is_next_candidate(t)]
    if candidates:
        print(f"Next task: {candidates[0]['task_id']}")
    else:
        print("No next task candidate.")
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

def get_next_task_id(tasks_dir="tasks"):
    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir)
    max_id = 0
    ids = []
    for filename in os.listdir(tasks_dir):
        m = re.match(r"^AOS-FARM-TASK-(\d+)\.md$", filename)
        if m:
            num = int(m.group(1))
            ids.append(num)
            if num > max_id:
                max_id = num
    return max_id + 1, ids

def generate_task_content(task_id_str, title="New Task"):
    dt = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return f"""---
task_id: "{task_id_str}"
title: "{title}"
type: "task"
template_level: "S"
status: "DRAFT"
queue_mode: "AUTO"
queue_position: null
queue_status: "BACKLOG"
queue_priority: "NORMAL"
risk_profile: "UNKNOWN_BLOCKED"
risk_assigned_by: "none"
approval_status: "NOT_APPROVED"
human_checkpoint_required: true
validator_status: "NOT_RUN"
evidence_status: "NOT_RUN"
log_uri: ".aos-tmp/tasks/{task_id_str}/agent-actions.log"
log_status: "NOT_STARTED"
owner: "human"
created_at: "{dt}"
updated_at: "{dt}"
---
## Задача

## Done когда

## История

## Evidence

## ⛔ Решение
"""

def cmd_task_new():
    tasks_dir = "tasks"
    next_id, _ = get_next_task_id(tasks_dir)
    task_id_str = f"AOS-FARM-TASK-{next_id:04d}"
    content = generate_task_content(task_id_str)

    target_path = os.path.join(tasks_dir, f"{task_id_str}.md")
    if os.path.exists(target_path):
        print(f"FAIL: {target_path} already exists")
        sys.exit(1)

    fd, temp_path = tempfile.mkstemp(dir=tasks_dir, text=True)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    os.replace(temp_path, target_path)
    print(f"Created {target_path}")

def cmd_task_new_batch():
    tasks_dir = "tasks"
    lines = sys.stdin.read().splitlines()
    tasks_to_create = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith("- "):
            print("FAIL: invalid non-list line")
            sys.exit(1)
        title = line[2:].strip()
        tasks_to_create.append(title)

    if not tasks_to_create:
        print("FAIL: empty batch plan")
        sys.exit(1)

    next_id, _ = get_next_task_id(tasks_dir)

    created_files = []
    try:
        for title in tasks_to_create:
            task_id_str = f"AOS-FARM-TASK-{next_id:04d}"
            target_path = os.path.join(tasks_dir, f"{task_id_str}.md")
            if os.path.exists(target_path):
                print(f"FAIL: {target_path} already exists")
                sys.exit(1)
            content = generate_task_content(task_id_str, title)

            fd, temp_path = tempfile.mkstemp(dir=tasks_dir, text=True)
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)
            os.replace(temp_path, target_path)
            created_files.append(target_path)
            next_id += 1
            print(f"Created {target_path}")
    except Exception as e:
        for f in created_files:
            if os.path.exists(f):
                os.remove(f)
        print(f"FAIL: write failed: {e}")
        sys.exit(1)

def cmd_task_set_queue(args):
    if len(args) < 1:
        print("FAIL: missing file path")
        sys.exit(1)
    filepath = args[0]
    updates = {}
    for arg in args[1:]:
        if '=' in arg:
            k, v = arg.split('=', 1)
            if v.lower() == 'null':
                v = None
            elif v.isdigit():
                v = int(v)
            updates[k] = v

    if not os.path.exists(filepath):
        print(f"FAIL: {filepath} not found")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        sys.exit(1)

    yaml_data, end_idx = parse_yaml_frontmatter(content)
    if not yaml_data:
        sys.exit(1)

    allowed_keys = {"queue_mode", "queue_position", "queue_status", "queue_priority"}
    for k in updates.keys():
        if k not in allowed_keys:
            print(f"FAIL: not allowed to mutate {k}")
            sys.exit(1)

    new_lines = []
    dt = datetime.datetime.now(datetime.timezone.utc).isoformat()
    in_yaml = True
    for i, line in enumerate(lines):
        if i > 0 and line.strip() == '---':
            in_yaml = False

        if in_yaml and ':' in line:
            parts = line.split(':', 1)
            k = parts[0].strip()
            if k in updates:
                v = updates[k]
                val_str = f'"{v}"' if isinstance(v, str) else ('null' if v is None else str(v))
                new_lines.append(f"{k}: {val_str}")
                continue
            if k == "updated_at":
                new_lines.append(f'updated_at: "{dt}"')
                continue

        new_lines.append(line)

    new_content = '\n'.join(new_lines)

    fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(filepath)), text=True)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(new_content)

    temp_valid, temp_msgs = validate_task_document(temp_path)
    if not temp_valid:
        os.remove(temp_path)
        print("FAIL: update results in invalid task document:")
        for m in temp_msgs: print(f"  - {m}")
        sys.exit(1)

    os.replace(temp_path, filepath)
    print(f"Updated {filepath}")

def cmd_task_validate_all():
    tasks_dir = "tasks"
    if not os.path.exists(tasks_dir):
        print("PASS: no tasks directory")
        sys.exit(0)

    all_pass = True
    ids = set()
    for filename in os.listdir(tasks_dir):
        if not filename.endswith(".md"): continue
        filepath = os.path.join(tasks_dir, filename)
        is_valid, msgs = validate_task_document(filepath)
        if not is_valid:
            print(f"FAIL: {filepath} is invalid:")
            for m in msgs: print(f"  - {m}")
            all_pass = False

        with open(filepath, 'r', encoding='utf-8') as f:
            yaml_data, _ = parse_yaml_frontmatter(f.read())
            if yaml_data:
                tid = yaml_data.get("task_id")
                if tid:
                    if tid != filename[:-3]:
                        print(f"FAIL: {filepath} filename mismatch with task_id {tid}")
                        all_pass = False
                    if tid in ids:
                        print(f"FAIL: {filepath} duplicate task_id {tid}")
                        all_pass = False
                    ids.add(tid)

    if all_pass:
        print("PASS: all tasks valid")
        sys.exit(0)
    else:
        sys.exit(1)

def cmd_task_renumber_preview():
    tasks_dir = "tasks"
    next_id, ids = get_next_task_id(tasks_dir)
    ids.sort()
    duplicates = set([x for x in ids if ids.count(x) > 1])
    gaps = []
    for i in range(1, max(ids)+1) if ids else []:
        if i not in ids:
            gaps.append(i)

    print(f"Existing IDs: {ids}")
    if gaps:
        print(f"Gaps: {gaps}")
    if duplicates:
        print(f"Duplicates: {duplicates}")
    print(f"Next ID by max+1 rule: {next_id}")

def check_task_readiness(filepath, all_tasks=None):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return "FAIL", [f"Failed to read file: {e}"]

    yaml_data, end_idx = parse_yaml_frontmatter(content)
    if not yaml_data:
        return "FAIL", ["Missing or invalid YAML frontmatter."]

    reasons_blocked = []
    reasons_human = []

    task_id = yaml_data.get("task_id")
    if not task_id:
        reasons_blocked.append("Missing task_id")
        task_id = "UNKNOWN"
    else:
        if not re.match(r"^AOS-FARM-TASK-\d+$", str(task_id)):
            reasons_blocked.append(f"Invalid task_id format: {task_id}")
        filename = os.path.basename(filepath)
        if filename != f"{task_id}.md":
            reasons_blocked.append(f"task_id {task_id} does not match filename {filename}")

    if all_tasks is not None:
        count = sum(1 for t in all_tasks if t.get("task_id") == task_id)
        if count > 1:
            return "FAIL", [f"duplicate task_id: {task_id}"]

    missing_fields = REQUIRED_YAML_FIELDS - set(yaml_data.keys())
    if missing_fields:
        reasons_blocked.append(f"Missing required YAML fields: {missing_fields}")

    for k, v in yaml_data.items():
        if v == "OK" and k != "title":
            reasons_blocked.append(f"Field {k} has forbidden value 'OK'")
        if v == "PASS" and k != "title":
            reasons_blocked.append(f"Field {k} has forbidden value 'PASS'")

    if yaml_data.get("queue_mode") not in QUEUE_MODES:
        reasons_blocked.append(f"Invalid queue_mode: {yaml_data.get('queue_mode')}")
    if yaml_data.get("queue_priority") not in QUEUE_PRIORITIES:
        reasons_blocked.append(f"Invalid queue_priority: {yaml_data.get('queue_priority')}")
    if yaml_data.get("queue_status") not in QUEUE_STATUSES:
        reasons_blocked.append(f"Invalid queue_status: {yaml_data.get('queue_status')}")

    qmode = yaml_data.get("queue_mode")
    qpos = yaml_data.get("queue_position")
    if qmode == "AUTO" and qpos is not None:
        reasons_blocked.append("queue_position must be null when queue_mode is AUTO")
    elif qmode in ("MANUAL", "PINNED"):
        if not isinstance(qpos, int) or qpos <= 0:
            reasons_blocked.append(f"queue_position must be integer > 0 when queue_mode is {qmode}")

    if yaml_data.get("status") not in LIFECYCLE_STATUSES:
        reasons_blocked.append(f"Invalid status: {yaml_data.get('status')}")

    if yaml_data.get("status") == "READY_FOR_EXECUTION":
        if yaml_data.get("approval_status") == "REJECTED":
            reasons_blocked.append("status READY_FOR_EXECUTION with REJECTED approval_status")
        if yaml_data.get("risk_profile_assigned_by_human") in (None, "", "null"):
            reasons_blocked.append("status READY_FOR_EXECUTION without human-assigned risk profile")
        if yaml_data.get("execution_authorized") is not True:
            reasons_blocked.append("status READY_FOR_EXECUTION without execution_authorized true")

    risk = yaml_data.get("risk_profile")
    if not risk:
        reasons_blocked.append("risk_profile is missing")
    elif risk == "UNKNOWN_BLOCKED":
        reasons_blocked.append("risk_profile is UNKNOWN_BLOCKED")
    else:
        assigned_by = yaml_data.get("risk_assigned_by")
        if not assigned_by or assigned_by == "none":
            reasons_human.append("risk_assigned_by is missing or 'none'")
        elif assigned_by.lower() in ("agent", "self", "ai"):
            reasons_blocked.append(f"risk_assigned_by: {assigned_by} is forbidden (agent/self)")

        if risk == "LOW_RISK_FAST" and assigned_by and assigned_by.lower() in ("agent", "self", "ai"):
            reasons_blocked.append("LOW_RISK_FAST cannot be self-assigned by agent")

    approval = yaml_data.get("approval_status")
    bad_approval_values = ["PASS", "Evidence", "CI PASS", "queue rank", "queue_position", "queue_priority", "queue_status", "validator PASS"]
    if not approval:
        reasons_blocked.append("approval_status is missing")
    elif approval in bad_approval_values:
        reasons_blocked.append(f"Invalid approval_status (cannot treat '{approval}' as approval)")
    elif approval == "NOT_APPROVED":
        if yaml_data.get("execution_authorized") is not True:
            reasons_human.append("approval_status is NOT_APPROVED and execution_authorized is not true")

    if yaml_data.get("commit_authorized") is True and approval != "APPROVED":
        reasons_blocked.append("commit_authorized is true without explicit APPROVED approval_status")
    if yaml_data.get("push_authorized") is True and approval != "APPROVED":
        reasons_blocked.append("push_authorized is true without explicit APPROVED approval_status")
    if yaml_data.get("release_authorized") is True and approval != "APPROVED":
        reasons_blocked.append("release_authorized is true without explicit APPROVED approval_status")

    body = '\n'.join(content.split('\n')[end_idx+1:])
    level = yaml_data.get("template_level")

    required_sections = ["## Задача", "## Done когда", "## История", "## Evidence", "## ⛔ Решение"]
    if level in ("M", "L"):
        required_sections.append("## Contract")
    if level == "L":
        required_sections.extend(["## Protected/canonical boundary", "## Risk notes", "## Rollback / recovery note"])

    for section in required_sections:
        if section not in body:
            reasons_blocked.append(f"Missing required section: {section}")

    def is_section_empty(section_name):
        idx = body.find(section_name)
        if idx == -1: return True
        start_idx = idx + len(section_name)
        end_idx = body.find("## ", start_idx)
        if end_idx == -1:
            end_idx = len(body)
        section_text = body[start_idx:end_idx].strip()
        return not section_text

    for section in required_sections:
        if is_section_empty(section):
            reasons_human.append(f"Empty section: {section}")

    if "auto approval" in body.lower() or "auto-approved" in body.lower() or approval == "AUTO_APPROVED":
         reasons_blocked.append("Auto approval is forbidden")

    evidence_text = ""
    idx = body.find("## Evidence")
    if idx != -1:
         end_idx_ev = body.find("## ", idx + len("## Evidence"))
         if end_idx_ev == -1:
             end_idx_ev = len(body)
         evidence_text = body[idx + len("## Evidence"):end_idx_ev].strip()

         if "approval" in evidence_text.lower() and "is not approval" not in evidence_text.lower():
             reasons_blocked.append("Evidence claims approval")

    decision_text = ""
    idx = body.find("## ⛔ Решение")
    if idx != -1:
         end_idx_dec = body.find("## ", idx + len("## ⛔ Решение"))
         if end_idx_dec == -1:
             end_idx_dec = len(body)
         decision_text = body[idx + len("## ⛔ Решение"):end_idx_dec].strip()
         if decision_text.upper() == "PENDING":
             reasons_human.append("human decision is PENDING")
         if approval == "APPROVED" and "APPROVED" not in decision_text:
             reasons_blocked.append("approval_status is APPROVED but human decision section does not contain APPROVED")

    v_status = yaml_data.get("validator_status")
    e_status = yaml_data.get("evidence_status")
    if v_status == "NOT_RUN":
        reasons_human.append("validator_status is NOT_RUN")
    if e_status == "NOT_RUN":
        reasons_human.append("evidence_status is NOT_RUN")

    log_uri = yaml_data.get("log_uri")
    if not log_uri:
        reasons_blocked.append("log_uri is missing")
    else:
        if not str(log_uri).startswith(f".aos-tmp/tasks/{task_id}/"):
            reasons_blocked.append(f"log_uri must be inside .aos-tmp/tasks/{task_id}/")

    log_status = yaml_data.get("log_status")
    if not log_status:
        reasons_blocked.append("log_status is missing")

    if reasons_blocked:
        return "BLOCKED", reasons_blocked + reasons_human
    if reasons_human:
        return "HUMAN_REVIEW_REQUIRED", reasons_human
    return "READY_FOR_HANDOFF", ["readiness passed"]

def cmd_task_readiness(filepath):
    if not os.path.exists(filepath) and not filepath.endswith(".md"):
        # try as task_id
        filepath = os.path.join("tasks", f"{filepath}.md")

    if not os.path.exists(filepath):
        print(f"FAIL: {filepath} not found")
        sys.exit(1)

    status, reasons = check_task_readiness(filepath)
    task_id = os.path.basename(filepath).replace(".md", "")
    print(f"Task: {task_id}")
    print(f"Readiness: {status}")
    print("Reasons:")
    for r in reasons:
        print(f"- {r}")
    print("Boundary:")
    if status == "READY_FOR_HANDOFF":
        print("- READY_FOR_HANDOFF is not approval")
        print("- READY_FOR_HANDOFF is not READY_FOR_EXECUTION")
        print("- READY_FOR_HANDOFF is not execution authorization")
        print("- Commit is not authorized")
        print("- Push is not authorized")
    else:
        print("- READY_FOR_HANDOFF is not READY_FOR_EXECUTION")
        print("- PASS is not approval")
        print("- Evidence is not approval")
        print("- CI PASS is not approval")

    if status == "READY_FOR_HANDOFF":
        sys.exit(0)
    else:
        sys.exit(1)

def cmd_task_readiness_all():
    tasks_dir = "tasks"
    if not os.path.exists(tasks_dir):
        print("PASS: no tasks directory")
        sys.exit(0)

    tasks = load_all_tasks(tasks_dir)
    print("task_id | readiness | notes")
    all_ready = True

    for filename in sorted(os.listdir(tasks_dir)):
        if not filename.endswith(".md"): continue
        filepath = os.path.join(tasks_dir, filename)
        status, reasons = check_task_readiness(filepath, all_tasks=tasks)
        notes = ", ".join(reasons) if reasons else "none"
        task_id = filename.replace(".md", "")
        print(f"{task_id} | {status} | {notes}")
        if status != "READY_FOR_HANDOFF":
            all_ready = False

    if all_ready:
        sys.exit(0)
    else:
        sys.exit(1)

def cmd_task_result_review(filepath):
    if not os.path.exists(filepath) and not filepath.endswith(".md"):
        filepath = os.path.join("tasks", f"{filepath}.md")

    if not os.path.exists(filepath):
        print("RESULT_REVIEW_BLOCKED")
        print(f"blocked_reason: file {filepath} not found")
        print("next_allowed_action: fix handoff_result report or escalate to human review")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    yaml_data, end_idx = parse_yaml_frontmatter(content)
    if not yaml_data:
        print("RESULT_REVIEW_BLOCKED")
        print("blocked_reason: Missing YAML frontmatter")
        print("next_allowed_action: fix handoff_result report or escalate to human review")
        sys.exit(1)

    task_id = yaml_data.get("task_id")
    if not task_id:
        print("RESULT_REVIEW_BLOCKED")
        print("blocked_reason: Missing task_id")
        print("next_allowed_action: fix handoff_result report or escalate to human review")
        sys.exit(1)

    status, reasons = check_task_readiness(filepath)
    if status != "READY_FOR_HANDOFF":
        print("RESULT_REVIEW_NOT_READY")
        print(f"blocked_reason: Task readiness is {status}. Reasons: {', '.join(reasons)}")
        print("next_allowed_action: fix task readiness before handoff")
        sys.exit(1)

    body = '\n'.join(content.split('\n')[end_idx+1:])
    body_lower = body.lower()

    idx = body_lower.find("handoff_result:")
    if idx == -1:
        idx = body_lower.find("## handoff result")
    if idx == -1:
        print("RESULT_REVIEW_BLOCKED")
        print("blocked_reason: missing handoff_result section")
        print("next_allowed_action: fix handoff_result report or escalate to human review")
        sys.exit(1)

    handoff_block = body[idx:]
    hb_lower = handoff_block.lower()

    blocked_reasons = []
    unknown_reasons = []

    if "reported_changed_files:" not in hb_lower and "changed files:" not in hb_lower:
        unknown_reasons.append("reported changed files missing or unknown")
    elif "changed files: unknown" in hb_lower or "reported_changed_files: unknown" in hb_lower:
        unknown_reasons.append("reported changed files unknown")

    protected_files = ["00_AOS_Core_Control.md", "01_AOS_Assembly_Pipelines_and_Build_Roadmap.md", "02_AOS_Governance_Control_Module_and_Safety_Rules.md", ".github/workflows", "aos/SELF_TEST.md"]
    for pf in protected_files:
        if pf.lower() in hb_lower:
            # ensure it's not just listed as a rule, but actually changed
            # we do a simple check: if it's in the block at all, we block unless we have a strict parser
            # To be safe and meet requirements: "Reported changed files не содержат protected/canonical files."
            blocked_reasons.append(f"root 00/01/02 or protected file changed: {pf}")

    if ".aos-tmp" in hb_lower and "source of truth" in hb_lower:
        blocked_reasons.append("/.aos-tmp/ used as Source of Truth")

    if ("registry" in hb_lower or "queue" in hb_lower or "cache" in hb_lower) and "source of truth" in hb_lower:
        blocked_reasons.append("generated registry/queue/cache used as Source of Truth")

    if "approval_claimed: true" in hb_lower or "approval granted" in hb_lower or "human approved" in hb_lower or "approved: true" in hb_lower:
        blocked_reasons.append("approval claimed")
    elif "approved" in hb_lower and "approval_claimed: false" not in hb_lower and "not approved" not in hb_lower:
        blocked_reasons.append("approval claimed or APPROVED found in result")

    if "ready_for_execution_claimed: true" in hb_lower or "ready to merge" in hb_lower or "ready to release" in hb_lower:
        blocked_reasons.append("READY_FOR_EXECUTION claimed")
    elif "ready_for_execution" in hb_lower and "ready_for_execution_claimed: false" not in hb_lower and "not ready_for_execution" not in hb_lower:
        blocked_reasons.append("READY_FOR_EXECUTION claimed")

    if "validation_results:" not in hb_lower and "validation results:" not in hb_lower:
        unknown_reasons.append("validation results missing without explicit NOT_RUN")
    elif "validation results: unknown" in hb_lower or "validation_results: unknown" in hb_lower:
        unknown_reasons.append("validation results unknown")

    if "handoff_ready: unknown" in hb_lower or "handoff ready: unknown" in hb_lower:
        unknown_reasons.append("handoff readiness unknown")

    if "status: pass" in hb_lower or " pass " in hb_lower or "pass\n" in hb_lower:
        if "evidence:" not in hb_lower and "evidence output" not in hb_lower:
            blocked_reasons.append("PASS without Evidence")

    if "not_run" in hb_lower and "pass" in hb_lower:
        if "not_run treated as pass" in hb_lower or "not_run=pass" in hb_lower:
            blocked_reasons.append("NOT_RUN treated as PASS")

    if "ci pass" in hb_lower and "approval" in hb_lower:
        blocked_reasons.append("CI PASS treated as approval")

    if "commit_performed: true" in hb_lower or "commit authorized" in hb_lower or ("commit performed" in hb_lower and "commit_performed: false" not in hb_lower):
        blocked_reasons.append("commit performed while commit_authorized=false")

    if "push_performed: true" in hb_lower or "push authorized" in hb_lower or ("push performed" in hb_lower and "push_performed: false" not in hb_lower):
        blocked_reasons.append("push performed while push_authorized=false")

    if "release_performed: true" in hb_lower or "release authorized" in hb_lower:
        blocked_reasons.append("release performed")

    if "unknown" in hb_lower and "ok" in hb_lower:
         blocked_reasons.append("UNKNOWN treated as OK")

    if " state: unknown" in hb_lower or "status: unknown" in hb_lower or "result: unknown" in hb_lower:
         unknown_reasons.append("ambiguous UNKNOWN state in handoff_result")

    if "stop_condition:" not in hb_lower and "stop condition:" not in hb_lower:
        blocked_reasons.append("stop condition missing")

    if "human review" not in hb_lower:
        blocked_reasons.append("stop condition missing explicit human review requirement")

    # 4. Handoff prompt boundary (checking globally in body)
    if "handoff prompt" not in body_lower and "controlled task handoff" not in body_lower and "handoff_result" not in body_lower:
        blocked_reasons.append("handoff prompt boundary missing")

    if blocked_reasons:
        print("RESULT_REVIEW_BLOCKED")
        print(f"blocked_reason: {blocked_reasons[0]}")
        print("next_allowed_action: fix handoff_result report or escalate to human review")
        sys.exit(1)

    if unknown_reasons:
        print("RESULT_REVIEW_UNKNOWN_BLOCKED")
        print(f"blocked_reason: {unknown_reasons[0]}")
        print("next_allowed_action: provide missing fields or clarify UNKNOWN state")
        sys.exit(1)

    print("RESULT_REVIEW_PASS")
    print(f"task_id: {task_id}")
    print("handoff_ready: true")
    print("handoff_prompt_boundary: present")
    print("handoff_result_report: present")
    print("reported_changed_files: present")
    print("protected_canonical_changes: none")
    print("generated_artifacts_as_source_of_truth: none")
    print("approval_claimed: false")
    print("ready_for_execution_claimed: false")
    print("pass_without_evidence: false")
    print("ci_pass_as_approval: false")
    print("commit_performed_without_authorization: false")
    print("push_performed_without_authorization: false")
    print("validation_results: present")
    print("stop_condition_report: present")
    print("next_allowed_state: READY_FOR_HUMAN_REVIEW")
    print("not_approval: true")
    print("not_ready_for_execution: true")
    print("not_commit_authorization: true")
    print("not_push_authorization: true")
    sys.exit(0)


def cmd_task_handoff_prompt(filepath):
    if not os.path.exists(filepath) and not filepath.endswith(".md"):
        filepath = os.path.join("tasks", f"{filepath}.md")

    if not os.path.exists(filepath):
        print(f"FAIL: {filepath} not found")
        sys.exit(1)

    status, reasons = check_task_readiness(filepath)
    if status != "READY_FOR_HANDOFF":
        print(f"FAIL: Task readiness is {status}. Must be READY_FOR_HANDOFF.")
        print("Reasons:")
        for r in reasons:
            print(f"- {r}")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    yaml_data, end_idx = parse_yaml_frontmatter(content)
    body = '\n'.join(content.split('\n')[end_idx+1:])

    def extract_section(section_name):
        idx = body.find(section_name)
        if idx == -1: return ""
        start_idx = idx + len(section_name)
        end_idx = body.find("## ", start_idx)
        if end_idx == -1: end_idx = len(body)
        return body[start_idx:end_idx].strip()

    scope = extract_section("## Задача")
    done_criteria = extract_section("## Done когда")
    evidence = extract_section("## Evidence")
    human_decision = extract_section("## ⛔ Решение")

    out_of_scope = extract_section("## Out of scope")
    if not out_of_scope:
        print("FAIL: out-of-scope boundary is missing")
        sys.exit(1)

    if not done_criteria:
        print("FAIL: done criteria are missing")
        sys.exit(1)
    if not evidence:
        print("FAIL: Evidence section is missing")
        sys.exit(1)
    if not human_decision:
        print("FAIL: human-only decision section is missing")
        sys.exit(1)

    risk_profile = yaml_data.get("risk_profile")
    if not risk_profile or risk_profile == "UNKNOWN_BLOCKED":
        print("FAIL: assigned Risk Profile is missing or invalid")
        sys.exit(1)

    task_id = yaml_data.get("task_id", "UNKNOWN")
    title = yaml_data.get("title", "UNKNOWN")
    task_status = yaml_data.get("status", "UNKNOWN")
    queue_status = yaml_data.get("queue_status", "UNKNOWN")
    queue_pos = yaml_data.get("queue_position")
    queue_pos_str = "null" if queue_pos is None else str(queue_pos)

    prompt = f"""AOS-FARM Controlled Task Handoff Prompt

* Task ID: {task_id}
* Task title: {title}
* Task status: {task_status}
* Risk Profile: {risk_profile}
* Queue status: {queue_status}
* Queue position: {queue_pos_str}
* Readiness: {status}

Source of Truth:
* The task file is the Source of Truth.
* This handoff prompt is derived output.
* If this prompt conflicts with the task file, the task file wins.

Scope:
{scope}

Out of scope:
{out_of_scope}

Done criteria:
{done_criteria}

Evidence boundary:
* Evidence may be collected.
* Evidence is not approval.
* PASS is not approval.
* CI PASS is not approval.
* NOT_RUN is not PASS.
* UNKNOWN is not OK.

Approval boundary:
* Human approval cannot be simulated.
* This prompt does not authorize approval.
* This prompt does not authorize READY_FOR_EXECUTION.
* This prompt does not authorize commit.
* This prompt does not authorize push.
* This prompt does not authorize release.

Mutation boundary:
* Do not edit human-only decision.
* Do not assign Risk Profile.
* Do not create approval.
* Do not create READY_FOR_EXECUTION.
* Do not change lifecycle unless explicitly authorized in a separate human instruction.

Protected/canonical boundary:
* Do not modify root 00/01/02 without separate human checkpoint.
* Do not modify protected/canonical files unless task scope explicitly allows it and human checkpoint is present.

Stop condition:
* Complete only the scoped work.
* Run validations.
* Report changed files.
* Report validation results.
* Do not commit unless separately authorized.
* Do not push unless separately authorized.
* Do not release unless separately authorized."""
    print(prompt)

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
    elif mode == "task":
        if len(sys.argv) < 3:
            sys.exit(1)
        sub = sys.argv[2]
        if sub == "--new":
            cmd_task_new()
        elif sub == "--new-batch":
            cmd_task_new_batch()
        elif sub == "--set-queue":
            cmd_task_set_queue(sys.argv[3:])
        elif sub == "--validate-all":
            cmd_task_validate_all()
        elif sub == "--renumber-preview":
            cmd_task_renumber_preview()
        elif sub == "--readiness":
            if len(sys.argv) < 4:
                sys.exit(1)
            cmd_task_readiness(sys.argv[3])
        elif sub == "--readiness-all":
            cmd_task_readiness_all()
        elif sub == "--result-review":
            if len(sys.argv) < 4:
                sys.exit(1)
            cmd_task_result_review(sys.argv[3])
        elif sub == "--handoff-prompt":
            if len(sys.argv) < 4:
                sys.exit(1)
            cmd_task_handoff_prompt(sys.argv[3])
        else:
            print(f"Unknown task sub-command: {sub}")
            sys.exit(1)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
