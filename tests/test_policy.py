import unittest
from datetime import datetime, timezone

from src.policy import PolicyError, Reference, parse_reference, validate


class PolicyTests(unittest.TestCase):
    def test_parses_one_closing_reference(self) -> None:
        self.assertEqual(parse_reference("Summary\n\nCloses #12"), Reference(12))

    def test_rejects_missing_reference(self) -> None:
        with self.assertRaisesRegex(PolicyError, "exactly one"):
            parse_reference("Relates to #12")

    def test_rejects_multiple_references(self) -> None:
        with self.assertRaisesRegex(PolicyError, "exactly one"):
            parse_reference("Fixes #1 and resolves #2")

    def test_accepts_issue_created_before_pull_request(self) -> None:
        issue = datetime(2026, 1, 1, tzinfo=timezone.utc)
        pull_request = datetime(2026, 1, 2, tzinfo=timezone.utc)
        validate(is_pull_request=False, issue_created=issue, pr_created=pull_request)

    def test_rejects_pull_request_reference(self) -> None:
        now = datetime.now(timezone.utc)
        with self.assertRaisesRegex(PolicyError, "not an issue"):
            validate(is_pull_request=True, issue_created=now, pr_created=now)

    def test_rejects_late_issue(self) -> None:
        issue = datetime(2026, 1, 2, tzinfo=timezone.utc)
        pull_request = datetime(2026, 1, 1, tzinfo=timezone.utc)
        with self.assertRaisesRegex(PolicyError, "before"):
            validate(False, issue, pull_request)


if __name__ == "__main__":
    unittest.main()
