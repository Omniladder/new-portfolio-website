# 0029 — Playwright tests run against the real data.json

**Status:** Accepted. Supersedes the "build from `data.template.json`" part
of [[0019-playwright-e2e-tests]]; the rest of 0019 still applies. The
`data.template.json` fallback is superseded by [[0033-test-against-data-json-only]]:
the suite now skips when `data.json` is missing.

## Context

0019 had the Playwright fixture build the site from `data.template.json` and
the tests assert on its placeholder values ("Example Person", "Example
Project", one project card). That kept the suite identical on every clone,
but the template's single demo project and missing images don't look like a
real site. Layout, card counts, featured sections and per-section content
(e.g. [[0028-per-section-header-quotes]]) can pass on the template and still
break with real content. [[0025-smoke-test-real-data-after-template]] already
made the same call for smoke builds.

## Decision

- The session fixture in `tests/playwright/conftest.py` builds with
  `python3 generate.py` against the real `data.json`, not
  `--data data.template.json`.
- Tests stop hardcoding placeholder values. They load the same `data.json`
  the site was built from and derive what they expect from it (name, quotes,
  project titles, project counts, featured projects).
- `data.json` stays read-only. Every protection in
  [[0014-generate-data-flag-and-protected-data-json]] still applies: tests
  never create, overwrite, move, or delete it.
- If `data.json` is missing (a fresh clone, or CI), the fixture falls back to
  `data.template.json`. Because expected values come from whichever file was
  built, the same tests pass on both.

## Consequences

- The browser suite checks the site the user actually ships.
- Tests can't assume a fixed number of projects or specific strings, so
  assertions are written in terms of the data rather than literals.
- Results can differ between machines, because each fork's `data.json` is
  different. The template fallback is still the reproducible baseline.
- Real assets exist for real data, so 404s from placeholder paths mostly go
  away. The `pageerror`-only check from 0019 stays, since the template
  fallback still has placeholder paths.

## Keywords

playwright, e2e, data.json, data.template.json, Example Person, fixture,
site_url, real data, supersedes 0019
