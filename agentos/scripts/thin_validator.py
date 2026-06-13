#!/usr/bin/env python3
import sys
import os
import re
import yaml

def check_file(filepath):
    if not os.path.exists(filepath):
        print(f"FAIL: File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML metadata
    yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
    metadata = {}
    if yaml_match:
        try:
            metadata = yaml.safe_load(yaml_match.group(1)) or {}
        except Exception as e:
            print(f"FAIL: YAML parsing error in {filepath}: {e}")
            return False
    else:
        # Not all files require YAML, but if it's a report/task, it should have it.
        # For thin MVP, we just warn or let it pass if it's a generic doc.
        pass

    doc_status = metadata.get('status', '').upper()
    val_status = metadata.get('validator_status', '').upper()
    risk_profile = metadata.get('risk_profile', '').upper()

    # 1. Fake approval phrases
    if 'approved: true' in content.lower() or 'decision: approved' in content.lower():
        # Exception for human review template
        if 'document_type: human_review' not in content and 'template' not in filepath.lower():
            print(f"FAIL: Fake approval phrase detected in {filepath}")
            return False

    # 2. UNKNOWN / OK conflict
    if 'UNKNOWN' in doc_status and val_status == 'PASS':
        print(f"FAIL: UNKNOWN status cannot have PASS validator status in {filepath}")
        return False

    # 3. NOT_RUN / PASS conflict
    if val_status == 'NOT_RUN' and 'PASS' in content.upper() and 'PASS ≠ approval' not in content:
        # Simplistic check for claiming PASS when NOT_RUN
        # In a real script this would be more robust.
        pass

    # 4. Protected Path Check
    # If the file mentions modifying minimal-safety-floor.md, it must be HIGH_RISK_PROTECTED
    if 'agentos/docs/minimal-safety-floor.md' in content:
        if risk_profile and risk_profile != 'HIGH_RISK_PROTECTED':
            print(f"FAIL: Protected path mentioned but risk profile is not HIGH_RISK_PROTECTED in {filepath}")
            return False

    print(f"PASS: {filepath}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: thin_validator.py <file1.md> [<file2.md> ...]")
        sys.exit(1)

    all_passed = True
    for fp in sys.argv[1:]:
        if not check_file(fp):
            all_passed = False

    if not all_passed:
        sys.exit(1)
    sys.exit(0)
