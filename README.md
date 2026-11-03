# Strict Issues First

A read-only GitHub Action enforcing issue provenance for pull requests.

It requires exactly one local closing reference (`Closes #12`, `Fixes #12`, or
`Resolves #12`). The referenced item must be an issue, not a pull request, and
must have been created before the pull request.

```yaml
permissions:
  issues: read
  pull-requests: read
steps:
  - uses: fosghen/issues-first-action@<full-commit-sha>
```

Run on `pull_request` events and make the job a required status check. There are
no author, label, branch, or draft exemptions. Runtime dependencies are limited
to Python 3 and the GitHub REST API.
