# 0042 — `process_core_assets` replaces `copy_core_assets`

**Status:** Accepted. Supersedes the pipeline decision in
[[0020-core-assets-copy-pipeline-and-icon-theming]], which made
`copy_core_assets` a plain copy. 0020's icon-theming rules still apply.

## Context

0020 copied `assets/core-assets/` into `dist/` byte-for-byte, on the
grounds that core assets are already final. Since
[[0040-pillow-dither-and-32-color-palette]] and
[[0041-pixelate-in-reduce-image-quality]], every per-fork image gets the
pixelated, dithered 32-color look. App-owned raster images should get it
too, so the site looks consistent.

## Decision

- Rename the operation `copy_core_assets` to `process_core_assets`
  (`src/operations/process_core_assets.py`). Its error type is now
  `CoreAssetsProcessingError` (`src/errors/process_core_assets.py`).
- `process_core_assets()` walks every file under `assets/core-assets/`.
  Images (by `IMAGE_EXTENSIONS`) go through `read_image_data()` →
  `process_image_data()` → `write_image_data()`, the same as in
  `process_assets`. Any other file, like the icon `LICENSE.txt`, is copied
  unchanged.
- `process_assets` still skips `assets/core-assets/`, so only one
  operation ever writes those files.
- `generate.py` runs it where `copy_core_assets` used to be, after
  `copy_downloads()`.

## Consequences

- Raster images added to `assets/core-assets/` get pixelated, dithered,
  and reduced to 32 colors.
- SVG icons are unchanged. Pillow can't decode them, so they pass
  through, which keeps the CSS `mask-image` tinting from 0020 working.
- An app-owned raster image that has to stay pristine would need its own
  exception. None exist today.

## Keywords

process_core_assets, copy_core_assets, core-assets, CoreAssetsProcessingError,
image pipeline, dither, palette, pixelate, LICENSE
