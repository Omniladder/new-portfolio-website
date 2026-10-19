# 0020 — Core assets get copied into dist/, themeable icons via CSS mask

**Status:** The `copy_core_assets` pipeline decision below is still
accepted. The icon-theming/icon-sourcing decisions are superseded by
[[0021-emoji-icons-with-brand-mark-exception]].

## Context

[[0017-core-assets-tracked]] left `assets/core-assets/` tracked but with
nothing copying it into `dist/` — noted as a TODO item, blocked on deciding
whether it should go through `process_assets`'s image pipeline or get a
plain copy like `copy_downloads`. That became a real blocker once
`templates/home.html` needed actual icon files: a themed nav/section-icon
set (computer, home, folder, user, tool-case, file-text, download, mail,
link, github, star) and a tiled starfield background for dark mode, both
app-owned rather than per-fork content.

Those icons also need to render in the right color for whichever theme is
active ([[0018-light-dark-theme-toggle]]) — light-mode black text, dark-mode
neon yellow/cyan — without shipping two copies of every icon file.

## Decision

- **Pipeline:** `copy_core_assets()`, a new operation mirroring
  `copy_downloads` exactly — a plain `copy_path_to_dist("assets/core-assets")`
  call, no image processing. Core assets are already final (SVGs authored or
  sourced at the right size/format), so `process_assets`'s read/manipulate/
  write hook isn't useful here. Wired into `generate.py` after
  `copy_downloads()`. New error type `CoreAssetsCopyError` in
  `src/errors/copy_core_assets.py`, per [[0012-explicit-errors-per-operation]].
- **Icon theming:** icons are referenced from templates as empty,
  `aria-hidden="true"` `<span class="icon icon-<name>">` elements, not
  `<img>` tags. `static/styles.css` gives `.icon` a fixed size and
  `background-color: currentColor` plus `mask-image: url(...)` (and
  `-webkit-mask-image` for Safari) pointing at the core-asset SVG. This lets
  a single monochrome SVG file pick up whatever color CSS currently applies
  to text at that point in the page — the same icon file renders black in a
  light-mode box title and neon yellow in dark mode, automatically, with no
  per-theme icon variants. `<img src="icon.svg">` can't do this: an
  externally-loaded SVG doesn't inherit the page's CSS, so `currentColor`
  inside it would always resolve to the SVG's own default (black).
- **Source for the icon set:** [pixelarticons](https://github.com/halfmage/pixelarticons)
  (MIT), chosen over inlining more hand-drawn SVGs because a consistent,
  pre-built pixel-icon set matches the 90s aesthetic better than one-off
  hand-authoring, and MIT only requires keeping the license notice — done via
  `assets/core-assets/icons/LICENSE.txt`. Deliberately *not* using full-color
  brand logos (e.g. a colored GitHub/LinkedIn mark) for consistency with the
  mask-image technique above, which only works for monochrome shapes.
- **Starfield tile:** `assets/core-assets/stars-tile.svg`, a small seamless
  tile of scattered dots, hand-authored for this project (deterministic
  pseudo-random placement, no external source) rather than sourced, since an
  exact-size seamless tile in the theme's own colors is easy to generate and
  avoids any licensing question. `[data-theme="dark"] body` repeats it via
  `background-image` + `background-repeat`, replacing the earlier multi-layer
  `radial-gradient` approach, closer to the "heaven's gate"-style tiled
  starfield look the design asked for.
- Icons are chosen per concept (e.g. `icon-folder` for "Projects") or per
  `link.type` (`github` → `icon-github`, anything else → generic
  `icon-link`), never by matching a label string — keeps icon choice correct
  for any fork's `data.json` content, not just this one's.

## Consequences

- `assets/core-assets/` now has real, non-trivial content
  (`icons/*.svg` + `LICENSE.txt`, `stars-tile.svg`), copied into
  `dist/assets/core-assets/` on every build.
- CSS paths to core assets are relative to `static/styles.css`'s location
  in `dist/` (`../assets/core-assets/...`), not to the page HTML — a
  template referencing the same path directly (e.g. `profile.picture`-style)
  would need `assets/core-assets/...` instead, since `dist/index.html` sits
  one level up from `dist/static/`.
- Any future core-asset icon must be a single-color SVG for the mask
  technique to work; multi-color source art (e.g. real brand logos) isn't a
  fit without a different approach.
- `docs/TODO.md`'s core-assets-copying item is resolved and removed.

## Keywords

core-assets, copy_core_assets, dist pipeline, icons, mask-image, currentColor,
theming, pixelarticons, starfield, stars-tile, heaven's gate
