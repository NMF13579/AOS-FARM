import unittest
import json
import os
from aos.scripts.aos_semantic_guard import collect_semantic_guard_violations

class TestAOSSemanticGuard(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "validator-readiness-approval-semantics"
        )
        
    def test_semantic_guard_fixtures(self):
        fixture_files = [f for f in os.listdir(self.fixtures_dir) if f.endswith(".json")]
        self.assertEqual(len(fixture_files), 10, "Expected exactly 10 semantic guard fixtures")
        
        for filename in fixture_files:
            filepath = os.path.join(self.fixtures_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                fixture = json.load(f)
                
            payload = fixture["payload"]
            expected_phrase = fixture["expected_phrase"]
            
            violations = collect_semantic_guard_violations(payload)
            self.assertIn(
                expected_phrase, 
                violations, 
                f"Fixture {filename} failed to trigger '{expected_phrase}'"
            )

    def test_safe_baseline_payload(self):
        safe_payload = {
            "title": "A safe task",
            "status": "IN_PROGRESS",
            "validation_status": "NOT_RUN",
            "approval_status": "NOT_APPROVED",
            "commit_authorized": False,
            "push_authorized": False,
            "release_authorized": False,
            "human_review_required": True,
            "evidence": [{"status": "VERIFIED"}]
        }
        violations = collect_semantic_guard_violations(safe_payload)
        self.assertEqual(len(violations), 0, f"Expected 0 violations for safe payload, got: {violations}")

if __name__ == "__main__":
    unittest.main()
