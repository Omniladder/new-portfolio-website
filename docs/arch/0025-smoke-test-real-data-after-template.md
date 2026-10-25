# 0025 — Smoke builds also run against the real data.json

**Status:** Accepted. Extends [[0014-generate-data-flag-and-protected-data-json]]. Partially superseded by [[0030-agents-may-edit-data-json-on-request]] (in-place edits allowed when the user asks). The template-first step is superseded by [[0033-test-against-data-json-only]]: smoke builds run against `data.json` only.

## Context

0014 told agents to smoke-test builds with `--data data.template.json` only,
so a build never risked the user's untracked `data.json`. In practice the
template has one demo project, while the real `data.json` has more projects,
featured entries, real images, and longer text. Changes could pass on the
template and still break or look wrong with the real content.

`generate.py` only reads its data file; it writes to `dist/` and nothing else.
Building from `data.json` doesn't risk it.

## Decision

- After a change, verify the build in two steps: first
  `python3 generate.py --data data.template.json`, then, if that succeeds,
  `python3 generate.py` against the real `data.json`.
- The real build is read-only for `data.json`. Every protection in 0014 still
  applies: never create, overwrite, move, or delete it.
- If `data.json` is missing, skip the second step and say so. Don't create
  one to make the step run.
- If the template build passes but the real build fails, report it as a real
  failure. Don't change `data.json` to make it pass; tell the user what in
  their data doesn't fit.

## Consequences

- Problems that only show up with real content are caught at change time.
- `dist/` ends up holding the real-data build, which is what the user would
  want to look at anyway.
- Real content isn't tracked, so this check can't run in CI or on another
  fork; the template build stays the reproducible check.

## Keywords

smoke test, data.json, data.template.json, real data, verify build, --data
