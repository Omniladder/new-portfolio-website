# 0015 — Every operation logs one INFO line when it finishes

**Status:** Accepted

## Context

`python3 generate.py` printed nothing on success. Someone building their
fork couldn't tell which steps ran, which data file was read, or how much
each step did (how many projects, pages, images) without opening `dist/`.

## Decision

- Logging uses the standard library `logging` module. No new dependency.
- `src/utils/log.py` holds the shared pieces:
  - `get_logger(operation)` returns the `portfolio.<operation>` logger. Every
    operation logs under the `portfolio` namespace and never touches the root
    logger.
  - `OperationFormatter` renders each record as one aligned line,
    `HH:MM:SS  LEVEL    operation        message`, where the operation column
    is the last segment of the logger name.
  - Colors (dim time, colored level, cyan operation) are used only when the
    stream is a terminal and `NO_COLOR` is unset (`supports_color`), so piped
    or redirected output stays plain text.
  - `pluralize(count, noun, plural=None)` keeps the counts in messages
    grammatical.
- Setup is its own operation, `src/operations/configure_logging.py`, called
  first in `generate.py`. That keeps `generate.py` a plain list of operation
  calls ([[0004-thin-entrypoint-src-layout]]). It attaches one handler, on
  stderr at INFO by default, to the `portfolio` logger. Calling it again
  replaces that handler instead of adding a second one. Like `parse_args`, it
  has no `src/errors/` type.
- **Every operation's root function logs exactly one INFO line as its last
  step, after it succeeds.** The line says what the operation did, with
  concrete counts or paths (e.g. `Validated data.template.json against the
  schema (1 project)`). Paths go through `display_path()` in
  `src/utils/paths.py`, which shows them relative to the repo root when
  they're inside it. Helpers that a root function calls (e.g.
  `generate_home`, `process_asset`) don't log at INFO, so each operation
  produces one line. They may log at DEBUG.
- A failed operation doesn't log a completion line. It raises its
  `src/errors/` type ([[0012-explicit-errors-per-operation]]), and the
  traceback reports the failure.
- Tests check the completion line with pytest's `caplog` fixture, in the
  operation's existing mirrored test file. They call
  `caplog.set_level(logging.INFO, logger="portfolio")`, because tests don't
  run `configure_logging()`.

## Consequences

- A successful build prints one line per step, in pipeline order, to stderr.
- Adding an operation means adding a `get_logger("<name>")` module logger, one
  INFO line at the end of its root function, and a `caplog` test for that
  line.
- Progress output from third-party libraries (e.g. `tqdm` in
  `process_assets`) still writes to stderr directly, alongside the log lines.

## Keywords

logging, log, console output, INFO, stderr, configure_logging, get_logger,
OperationFormatter, NO_COLOR, ANSI colors, caplog
