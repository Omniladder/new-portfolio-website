# 0041 — `reduce_image_quality` pixelates at 50% with a nearest-neighbor regrow

**Status:** Accepted. Fills in the stage [[0040-pillow-dither-and-32-color-palette]]
left as a no-op.

## Context

0040 put Pillow behind a three-stage image pipeline but left
`reduce_image_quality()`, the first stage, as a passthrough. The
dithered, 32-color output still kept full-resolution detail, which doesn't
match the low-resolution look of 90s homepage graphics.

## Decision

- `reduce_image_quality()` shrinks each raster image to `SHRINK_FACTOR`
  (0.5) of its width and height, then resizes it back to its original
  dimensions with nearest-neighbor interpolation.
- The shrink uses a box filter, so each small pixel is the average of the
  2×2 block it replaces. Only the regrow is nearest-neighbor, which is what
  gives the hard-edged blocks.
- Output dimensions match the input, so templates and layout don't change.
  Format, alpha, and the SVG/animated passthrough work the same as in the
  other two stages.

## Consequences

- Every raster image in `dist/assets/` is visibly pixelated (2×2 blocks)
  before it's dithered and reduced to 32 colors.
- Small images like logos lose fine detail, such as thin lines and small
  text. A fork that wants them sharp has to change `SHRINK_FACTOR` or skip
  the stage.

## Keywords

reduce_image_quality, pixelate, downscale, nearest neighbor, resize,
SHRINK_FACTOR, Pillow, image pipeline, process_image_data
