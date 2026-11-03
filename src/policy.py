"""Pure issues-first policy decisions."""

from dataclasses import dataclass
from datetime import datetime
import re


class PolicyError(ValueError):
    """Raised when a pull request violates the policy."""


@dataclass(frozen=True)
class Reference:
    """A same-repository issue reference."""

    number: int


_CLOSING_REFERENCE = re.compile(
    r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(?P<number>[1-9]\d*)\b",
    re.IGNORECASE,
)


def parse_reference(body: str) -> Reference:
    """Return the only local closing reference in a PR body."""
    matches = list(_CLOSING_REFERENCE.finditer(body))
    if len(matches) != 1:
        raise PolicyError("pull request body must contain exactly one closing issue reference")
    return Reference(int(matches[0].group("number")))


def validate(
    is_pull_request: bool,
    issue_created: datetime,
    pr_created: datetime,
) -> None:
    """Validate the referenced item and temporal order."""
    if is_pull_request:
        raise PolicyError("closing reference points to a pull request, not an issue")
    if issue_created >= pr_created:
        raise PolicyError("referenced issue must be created before the pull request")
