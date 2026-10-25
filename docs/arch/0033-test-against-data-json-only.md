# 0033 — Smoke builds and browser tests use only the real data.json

**Status:** Accepted. Supersedes the `data.template.json` fallback in
[[0029-playwright-tests-run-against-data-json]] and the template-first smoke
build step in [[0025-smoke-test-real-data-after-template]]. The read-only
protections for `data.json` in [[0014-generate-data-flag-and-protected-data-json]]
and [[0030-agents-may-edit-data-json-on-request]] are unchanged.

## Context

0029 decided the Playwright suite should build from the real `data.json`,
falling back to `data.template.json` when it's missing, but the fixture
was never switched over. It still built from the template, and the tests
hardcoded the template's placeholder values ("Example Person", one example
project). 0025 had agents verify every change with a template build first,
then a real one. In practice the example user exercised almost nothing the
real site does (one project, no images), so passing against it said little.
The user asked to stop testing against the example user entirely.

## Decision

- The session fixture in `tests/playwright/conftest.py` builds with plain
  `python3 generate.py`, which reads `data.json`. There is no fallback: if
  `data.json` doesn't exist, the `site_data` fixture skips the whole suite
  with a message saying so.
- Browser tests take every expected value from `data.json` via the
  `site_data` fixture, never from literals. Project page tests loop over
  every project, and checks for optional content (gallery, highlights,
  phone, ...) run when the data has it and skip otherwise.
- To verify a build after a change, agents run `python3 generate.py`
  against `data.json` only. The `--data data.template.json` step is
  dropped. If `data.json` is missing, report that the build couldn't be
  verified; never create one.
- `data.template.json` is only checked for schema validity: one unit test
  parses it with `parse_data()` and passes if it validates. It doesn't pin
  the file's exact contents, so the example can be edited freely, and the
  site is never built or tested from it. The `--data` flag
  also stays, for people who want to preview the example content.

## Consequences

- Tests and smoke builds check the site the user actually ships.
- On a machine without a `data.json` (a fresh clone, or CI) the browser suite
  is skipped, not run, and a build can't be smoke-tested. There is no longer
  a reproducible baseline that runs everywhere.
- Results depend on each fork's content. A test that skips today (e.g. the
  gallery test, while no project has a gallery) starts running once the data
  includes that feature.
- Changes to templates are no longer exercised against the template's
  every-optional-field example project, so optional sections are only
  covered once real data uses them.

## Keywords

playwright, e2e, smoke test, data.json, data.template.json, example user,
Example Person, site_data, fixture, skip, supersedes 0029, supersedes 0025
