# 0005 — dist/ mirrors root paths for mirrored source directories

**Status:** Accepted

## Context

`dist/` is the generated output root (see [[0004-thin-entrypoint-src-layout]]). Some
root-level directories are raw assets that get carried into the output largely
as-is (e.g. `assets/download/resume.pdf` should be reachable at
`dist/assets/download/resume.pdf`). Others are build-time inputs that are
*consumed* to produce output but have no reason to exist as a directory shape
in `dist/` (e.g. `templates/` is rendered into HTML files, not copied as a
`templates/` folder).

Picking a path convention up front avoids every future operation inventing
its own mapping between a source path and its `dist/` equivalent.

## Decision

- For a fixed, explicit set of root-level directories — currently `assets/`
  and `static/` — the path from repo root to any file or directory is
  reproduced identically under `dist/`. `assets/download/` becomes
  `dist/assets/download/`, `static/styles.css` becomes `dist/static/styles.css`.
- This set is named `MIRRORED_DIRS` in `src/utils/paths.py` and is the single
  place that decides what gets a path-mirrored presence in `dist/`. Adding a
  new mirrored directory is a one-line change there.
- Directories that are inputs to generation rather than carried-through
  assets — `templates/`, `docs/`, `src/`, `data.json` — are not mirrored.
  Their output lands wherever the relevant operation decides (e.g. a rendered
  template goes to `dist/index.html`, not `dist/templates/index.html`).
- `dist/` is fully rebuilt each run (per [[0004-thin-entrypoint-src-layout]]),
  so scaffolding it means clearing any previous `dist/` and recreating the
  mirrored directory tree before anything is written into it.

## Consequences

- Any operation that writes a mirrored asset can compute its target path
  mechanically: swap the repo root for `dist/` and keep the rest identical.
- Operations that render content (templates) are responsible for deciding
  their own output path under `dist/` — this ADR only governs the mirrored
  directories.
- Extending which directories get mirrored is a one-line edit to
  `MIRRORED_DIRS`, not a new convention to invent per operation.

## Keywords

dist, path mirroring, assets, static, scaffold, directory structure, MIRRORED_DIRS
