# Setting up data.json

`data.json` holds all of your site's text content. Along with your files in `assets/` ([assets.md](assets.md)), it's the only thing most forks need to touch. New here? Start with [getting-started.md](getting-started.md).

`data.json` isn't tracked in git (your name, bio, and links are yours, not this repo's), so you start by copying the tracked template:

```bash
cp data.template.json data.json
```

Then edit `data.json` with your own content and run `python3 generate.py`.

## Example

```json
{
  "projects": [
    {
      "project_name": "flashcard-factory",
      "title": "Flashcard Factory",
      "tagline": "Turns lecture notes into study decks",
      "description": "A longer description of what the project does and why you built it.",
      "image": "assets/flashcard-factory.png",
      "technologies": [
        { "name": "Python", "logo": "assets/pythonLogo.png" },
        { "name": "PostgreSQL", "logo": "assets/postgresLogo.png" }
      ],
      "links": [
        { "label": "Source", "url": "https://github.com/you/flashcard-factory", "type": "github" },
        { "label": "Live demo", "url": "https://flashcards.example.com", "type": "website" },
        { "label": "Write-up (PDF)", "url": "assets/download/flashcard-factory.pdf", "type": "download" }
      ]
    }
  ]
}
```

This is illustrative, not a file this repo validates automatically. `data.template.json` is checked against the schema by a test on every run; this block is maintained by hand. If you're adding a field to `src/schema/data.schema.json`, update this example in the same change so it never shows something `parse_data()` would reject.

## Fields

The top level has one field, `projects`: a list with one object per project. Every project field below is required, and fields not listed here are rejected.

| Field | Type | What it is |
|---|---|---|
| `project_name` | text | Short, URL-safe ID, e.g. `flashcard-factory`. Becomes the page's address: `dist/projects/<project_name>/index.html`. Stick to lowercase letters, numbers, and hyphens. |
| `title` | text | The project's display name. |
| `tagline` | text | A one-line summary. |
| `description` | text | The longer explanation. |
| `image` | text | Path to a screenshot in `assets/`, e.g. `assets/flashcard-factory.png`. |
| `technologies` | list | Tools the project uses. Each entry has `name` and `logo` (a path to an image in `assets/`). Can be empty: `[]`. |
| `links` | list | Each entry has `label` (the link text), `url`, and `type`, which is one of `github`, `linkedin`, `website`, or `download`. For `download`, `url` is a path under `assets/download/`. `github` and `linkedin` get a distinct icon on the home page ([docs/arch/0021](../arch/0021-emoji-icons-with-brand-mark-exception.md)); everything else (including `linkedin` itself, since the real logo can't be redistributed) gets a generic one. Can be empty: `[]`. |

Each project gets its own page, rendered from `templates/project.html` ([docs/arch/0010](../arch/0010-project-pages-from-single-template.md)), and is also listed on the projects index page.

## Current state

Only `projects` exists so far. Bio, site-wide links, and other sections haven't been designed yet. The templates don't display most of these fields yet either: they're validated, but not all of them show up on the page. This guide, the template, and the schema will grow together as features land.

## Where validation happens

`generate.py` parses `data.json` through `src/operations/parse_data.py`, which checks it against `src/schema/data.schema.json` before anything else runs. If your `data.json` doesn't match the schema, generation fails immediately with a validation error instead of producing a broken site.
