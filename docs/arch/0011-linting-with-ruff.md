# 0011 — Ruff and file-hygiene hooks run on pre-commit

**Status:** Accepted

## Context

[[0007-pre-commit-runs-tests]] made pre-commit run the test suite, but
nothing checked style, import order, common bug patterns, or the
Google-style docstrings that [[0006-testing-framework]]-era conventions
require on every `src/operations/` and `src/utils/` function. Basic file
hygiene (trailing whitespace, missing final newline, malformed
`data.template.json`) was also unchecked.

## Decision

- **Ruff** is the Python linter and formatter — one dev-only tool replacing
  flake8, isort, pyupgrade, pydocstyle, and black. Config lives in
  `ruff.toml` at repo root (no `pyproject.toml`; the project isn't packaged).
- Enabled rule sets: `E`, `W` (pycodestyle), `F` (pyflakes), `I` (isort),
  `B` (bugbear), `UP` (pyupgrade), `SIM` (simplify), `D` (pydocstyle, Google
  convention). `D` is ignored for `generate.py` (no logic, per
  [[0004-thin-entrypoint-src-layout]]) and `tests/`; module docstrings are
  optional in `src/`.
- **pre-commit-hooks** (the pip package) supplies generic checks:
  trailing whitespace, end-of-file newline, JSON/YAML syntax, merge-conflict
  markers, large files.
- Both are installed via `requirements-dev.txt` and wired into
  `.pre-commit-config.yaml` as `language: system` local hooks, following
  [[0007-pre-commit-runs-tests]]'s choice of not letting pre-commit manage
  separate environments. They run before the test hook. This extends 0007
  (which described a single hook); it does not change its reasoning.
- `ruff check --fix` and `ruff format` auto-fix in the hook. If they modify
  files the commit is aborted; re-stage and commit again.

## Consequences

- Style and docstring drift is caught at commit time rather than in review.
- No linting for HTML templates, CSS, or JS yet — add a new ADR if one is
  introduced.
- Run manually with `ruff check . && ruff format .`, or all hooks with
  `pre-commit run --all-files`.

## Keywords

ruff, lint, linter, formatter, format, pre-commit-hooks, docstrings,
pydocstyle, ruff.toml, style
