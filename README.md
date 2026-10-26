# new-portfolio-site

A personal portfolio site generated from a single JSON file, styled like it's 1997.

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Description](#description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Deploying](#deploying)
- [Customizing](#customizing)
- [Documentation](#documentation)
- [License](#license)

# Description

All of a portfolio's content (name, bio, projects, links, downloads, and more) lives in `data.json`. Most portfolio templates make you edit HTML to change your own bio; this one doesn't. The generator reads `data.json`, renders Jinja2 templates, and writes plain HTML, CSS, and JS to `dist/`. Fork the repo, edit the JSON, and you're done.

# Features

- Entire site driven by `data.json`, validated against a JSON Schema before anything builds
- 90s personal homepage theme with a dark default and a light mode toggle
- Retro image pipeline: pixelated, dithered, and reduced to a 32-color palette
- Project pages with galleries, highlights, facts, and technology logos
- Optional education and experience sections, with GPA and career timeline charts
- 404 page styled as a 90s error dialog
- Ansible deploy to an nginx host
- Tested build pipeline, with browser end-to-end tests

# Tech Stack

- Python 3
- Jinja2 templates
- jsonschema and Pillow for validation and image processing
- Plain HTML, CSS, and JavaScript (no framework, no bundler)
- Ansible and nginx for deployment
- pytest, Playwright, pre-commit, and Ruff for testing and linting

# Getting Started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp data.template.json data.json   # data.json is gitignored, see docs/guides/data-json.md
# edit data.json with your own info

python3 generate.py
```

Open `dist/index.html` in a browser, or serve it with `python3 -m http.server --directory dist`.

Image processing is the slow part of a build. Pass `--no-image-processing` to copy images as-is for a quick preview. Don't publish a build made with it, since the images won't have the retro look.

To build from a different file, pass `--data`, e.g. `python3 generate.py --data data.template.json` to try the example content without creating `data.json`.

# Deploying

`infra/` holds an Ansible playbook that puts the site on a Debian or Ubuntu server behind nginx. It syncs the repo (including your `data.json` and `assets/`) to the host, builds it there, and publishes `dist/`.

```bash
pip install -r infra/requirements.txt              # one-time, installs Ansible
cp infra/inventory.example.ini infra/inventory.ini # one-time, set your host (gitignored)
infra/deploy.sh                                    # or --check for a dry run
```

See [docs/guides/deploying.md](docs/guides/deploying.md) for the full walkthrough and troubleshooting.

# Customizing

New to the repo? [docs/guides/getting-started.md](docs/guides/getting-started.md) walks through everything you need to touch, step by step.

- **Your content** goes in `data.json`, the only file most people need to edit. See [docs/guides/data-json.md](docs/guides/data-json.md).
- **Images and downloads** (resume, etc.) go in `assets/` and `assets/download/`. These are gitignored and per-fork. The exception is `assets/core-assets/`, which the site itself uses and which is tracked. See [docs/guides/assets.md](docs/guides/assets.md).
- **Visual style** lives in one stylesheet: `static/styles.css`.
- **Deeper changes** (new pages, generation logic) are covered in `CLAUDE.md` and `docs/arch/`.

# Documentation

- [Getting started](docs/guides/getting-started.md): the entry point for forking the repo
- [data.json reference](docs/guides/data-json.md): every field in `data.json`
- [Assets](docs/guides/assets.md): images, downloads, and core assets
- [Deploying](docs/guides/deploying.md): publishing to an nginx host
- [Testing and linting](docs/guides/testing.md): pytest, Playwright, pre-commit, and Ruff
- [Project layout](docs/guides/project-layout.md): the repo tree and the build steps
- [Architecture decisions](docs/arch/): why the project is built the way it is
- [Deferred work](docs/TODO.md)

# License

MIT, see [LICENSE](LICENSE).
