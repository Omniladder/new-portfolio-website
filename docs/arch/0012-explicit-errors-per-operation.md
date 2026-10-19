# 0012 — Explicit, operation-scoped error types in src/errors/

**Status:** Accepted

## Context

Before this decision, a failure inside a `src/operations/` function surfaced
as whatever low-level exception caused it — a raw `OSError`,
`json.JSONDecodeError`, `jsonschema.ValidationError`, or `jinja2.TemplateError`
bubbling straight out of `generate.py`. That exception says *what the
underlying library did* but not *which build step was running*, so debugging
a broken fork means reading a traceback and inferring the operation from file
names rather than being told directly.

## Decision

- `src/errors/` is a new top-level directory, mirroring `src/operations/`
  one file per operation module: `src/errors/parse_data.py`,
  `src/errors/scaffold_dist.py`, `src/errors/copy_static.py`,
  `src/errors/generate_pages.py`. Each defines one exception class for that
  operation (e.g. `DataParseError`, `DistScaffoldError`, `StaticCopyError`,
  `PageGenerationError`), subclassing a shared `OperationError` base in
  `src/errors/base.py`.
- Each operation's **root function** — the function other code actually
  calls (`parse_data`, `scaffold_dist`, `copy_static`, and, inside
  `generate_pages.py`, each of `generate_home`, `generate_projects_home`,
  and `generate_projects` individually) — catches the specific low-level
  exceptions it can produce and re-raises the matching `OperationError`
  subclass with a short, human-readable message, chaining the original via
  `raise ... from e`.
- `generate_pages()` itself (the dispatcher that just calls the three
  `generate_*` functions above) is deliberately **not** wrapped — it adds no
  information the functions it calls don't already provide, and wrapping it
  too would double-wrap the same failure.
- Error messages stay short and state what failed (e.g. "Failed to generate
  the project page for 'my-project'"); the full underlying exception is
  still reachable via `__cause__`/the chained traceback for anyone who needs
  more detail, rather than being inlined into the message itself.
- `src/errors/` classes are exempt from the per-function test requirement in
  [[0006-testing-framework]] — they carry no logic, same rationale as
  `generate.py`'s exemption. What *is* tested is that each operation's root
  function raises the right `OperationError` subclass on failure; that
  coverage lives in the existing mirrored test file for the operation (e.g.
  `tests/operations/test_parse_data.py`), not in a new `tests/errors/`.

## Consequences

- A failure during `python3 generate.py` names the build step that failed
  at the top of the traceback, with the original exception still chained
  underneath for full detail.
- Adding a new operation module means adding a matching file in
  `src/errors/` with one exception class, not inventing a new error
  convention.
- `src/errors/` has no tests of its own; `tests/operations/` grows one
  failure-path test per wrapped function instead.

## Keywords

errors, exceptions, src/errors, OperationError, DataParseError,
DistScaffoldError, StaticCopyError, PageGenerationError, error handling,
traceback, raise from
