# 0039 — Drop the large-file pre-commit check

**Status:** Accepted. Amends the hook list in [[0011-linting-with-ruff]].

## Context

0011 included `check-added-large-files` among the file-hygiene hooks. The
repo deliberately tracks binary files, such as the reference screenshots in
`docs/refs/` ([[0031-docs-refs-tracked]]) and the shared assets in
`assets/core-assets/` ([[0017-core-assets-tracked]]). Those regularly go
over the hook's default 500 KB limit and block commits that are intended.

## Decision

Remove `check-added-large-files` from `.pre-commit-config.yaml`. The other
hygiene hooks, Ruff, and the test run stay as they were.

## Consequences

- Committing large images and reference files no longer fails the hook.
- Nothing stops an accidentally huge file from being committed now. Per-fork
  content (`assets/`, `data.json`, `dist/`) is still gitignored, so the main
  source of big files stays out of git anyway.

## Keywords

pre-commit, hooks, check-added-large-files, large files, binary, docs/refs, core-assets
