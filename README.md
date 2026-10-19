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

Open `dist/index.html` in a browser, or serve it:

```bash
python3 -m http.server --directory dist
```

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

## Linting

Python is linted and formatted with [Ruff](https://docs.astral.sh/ruff/) (config in `ruff.toml`). The pre-commit hook runs it automatically, along with basic file checks (trailing whitespace, final newlines, JSON/YAML syntax). To run by hand:

```bash
ruff check . && ruff format .   # lint + format Python
pre-commit run --all-files      # run every hook
```

If a hook auto-fixes something, the commit is stopped — re-stage the changes and commit again.

## Customizing

- **Your content** goes in `data.json`. That's the only file most people need to touch — it's gitignored, so start by copying `data.template.json`. See [docs/guides/data-json.md](docs/guides/data-json.md) for the full walkthrough. `generate.py` validates it against a schema before building anything, so a malformed `data.json` fails fast with a clear error.
- **Images and downloadable files** (resume, etc.) go in `assets/`.
- **Visual style** lives in a single stylesheet: `static/styles.css`.
- Anything deeper (adding a new page/template, changing generation logic) is covered in the root `CLAUDE.md` and `docs/arch/`, which log the structural decisions behind this repo.

## Project layout

```
generate.py           # entry point — delegates to src/operations, contains no logic itself
data.json              # source of truth for all site content (gitignored — copy from data.template.json)
data.template.json     # tracked starting point for data.json; validated against src/schema/ by tests
templates/             # Jinja2 HTML templates
static/styles.css      # the one stylesheet
src/operations/        # build steps (one concern per operation)
src/utils/             # shared helpers used by operations
src/schema/            # JSON Schema for data.json
tests/                 # pytest suite, mirrors src/ path-for-path
assets/                # images, and assets/download/ for files like a resume
docs/arch/             # architecture decision records
docs/refs/             # visual reference material (inspiration, not used at build time)
docs/guides/           # human-readable docs for people forking the repo
dist/                  # generated output (gitignored, rebuilt by generate.py)
requirements.txt       # runtime deps (Jinja2, jsonschema)
requirements-dev.txt   # dev-only deps (pytest, pre-commit, ruff), on top of requirements.txt
ruff.toml              # Ruff lint/format config
.pre-commit-config.yaml  # local hooks: file checks, ruff, then tests/test.py
```

## Status

Early scaffold. `generate.py` runs four build steps, each covered by tests under `tests/`: `parse_data()` (loads and validates `data.json`), `scaffold_dist()` ((re)creates `dist/`'s directory structure), `copy_static()` (copies `static/` into `dist/static/`), and `generate_pages()` (renders `templates/home.html` to `dist/index.html`, and `templates/project.html` once per entry in `data.json`'s `projects` array to `dist/projects/<project_name>/index.html`). `data.json`'s schema currently only models that `projects` array — just `project_name` per entry so far; other content fields (bio, links, downloads) haven't been designed yet. See `CLAUDE.md` for current state; this section is kept in sync as development lands.

## License

MIT, see `LICENSE`.
