import os
import re
import unittest


class TestAOSRoutesDocs(unittest.TestCase):
    def setUp(self):
        self.filepath = "aos/docs/ROUTES.md"
        self.assertTrue(os.path.exists(self.filepath), f"{self.filepath} not found")
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.content = f.read()
        self.lower_content = self.content.lower()
        self.normalized_content = re.sub(r"\s+", " ", self.content.replace("`", " "))

    def test_first_interaction_route_matrix_required_phrases(self):
        self.assertIn("First-Interaction Route Matrix", self.content)
        for phrase in [
            "сделай",
            "исправь",
            "проверь",
            "собери задачу",
            "передай агенту",
            "можно выполнять?",
            "готово?",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.content)

    def test_first_interaction_route_matrix_forbidden_implications(self):
        required_boundaries = [
            "сделай must not create execution authorization",
            "проверь must not create approval",
            "исправь must not create broad repo mutation",
            "собери задачу must not authorize execution",
            "передай агенту must not grant approval or execution authorization",
            "можно выполнять? must not create automatic approval",
            "готово? must not mutate lifecycle",
            "Vague wording must not create merge authorization",
            "Vague wording must not create release authorization",
            "Vague wording must not create destructive operation authorization",
            "Vague wording must not create protected/canonical mutation authorization",
            "Vague wording must not create scope expansion",
        ]
        for boundary in required_boundaries:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.normalized_content)

    def test_first_interaction_route_matrix_keeps_transport_separate(self):
        for boundary in [
            "Commit authorization requires an explicit commit phrase",
            "Push authorization requires a separate explicit push phrase",
            "Merge authorization requires a separate explicit merge phrase",
            "Release authorization requires a separate explicit release phrase",
            "Destructive operations are forbidden by default",
            "Protected/canonical changes require a human checkpoint",
        ]:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.normalized_content)

    def test_first_interaction_route_matrix_is_not_runtime_classifier(self):
        self.assertIn("not a runtime", self.lower_content)
        self.assertIn("natural-language classifier", self.lower_content)
        self.assertIn("ai auto-approval", self.lower_content)


if __name__ == "__main__":
    unittest.main()
