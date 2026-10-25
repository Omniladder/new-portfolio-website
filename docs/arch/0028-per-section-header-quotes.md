# 0028 — One header quote per top-level section

**Status:** Accepted.

## Context

The shared header ([[0024-shared-header-partial]]) showed a single
`profile.quote` on every page. The previous React portfolio gave each
top-level page its own quote (Home, Projects, About), which made each section
feel distinct. A single field can't do that, and the name `quote` stops
fitting once there's more than one.

## Decision

- `profile.quote` is removed. `data.json` gains a top-level `quotes` object,
  keyed by section: `quotes.home` and `quotes.projects`, both required.
- The keys match the `current_page` value each template already sets for the
  header, and `templates/partials/header.html` renders
  `quotes[current_page]`.
- Individual project pages (`projects/<slug>/index.html`) belong to the
  Projects section. They set `current_page = "projects"` and show the
  projects quote; there's no per-project quote.
- A new top-level page adds a matching key to `quotes` in the schema,
  `data.template.json`, and the guide in the same change.

## Consequences

- Each section's quote is edited independently in `data.json`.
- Existing `data.json` files with `profile.quote` fail validation until
  they move to `quotes`.
- A template that sets a `current_page` with no matching `quotes` key
  renders an empty quote, so new sections must add a key.

## Keywords

quote, quotes, header, current_page, per-page quote, section, data.json,
schema, profile.quote
