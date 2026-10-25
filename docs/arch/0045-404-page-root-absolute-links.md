# 0045 — 404 page at dist/404.html with root-absolute links

**Status:** Accepted.

## Context

Since [[0044-ansible-deploy-to-nginx-host]] the site is served by nginx, and
a missing URL got nginx's stock error page. A themed 404 needs links that
work from wherever the server returns it: `/projects/typo/index.html` and
`/nope` are at different depths, but nginx returns the same file for both.
The relative `root` prefix every other page uses
([[0024-shared-header-partial]]) depends on the page's own path, so it
can't work here.

## Decision

- `templates/404.html` is rendered to `dist/404.html` by
  `generate_not_found()` in `generate_pages`.
- It's the one template whose links are root-absolute: it sets
  `root = "/"` for the header partial, and its stylesheet, script, favicon,
  and footer links start with `/`. They still target `index.html`
  explicitly ([[0027-explicit-index-html-links]]).
- It sets `current_page = "not_found"`. That's not a nav section and has no
  `quotes` key, so no nav link is marked current and no quote is shown
  ([[0028-per-section-header-quotes]], [[0035-education-and-experience-pages]]).
  `data.json` gets no new fields.
- The nginx site config sets `error_page 404 /404.html;`.
- The look: a big blinking "404" (static under `prefers-reduced-motion`), a
  Windows 95-style error dialog with "Return to Home" and "Browse Projects"
  buttons, an under-construction line, and a fake hit counter.

## Consequences

- Any missing URL on the deployed site gets a themed page with a way home.
- Opened from disk (`file://`), "/" is the filesystem root. A small inline
  script in the page's `<head>` runs only under `file://`: it loads the
  stylesheet and theme script relative to `dist/404.html` and strips the
  leading `/` from every link, so the page previews like the others. Served,
  the script does nothing and the page needs no JS.
- Static hosts that look for `404.html` at the root (GitHub Pages,
  Netlify) pick it up without extra config.
- A site served from a subpath (`example.com/portfolio/`) would need these
  links changed.

## Keywords

404, not found, error page, error_page, nginx, root-absolute links,
generate_not_found, templates/404.html
