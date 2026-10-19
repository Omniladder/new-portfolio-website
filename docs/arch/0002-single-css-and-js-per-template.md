# 0002 — One global stylesheet, at most one JS file per template

**Status:** Accepted

## Context

A 90s-themed site doesn't need per-component stylesheets or a JS bundle graph. Splitting CSS/JS across many small files makes a "just edit the data" project harder to reason about for someone unfamiliar with the code.

## Decision

- Exactly one stylesheet for the whole site: `static/styles.css`. No per-page or per-component CSS files.
- At most one JS file per template, only if that template actually needs behavior (e.g. a guestbook widget, a visitor counter). No JS is created speculatively.
- No CSS/JS frameworks or preprocessors (no Sass, no Tailwind, no bundlers). What's written to `static/` is what ships to `dist/`.

## Consequences

- Styling changes always happen in one place.
- If a template's JS need grows complex enough to want multiple files, that's a signal to reconsider the template's scope rather than split the file.

## Keywords

css, styles.css, javascript, static assets, styling, theme, no bundler
