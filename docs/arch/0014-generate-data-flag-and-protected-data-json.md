# 0014 — `generate.py --data`, and data.json is never touched by tooling

**Status:** Accepted

## Context

`generate.py` always read `ROOT_DIR/data.json`, the per-fork, gitignored
content file from [[0009-data-json-gitignored-with-tracked-example]]. To run
a real build, the only option was to put something at that exact path. Several
agent sessions smoke-tested the build by copying `data.template.json` over
`data.json` (sometimes overwriting it), running the build, and then deleting
`data.json` as "cleanup." Because `data.json` is never committed, each of those
runs destroyed the user's content with nothing to restore it from.

## Decision

- `generate.py` accepts an optional `--data PATH` argument. Without it, the
  build reads `data.json` at the repo root as before. With it, the build reads
  `PATH` instead, e.g. `python3 generate.py --data data.template.json`.
- Argument parsing is its own operation, `src/operations/parse_args.py`, so
  `generate.py` stays a thin list of calls
  ([[0004-thin-entrypoint-src-layout]]). It returns an `argparse.Namespace`
  whose `data` is passed straight to `parse_data()`.
- `parse_args` has no `src/errors/` type, an exception to
  [[0012-explicit-errors-per-operation]]: argparse already prints a usage
  message naming the bad argument and exits with status 2, which is the
  standard behavior for a CLI and clearer than a wrapped exception.
- **Tooling and agents never create, overwrite, move, or delete `data.json`.**
  It belongs to whoever forked the repo. Smoke tests and throwaway builds use
  `--data` with `data.template.json` or a file in a temp directory. If a
  build needs the real `data.json` and it's missing, ask the user rather than
  creating one.

## Consequences

- A full build can be checked without touching the user's content.
- Tests already used `tmp_path` for data files; this extends the same rule to
  manual and agent-driven runs.
- `dist/` is still overwritten by any build, `--data` or not. It's generated
  output and safe to rebuild ([[0004-thin-entrypoint-src-layout]]).

## Keywords

generate.py, --data, argparse, parse_args, CLI, command line, data.json,
smoke test, deleted, overwritten, data.template.json
