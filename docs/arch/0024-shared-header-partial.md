# 0024 — One shared header partial for every page

**Status:** Accepted

## Context

`templates/home.html` and `templates/project_home.html` each carried their
own copy of the site header, and the copies had already drifted: the
projects page was missing the floppy-disk icon and differed in nav
attributes. Every future page (`templates/project.html` included) would add
another copy to keep in sync.

## Decision

- The header lives once, in `templates/partials/header.html`, and every page
  template pulls it in with `{% include "partials/header.html" %}` at the
  top of `.page`.
- The including template sets two variables first:
  - `root` — the relative prefix back to the `dist/` root, since pages are
    rendered at different depths (`""` for `index.html`, `"../"` for
    `projects/index.html`, `"../../"` for `projects/<slug>/index.html`).
  - `current_page` — `"home"` or `"projects"`, which marks the matching nav
    link with `aria-current="page"`.
- `templates/partials/` is for shared fragments only; it's never rendered
  to `dist/` on its own. This doesn't change [[0010-project-pages-from-single-template]]
  or [[0002-single-css-and-js-per-template]] — partials are markup, not
  extra stylesheets or scripts.

## Consequences

- Header changes are made in one place and show up on every page.
- A new page template must set `root` and `current_page` before the include,
  or its header links and icons will point at the wrong paths.
- The footer is still duplicated per template; it can move to a partial the
  same way if it needs to.

## Keywords

header, partial, include, jinja, templates/partials, root prefix,
current_page, aria-current
