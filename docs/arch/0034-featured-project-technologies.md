# 0034 — Featured technologies above a table of the rest

**Status:** Accepted.

## Context

A project page showed its technologies either as a large logo grid (when no
entry had `layer`/`purpose`) or as a table (when any did). Filling in
`layer`/`purpose` for a project turned every technology into a small table
row, so the core stack lost the at-a-glance logo grid, and minor tools sat at
the same weight as the main ones.

## Decision

- Each entry in `projects[].technologies` gains an optional boolean
  `featured`, defaulting to false.
- Featured technologies render as the large logo grid (`.tech-grid-featured`)
  at the top of the Technologies section; a featured entry's `purpose`, if
  any, becomes its hover title.
- The non-featured technologies render underneath, headed "Also Used" when
  there are featured ones above. They keep the old rule: a table with
  Layer/Purpose columns if any of *them* has those fields, otherwise a plain
  logo grid.
- A project with no featured technologies renders exactly as before.
- When there are featured technologies, the "Also Used" list is collapsed
  by default inside a native `<details>` element ("Also Used (N)"), so a
  long list stays available without lengthening the page. No JavaScript.
- Highlights get the same treatment: the first three always show, and any
  beyond that collapse into a `<details>` labeled "More highlights (N)".
- Highlights move to the bottom of the project page, after the gallery
  (a layout change, recorded here because it shipped together).

## Consequences

- Existing `data.json` files keep working unchanged.
- The Layer/Purpose columns are decided by the non-featured entries only, so
  featuring every technology that has a purpose can make the columns vanish.

## Keywords

technologies, featured, tech-grid, tech table, layer, purpose, also used,
project page, highlights order, schema, details, collapsible,
expandable, more highlights
