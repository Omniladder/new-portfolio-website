# 0040 — Pillow for image processing: Floyd–Steinberg dither and a 32-color palette

**Status:** Accepted. Amends [[0016-process-assets-image-pipeline]], whose
Consequences said no image-decoding library would be pulled in.

## Context

`process_image_data()` was a no-op hook. It now runs three stages,
`reduce_image_quality()` → `dither_image()` → `reduce_color_palette()`, to
give images the limited-color, dithered look of 90s personal homepages.
Dithering and quantizing need decoded pixel data, so the stages can't keep
treating images as opaque bytes.

## Decision

- Add Pillow to `requirements.txt` as a runtime dependency. Decoding,
  quantizing, and dithering all go through it, with no hand-rolled pixel
  loops.
- `PALETTE_SIZE = 32` in `src/utils/images.py` is the color cap. The palette
  is adaptive: it's built per image from that image's own colors (median
  cut), not taken from a fixed system palette.
- `dither_image()` maps the image onto that palette with Floyd–Steinberg
  error diffusion. Error diffusion needs a target palette, so dithering and
  quantizing to the palette happen in the same step.
  `reduce_color_palette()` then quantizes with no dithering. On
  already-dithered input it only enforces the cap, and on its own it
  posterizes.
- Alpha is split off before quantizing and put back afterwards unchanged.
  Only the color channels are reduced.
- Each image is saved back in the format it came in as, so the paths in
  `data.json` stay valid. Bytes Pillow can't decode (SVG, or anything else)
  and animated images pass through unchanged.
- `reduce_image_quality()` stays a no-op for now.

## Consequences

- Every raster PNG/GIF/WebP in `dist/assets/` has at most 32 colors.
- JPEGs are dithered too, but re-encoding as JPEG brings back compression
  artifacts, so their color count isn't capped in practice.
- Builds are noticeably slower. A real 176-image `assets/` took about 40 s.
- A fork that doesn't want the look has to edit `process_image_data()`.
  There's no config switch for it.

## Keywords

Pillow, PIL, dither, Floyd–Steinberg, quantize, palette, 32 colors,
PALETTE_SIZE, reduce_color_palette, dither_image, reduce_image_quality,
process_image_data, image pipeline
