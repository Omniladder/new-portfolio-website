# 0019 — Playwright end-to-end tests, separate from the pytest unit suite

**Status:** Accepted

## Context

[[0006-testing-framework]] covers `src/operations/` and `src/utils/`: plain
data/filesystem logic that's cheap to unit test and deliberately doesn't need
a browser. Once `templates/home.html` started rendering real content with
client-side behavior (the dark mode toggle, see
[[0018-light-dark-theme-toggle]]), there was no coverage for whether the
*rendered page* actually works in a browser — whether the toggle flips
`data-theme`, whether the choice survives a reload via `localStorage`,
whether `data.json` content actually shows up. That's not something
0006's unit tests are meant to catch, and doesn't fit tests/'s
mirrors-src/ convention either, since it tests the built site, not a
single `src/` module.

## Decision

- **Playwright**, via the `pytest-playwright` plugin, drives a real
  (headless) browser against the generated site. It's a dev-only dependency
  in `requirements-dev.txt`, same as pytest itself.
- Tests live in `tests/playwright/`, a sibling to `tests/operations/` and
  `tests/utils/` rather than mirroring a `src/` path — there's no single
  `src/` module an end-to-end page test corresponds to.
- A session-scoped fixture in `tests/playwright/conftest.py` builds the site
  with `python3 generate.py --data data.template.json` (the tracked example
  data, not a developer's personal `data.json`) and serves `dist/` over a
  local HTTP server, so the suite runs identically on every clone.
- **Excluded from the default `pytest` run, `tests/test.py`, and the
  pre-commit hook.** `tests/conftest.py` sets `collect_ignore = ["playwright"]`.
  Reason: Playwright needs a one-time `playwright install chromium` browser
  download that pytest/pre-commit can't assume is present, and a real
  browser launch is much slower than the unit suite pre-commit already runs
  on every commit. Run it explicitly with `pytest tests/playwright`.
- These tests assert on rendered behavior (theme toggle, nav anchors,
  content from `data.json` appearing on the page) and on uncaught JS
  exceptions via Playwright's `pageerror` event — not on console "error"
  messages generally, since `data.template.json`'s placeholder asset paths
  (e.g. `assets/example.png`) have no backing file and legitimately 404 in
  the browser; that's expected per-fork asset behavior, not a page bug.

## Consequences

- Running the full picture now takes two commands: `pytest` (or
  `tests/test.py`) for the fast unit suite that pre-commit already runs, and
  `pytest tests/playwright` for the slower browser suite, after a one-time
  `playwright install chromium`.
- A module in `src/` still must have a mirrored unit test per 0006; a new
  template or piece of page behavior should get a matching case in
  `tests/playwright/`, but there's no 1:1 file mapping to enforce the way
  there is for `src/`.
- CI (if/when one exists) needs its own `playwright install chromium` step
  before running `tests/playwright`.

## Keywords

playwright, pytest-playwright, end-to-end tests, e2e, browser tests, theme
toggle, tests/playwright, collect_ignore
