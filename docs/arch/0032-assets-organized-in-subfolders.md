# 0032 — `assets/` images can live in subfolders, organized by context

**Status:** Accepted. Supersedes the "top-level files only" part of
[[0016-process-assets-image-pipeline]]; the read → manipulate → write
pipeline it describes is unchanged.

## Context

[[0016-process-assets-image-pipeline]] had `process_assets()` copy only the
files directly inside `assets/`, so every image a fork uses (project
screenshots, dozens of technology logos, profile photos) sat in one flat
folder. With 80+ images that's hard to navigate, and the planned per-project
galleries would make it worse. The top-level-only rule existed to keep
`process_assets()` away from `assets/download/`, not because the flat layout
itself was wanted.

## Decision

- `process_assets()` walks `assets/` recursively and processes every image
  file it finds, mirroring each one's relative path into `dist/assets/`
  (consistent with [[0005-dist-mirrors-root-paths]]).
- It skips `assets/download/` and `assets/core-assets/` by name
  (`SKIPPED_SUBDIRS` in `src/operations/process_assets.py`), since
  `copy_downloads()` and `copy_core_assets()` already copy those as-is.
- The folder structure is the fork's choice: nothing in the build depends on
  it, because `data.json` references every file by its full path. The
  recommended layout, documented in `docs/guides/assets.md`, is:
  - `assets/projects/<project_name>/` for a project's screenshots and
    gallery images, matching the `dist/projects/<project_name>/` page slug;
  - `assets/logos/` for technology logos, shared across projects and the
    skills table so each logo is stored once;
  - `assets/profile/` for photos and personal branding;
  - any other folder (e.g. `assets/misc/`) for anything else.
- New subfolders stay gitignored under the existing `/assets/*` rule
  ([[0013-assets-gitignored-with-tracked-placeholders]]); `.gitignore`
  doesn't change.

## Consequences

- Moving an image means updating its path in `data.json`. The build doesn't
  check that referenced files exist, so a stale path shows up as a broken
  image, not a build error.
- A new subfolder that another operation should own (like `download/`) must
  be added to `SKIPPED_SUBDIRS`, or `process_assets()` will also copy any
  images inside it.
- Non-image files in a subfolder other than `download/` are still ignored,
  same as before.

## Keywords

assets, subfolders, subdirectories, organization, process_assets, recursive,
rglob, SKIPPED_SUBDIRS, assets/projects, assets/logos, assets/profile,
dist/assets
