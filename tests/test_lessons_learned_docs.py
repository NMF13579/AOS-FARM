import unittest
import os

class TestLessonsLearnedDocs(unittest.TestCase):
    def test_lessons_learned_boundaries(self):
        filepath = "aos/docs/LESSONS-LEARNED.md"
        self.assertTrue(os.path.exists(filepath), f"{filepath} not found")
        
        with open(filepath, 'r') as f:
            content = f.read().lower()
            
        # Verify boundary statements
        self.assertIn("guidance only", content)
        self.assertIn("not source of truth", content)
        self.assertIn("not approval", content)
        self.assertIn("do not mutate lifecycle", content)
        self.assertIn("do not assign risk profile", content)
        
        # Verify initial lessons
        self.assertIn("pass / evidence / ci pass are never approval", content)
        self.assertIn("queue next is not execution authorization", content)

if __name__ == '__main__':
    unittest.main()
