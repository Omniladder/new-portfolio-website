# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Early-stage scaffold. Directory structure and governing docs are in place; `generate.py`, the templates, and `src/` contain no implementation logic yet. Do not assume generation works — check before relying on it.

## What this is

A personal portfolio site, generated as plain static HTML/CSS/JS from a single `data.json` file, themed like a 90s personal homepage. The explicit goal is that someone can fork this repo and produce their own portfolio by editing `data.json` alone — see `docs/arch/0001-overview-and-goals.md` for the full rationale.

## Structure

```
generate.py        entry point — no logic of its own, calls into src/operations/
data.json           all site content — gitignored, per-fork, see docs/arch/0009
data.template.json  tracked starting point for data.json, validated against src/schema/ by tests
templates/          Jinja2 HTML templates, presentation only
static/styles.css   the one and only stylesheet
src/operations/     build steps (one concern each), called by generate.py
src/utils/           shared helpers used by operations
src/errors/          one exception type per operation, raised at its root function — see docs/arch/0012
src/schema/          JSON Schema for data.json (data.schema.json) — see docs/arch/0008
assets/              images; assets/download/ for files like a resume PDF
dist/                generated output — gitignored, fully rebuilt each run, never hand-edited
docs/arch/           architecture decision records — read before structural changes
docs/refs/           visual inspiration only, not consumed at build time
docs/guides/         human-readable, user-facing docs (e.g. setting up data.json)
requirements.txt     runtime Python deps (Jinja2, jsonschema)
requirements-dev.txt  dev-only deps (pytest, pre-commit, ruff, pre-commit-hooks), on top of requirements.txt
tests/               pytest suite, mirrors src/ path-for-path — see docs/arch/0006
tests/test.py         runs the full suite via pytest.main(); also what the pre-commit hook calls
pytest.ini            pytest config (testpaths, pythonpath)
ruff.toml            Ruff lint/format config — see docs/arch/0011
.pre-commit-config.yaml  local hooks: file hygiene, ruff lint/format, then tests/test.py — see docs/arch/0007, 0011
LICENSE              MIT
```

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

python3 tests/test.py   # run the test suite (same command the pre-commit hook runs)
ruff check . && ruff format .   # lint + format (also run by the pre-commit hook)
pre-commit run --all-files      # run every hook manually
```

## Conventions

- One global stylesheet, at most one JS file per template, only if that template needs behavior.
- No frontend framework, no bundler, no CSS preprocessor.
- `generate.py` stays a thin list of calls into `src/operations/`; actual logic never lives in the entrypoint.
- New architectural decisions get a new numbered file in `docs/arch/`, not edits to old ones.
- Python must pass `ruff check` and `ruff format` (config in `ruff.toml`, see [0011](docs/arch/0011-linting-with-ruff.md)); the pre-commit hook enforces it.
- Every function in `src/operations/` and `src/utils/` gets a Google-style docstring and a test in the mirrored path under `tests/` (see [0006](docs/arch/0006-testing-framework.md)). `generate.py` is exempt from both — it has no logic of its own to document or test.
- Each operation's root function catches the low-level exceptions it can raise and re-raises the matching type from `src/errors/` with a short message, chaining the original via `raise ... from e` (see [0012](docs/arch/0012-explicit-errors-per-operation.md)). `src/errors/` classes themselves have no tests of their own — the failure path is tested in the operation's existing test file instead.

## Recording decisions as they're made

When the user states an architectural or structural decision in conversation — not just when asked to "update the docs" — do the following in the same turn, not as a deferred follow-up:

1. Add a new numbered file in `docs/arch/` capturing it (Context/Decision/Consequences/Keywords, matching the existing ADRs). Never edit an old ADR to reflect a new decision; supersede it instead.
2. Add a row to the table in `docs/CLAUDE.md` so the decision is discoverable by "if you're about to do X."
3. Update this file (root `CLAUDE.md`) if the decision changes the Structure, Workflow, or Conventions sections above.

## Keeping README.md current

`README.md` is user-facing, not agent-facing — treat it as something that drifts out of date the moment functionality changes underneath it. Whenever a change lands that affects something README.md describes (quickstart steps, project layout, status, how to run/test), update the relevant section in the same change rather than leaving it for a separate pass.
