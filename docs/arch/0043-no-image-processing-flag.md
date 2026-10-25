# 0043 — `--no-image-processing` flag skips the image pipeline

**Status:** Accepted.

## Context

Since [[0040-pillow-dither-and-32-color-palette]] and
[[0041-pixelate-in-reduce-image-quality]], every build pixelates, dithers,
and palette-reduces each raster image. On a real `assets/` folder
(176 images) that takes about 45 s, while the rest of the build takes under
a second. Most builds, including agents' smoke tests of template or data
changes, don't need processed images.

## Decision

- `parse_args` gains a `--no-image-processing` switch (`args.no_image_processing`).
  It's off by default, so a plain `python3 generate.py` still processes
  images.
- `process_assets()` / `process_asset()` and `process_core_assets()` /
  `process_core_asset()` take a `process_images: bool = True` parameter.
  When it's False, each image is still read and written to its mirrored
  `dist/` path, but `process_image_data()` is skipped, so the bytes go
  through unchanged.
- `generate.py` passes `process_images=not args.no_image_processing` to
  both operations. The entrypoint has no other logic.
- The `parse_args` log line and both operations' summaries say when
  processing was off, so a raw build can't be mistaken for a final one.
- Agents use `--no-image-processing` for smoke builds unless the change
  being verified touches image processing (`src/utils/images.py`,
  `process_assets`, `process_core_assets`).

## Consequences

- A smoke build of the real `data.json` takes under a second instead of
  about 45 s.
- `dist/` built with the flag isn't the shipped look. Anything published
  has to come from a build without it.

## Keywords

--no-image-processing, parse_args, flag, process_images, process_assets,
process_core_assets, smoke test, build speed, image pipeline
