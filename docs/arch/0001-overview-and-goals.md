# 0001 — Overview and goals

**Status:** Accepted

## Context

This repo is a personal portfolio site. It needs to be easy for someone else (or future me) to fork and re-theme with their own content without touching code.

## Decision

- Vanilla HTML/CSS/JS output only — no frontend framework, no bundler, no build toolchain beyond Python + Jinja2.
- `data.json` is the single source of truth for all site content (bio, projects, links, downloads). `generate.py` renders it through templates into `dist/`.
- Visual theme is deliberately 90s-web: simple enough that one stylesheet (see [[0002-single-css-and-js-per-template]]) can carry the whole look.
- Someone should be able to get a working personal site by cloning the repo and editing only `data.json`.

## Consequences

- Any feature that can't be expressed as "add a field to data.json + a template loop" is probably out of scope.
- Keeps `generate.py` itself free of logic — see [[0004-thin-entrypoint-src-layout]].

## Keywords

static site generator, project goals, scope, vanilla JS, 90s theme, no framework
