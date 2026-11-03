import unittest

from src.entrypoint import evaluate
from src.policy import PolicyError


class EntrypointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.event = {
            "pull_request": {
                "body": "Closes #7",
                "created_at": "2026-01-02T00:00:00Z",
            }
        }
        self.issue = {
            "number": 7,
            "created_at": "2026-01-01T00:00:00Z",
        }

    def test_returns_issue_number_for_valid_event(self) -> None:
        self.assertEqual(evaluate(self.event, self.issue), 7)

    def test_rejects_non_pull_request_event(self) -> None:
        with self.assertRaisesRegex(PolicyError, "pull_request event"):
            evaluate({}, self.issue)

    def test_rejects_mismatched_api_response(self) -> None:
        self.issue["number"] = 8
        with self.assertRaisesRegex(PolicyError, "unexpected item"):
            evaluate(self.event, self.issue)

    def test_rejects_api_item_that_is_a_pull_request(self) -> None:
        self.issue["pull_request"] = {"url": "https://example.invalid"}
        with self.assertRaisesRegex(PolicyError, "not an issue"):
            evaluate(self.event, self.issue)


if __name__ == "__main__":
    unittest.main()
