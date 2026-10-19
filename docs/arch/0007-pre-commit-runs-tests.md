# 0007 — pre-commit runs the test suite before every commit

**Status:** Accepted

## Context

[[0006-testing-framework]] established pytest and `tests/test.py` as the way
to run the suite, but nothing enforced actually running it before code
landed. Catching a broken `src/operations/`/`src/utils/` function at commit
time is cheaper than catching it later.

## Decision

- `pre-commit` is a dev-only dependency, added to `requirements-dev.txt`
  alongside pytest.
- `.pre-commit-config.yaml` defines a single local hook that runs
  `python3 tests/test.py` (not a separate pytest invocation) — one command is
  the source of truth for "run the tests," whether invoked by a human or by
  the hook.
- The hook uses `language: system`, running against whatever Python
  environment the developer already has active (the one `requirements-dev.txt`
  was installed into), rather than pre-commit managing its own isolated
  environment. This avoids a second place where test dependencies need
  installing.
- `always_run: true` / `pass_filenames: false`: the full suite runs on every
  commit regardless of which files changed, since the suite is small and a
  changed file in `src/` can affect behavior tested elsewhere.
- Each developer runs `pre-commit install` once after setting up their venv;
  this is a local git hook (`.git/hooks/pre-commit`), not something committed
  or enforced server-side.

## Consequences

- A commit with a failing test is blocked locally before it's made, not
  caught later in CI or review.
- Anyone who skips `pip install -r requirements-dev.txt` or
  `pre-commit install` doesn't get the hook — this is a local safety net, not
  a substitute for CI if one is added later.
- If the test suite ever becomes slow enough that `always_run` on every
  commit is painful, that's a signal to speed up the suite, not to start
  scoping the hook to changed files.

## Keywords

pre-commit, git hooks, tests/test.py, local hook, requirements-dev.txt
