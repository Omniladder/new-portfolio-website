# Testing and Linting

## Unit and integration tests

Tests cover `src/operations/` and `src/utils/` (not `generate.py`, which contains no logic of its own). Install dev dependencies and run:

```bash
pip install -r requirements-dev.txt
pytest
```

`tests/` mirrors `src/`'s layout path-for-path — e.g. `src/operations/scaffold_dist.py` is tested by `tests/operations/test_scaffold_dist.py`. `python3 tests/test.py` is equivalent to running `pytest`, for anyone who'd rather not remember the command.

A local pre-commit hook runs the linters and then `tests/test.py` before every commit, so a broken test can't be committed. Enable it once per clone:

```bash
pre-commit install
```

## End-to-end tests

`tests/playwright/` drives a real browser against the generated site (the dark mode toggle, nav, rendered `data.json` content). It's separate from the pytest suite — not run by `pytest`, `tests/test.py`, or the pre-commit hook, since it needs a browser binary pre-commit can't assume is installed. Run it explicitly, after a one-time browser install:

```bash
playwright install chromium   # one-time
pytest tests/playwright
```

The suite builds the site from your own `data.json` and checks it against that same content (every project page, your quotes, your skills), so it tests the site you actually publish. If `data.json` doesn't exist yet, the whole suite is skipped. Checks for optional features, like a project gallery, skip until your data uses them. See [docs/arch/0019](../arch/0019-playwright-e2e-tests.md) and [docs/arch/0033](../arch/0033-test-against-data-json-only.md).

## Linting

Python is linted and formatted with [Ruff](https://docs.astral.sh/ruff/) (config in `ruff.toml`). The pre-commit hook runs it automatically, along with basic file checks (trailing whitespace, final newlines, JSON/YAML syntax). To run by hand:

```bash
ruff check . && ruff format .   # lint + format Python
pre-commit run --all-files      # run every hook
```

If a hook auto-fixes something, the commit is stopped — re-stage the changes and commit again.
