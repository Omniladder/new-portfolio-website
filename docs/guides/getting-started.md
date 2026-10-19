# Getting started: making this site yours

This guide is for someone who just forked or cloned the repo and wants their own content on the page. You shouldn't need to read any Python to get there.

## What you touch, and what you don't

| You edit | What it's for | Guide |
|---|---|---|
| `data.json` | All of your text content: projects, titles, descriptions, links | [data-json.md](data-json.md) |
| `assets/` | Your images: screenshots, logos, photos | [assets.md](assets.md) |
| `assets/download/` | Files visitors can download, like a resume PDF | [assets.md](assets.md) |
| `static/styles.css` *(optional)* | The look of the site, if you want to restyle it | — |

Everything else (`generate.py`, `src/`, `templates/`, `tests/`) is the machinery that turns those files into a website. You can leave it alone. `dist/` is the generated output; it's wiped and rebuilt on every run, so don't edit anything in it by hand.

`data.json` and the contents of `assets/` are gitignored. They're yours, so they never end up in this repo's history, and a fresh clone starts with neither. That also means git can't restore them for you, so keep your own backup.

## Setup, step by step

### 1. Install Python dependencies

You need Python 3. From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run `source .venv/bin/activate` again whenever you open a new terminal.

### 2. Try a build with the example content

Before adding anything of your own, check that the build works:

```bash
python3 generate.py --data data.template.json
```

`--data` tells the generator which content file to read. Here it reads the tracked example instead of your `data.json`, which doesn't exist yet. If this finishes without an error, you're set up correctly.

### 3. Create your data.json

```bash
cp data.template.json data.json
```

Do this once. Running it again later would overwrite your content with the example.

### 4. Add your images and files

Put images in `assets/` and downloadable files in `assets/download/`, then point at them from `data.json` by path, e.g. `"image": "assets/my-project.png"`. See [assets.md](assets.md) for details.

### 5. Fill in data.json

Replace the example project with your own and add more entries to the `projects` list. [data-json.md](data-json.md) lists every field and what it means.

### 6. Build and preview

```bash
python3 generate.py
python3 -m http.server --directory dist
```

Then open <http://localhost:8000> in a browser. Re-run `python3 generate.py` after each change to `data.json` and refresh the page.

## When the build fails

- **A validation error mentioning a field name:** `data.json` doesn't match what the generator expects. Common causes are a missing required field, a misspelled field name (unknown fields are rejected), or a `type` on a link that isn't `github`, `website`, or `download`. Compare your file against `data.template.json` and [data-json.md](data-json.md).
- **A JSON syntax error:** usually a trailing comma or a missing quote. Running `python3 -m json.tool data.json` prints the line it got stuck on.
- **An error saying data.json can't be found or read:** you haven't done step 3 yet, or you're running the command from somewhere other than the repo root.

## Current state

The project is still early. Today the generator validates `data.json`, builds a home page, a projects index page, and one page per project. Some things aren't hooked up yet:

- The page templates don't display most of your `data.json` fields yet. The fields are checked, but they won't all show up on the page.
- Files in `assets/` aren't copied into `dist/` yet, so images you reference won't load in the preview.
- Only projects exist so far. Bio, site-wide links, and other sections haven't been designed.

You can still fill in `data.json` and `assets/` now. Your content will carry over as these features land, and this guide will be updated when they do.
