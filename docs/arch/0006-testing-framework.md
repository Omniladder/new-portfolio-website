# 0006 — pytest, with tests/ mirroring src/

**Status:** Accepted

## Context

`src/operations/` and `src/utils/` are starting to accumulate real logic
(e.g. [[0005-dist-mirrors-root-paths]]). That logic needs automated coverage
that doesn't depend on being able to render a browser or inspect generated
HTML by eye — it operates on the filesystem and on plain data, which is cheap
to unit test directly.

## Decision

- **pytest** is the test framework. It's a dev-only dependency, not something
  `generate.py` or any shipped site needs at runtime, so it lives in
  `requirements-dev.txt` (which pulls in `requirements.txt`) rather than
  `requirements.txt` itself.
- `tests/` mirrors `src/`'s internal layout path-for-path:
  `src/operations/scaffold_dist.py` is tested by
  `tests/operations/test_scaffold_dist.py`, `src/utils/paths.py` by
  `tests/utils/test_paths.py`, and so on. Finding the test for a module never
  requires guessing a different convention.
- Every function in `src/operations/` and `src/utils/` gets a test. New
  functions added there come with a test in the mirrored path in the same
  change.
- `generate.py` is explicitly **not** unit tested. Per
  [[0004-thin-entrypoint-src-layout]] it contains no logic of its own — it's
  a list of calls into `src/operations/`, which are tested individually.
  Testing it would mean re-testing those operations through an extra layer of
  indirection for no added signal.
- `pytest.ini` sets `pythonpath = .` so test modules can `import src...`
  without `src/` needing `__init__.py` files or install-time packaging.

## Consequences

- Running `pytest` from repo root is the whole test workflow; no extra
  config or `PYTHONPATH` exports needed.
- A module in `src/` with no corresponding file under `tests/` is a gap, not
  a style choice — the mirrored layout makes missing coverage visible by
  inspection.
- If `generate.py` ever grows actual logic instead of delegating, that logic
  belongs in a new `src/operations/` function (per 0004) and gets tested
  there, not by special-casing `generate.py` in the test suite.

## Keywords

pytest, testing, tests/, test framework, requirements-dev.txt, pythonpath, unit tests
