import re
from typing import Dict, Any, List

def _parse_val(v: str) -> Any:
    v = v.strip()
    if not v:
        return ""
    if v.lower() == 'null':
        return None
    if v.lower() == 'true':
        return True
    if v.lower() == 'false':
        return False
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    if v == '[]':
        return []
    return v

def parse_markdown_yaml(text: str) -> Dict[str, Any]:
    """Fallback parser extracting yaml from markdown blocks without pyyaml."""
    match = re.search(r'```(?:yaml)?\n(.*?)\n```', text, re.DOTALL)
    yaml_text = match.group(1) if match else text
    
    result = {}
    current_list = None
    current_dict = None
    last_key = None
    
    for line in yaml_text.splitlines():
        line = line.rstrip()
        if not line or line.strip().startswith('#'):
            continue
            
        # Detect list item
        if line.startswith('  - '):
            if current_list is None and last_key is not None:
                current_list = []
                result[last_key] = current_list
            
            content = line[4:]
            if ':' in content:
                current_dict = {}
                if current_list is not None:
                    current_list.append(current_dict)
                k, v = content.split(':', 1)
                current_dict[k.strip()] = _parse_val(v)
            else:
                # Flat list item (e.g. depends_on: \n  - AOS-FARM.100)
                if current_list is not None:
                    current_list.append(_parse_val(content))
                current_dict = None
                
        elif line.startswith('    '):
            # Property of current dict in list
            if current_dict is not None and ':' in line:
                k, v = line.strip().split(':', 1)
                current_dict[k.strip()] = _parse_val(v)
                
        elif not line.startswith(' ') and ':' in line:
            # Top level key
            current_list = None
            current_dict = None
            k, v = line.split(':', 1)
            k = k.strip()
            v = v.strip()
            if v == "" or v == "[]":
                result[k] = _parse_val(v) if v else []
                current_list = result[k] if v == "" else None
            else:
                result[k] = _parse_val(v)
            last_key = k
                
    return result

def validate_registry_queue(registry_text: str, queue_text: str) -> dict:
    reg_data = parse_markdown_yaml(registry_text)
    queue_data = parse_markdown_yaml(queue_text)

    errors = []
    warnings = []

    # Required fields in registry
    if "schema_version" not in reg_data:
        errors.append("Registry missing schema_version")
    if "tasks" not in reg_data and "task_id" not in reg_data:
        errors.append("Registry missing tasks or task_id")

    # Required fields in queue
    if queue_data and "queue_items" not in queue_data:
        errors.append("Queue missing queue_items")

    tasks = reg_data.get("tasks", [])
    if not tasks and "task_id" in reg_data:
        tasks = [reg_data]

    task_ids = set()
    for t in tasks:
        tid = t.get("task_id")
        if not tid:
            errors.append("Task missing task_id")
        else:
            if tid in task_ids:
                errors.append(f"Duplicate task_id: {tid}")
            task_ids.add(tid)

        # Check dependencies
        for dep in t.get("depends_on", []):
            if dep not in task_ids:
                errors.append(f"Task {tid} depends on missing task_id {dep}")

        replaced_by = t.get("replaced_by")
        if replaced_by and replaced_by not in task_ids:
            warnings.append(f"Task {tid} replaced_by {replaced_by} which is not in this registry")
            
        status = t.get("registry_status")
        lifecycle = t.get("lifecycle_stage")

        # Invalid transition checks (approximated via state mismatches without full history)
        if status == "IN_PROGRESS" and lifecycle == "CANDIDATE":
            errors.append(f"Task {tid} invalid transition: CANDIDATE -> IN_PROGRESS")
        if status == "CLOSED" and lifecycle in ["CANDIDATE", "QUEUED"]:
            errors.append(f"Task {tid} invalid transition: {lifecycle} -> CLOSED")

        if status == "READY_FOR_EXECUTION":
            if not t.get("risk_profile"):
                errors.append(f"Task {tid} READY_FOR_EXECUTION but Risk Profile missing")
            if not t.get("risk_profile_assigned_by_human"):
                errors.append(f"Task {tid} READY_FOR_EXECUTION but risk_profile_assigned_by_human is false")
            if not t.get("execution_authorized"):
                errors.append(f"Task {tid} READY_FOR_EXECUTION but execution_authorized is false")
        
        final_status = t.get("final_status")
        if final_status == "UNKNOWN":
            errors.append(f"Task {tid} final_status is UNKNOWN, which is BLOCKED/not OK")
        if final_status == "NOT_RUN":
            warnings.append(f"Task {tid} final_status is NOT_RUN, which is not PASS")
        if final_status in ["PASS", "Evidence"] and t.get("execution_authorized"):
            warnings.append(f"Task {tid} has final_status {final_status} which does not imply approval, yet execution_authorized is true")


    queue_items = queue_data.get("queue_items", [])
    q_ids = set()
    q_orders = set()
    
    for q in queue_items:
        qid = q.get("queue_item_id")
        if not qid:
            errors.append("Queue item missing queue_item_id")
        else:
            if qid in q_ids:
                errors.append(f"Duplicate queue_item_id: {qid}")
            q_ids.add(qid)
            
        qorder = q.get("queue_order")
        if qorder:
            if qorder in q_orders:
                errors.append(f"Duplicate queue_order within revision: {qorder}")
            q_orders.add(qorder)
            
        tid = q.get("task_id")
        if tid and tid not in task_ids:
            errors.append(f"Queue references task_id {tid} not found in registry")

    ok = len(errors) == 0
    return {
        "ok": ok,
        "final_status": "PASS" if ok else "BLOCKED",
        "errors": errors,
        "warnings": warnings,
    }

def get_task_by_id(tasks, tid):
    for t in tasks:
        if t.get("task_id") == tid:
            return t
    return None

def _get_eligible_tasks(registry_text: str, queue_text: str):
    reg_data = parse_markdown_yaml(registry_text)
    queue_data = parse_markdown_yaml(queue_text)

    tasks = reg_data.get("tasks", [])
    if not tasks and "task_id" in reg_data:
        tasks = [reg_data]

    queue_items = queue_data.get("queue_items", [])
    # Sort by queue order
    queue_items = sorted(queue_items, key=lambda x: str(x.get("queue_order", "")))

    eligible = []
    selected_tid = None
    
    for q in queue_items:
        tid = q.get("task_id")
        t = get_task_by_id(tasks, tid)
        if q.get("status") == "SELECTED" and selected_tid is None:
            selected_tid = tid
            
        if not t:
            continue
            
        status = t.get("registry_status")
        # Ignore CLOSED, BLOCKED, REPLACED, DEFERRED
        if status in ["CLOSED", "BLOCKED", "REPLACED", "DEFERRED"]:
            continue
            
        eligible.append(t)
        
    return eligible, selected_tid

def select_current_task(registry_text: str, queue_text: str) -> dict:
    eligible, selected_tid = _get_eligible_tasks(registry_text, queue_text)
    
    reg_data = parse_markdown_yaml(registry_text)
    tasks = reg_data.get("tasks", [])
    if not tasks and "task_id" in reg_data:
        tasks = [reg_data]
        
    t = None
    if selected_tid:
        t = get_task_by_id(tasks, selected_tid)
    elif eligible:
        t = eligible[0]
        
    if not t:
        return {"ok": False, "final_status": "HUMAN_REVIEW_REQUIRED", "errors": ["No eligible current task"], "warnings": [], "task": None}
    
    if not t.get("execution_authorized"):
        return {"ok": False, "final_status": "HUMAN_REVIEW_REQUIRED", "errors": ["Selected task is not execution_authorized"], "warnings": [], "task": t}
        
    return {"ok": True, "final_status": "PASS", "errors": [], "warnings": [], "task": t}

def select_next_task(registry_text: str, queue_text: str) -> dict:
    eligible, selected_tid = _get_eligible_tasks(registry_text, queue_text)
    
    t = None
    if selected_tid:
        found_selected = False
        for el in eligible:
            if el.get("task_id") == selected_tid:
                found_selected = True
            elif found_selected:
                t = el
                break
    else:
        if eligible:
            t = eligible[0]

    if not t:
        return {"ok": False, "final_status": "HUMAN_REVIEW_REQUIRED", "errors": ["No eligible next task"], "warnings": [], "task": None}
    
    if not t.get("execution_authorized"):
        return {"ok": False, "final_status": "HUMAN_REVIEW_REQUIRED", "errors": ["Selected task is not execution_authorized"], "warnings": [], "task": t}
        
    return {"ok": True, "final_status": "PASS", "errors": [], "warnings": [], "task": t}

def summarize_registry_queue(registry_text: str, queue_text: str) -> dict:
    reg_data = parse_markdown_yaml(registry_text)
    tasks = reg_data.get("tasks", [])
    if not tasks and "task_id" in reg_data:
        tasks = [reg_data]
    
    counts = {}
    for t in tasks:
        st = t.get("registry_status", "UNKNOWN")
        counts[st] = counts.get(st, 0) + 1
        
    return {
        "ok": True,
        "final_status": "PASS",
        "errors": [],
        "warnings": [],
        "summary": counts
    }
