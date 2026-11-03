from datetime import datetime
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .policy import PolicyError, parse_reference, validate

def _timestamp(value: object) -> datetime:
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def evaluate(event: dict, item: dict) -> int:
    pull_request = event.get("pull_request")
    if not isinstance(pull_request, dict):
        raise PolicyError("issues-first requires a pull_request event")
    reference = parse_reference(str(pull_request.get("body") or ""))
    if item.get("number") != reference.number:
        raise PolicyError("GitHub returned an unexpected item")
    validate(
        "pull_request" in item,
        _timestamp(item.get("created_at")),
        _timestamp(pull_request.get("created_at")),
    )
    return reference.number

def _fetch_item(number: int) -> dict:
    url = f"{os.environ['GITHUB_API_URL']}/repos/{os.environ['GITHUB_REPOSITORY']}/issues/{number}"
    request = Request(url, headers={"Authorization": f"Bearer {os.environ['INPUT_TOKEN']}"})
    try:
        with urlopen(request) as response:  # nosec: B310 - URL is GitHub-provided
            return json.load(response)
    except HTTPError as error:
        raise PolicyError(f"GitHub issue lookup failed with HTTP {error.code}") from error

def main() -> None:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    pull_request = event.get("pull_request") or {}
    reference = parse_reference(str(pull_request.get("body") or ""))
    number = evaluate(event, _fetch_item(reference.number))
    with Path(os.environ["GITHUB_OUTPUT"]).open("a") as output:
        output.write(f"issue-number={number}\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, PolicyError, ValueError) as error:
        raise SystemExit(f"issues-first: {error}") from error
