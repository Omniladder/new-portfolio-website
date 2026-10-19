# 0017 — `assets/core-assets/` is tracked: app-owned assets, not per-fork content

**Status:** Accepted

## Context

[[0013-assets-gitignored-with-tracked-placeholders]] gitignores everything
under `assets/` except `.gitkeep` placeholders, because those files are one
person's content (headshots, project screenshots, a resume) and shouldn't ride
along in every fork's history. But the site itself also needs some assets that
aren't personal and aren't meant to be swapped out per fork — images and files
the templates/stylesheet depend on as part of the app (e.g. theme graphics for
the 90s look). Those have to exist on a fresh clone, so they can't be gitignored.

## Decision

- `assets/core-assets/` holds app-owned assets: files the site itself uses,
  that every fork shares, and that aren't referenced from `data.json`.
- `assets/core-assets/` and everything in it is **tracked**. `.gitignore`
  re-includes the whole directory after the `/assets/*` rule from 0013:
  ```
  !/assets/core-assets/
  ```
- Everything else in 0013 stands: the rest of `assets/` and `assets/download/`
  remains gitignored, per-fork content.
- Rule of thumb for which folder a file belongs in: if a fork would replace or
  remove it with their own, it's per-fork content and goes in `assets/` or
  `assets/download/`. If the app breaks or looks wrong without it regardless of
  whose portfolio it is, it goes in `assets/core-assets/`.

## Consequences

- A fresh clone has a populated `assets/core-assets/`, so app-level assets
  don't need to be supplied by whoever forks.
- Personal files must not be put in `assets/core-assets/` — anything there is
  committed and ends up in every fork's history.
- `process_assets` ([[0016-process-assets-image-pipeline]]) only handles
  top-level files in `assets/`, and `copy_downloads` only handles
  `assets/download/`, so nothing copies `assets/core-assets/` into `dist/` yet.
  Tracked in `docs/TODO.md`.

## Keywords

assets, core-assets, gitignore, tracked assets, app-owned assets, theme assets,
per-fork content
