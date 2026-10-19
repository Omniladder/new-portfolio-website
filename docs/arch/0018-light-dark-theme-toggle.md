# 0018 — Light mode default, with a dark mode toggle

**Status:** Accepted

## Context

`docs/refs/light_mode_idea.png` and `docs/refs/dark_mode_idea.png` show two
directions for the same page, both in the 90s-homepage style this project is
going for:

- **Light mode** (`light_mode_idea.png`): white background, black hairline
  borders, lavender (`#CCCCFF`-ish) section headers, navy/blue links — a
  clean "GeoCities/early-web" look.
- **Dark mode** (`dark_mode_idea.png`): black starfield background, neon
  yellow headings, cyan links, red accent text, a blinking "UNDER
  CONSTRUCTION" banner and hit counter — a BBS/hacker-night look.

`docs/refs/CLAUDE.md` says images in that folder are inspiration only, not
consumed at build time, until a design idea gets adopted. This ADR is that
adoption: both mockups become real target designs, not just inspiration.

## Decision

- The site ships both themes. **Light mode is the default** — it's what a
  visitor sees on first load, with no stored preference.
- A visible **dark mode toggle** (placed in the header, near the nav) flips
  to the dark theme on click. The choice is remembered across visits via
  `localStorage` — there's no backend to persist it server-side.
- Both palettes live in the single stylesheet, `static/styles.css`
  ([[0002-single-css-and-js-per-template]]), as CSS custom properties scoped
  under a `data-theme` attribute set on `<html>`. No second stylesheet.
- The toggle needs a small amount of JS (read/write `localStorage`, flip
  `data-theme`). Because the toggle appears on every page, this is **one
  shared script, `static/theme-toggle.js`, included by every template** —
  the same file reused everywhere, not a new file per template. This fits
  inside 0002's "at most one JS file per template" cap; it's a narrow,
  explicit exception to the *"only if that template needs behavior"* clause,
  since the behavior (the toggle) is site-wide rather than template-specific.
- Mockup flourishes specific to each theme (starfield, glow, under-
  construction banner, hit counter) should be built with CSS where possible
  rather than shipped as image assets, in keeping with 0001's "no logic
  beyond data + templates" spirit. Where an image is simpler (e.g. a
  decorative GIF-style banner), it goes through the normal `assets/` /
  `assets/core-assets/` rules ([[0013-assets-gitignored-with-tracked-placeholders]],
  [[0017-core-assets-tracked]]) depending on whether it's app-owned or
  per-fork.

## Consequences

- `static/styles.css` carries two palettes going forward; theme-specific
  values should be grouped under the `data-theme` selector rather than
  scattered through the file.
- This is the first site-wide JS file the project ships. It loads on every
  page regardless of whether that specific page has other interactivity.
- Any new template or component isn't done until it's been checked under
  both themes, not just the one it was designed in.
- `docs/refs/light_mode_idea.png` and `docs/refs/dark_mode_idea.png` stay in
  place as the reference for what each theme should look like.

## Keywords

theme, dark mode, light mode, toggle, css custom properties, data-theme,
localStorage, styles.css, theme-toggle.js, docs/refs
