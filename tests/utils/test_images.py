from io import BytesIO

from PIL import Image

from src.utils.images import (
    PALETTE_SIZE,
    SHRINK_FACTOR,
    dither_image,
    process_image_data,
    read_image_data,
    reduce_color_palette,
    reduce_image_quality,
    write_image_data,
)


def _gradient_png(mode="RGB"):
    """Build a 64x64 PNG with far more than PALETTE_SIZE distinct colors."""
    image = Image.new(mode, (64, 64))
    for x in range(64):
        for y in range(64):
            pixel = (x * 4, y * 4, (x + y) * 2)
            image.putpixel((x, y), pixel + (x * 4,) if mode == "RGBA" else pixel)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _color_count(data):
    """Count the distinct RGB colors in encoded image bytes."""
    return len(Image.open(BytesIO(data)).convert("RGB").getcolors(maxcolors=1 << 24))


def test_read_image_data_returns_raw_bytes(tmp_path):
    """read_image_data returns a file's exact contents as bytes."""
    image_path = tmp_path / "logo.png"
    image_path.write_bytes(b"\x89PNG raw bytes")

    assert read_image_data(image_path) == b"\x89PNG raw bytes"


def test_process_image_data_limits_colors_to_palette_size():
    """process_image_data outputs an image with at most PALETTE_SIZE colors."""
    assert _color_count(process_image_data(_gradient_png())) <= PALETTE_SIZE


def test_process_image_data_passes_through_undecodable_bytes():
    """process_image_data returns bytes it can't decode (e.g. SVG) unchanged."""
    svg = b"<svg xmlns='http://www.w3.org/2000/svg'></svg>"

    assert process_image_data(svg) == svg


def test_reduce_image_quality_keeps_original_size_and_format():
    """reduce_image_quality regrows the image to its original size and format."""
    result = Image.open(BytesIO(reduce_image_quality(_gradient_png())))

    assert result.size == (64, 64)
    assert result.format == "PNG"


def test_reduce_image_quality_pixelates_into_blocks():
    """reduce_image_quality turns each shrunk pixel into a uniform block."""
    block = round(1 / SHRINK_FACTOR)
    result = Image.open(BytesIO(reduce_image_quality(_gradient_png())))

    for x in range(0, 64, block):
        for y in range(0, 64, block):
            corner = result.getpixel((x, y))
            assert all(
                result.getpixel((x + dx, y + dy)) == corner
                for dx in range(block)
                for dy in range(block)
            )


def test_reduce_image_quality_passes_through_undecodable_bytes():
    """reduce_image_quality returns bytes it can't decode unchanged."""
    assert reduce_image_quality(b"some image bytes") == b"some image bytes"


def test_dither_image_limits_colors_to_palette_size():
    """dither_image maps the image onto a PALETTE_SIZE-color palette."""
    assert _color_count(dither_image(_gradient_png())) <= PALETTE_SIZE


def test_dither_image_diffuses_error_unlike_plain_quantizing():
    """dither_image's Floyd–Steinberg output differs from undithered quantizing."""
    data = _gradient_png()

    assert dither_image(data) != reduce_color_palette(data)


def test_dither_image_keeps_format_and_alpha():
    """dither_image keeps the input's format and its alpha channel."""
    data = _gradient_png("RGBA")

    result = Image.open(BytesIO(dither_image(data)))

    assert result.format == "PNG"
    assert result.getchannel("A").tobytes() == (
        Image.open(BytesIO(data)).getchannel("A").tobytes()
    )


def test_dither_image_passes_through_undecodable_bytes():
    """dither_image returns bytes it can't decode unchanged."""
    assert dither_image(b"some image bytes") == b"some image bytes"


def test_reduce_color_palette_limits_colors_to_palette_size():
    """reduce_color_palette leaves at most PALETTE_SIZE colors."""
    assert _color_count(reduce_color_palette(_gradient_png())) <= PALETTE_SIZE


def test_reduce_color_palette_passes_through_undecodable_bytes():
    """reduce_color_palette returns bytes it can't decode unchanged."""
    assert reduce_color_palette(b"some image bytes") == b"some image bytes"


def test_write_image_data_writes_bytes_to_file(tmp_path):
    """write_image_data writes the given bytes to the given path."""
    image_path = tmp_path / "logo.png"

    write_image_data(image_path, b"\x89PNG raw bytes")

    assert image_path.read_bytes() == b"\x89PNG raw bytes"


def test_write_image_data_creates_missing_parent_directories(tmp_path):
    """write_image_data creates any missing parent directories first."""
    image_path = tmp_path / "assets" / "logo.png"

    write_image_data(image_path, b"data")

    assert image_path.read_bytes() == b"data"
