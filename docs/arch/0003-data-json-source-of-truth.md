# 0003 — data.json as the single source of truth

**Status:** Accepted

## Context

The project's whole value proposition (see [[0001-overview-and-goals]]) is that forking the site and making it your own shouldn't require touching HTML, CSS, or Python.

## Decision

- All page content — bio, project list, links, downloadable files, section text — lives in `data.json`.
- Templates only contain presentation logic (loops, conditionals, markup structure). They read from the data passed in by the generator; they never hardcode content that belongs to a specific person's portfolio.
- `assets/` holds the binary/media files `data.json` references (images, resume PDFs in `assets/download/`), not content itself.

## Consequences

- `data.json`'s schema is effectively the project's public API. Changes to it should be treated as breaking changes once the project has real users forking it.
- Validation of `data.json` (required fields, shape) will need to live in `src/utils` once generation logic exists — not decided yet how strict this should be.

## Keywords

data.json, content, schema, source of truth, customization, assets, fork
