# Setting up data.json

`data.json` holds all of your site's content — it's the only file most forks need to touch. It's not tracked in git (your name, bio, and links are yours, not this repo's), so you start by copying the tracked template:

```bash
cp data.template.json data.json
```

Then edit `data.json` with your own content and run `python3 generate.py`.

## Example

```json
{
  "projects": [
    {
      "project_name": "example_project"
    }
  ]
}
```

This is illustrative, not a file this repo validates automatically — unlike `data.template.json` (checked against the schema by a test every run), this block is maintained by hand. If you're adding a field to `src/schema/data.schema.json`, update this example in the same change so it never shows something `parse_data()` would actually reject.

## Current state

Only the `projects` field exists so far: a root-level array, one object per project, each with just `project_name` for now. Each entry gets its own page at `dist/projects/<project_name>/index.html`, rendered from `templates/project.html` — see [docs/arch/0010](../arch/0010-project-pages-from-single-template.md). Bio, links, downloads, and other content fields haven't been designed yet; this guide, the template, and the schema will all grow together as they land.

## Where validation happens

`generate.py` parses `data.json` through `src/operations/parse_data.py`, which checks it against `src/schema/data.schema.json` before anything else runs. If your `data.json` doesn't match the schema, generation fails immediately with a validation error instead of producing a broken site.
