# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Core pipeline is implemented and working: `generate.py` runs `parse_args` → `parse_data` → `scaffold_dist` → `copy_static` → `process_assets` → `copy_downloads` → `copy_core_assets` → `generate_pages`, each covered by tests under `tests/` (79 passing as of this writing). The `data.json` schema (`src/schema/data.schema.json`) models a full `profile` and `projects[]`, and `templates/home.html` renders it. `templates/project_home.html` renders the projects index, and `templates/project.html` renders each project page (links as buttons, preview, technologies, optional gallery with a CSS-only lightbox, highlights, and facts). `templates/education.html` renders the optional `education` list (school hero, facts, honors, a GPA-by-term chart, course projects, and an expandable per-term transcript; see docs/arch/0036) at `education/index.html`, and `templates/experience.html` renders the optional `experience` section (current-role hero, a career timeline chart, work history, hackathon cards linked to their projects, certifications, and a merged technology toolbox; see docs/arch/0037) at `experience/index.html`; both are linked from the header and footer nav (see docs/arch/0035). Run `python3 generate.py` (against `data.json`) to verify a build before relying on it.

## What this is

A personal portfolio site, generated as plain static HTML/CSS/JS from a single `data.json` file, themed like a 90s personal homepage. The explicit goal is that someone can fork this repo and produce their own portfolio by editing `data.json` alone — see `docs/arch/0001-overview-and-goals.md` for the full rationale.

## Structure

```
generate.py        entry point — no logic of its own, calls into src/operations/
data.json           all site content — gitignored, per-fork, see docs/arch/0009
data.template.json  tracked starting point for data.json, validated against src/schema/ by tests
templates/          Jinja2 HTML templates, presentation only
templates/partials/ shared fragments included by every page (e.g. header.html), never rendered alone, see docs/arch/0024
static/styles.css   the one and only stylesheet — dark (default) + light theme via CSS vars, see docs/arch/0018, 0026
static/theme-toggle.js  shared theme toggle script, included by every template, see docs/arch/0018
src/operations/     build steps (one concern each), called by generate.py
src/utils/           shared helpers used by operations
src/errors/          one exception type per operation, raised at its root function — see docs/arch/0012
src/schema/          JSON Schema for data.json (data.schema.json) — see docs/arch/0008
assets/              images; assets/download/ for files like a resume PDF — gitignored, per-fork, see docs/arch/0013
                     assets/core-assets/ is the exception: tracked, app-owned assets every fork shares, see docs/arch/0017
                     images (any subfolder, e.g. assets/projects/<project_name>/, assets/logos/) are copied/processed
                     into dist/assets/ by process_assets, see docs/arch/0016, 0032
                     assets/core-assets/ is copied into dist/assets/core-assets/ by copy_core_assets, see docs/arch/0020
dist/                generated output — gitignored, fully rebuilt each run, never hand-edited
docs/arch/           architecture decision records — read before structural changes
docs/design/         AI-facing design decision records and style guides — read before visual changes
docs/refs/           visual inspiration only, not consumed at build time
docs/guides/         human-readable, user-facing docs (e.g. setting up data.json)
docs/examples/       example projects — empty placeholder for now, see docs/TODO.md
docs/TODO.md         deferred work, not yet decisions
requirements.txt     runtime Python deps (Jinja2, jsonschema, tqdm)
requirements-dev.txt  dev-only deps (pytest, pre-commit, ruff, pre-commit-hooks, pytest-playwright), on top of requirements.txt
tests/               pytest suite, mirrors src/ path-for-path — see docs/arch/0006
tests/playwright/     browser end-to-end tests against data.json only (skipped if it's missing), run separately (not part of tests/test.py or pre-commit), see docs/arch/0019, 0033
tests/test.py         runs the full suite via pytest.main(); also what the pre-commit hook calls
pytest.ini            pytest config (testpaths, pythonpath)
ruff.toml            Ruff lint/format config — see docs/arch/0011
.pre-commit-config.yaml  local hooks: file hygiene, ruff lint/format, then tests/test.py — see docs/arch/0007, 0011
LICENSE              MIT
```

## Editing data.json

`data.json` is the user's own content. It's gitignored and never committed, so if it's overwritten or deleted there is no copy to restore. When the user asks for a content change, edit it in place, change only the fields the request covers, and say what changed. Never delete, move, or recreate it, and never replace it with `data.template.json` or test data, including as "cleanup" after a test. To check that a build works, run `python3 generate.py` against the real `data.json`; don't build or test with `data.template.json`. If `data.json` is missing, say the build couldn't be verified; never create one. If the real build fails, report it and don't edit `data.json` to fix it unless the user asks. See [0014](docs/arch/0014-generate-data-flag-and-protected-data-json.md), [0025](docs/arch/0025-smoke-test-real-data-after-template.md), [0033](docs/arch/0033-test-against-data-json-only.md), and [0030](docs/arch/0030-agents-may-edit-data-json-on-request.md).

## Before making structural changes

Check `docs/CLAUDE.md` — it maps "if you're about to do X" to the relevant decision record in `docs/arch/`. The decisions already made there (single stylesheet, data.json as sole content source, thin `generate.py`, no framework/bundler) override default instincts to add tooling or split files "for organization." If a request conflicts with a recorded decision, say so rather than silently working around it.

## Workflow (once implemented)

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install   # one-time, enables the pre-commit test hook
cp data.template.json data.json   # one-time, data.json is gitignored (docs/arch/0009)
# edit data.json
python3 generate.py
# output in dist/

python3 generate.py   # smoke test: real data.json only (read-only), see docs/arch/0033

python3 tests/test.py   # run the test suite (same command the pre-commit hook runs)
ruff check . && ruff format .   # lint + format (also run by the pre-commit hook)
pre-commit run --all-files      # run every hook manually

playwright install chromium     # one-time, for the e2e suite below
pytest tests/playwright         # browser end-to-end tests against data.json only; not run by tests/test.py or pre-commit, see docs/arch/0019, 0033
```

## Conventions

- One global stylesheet, at most one JS file per template, only if that template needs behavior.
- No frontend framework, no bundler, no CSS preprocessor.
- Dark mode is the default theme (see [0026](docs/arch/0026-dark-mode-default.md)); a toggle in the header switches to the light palette and the choice is remembered via `localStorage`. Both palettes live in `static/styles.css` as CSS custom properties under a `data-theme` attribute; the toggle behavior is one shared `static/theme-toggle.js` included by every template (see [0018](docs/arch/0018-light-dark-theme-toggle.md)).
- `generate.py` stays a thin list of calls into `src/operations/`; actual logic never lives in the entrypoint.
- New architectural decisions get a new numbered file in `docs/arch/`, not edits to old ones.
- Durable non-architectural design decisions and AI-facing style guides get a new numbered file in `docs/design/`, using the same Context/Decision/Consequences/Keywords format as ADRs. See `docs/design/CLAUDE.md`.
- Python must pass `ruff check` and `ruff format` (config in `ruff.toml`, see [0011](docs/arch/0011-linting-with-ruff.md)); the pre-commit hook enforces it.
- Every function in `src/operations/` and `src/utils/` gets a Google-style docstring and a test in the mirrored path under `tests/` (see [0006](docs/arch/0006-testing-framework.md)). `generate.py` is exempt from both — it has no logic of its own to document or test.
- Each operation's root function ends by logging one INFO line through `get_logger("<operation>")` from `src/utils/log.py`, saying what it did with concrete counts/paths. It never uses `print()`. `configure_logging()` is the first call in `generate.py` (see [0015](docs/arch/0015-operations-log-on-completion.md)).
- App-owned assets the site depends on regardless of whose portfolio it is go in `assets/core-assets/` (tracked); never put personal/per-fork files there, they'd be committed (see [0017](docs/arch/0017-core-assets-tracked.md)). `copy_core_assets` copies it into `dist/assets/core-assets/` as a plain copy, same as `copy_downloads` (see [0020](docs/arch/0020-core-assets-copy-pipeline-and-icon-theming.md)).
- `process_assets` copies every image under `assets/`, recursively, into the mirrored path in `dist/assets/`, skipping `assets/download/` and `assets/core-assets/` (copied by their own operations). Each image goes through a read → manipulate → write hook in `src/utils/images.py`; the manipulate step is a no-op today (see [0016](docs/arch/0016-process-assets-image-pipeline.md), [0032](docs/arch/0032-assets-organized-in-subfolders.md)). Recommended layout: `assets/projects/<project_name>/`, `assets/logos/`, `assets/profile/`, `assets/education/`, `assets/events/<event>/`.
- Icons referenced from templates use `<span class="icon icon-<name>">`, never `<img>`, so `static/styles.css`'s `mask-image` + `background-color: currentColor` technique can tint a single monochrome SVG per theme (see [0020](docs/arch/0020-core-assets-copy-pipeline-and-icon-theming.md)).
- Internal links between pages target `index.html` explicitly (`projects/index.html`, never `projects/`), so the site works when opened from disk via `file://` (see [0027](docs/arch/0027-explicit-index-html-links.md)).
- Each operation's root function catches the low-level exceptions it can raise and re-raises the matching type from `src/errors/` with a short message, chaining the original via `raise ... from e` (see [0012](docs/arch/0012-explicit-errors-per-operation.md)). `src/errors/` classes themselves have no tests of their own — the failure path is tested in the operation's existing test file instead.

## Recording decisions as they're made

When the user states an architectural or structural decision in conversation — not just when asked to "update the docs" — do the following in the same turn, not as a deferred follow-up:

1. Add a new numbered file in `docs/arch/` capturing it (Context/Decision/Consequences/Keywords, matching the existing ADRs). Never edit an old ADR to reflect a new decision; supersede it instead.
2. Add a row to the table in `docs/CLAUDE.md` so the decision is discoverable by "if you're about to do X."
3. Update this file (root `CLAUDE.md`) if the decision changes the Structure, Workflow, or Conventions sections above.

## Keeping README.md current

`README.md` is user-facing, not agent-facing — treat it as something that drifts out of date the moment functionality changes underneath it. Whenever a change lands that affects something README.md describes (quickstart steps, project layout, status, how to run/test), update the relevant section in the same change rather than leaving it for a separate pass.
