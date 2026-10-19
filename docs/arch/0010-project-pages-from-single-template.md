# 0010 — Project pages render from one template, driven by data.json

**Status:** Accepted

## Context

The first pass at project pages had `generate_projects()` glob
`templates/projects/*.html` and render each file it found to
`dist/projects/<filename>/index.html`, using the filename as the slug. That
makes the template directory, not `data.json`, the thing that defines which
projects exist — a fork adding a project would need to add a new template
file, not just edit `data.json`. That contradicts
[[0003-data-json-source-of-truth]], which treats `data.json` as the single
source of truth for content including the project list.

## Decision

- `templates/project.html` (singular) is the one template for a project
  page. There is no `templates/projects/` directory of per-project files.
- `data.json` gets a root-level `projects` field: an array of objects, one
  per project. For now each object has just `project_name` (a string); more
  fields will be added here as project content is designed, same as any
  other `data.json` field.
- `generate_projects()` in `src/operations/generate_pages.py` loops over
  `data["projects"]` (not the filesystem) and renders `templates/project.html`
  once per entry, passing that entry's data to the template, to
  `dist/projects/<project_name>/index.html` — so each project still gets a
  clean URL, the same `dist/` shape as before.
- The home page template was renamed `templates/home.html` (from
  `templates/index.html`) for the same reason `project.html` is singular —
  the template name describes what it is, not where its output lands.
  `generate_home()` renders it explicitly to `dist/index.html` via
  `render_template_to_dist`'s `output_path` argument; template name and
  output path are allowed to differ.

## Consequences

- Adding, removing, or reordering a project is purely a `data.json` edit —
  consistent with [[0001-overview-and-goals]] and [[0003-data-json-source-of-truth]].
  No template file to add or remove.
- `project_name` currently doubles as both the dict key people edit and the
  `dist/projects/` directory slug. If a name that isn't filesystem-safe is
  ever needed, a separate slug field can be added later — not needed yet
  since the only value is `project_name` itself.
- `templates/project.html` must stay generic across all projects, same as
  any other data-driven template — it cannot hardcode content specific to
  one project.

## Keywords

projects, data.json, data-driven, project.html, home.html, template naming,
generate_projects, dist/projects, slug
