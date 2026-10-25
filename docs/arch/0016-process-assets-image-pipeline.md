# 0016 — `process_assets` copies top-level `assets/` images through a processing hook

**Status:** Accepted. The "top-level files only" rule is superseded by [[0032-assets-organized-in-subfolders]]: `process_assets()` now also processes images in subfolders.

## Context

`assets/` holds per-fork images (see [[0013-assets-gitignored-with-tracked-placeholders]])
and is listed in `MIRRORED_DIRS` (see [[0005-dist-mirrors-root-paths]]), but no
operation actually copied its files into `dist/assets/` — `docs/guides/assets.md`
called this out explicitly as not wired up yet. Separately, images in `assets/`
will eventually need per-file manipulation (resizing, recompression, etc.)
before they reach `dist/`, not just a byte-for-byte copy.

## Decision

- A new operation, `src/operations/process_assets.py`, fills the
  `assets/` → `dist/assets/` gap. Its root function, `process_assets()`,
  lists only the **files directly inside `assets/`** whose extension is a
  known image type (`src/utils/images.py`'s `IMAGE_EXTENSIONS`).
  Subdirectories — namely `assets/download/`, which holds non-image
  downloadable files — are left untouched by this operation, consistent with
  `docs/arch/0013`.
- Each image goes through `process_asset(source_path)`, which does three
  steps via `src/utils/images.py`: `read_image_data()` (raw bytes in),
  `process_image_data()` (the manipulation hook — a no-op passthrough today,
  returning its input unchanged), then `write_image_data()` (raw bytes out,
  to the mirrored path under `DIST_DIR`). Keeping these as three separate
  utils means a future resize/recompress implementation only has to change
  `process_image_data()`.
- `process_assets()` loops over the per-file calls wrapped in `tqdm`, so a
  fork with many images gets a progress bar instead of a silent pause. This
  adds `tqdm` as a new runtime dependency in `requirements.txt`.
- `process_asset()` catches `OSError` from the read/write steps and raises
  `AssetProcessingError` (`src/errors/process_assets.py`) naming the failing
  file, per [[0012-explicit-errors-per-operation]]. `process_assets()` itself
  isn't wrapped again, matching how `generate_pages()` doesn't re-wrap its
  already-wrapped `generate_*` calls.
- `generate.py` calls `process_assets()` after `copy_static()` and before
  `generate_pages()`.

## Consequences

- `dist/assets/<name>` now exists for every top-level image in `assets/`
  after a build, matching what `docs/guides/assets.md` had flagged as
  missing.
- `assets/download/` and any other subdirectory still isn't copied into
  `dist/` by this operation — that remains a gap, tracked in `docs/TODO.md`.
- Adding real image manipulation later (resize, strip EXIF, recompress) means
  editing the body of `process_image_data()` only; `process_asset()` and
  `process_assets()` don't need to change.
- `requirements.txt` gains `tqdm`, the only addition — no image-decoding
  library (e.g. Pillow) is pulled in, since `process_image_data()` still
  operates on raw bytes, not decoded pixel data.

## Keywords

process_assets, assets, dist/assets, image pipeline, read_image_data,
process_image_data, write_image_data, tqdm, progress bar, AssetProcessingError
