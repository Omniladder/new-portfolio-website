from io import BytesIO
from pathlib import Path

from PIL import Image, UnidentifiedImageError

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
PALETTE_SIZE = 32
SHRINK_FACTOR = 0.5


def read_image_data(path: Path) -> bytes:
    """Read an image file's raw bytes.

    Args:
        path: Path to the image file to read.

    Returns:
        bytes: The file's raw contents.
    """
    return path.read_bytes()


def _decode_image(data: bytes) -> Image.Image | None:
    """Decode image bytes into a Pillow image, if they're a still raster image.

    Args:
        data: Raw image bytes.

    Returns:
        Image.Image | None: The decoded image, or None if the bytes aren't
        something Pillow can read (e.g. SVG) or are an animated image, which
        the palette stages would flatten to a single frame.
    """
    try:
        image = Image.open(BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError):
        return None
    if getattr(image, "is_animated", False):
        return None
    return image


def _encode_image(image: Image.Image, image_format: str) -> bytes:
    """Encode a Pillow image back into bytes in the given format.

    Args:
        image: The image to encode.
        image_format: Pillow format name to save as (e.g. "PNG", "JPEG").

    Returns:
        bytes: The encoded image.
    """
    if image_format == "JPEG":
        image = image.convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return buffer.getvalue()


def _quantize(image: Image.Image, dither: Image.Dither) -> Image.Image:
    """Map an image onto an adaptive PALETTE_SIZE-color palette.

    The palette is built from the image's own colors (median cut). Alpha is
    split off first and reattached afterwards untouched, so only the color
    channels are quantized.

    Args:
        image: The image to quantize.
        dither: Pillow dithering method used when mapping pixels onto the
            palette, e.g. Image.Dither.FLOYDSTEINBERG or Image.Dither.NONE.

    Returns:
        Image.Image: The quantized image, in RGB mode, or RGBA if the input
        had transparency.
    """
    if image.mode == "P" and "transparency" in image.info:
        image = image.convert("RGBA")
    has_alpha = image.mode in ("RGBA", "LA")
    rgba = image.convert("RGBA") if has_alpha else None
    rgb = image.convert("RGB")
    palette = rgb.quantize(colors=PALETTE_SIZE)
    quantized = rgb.quantize(palette=palette, dither=dither).convert("RGB")
    if rgba is not None:
        quantized.putalpha(rgba.getchannel("A"))
    return quantized


def reduce_image_quality(data: bytes) -> bytes:
    """Pixelate an image, the first stage of processing.

    Shrinks the image to SHRINK_FACTOR of its width and height (box filter,
    so each new pixel averages the block it replaces), then scales it back
    up to its original size with nearest-neighbor interpolation. The result
    keeps its dimensions, so page layout is unaffected, but each source pixel
    becomes a hard-edged block, like a low-resolution 90s web graphic. Bytes
    Pillow can't decode (e.g. SVG) and animated images are returned unchanged.

    Args:
        data: Raw image bytes, as returned by read_image_data().

    Returns:
        bytes: The pixelated image, in the same format it came in as.
    """
    image = _decode_image(data)
    if image is None:
        return data
    image_format = image.format
    if image.mode == "P":
        image = image.convert("RGBA" if "transparency" in image.info else "RGB")
    size = image.size
    small = (
        max(1, round(size[0] * SHRINK_FACTOR)),
        max(1, round(size[1] * SHRINK_FACTOR)),
    )
    shrunk = image.resize(small, Image.Resampling.BOX)
    return _encode_image(shrunk.resize(size, Image.Resampling.NEAREST), image_format)


def dither_image(data: bytes) -> bytes:
    """Floyd–Steinberg dither an image, the second stage of processing.

    Error diffusion needs a target palette to diffuse towards, so this builds
    the same adaptive PALETTE_SIZE-color palette reduce_color_palette() uses
    and maps the image onto it with Floyd–Steinberg dithering. The output
    therefore already fits the palette, with gradients broken into the dot
    patterns of 90s web graphics instead of flat bands. Bytes Pillow can't
    decode (e.g. SVG) and animated images are returned unchanged.

    Args:
        data: Image bytes, as returned by reduce_image_quality().

    Returns:
        bytes: The dithered image, in the same format it came in as.
    """
    image = _decode_image(data)
    if image is None:
        return data
    return _encode_image(_quantize(image, Image.Dither.FLOYDSTEINBERG), image.format)


def reduce_color_palette(data: bytes) -> bytes:
    """Quantize an image to PALETTE_SIZE colors, the final stage of processing.

    Maps every pixel onto an adaptive PALETTE_SIZE-color palette (median cut)
    without dithering, mimicking the limited-color graphics of 90s personal
    homepages. After dither_image() the image already fits the palette, so
    this mainly guarantees the cap; on its own it posterizes. Transparency is
    kept as-is. Bytes Pillow can't decode (e.g. SVG) and animated images are
    returned unchanged. JPEG output is re-compressed, so its artifacts can
    add colors back beyond the cap.

    Args:
        data: Image bytes, as returned by dither_image().

    Returns:
        bytes: The quantized image, in the same format it came in as.
    """
    image = _decode_image(data)
    if image is None:
        return data
    return _encode_image(_quantize(image, Image.Dither.NONE), image.format)


def process_image_data(data: bytes) -> bytes:
    """Manipulate raw image bytes before they're written back out.

    Runs the image through three stages in order: reduce_image_quality(),
    dither_image(), then reduce_color_palette(): pixelate, Floyd–Steinberg
    dither onto a PALETTE_SIZE-color palette, then enforce that palette.

    Args:
        data: Raw image bytes, as returned by read_image_data().

    Returns:
        bytes: The processed image bytes.
    """
    data = reduce_image_quality(data)
    data = dither_image(data)
    return reduce_color_palette(data)


def write_image_data(path: Path, data: bytes) -> None:
    """Write raw image bytes to a file, creating parent directories as needed.

    Args:
        path: Destination path to write the image bytes to.
        data: Raw image bytes to write.

    Returns:
        None.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
