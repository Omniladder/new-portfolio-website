# Project Layout

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

## Build status

Core pipeline is implemented and tested. `generate.py` reads its arguments with `parse_args()` (`--data PATH`, `--no-image-processing`), then runs its build steps, each covered by tests under `tests/`:

- `parse_data()` loads and validates `data.json` against `src/schema/data.schema.json`.
- `scaffold_dist()` (re)creates `dist/`'s directory structure.
- `copy_static()` copies `static/` into `dist/static/`.
- `process_assets()` copies the images in `assets/` and its subfolders into `dist/assets/`, pixelating each raster image (shrunk to 50%, regrown with nearest-neighbor) and Floyd–Steinberg dithering it down to a 32-color palette. SVGs pass through as-is.
- `copy_downloads()` copies `assets/download/` into `dist/assets/download/` as-is.
- `process_core_assets()` writes `assets/core-assets/` into `dist/assets/core-assets/`, running its images through the same pipeline and copying other files as-is.
- `generate_pages()` renders the templates into `dist/`: `home.html` to `index.html`, `project_home.html` to `projects/index.html`, `project.html` once per project, `education.html` and `experience.html` (optional sections), and `404.html` (a 90s error-dialog page that nginx serves for missing URLs).

`data.json`'s schema models a full `profile` and `projects[]`, plus the optional `education` and `experience` sections. Each build step prints a one-line summary to stderr when it finishes. The summaries are colored in a terminal; set `NO_COLOR=1` for plain output.
