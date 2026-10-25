# 0027 — Internal links point at index.html explicitly

**Status:** Accepted.

## Context

Pages are generated as `<dir>/index.html` (see
[[0010-project-pages-from-single-template]]), and templates linked to them by
directory (`projects/`, `<project_name>/`). Any web server resolves a directory
URL to its `index.html`, but a browser opening `dist/` from disk via `file://`
does not — it shows a directory listing instead. Opening `dist/index.html`
directly is a supported way to preview the site (README,
[[0021-emoji-icons-with-brand-mark-exception]],
[[0022-inline-svg-icons-and-real-computer-image]]), so every link except Home
was broken in that mode. There's no static-site setting that changes how
`file://` resolves directories; only a server does that.

## Decision

- Every internal link to a page targets its `index.html` file explicitly:
  `projects/index.html`, `{{ project.project_name }}/index.html`,
  `{{ root }}projects/index.html`, never `projects/` or `./`.
- In-page anchors (`#about`) and external URLs are unaffected.

## Consequences

- The site navigates identically from `file://` and from any static host.
- Deployed URLs show `/index.html` in the address bar. Cosmetic only; both
  forms load the same file on a server.
- New templates and links must follow the same rule, or they'll break when
  previewed from disk.

## Keywords

links, href, index.html, file://, directory listing, navigation, static hosting
