import subprocess
from pathlib import Path
import re

class AOSBindingError(Exception):
    pass

def _run_git(args, cwd):
    allowed_commands = ["rev-parse", "branch", "remote", "status"]
    if args[0] not in allowed_commands:
        raise AOSBindingError("Forbidden Git command")
        
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=5
        )
        if res.returncode != 0:
            raise AOSBindingError(f"Git command failed: {res.stderr.strip()}")
        return res.stdout.strip()
    except Exception as e:
        raise AOSBindingError(f"Git execution error: {str(e)}")

def validate_repository_root(root_path: str) -> str:
    path = Path(root_path).resolve()
    if not path.exists() or not path.is_dir():
        raise AOSBindingError("INVALID_REPOSITORY_ROOT")
        
    try:
        top_level = _run_git(["rev-parse", "--show-toplevel"], cwd=str(path))
        if Path(top_level).resolve() != path:
            raise AOSBindingError("INVALID_REPOSITORY_ROOT")
    except AOSBindingError:
        raise AOSBindingError("INVALID_REPOSITORY_ROOT")
        
    return str(path)

def normalize_remote_url(url: str) -> str:
    if url.startswith("file://") or url.startswith("/") or url.startswith("."):
        raise AOSBindingError("LOCAL_REMOTE_BLOCKED")
        
    url = re.sub(r'^[a-zA-Z0-9+-]+://', '', url)
    url = re.sub(r'^[^@]+@', '', url)
    if url.endswith('.git'):
        url = url[:-4]
    if url.endswith('/'):
        url = url[:-1]
        
    parts = url.split('/', 1)
    if len(parts) == 2:
        host, path = parts
        if ':' in host:
            host_parts = host.split(':', 1)
            host = host_parts[0]
            path = host_parts[1] + '/' + path
        url = host.lower() + '/' + path
    else:
        if ':' in url:
            host, path = url.split(':', 1)
            url = host.lower() + '/' + path
        else:
            url = url.lower()
            
    if not url or '/' not in url:
        raise AOSBindingError("MALFORMED_REMOTE")
        
    return url

def _get_actual_remote(cwd: str, selected_remote_name: str = None) -> str:
    remotes_str = _run_git(["remote"], cwd=cwd)
    if not remotes_str:
        raise AOSBindingError("NO_REMOTES")
        
    remotes = remotes_str.splitlines()
    
    if selected_remote_name:
        if selected_remote_name not in remotes:
            raise AOSBindingError("SELECTED_REMOTE_MISSING")
        remote_name = selected_remote_name
    else:
        if len(remotes) == 1:
            remote_name = remotes[0]
        else:
            raise AOSBindingError("MULTIPLE_REMOTES_AMBIGUOUS")
            
    url = _run_git(["remote", "get-url", remote_name], cwd=cwd)
    return normalize_remote_url(url)

def _get_actual_branch(cwd: str) -> str:
    try:
        branch = _run_git(["branch", "--show-current"], cwd=cwd)
        if not branch:
            return None
        return branch
    except AOSBindingError:
        return None

def _get_actual_head(cwd: str) -> str:
    return _run_git(["rev-parse", "HEAD"], cwd=cwd)

def _get_baseline_state(cwd: str) -> dict:
    status_output = _run_git(["status", "--porcelain=v1"], cwd=cwd)
    staged = False
    unstaged_tracked = False
    untracked = False
    
    for line in status_output.splitlines():
        if len(line) < 2:
            continue
        x = line[0]
        y = line[1]
        
        if x == 'U' or y == 'U' or (x == 'D' and y == 'D') or (x == 'A' and y == 'A'):
            raise AOSBindingError("UNMERGED_STATE_BLOCKED")
            
        if x == '?' and y == '?':
            untracked = True
        else:
            if x != ' ':
                staged = True
            if y != ' ':
                unstaged_tracked = True
                
    return {
        "staged_changes_present": staged,
        "unstaged_tracked_changes_present": unstaged_tracked,
        "untracked_inventory_present": untracked,
        "tracked_clean": not staged and not unstaged_tracked
    }

def bind_repository(validated_package: dict, context_root: str, selected_remote_name: str = None) -> list:
    results = []
    
    try:
        root = validate_repository_root(context_root)
    except AOSBindingError:
        return [{
            "check": "repository_root",
            "status": "BLOCKED",
            "error_code": "INVALID_REPOSITORY_ROOT",
            "expected": None,
            "actual": context_root,
            "message": "Invalid repository root"
        }]

    expected_remote = validated_package.get("remote_identity")
    if not expected_remote:
        results.append({"check": "remote_identity", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD", "expected": None, "actual": None, "message": "Required"})
    else:
        try:
            actual_remote = _get_actual_remote(root, selected_remote_name)
            if expected_remote == actual_remote:
                results.append({"check": "remote_identity", "status": "PASS", "error_code": None, "expected": expected_remote, "actual": actual_remote, "message": "Match"})
            else:
                results.append({"check": "remote_identity", "status": "BLOCKED", "error_code": "REPOSITORY_MISMATCH", "expected": expected_remote, "actual": actual_remote, "message": "Mismatch"})
        except AOSBindingError as e:
            results.append({"check": "remote_identity", "status": "UNKNOWN_BLOCKED", "error_code": str(e), "expected": expected_remote, "actual": None, "message": str(e)})

    expected_branch = validated_package.get("branch")
    if not expected_branch:
         results.append({"check": "branch", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD", "expected": None, "actual": None, "message": "Required"})
    else:
        try:
            actual_branch = _get_actual_branch(root)
            if actual_branch is None:
                results.append({"check": "branch", "status": "BLOCKED", "error_code": "DETACHED_HEAD_BLOCKED", "expected": expected_branch, "actual": None, "message": "Detached HEAD"})
            elif expected_branch == actual_branch:
                results.append({"check": "branch", "status": "PASS", "error_code": None, "expected": expected_branch, "actual": actual_branch, "message": "Match"})
            else:
                results.append({"check": "branch", "status": "BLOCKED", "error_code": "BRANCH_MISMATCH", "expected": expected_branch, "actual": actual_branch, "message": "Mismatch"})
        except AOSBindingError as e:
            results.append({"check": "branch", "status": "UNKNOWN_BLOCKED", "error_code": str(e), "expected": expected_branch, "actual": None, "message": str(e)})
            
    expected_head = validated_package.get("baseline_head")
    if not expected_head:
         results.append({"check": "baseline_head", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD", "expected": None, "actual": None, "message": "Required"})
    elif len(expected_head) != 40 or not expected_head.islower() or not all(c in '0123456789abcdef' for c in expected_head):
         results.append({"check": "baseline_head", "status": "BLOCKED", "error_code": "INVALID_BASELINE_HASH", "expected": expected_head, "actual": None, "message": "Invalid format"})
    else:
        try:
            actual_head = _get_actual_head(root)
            if len(actual_head) != 40:
                results.append({"check": "baseline_head", "status": "UNKNOWN_BLOCKED", "error_code": "UNSUPPORTED_GIT_OBJECT_FORMAT", "expected": expected_head, "actual": actual_head, "message": "Format"})
            elif expected_head == actual_head:
                results.append({"check": "baseline_head", "status": "PASS", "error_code": None, "expected": expected_head, "actual": actual_head, "message": "Match"})
            else:
                results.append({"check": "baseline_head", "status": "BLOCKED", "error_code": "BASELINE_HEAD_MISMATCH", "expected": expected_head, "actual": actual_head, "message": "Mismatch"})
        except AOSBindingError as e:
            results.append({"check": "baseline_head", "status": "UNKNOWN_BLOCKED", "error_code": str(e), "expected": expected_head, "actual": None, "message": str(e)})

    try:
        state = _get_baseline_state(root)
        results.append({"check": "baseline_state", "status": "PASS", "error_code": None, "expected": None, "actual": state, "message": "Reported"})
    except AOSBindingError as e:
        results.append({"check": "baseline_state", "status": "BLOCKED", "error_code": str(e), "expected": None, "actual": None, "message": "Failed"})

    return results

def bind_platform(validated_package: dict, context_platform_profile: str, context_environment_id: str, context_execution_mode: str) -> list:
    results = []
    
    exp = validated_package.get("platform_profile")
    if not exp:
        results.append({"check": "platform_profile", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD", "expected": None, "actual": context_platform_profile, "message": "Required"})
    elif exp == context_platform_profile:
        results.append({"check": "platform_profile", "status": "PASS", "error_code": None, "expected": exp, "actual": context_platform_profile, "message": "Match"})
    else:
        results.append({"check": "platform_profile", "status": "BLOCKED", "error_code": "PLATFORM_PROFILE_MISMATCH", "expected": exp, "actual": context_platform_profile, "message": "Mismatch"})

    exp = validated_package.get("execution_environment_id")
    if not exp:
        results.append({"check": "execution_environment_id", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD", "expected": None, "actual": context_environment_id, "message": "Required"})
    elif exp == context_environment_id:
        results.append({"check": "execution_environment_id", "status": "PASS", "error_code": None, "expected": exp, "actual": context_environment_id, "message": "Match"})
    else:
        results.append({"check": "execution_environment_id", "status": "BLOCKED", "error_code": "EXECUTION_ENVIRONMENT_MISMATCH", "expected": exp, "actual": context_environment_id, "message": "Mismatch"})

    exp = validated_package.get("execution_mode")
    if not exp:
        results.append({"check": "execution_mode", "status": "UNKNOWN_BLOCKED", "error_code": "MISSING_REQUIRED_FIELD", "expected": None, "actual": context_execution_mode, "message": "Required"})
    elif exp == context_execution_mode:
        results.append({"check": "execution_mode", "status": "PASS", "error_code": None, "expected": exp, "actual": context_execution_mode, "message": "Match"})
    else:
        results.append({"check": "execution_mode", "status": "BLOCKED", "error_code": "EXECUTION_MODE_MISMATCH", "expected": exp, "actual": context_execution_mode, "message": "Mismatch"})
        
    return results

def aggregate_binding_results(results: list, required_checks: set = frozenset()) -> dict:
    precedence = {"UNKNOWN_BLOCKED": 0, "BLOCKED": 1, "FAIL": 2, "NOT_RUN": 3, "PASS": 4}
    
    if not results:
        return {"status": "UNKNOWN_BLOCKED", "error_code": "NO_RESULTS"}
        
    worst_status = "PASS"
    worst_score = precedence["PASS"]
    worst_error_code = None
    
    for res in results:
        s = res["status"]
        if s == "NOT_RUN" and res["check"] in required_checks:
            s = "UNKNOWN_BLOCKED"
            
        if precedence[s] < worst_score:
            worst_score = precedence[s]
            worst_status = s
            worst_error_code = res.get("error_code")
            
    return {
        "status": worst_status,
        "error_code": worst_error_code,
        "details": results
    }
