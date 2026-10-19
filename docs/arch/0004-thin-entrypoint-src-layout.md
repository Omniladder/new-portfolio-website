# 0004 — Thin entrypoint, logic in src/operations and src/utils

**Status:** Accepted

## Context

`generate.py` is the command a user runs. Keeping it readable matters more than keeping it short in the usual "entrypoint" sense — someone debugging their own fork should be able to open it and see the build as a sequence of named steps.

## Decision

- `generate.py` contains no logic of its own. It only imports and calls functions from `src/operations/`.
- `src/operations/` holds the actual build steps (e.g. loading `data.json`, rendering a template, writing `dist/`), one concern per operation.
- `src/utils/` holds helpers shared across operations (e.g. path resolution, Jinja environment setup) that aren't themselves a build step.
- Output always goes to `dist/`, which is gitignored and fully regenerated on each run — nothing in `dist/` is hand-edited or persisted between builds.

## Consequences

- Adding a build step means adding a function in `src/operations/` and one line in `generate.py`, not editing a monolith.
- `dist/` must never be relied on as a place to store state; a `generate.py` run should be safe to treat as "delete dist/ and rebuild."

## Keywords

generate.py, entrypoint, src/operations, src/utils, dist, build pipeline
