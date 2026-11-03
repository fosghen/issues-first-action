# Contribution rules

Work from an existing GitHub issue on a separate branch and deliver through one
pull request that closes that issue. Keep commits at or below 50 changed lines
and pull requests at or below five commits.

Use the Python standard library only at runtime. Keep policy decisions pure and
typed; isolate GitHub event and API access. Add a failing test before behavior
changes, then run the complete test suite. Never add author, branch, or label
exemptions to the core issues-first rule.

The action must need read-only permissions. Pin all third-party actions to full
commit SHAs. Do not publish tags or releases without explicit authorization.
