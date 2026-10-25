# new-portfolio-site

A personal portfolio site generated from a single JSON file, styled like it's 1997.

No frameworks, no bundler, no build step beyond a small Python script. Edit `data.json`, run `generate.py`, get a static site in `dist/`.

## Why

Most portfolio templates require you to touch HTML to change your own bio. This one doesn't: all content (name, bio, projects, links, downloads, whatever) lives in `data.json`. The generator reads that file, runs it through Jinja2 templates, and writes plain HTML/CSS/JS to `dist/`. Fork the repo, edit the JSON, done.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp data.template.json data.json   # data.json is gitignored, see docs/guides/data-json.md
# edit data.json with your own info

python3 generate.py
```

To build from a different file, pass `--data`, e.g. `python3 generate.py --data data.template.json` to try the example content without creating `data.json`.

Image processing (pixelating, dithering, and the 32-color palette) is the slow part of a build. Pass `--no-image-processing` to copy images as-is for a quick preview. Don't publish a build made with it, since the images won't have the retro look.

Open `dist/index.html` in a browser, or serve it:

```bash
python3 -m http.server --directory dist
```

## Deploying

`infra/` holds an Ansible playbook that puts the site on a Debian/Ubuntu server or container behind nginx. It syncs the repo (including your `data.json` and `assets/`) to the host, builds it there, and publishes `dist/`. Run it with:

```bash
pip install -r infra/requirements.txt              # one-time, installs Ansible
cp infra/inventory.example.ini infra/inventory.ini # one-time, set your host (gitignored)
infra/deploy.sh                                    # or --check for a dry run
```

See [docs/guides/deploying.md](docs/guides/deploying.md) for the full walkthrough and troubleshooting.

## Testing

Tests cover `src/operations/` and `src/utils/` (not `generate.py`, which contains no logic of its own). Install dev dependencies and run:

```bash
pip install -r requirements-dev.txt
pytest
```

`tests/` mirrors `src/`'s layout path-for-path — e.g. `src/operations/scaffold_dist.py` is tested by `tests/operations/test_scaffold_dist.py`. `python3 tests/test.py` is equivalent to running `pytest`, for anyone who'd rather not remember the command.

A local pre-commit hook runs the linters and then `tests/test.py` before every commit, so a broken test can't be committed. Enable it once per clone:

```bash
pre-commit install
```

### End-to-end tests

`tests/playwright/` drives a real browser against the generated site (the dark mode toggle, nav, rendered `data.json` content). It's separate from the pytest suite above — not run by `pytest`, `tests/test.py`, or the pre-commit hook, since it needs a browser binary pre-commit can't assume is installed. Run it explicitly, after a one-time browser install:

```bash
playwright install chromium   # one-time
pytest tests/playwright
```

The suite builds the site from your own `data.json` and checks it against that same content (every project page, your quotes, your skills), so it tests the site you actually publish. If `data.json` doesn't exist yet, the whole suite is skipped. Checks for optional features, like a project gallery, skip until your data uses them. See [docs/arch/0019](docs/arch/0019-playwright-e2e-tests.md) and [docs/arch/0033](docs/arch/0033-test-against-data-json-only.md).

## Linting

Python is linted and formatted with [Ruff](https://docs.astral.sh/ruff/) (config in `ruff.toml`). The pre-commit hook runs it automatically, along with basic file checks (trailing whitespace, final newlines, JSON/YAML syntax). To run by hand:

```bash
ruff check . && ruff format .   # lint + format Python
pre-commit run --all-files      # run every hook
```

If a hook auto-fixes something, the commit is stopped — re-stage the changes and commit again.

## Customizing

New to the repo? [docs/guides/getting-started.md](docs/guides/getting-started.md) walks through everything you need to touch, step by step.

- **Your content** goes in `data.json`. That's the only file most people need to touch — it's gitignored, so start by copying `data.template.json`. See [docs/guides/data-json.md](docs/guides/data-json.md) for the full walkthrough. `generate.py` validates it against a schema before building anything, so a malformed `data.json` fails fast with a clear error.
- **Images and downloadable files** (resume, etc.) go in `assets/` and `assets/download/`. Like `data.json`, these are gitignored and per-fork — only `.gitkeep` placeholders are tracked, so you add your own files after cloning. The one exception is `assets/core-assets/`, which holds assets the site itself uses and is tracked. See [docs/guides/assets.md](docs/guides/assets.md).
- **Visual style** lives in a single stylesheet: `static/styles.css`.
- Anything deeper (adding a new page/template, changing generation logic) is covered in the root `CLAUDE.md` and `docs/arch/`, which log the structural decisions behind this repo.

## Project layout

```
generate.py           # entry point — delegates to src/operations, contains no logic itself
data.json              # source of truth for all site content (gitignored — copy from data.template.json)
data.template.json     # tracked starting point for data.json; validated against src/schema/ by tests
templates/             # Jinja2 HTML templates
templates/partials/    # shared pieces every page includes (e.g. the site header)
static/styles.css      # the one stylesheet
src/operations/        # build steps (one concern per operation)
src/utils/             # shared helpers used by operations
src/schema/            # JSON Schema for data.json
tests/                 # pytest suite, mirrors src/ path-for-path
tests/playwright/      # browser end-to-end tests, run separately (see docs/arch/0019)
assets/                # images, and assets/download/ for files like a resume (gitignored, per-fork)
assets/core-assets/    # assets the site itself uses (tracked, shared by every fork)
infra/                 # Ansible deploy to an nginx host (infra/deploy.sh, see docs/guides/deploying.md)
docs/arch/             # architecture decision records
docs/design/           # AI-facing design decision records and style guides
docs/refs/             # visual reference material (inspiration, not used at build time)
docs/guides/           # human-readable docs for people forking the repo
docs/examples/         # example projects (placeholder — not written yet)
docs/TODO.md           # deferred work
dist/                  # generated output (gitignored, rebuilt by generate.py)
requirements.txt       # runtime deps (Jinja2, jsonschema, Pillow, tqdm)
requirements-dev.txt   # dev-only deps (pytest, pre-commit, ruff), on top of requirements.txt
ruff.toml              # Ruff lint/format config
.pre-commit-config.yaml  # local hooks: file checks, ruff, then tests/test.py
```

## Status

Core pipeline is implemented and tested. `generate.py` reads its arguments with `parse_args()` (`--data PATH`, `--no-image-processing`), then runs its build steps, each covered by tests under `tests/`: `parse_data()` (loads and validates `data.json` against `src/schema/data.schema.json`), `scaffold_dist()` ((re)creates `dist/`'s directory structure), `copy_static()` (copies `static/` into `dist/static/`), `process_assets()` (copies the images in `assets/` and its subfolders into `dist/assets/`, pixelating each raster image (shrunk to 50%, regrown with nearest-neighbor) and Floyd–Steinberg dithering it down to a 32-color palette; SVGs pass through as-is), `copy_downloads()` (copies `assets/download/` into `dist/assets/download/` as-is), `process_core_assets()` (writes `assets/core-assets/` into `dist/assets/core-assets/`, running its images through the same pipeline and copying other files as-is), and `generate_pages()` (renders `templates/home.html` to `dist/index.html`, `templates/project.html` once per entry in `data.json`'s `projects` array to `dist/projects/<project_name>/index.html`, `templates/education.html` / `templates/experience.html` to `dist/education/index.html` / `dist/experience/index.html`, and `templates/404.html` to `dist/404.html` (a 90s error-dialog page with a Return to Home button, served by nginx for missing URLs); the education page renders the optional `education` list in `data.json` — schools, honors, a GPA chart, and an expandable transcript — while the experience page renders the optional `experience` section — jobs, a career timeline, events, certifications, and a technology toolbox). `data.json`'s schema now models a full `profile` (name, role, tagline, bio, skills, links) and `projects[]` (title, tagline, description, image, technologies, links, plus optional gallery, highlights, and facts). `templates/project_home.html` renders the projects index and `templates/project.html` renders each project page, including optional fields for a screenshot gallery, highlights, project facts, and technologies (featured ones as a logo grid, the rest in a collapsible table underneath; see [docs/guides/data-json.md](docs/guides/data-json.md)). Each build step prints a one-line summary to stderr when it finishes (e.g. `23:05:42  INFO     generate_pages   Rendered 6 pages (home, projects index, 1 project page, education, experience, 404)`). The summaries are colored in a terminal; set `NO_COLOR=1` for plain output. 99 tests pass under `tests/test.py`. See `CLAUDE.md` for current state; this section is kept in sync as development lands.

## License

MIT, see `LICENSE`.
